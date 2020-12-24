# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/websockets/registrars/notifications.py
# Compiled at: 2014-08-29 12:10:31
import simplejson as json
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse
from django.conf import settings
from nodeshot.community.notifications.models import Notification
from ..tasks import send_message

@receiver(post_save, sender=Notification)
def new_notification_handler(sender, **kwargs):
    if kwargs['created']:
        obj = kwargs['instance']
        message = {'user_id': str(obj.to_user.id), 
           'model': 'notification', 
           'type': obj.type, 
           'url': reverse('api_notification_detail', args=[obj.id])}
        send_message(json.dumps(message), pipe='private')


def disconnect():
    """ disconnect signals """
    post_save.disconnect(new_notification_handler, sender=Notification)


def reconnect():
    """ reconnect signals """
    post_save.connect(new_notification_handler, sender=Notification)


from nodeshot.core.base.settings import DISCONNECTABLE_SIGNALS
DISCONNECTABLE_SIGNALS.append({'disconnect': disconnect, 
   'reconnect': reconnect})
setattr(settings, 'NODESHOT_DISCONNECTABLE_SIGNALS', DISCONNECTABLE_SIGNALS)