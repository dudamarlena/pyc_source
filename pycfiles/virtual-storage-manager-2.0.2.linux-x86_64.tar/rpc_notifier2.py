# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/notifier/rpc_notifier2.py
# Compiled at: 2016-06-13 14:11:03
"""messaging based notification driver, with message envelopes"""
from oslo.config import cfg
from vsm.openstack.common import context as req_context
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import log as logging
from vsm.openstack.common import rpc
LOG = logging.getLogger(__name__)
notification_topic_opt = cfg.ListOpt('topics', default=['notifications'], help='AMQP topic(s) used for openstack notifications')
opt_group = cfg.OptGroup(name='rpc_notifier2', title='Options for rpc_notifier2')
CONF = cfg.CONF
CONF.register_group(opt_group)
CONF.register_opt(notification_topic_opt, opt_group)

def notify(context, message):
    """Sends a notification via RPC"""
    if not context:
        context = req_context.get_admin_context()
    priority = message.get('priority', CONF.default_notification_level)
    priority = priority.lower()
    for topic in CONF.rpc_notifier2.topics:
        topic = '%s.%s' % (topic, priority)
        try:
            rpc.notify(context, topic, message, envelope=True)
        except Exception:
            LOG.exception(_('Could not send notification to %(topic)s. Payload=%(message)s'), locals())