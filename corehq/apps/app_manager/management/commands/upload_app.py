import json
from optparse import make_option
from django.core.management.base import BaseCommand, CommandError

import os
from corehq.apps.app_manager.models import Application
from corehq.apps.app_manager.util import save_xform
from datetime import datetime
from corehq.apps.users.models import CouchUser
from corehq.const import SERVER_DATETIME_FORMAT_NO_SEC


class Command(BaseCommand):
    args = '<path_to_dir> <app_id>'
    help = """
        Uploads a a directory of forms to an app. See also: download_app
    """
    option_list = BaseCommand.option_list + (
        make_option('--deploy',
                    action='store_true',
                    dest='deploy',
                    default=False,
                    help="Deploy application, by making a new build and starring it."),
        make_option('--user',
                    action='store',
                    dest='user',
                    default=None,
                    help="Username to use for deployer."),
        make_option('--comment',
                    action='store',
                    dest='comment',
                    default=None,
                    help="Comment (used for if you deploy the application)"),
        make_option('--force',
                    action='store_true',
                    dest='force',
                    default=False,
                    help="Force overwrite an app that has been changed."),
    )

    def handle(self, *args, **options):
        if len(args) != 2:
            raise CommandError('Usage: %s\n%s' % (self.args, self.help))
        if options['deploy'] and not options['user']:
            raise CommandError('Deploy argument requires a user')
        elif options['deploy']:
            user = CouchUser.get_by_username(options['user'])
            if not user:
                raise CommandError("Couldn't find user with username {}".format(options['user']))

        force = options['force']

        # todo: would be nice if this worked off remote servers too
        path, app_id = args

        app_path = os.path.join(path, 'app-{}.json'.format(app_id))
        with open(app_path, 'r') as f:
            app_json = json.load(f)
            app = Application.wrap(app_json)
            assert app.id == app_id
            latest_rev = Application.get_db().get_rev(app_id)
            if app._rev != latest_rev:
                if not force:
                    raise CommandError(
                        "Application has been updated since being exported. "
                        "Use --force to overwrite it.")
                else:
                    app._rev = latest_rev

        for module_dir in os.listdir(path):
            if not os.path.isdir(module_dir):
                continue
            module_index, name = module_dir.split(' - ')
            module = app.get_module(int(module_index))
            for form_name in os.listdir(os.path.join(path, module_dir)):
                form_index, name = form_name.split(' - ')
                form = module.get_form(int(form_index))
                with open(os.path.join(path, module_dir, form_name)) as f:
                    save_xform(app, form, f.read())

        app.save()
        print 'successfully updated {}'.format(app.name)
        if options['deploy']:
            # make build and star it
            comment = options.get('comment', 'form changes from {0}'.format(datetime.utcnow().strftime(SERVER_DATETIME_FORMAT_NO_SEC)))
            copy = app.make_build(
                comment=comment,
                user_id=user._id,
                previous_version=app.get_latest_app(released_only=False),
            )
            copy.is_released = True
            copy.save(increment_version=False)
            print 'successfully released new version'
