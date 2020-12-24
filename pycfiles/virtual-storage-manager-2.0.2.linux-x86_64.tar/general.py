# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/physical/general.py
# Compiled at: 2016-06-13 14:11:03
"""
Drivers for Agent Services.
"""
from oslo.config import cfg
from vsm import flags
from vsm import utils
from vsm.physical import driver
from vsm.physical.worker import cpu as cpu_worker
from vsm.physical.worker import network as network_worker
from vsm.physical.worker import disk as disk_worker
from vsm.physical.worker import memory as memory_worker
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import log as logging
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

class GeneralDriver(driver.PhysicalDriver):
    """General class for Physical Driver.

    """

    def __init__(self):
        super(GeneralDriver, self).__init__()
        self._cpu_worker = cpu_worker.CPUWorker()
        self._network_worker = network_worker.NetworkWorker()
        self._disk_worker = disk_worker.DiskWorker()
        self._memory_worker = memory_worker.MemoryWorker()