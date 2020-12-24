# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/websockets/registrars/nodes.py
# Compiled at: 2014-08-29 12:11:18
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from nodeshot.core.nodes.signals import node_status_changed
from nodeshot.core.nodes.models import Node
from ..tasks import send_message

@receiver(post_save, sender=Node)
def node_created_handler(sender, **kwargs):
    if kwargs['created']:
        obj = kwargs['instance']
        message = 'node "%s" has been added' % obj.name
        send_message.delay(message)


@receiver(node_status_changed)
def node_status_changed_handler(**kwargs):
    obj = kwargs['instance']
    obj.old_status = kwargs['old_status'].name
    obj.new_status = kwargs['new_status'].name
    message = 'node "%s" changed its status from "%s" to "%s"' % (obj.name, obj.old_status, obj.new_status)
    send_message.delay(message)


@receiver(pre_delete, sender=Node)
def node_deleted_handler(sender, **kwargs):
    obj = kwargs['instance']
    message = 'node "%s" has been deleted' % obj.name
    send_message.delay(message)


def disconnect():
    """ disconnect signals """
    post_save.disconnect(node_created_handler, sender=Node)
    node_status_changed.disconnect(node_status_changed_handler)
    pre_delete.disconnect(node_deleted_handler, sender=Node)


def reconnect():
    """ reconnect signals """
    post_save.connect(node_created_handler, sender=Node)
    node_status_changed.connect(node_status_changed_handler)
    pre_delete.connect(node_deleted_handler, sender=Node)


from nodeshot.core.base.settings import DISCONNECTABLE_SIGNALS
DISCONNECTABLE_SIGNALS.append({'disconnect': disconnect, 
   'reconnect': reconnect})
setattr(settings, 'NODESHOT_DISCONNECTABLE_SIGNALS', DISCONNECTABLE_SIGNALS)