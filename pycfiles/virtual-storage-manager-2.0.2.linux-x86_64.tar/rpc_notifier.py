# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/notifier/rpc_notifier.py
# Compiled at: 2016-06-13 14:11:03
from oslo.config import cfg
from vsm.openstack.common import context as req_context
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import log as logging
from vsm.openstack.common import rpc
LOG = logging.getLogger(__name__)
notification_topic_opt = cfg.ListOpt('notification_topics', default=['notifications'], help='AMQP topic used for openstack notifications')
CONF = cfg.CONF
CONF.register_opt(notification_topic_opt)

def notify(context, message):
    """Sends a notification via RPC"""
    if not context:
        context = req_context.get_admin_context()
    priority = message.get('priority', CONF.default_notification_level)
    priority = priority.lower()
    for topic in CONF.notification_topics:
        topic = '%s.%s' % (topic, priority)
        try:
            rpc.notify(context, topic, message)
        except Exception:
            LOG.exception(_('Could not send notification to %(topic)s. Payload=%(message)s'), locals())