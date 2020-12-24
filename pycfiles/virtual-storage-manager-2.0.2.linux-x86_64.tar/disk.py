# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/physical/worker/disk.py
# Compiled at: 2016-06-13 14:11:03
"""
Worker for disk.
"""
import os
from vsm import utils
from vsm.openstack.common import log as logging
from oslo.config import cfg
LOG = logging.getLogger(__name__)

class DiskWorker(object):
    """Worker for disk."""

    def __init__(self):
        pass