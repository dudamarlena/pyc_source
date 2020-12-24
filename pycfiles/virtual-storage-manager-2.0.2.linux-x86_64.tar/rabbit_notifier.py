# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/notifier/rabbit_notifier.py
# Compiled at: 2016-06-13 14:11:03
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import log as logging
from vsm.openstack.common.notifier import rpc_notifier
LOG = logging.getLogger(__name__)

def notify(context, message):
    """Deprecated in Grizzly. Please use rpc_notifier instead."""
    LOG.deprecated(_('The rabbit_notifier is now deprecated. Please use rpc_notifier instead.'))
    rpc_notifier.notify(context, message)