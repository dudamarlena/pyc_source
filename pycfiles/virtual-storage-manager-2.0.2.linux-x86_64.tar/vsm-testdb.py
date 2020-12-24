# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/tests/db/vsm-testdb.py
# Compiled at: 2016-06-13 14:11:03
"""Starter script for Vsm Hardware."""
import eventlet
eventlet.monkey_patch()
import os, sys
from oslo.config import cfg
possible_topdir = os.path.normpath(os.path.join(os.path.abspath(sys.argv[0]), os.pardir, os.pardir))
if os.path.exists(os.path.join(possible_topdir, 'vsm', '__init__.py')):
    sys.path.insert(0, possible_topdir)
from vsm import flags
from vsm.openstack.common import log as logging
from vsm import service
from vsm import utils
FLAGS = flags.FLAGS
if __name__ == '__main__':
    flags.parse_args(sys.argv)
    logging.setup('vsm')
    utils.monkey_patch()
    launcher = service.ProcessLauncher()
    server = service.Service.create(binary='vsm-testdb')
    launcher.launch_server(server)
    launcher.wait()