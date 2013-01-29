from django import forms
from corehq.apps.locations.models import Location, root_locations
from django.template.loader import get_template
from django.template import Template, Context
from corehq.apps.locations.util import load_locs_json, allowed_child_types, location_custom_properties

class ParentLocWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return get_template('locations/manage/partials/parent_loc_widget.html').render(Context({
                    'name': name,
                    'value': value,
                    'locations': load_locs_json(self.domain, value),
                }))

class LocTypeWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        return get_template('locations/manage/partials/loc_type_widget.html').render(Context({
                    'name': name,
                    'value': value,
                }))

class LocationForm(forms.Form):
    parent_id = forms.CharField(label='Parent', required=False, widget=ParentLocWidget())
    name = forms.CharField(max_length=100)
    location_type = forms.CharField(widget=LocTypeWidget())

    def __init__(self, location, bound_data=None, *args, **kwargs):
        self.location = location

        kwargs['prefix'] = 'main'
        # seed form data from couch doc
        kwargs['initial'] = self.location._doc
        kwargs['initial']['parent_id'] = self.cur_parent_id

        super(LocationForm, self).__init__(bound_data, *args, **kwargs)
        self.fields['parent_id'].widget.domain = self.location.domain
        
        # custom properties
        self.sub_forms = {}
        for potential_type in allowed_child_types(self.location.domain, self.location.parent):
            subform = LocationCustomPropertiesSubForm(self.location, potential_type, bound_data)
            if subform.fields:
                self.sub_forms[potential_type] = subform

    @property
    def cur_parent_id(self):
        try:
            return self.location.lineage[0]
        except Exception:
            return None

    def clean_parent_id(self):
        parent_id = self.cleaned_data['parent_id']
        if not parent_id:
            parent_id = None # normalize ''

        if self.location._id is not None and self.cur_parent_id != parent_id:
            raise forms.ValidationError('Sorry, you cannot move locations around yet!')
        # TODO:
        # * allow moving of existing locs (requires background task to update
        #   loc path properties in all descendants and linked docs
        # * sanity check for re-parentage to self or descendant

        self.cleaned_data['parent'] = Location.get(parent_id) if parent_id else None
        return parent_id

    def clean_name(self):
        name = self.cleaned_data['name']

        parent = self.cleaned_data.get('parent')
        siblings = [loc for loc in (parent.children if parent else root_locations(self.location.domain)) if loc._id != self.location._id]
        if name in [loc.name for loc in siblings]:
            raise forms.ValidationError('name conflicts with another location with this parent')

        return name

    def clean_location_type(self):
        loc_type = self.cleaned_data['location_type']

        child_types = allowed_child_types(self.location.domain, self.cleaned_data.get('parent'))
        # neither of these should be seen in normal usage
        if not child_types:
            raise forms.ValidationError('the selected parent location cannot have sub-locations!')
        elif loc_type not in child_types:
            raise forms.ValidationError('not valid for the select parent location')

        return loc_type

    def clean(self):
        super(LocationForm, self).clean()

        subform = self.sub_forms[self.cleaned_data['location_type']]
        if not subform.is_valid():
            raise forms.ValidationError('Error in location properties')
        self.cleaned_data.update(('prop:%s' % k, v) for k, v in subform.cleaned_data.iteritems())

        return self.cleaned_data

    def save(self, instance=None, commit=True):
        if self.errors:
            raise ValueError('form does not validate')

        location = instance or self.location

        for field in ('name', 'location_type'):
            setattr(location, field, self.cleaned_data[field])
        location.lineage = Location(parent=self.cleaned_data['parent_id']).lineage

        for k, v in self.cleaned_data.iteritems():
            if k.startswith('prop:'):
                prop_name = k[len('prop:'):]
                setattr(location, prop_name, v)

        if commit:
            location.save()

        return location

class LocationCustomPropertiesSubForm(forms.Form):
    def __init__(self, location, potential_type, *args, **kwargs):
        kwargs['prefix'] = 'props_%s' % potential_type
        super(LocationCustomPropertiesSubForm, self).__init__(*args, **kwargs)

        for p in location_custom_properties(location.domain, potential_type):
            self.fields[p.name] = p.field(getattr(location, p.name, None))

