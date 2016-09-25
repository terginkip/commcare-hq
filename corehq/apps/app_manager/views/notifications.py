import json
import datetime
from django.utils.translation import ugettext as _
from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage
from dimagi.utils.parsing import json_format_datetime


def notify_form_changed(domain, couch_user, app_id, unique_form_id):
    message = {
        'domain': domain,
        'user_id': couch_user._id,
        'username': couch_user.username,
        'text': _('This form has been updated by {}. Reload the page to see the latest changes.').format(couch_user.username),
        'timestamp': json_format_datetime(datetime.datetime.utcnow()),
    }
    message = RedisMessage(json.dumps(message))
    RedisPublisher(facility=get_facility_for_form(app_id, unique_form_id), broadcast=True).publish_message(message)


def get_facility_for_form(app_id, unique_form_id):
    """
    Gets the websocket facility (topic) for a particular form.
    """
    return '{}:{}'.format(app_id, unique_form_id)
