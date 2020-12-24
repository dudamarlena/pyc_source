# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/notifier/log_notifier.py
# Compiled at: 2016-06-13 14:11:03
from oslo.config import cfg
from vsm.openstack.common import jsonutils
from vsm.openstack.common import log as logging
CONF = cfg.CONF

def notify(_context, message):
    """Notifies the recipient of the desired event given the model.
    Log notifications using openstack's default logging system"""
    priority = message.get('priority', CONF.default_notification_level)
    priority = priority.lower()
    logger = logging.getLogger('vsm.openstack.common.notification.%s' % message['event_type'])
    getattr(logger, priority)(jsonutils.dumps(message))