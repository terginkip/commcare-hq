from django.conf.urls import *

from .api import EmwfOptionsView, LocationRestrictedEmwfOptionsView
from .case_list import CaseListFilterOptions
from .location import LocationGroupFilterOptions

urlpatterns = patterns('',
                       url(r'^emwf_options/$', EmwfOptionsView.as_view(), name='emwf_options'),
                       url(r'^new_emwf_options/$', LocationRestrictedEmwfOptionsView.as_view(), name='new_emwf_options'),
                       url(r'^case_list_options/$', CaseListFilterOptions.as_view(),
                           name='case_list_options'
                           ),
                       url(r'^grouplocationfilter_options/$', LocationGroupFilterOptions.as_view(),
                           name='grouplocationfilter_options'
                           ),
                       )
