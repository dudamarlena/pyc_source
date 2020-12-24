# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/db/base.py
# Compiled at: 2016-06-13 14:11:03
"""Base class for classes that need modular database access."""
from oslo.config import cfg
from vsm import flags
from vsm.openstack.common import importutils
db_driver_opt = cfg.StrOpt('db_driver', default='vsm.db', help='driver to use for database access')
FLAGS = flags.FLAGS
FLAGS.register_opt(db_driver_opt)

class Base(object):
    """DB driver is injected in the init method."""

    def __init__(self, db_driver=None):
        if not db_driver:
            db_driver = FLAGS.db_driver
        self.db = importutils.import_module(db_driver)