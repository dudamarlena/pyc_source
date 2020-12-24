# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/tests/db/manager.py
# Compiled at: 2016-06-13 14:11:03
"""
TestDB Service
"""
import os, json
from oslo.config import cfg
import datetime
from vsm import context
from vsm import db
from vsm import exception
from vsm import flags
from vsm import manager
from vsm import conductor
from vsm.conductor import rpcapi as conductor_rpcapi
from vsm.openstack.common import excutils
from vsm.openstack.common import importutils
from vsm.openstack.common import log as logging
from vsm.openstack.common.notifier import api as notifier
from vsm.openstack.common import timeutils
from vsm.tests.db import driver
from vsm import version
testdb_opts = [
 cfg.StrOpt('testdb_manager', default='vsm.tests.db.manager.TestDBManager', help='full class name for the Manager for storage backup'),
 cfg.StrOpt('testdb_topic', default='vsm-testdb', help='the topic testdb nodes listen on')]
testdb_group = cfg.OptGroup(name='testdb', title='TestDB Options')
CONF = cfg.CONF
CONF.register_group(testdb_group)
CONF.register_opts(testdb_opts, testdb_group)
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

class TestDBManager(manager.Manager):
    """Chooses a host to create storages."""
    RPC_API_VERSION = '1.2'

    def __init__(self, service_name=None, *args, **kwargs):
        super(TestDBManager, self).__init__(*args, **kwargs)
        self._context = context.get_admin_context()
        self._conductor_api = conductor.API()