# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/datawatcher/hdf5dwprocess.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 2373 bytes
"""
data watcher classes used to define the status of an acquisition for EDF
acquisitions
"""
__authors__ = [
 'C. Nemoz', 'H. Payno']
__license__ = 'MIT'
__date__ = '30/09/2019'
from .datawatcherprocess import _DataWatcherProcess
from tomwer.core.scan.hdf5scan import HDF5TomoScan
import logging
_logger = logging.getLogger(__name__)

class _DataWatcherProcessHDF5(_DataWatcherProcess):
    __doc__ = '\n    look for hdf5 information\n    '

    def __init__(self, dataDir, srcPattern, destPattern):
        super(_DataWatcherProcessHDF5, self).__init__(dataDir, srcPattern, destPattern)
        self.scan = HDF5TomoScan(scan=dataDir)

    def _removeAcquisition(self, scanID, reason):
        _logger.warning('remoing acquisition is not done for hdf5 data watcher process')

    def is_data_complete(self):
        self._sync()
        self.scan.updateDataset()
        return self.scan.is_finish()

    def is_abort(self):
        return self.scan.is_abort(src_pattern=(self.srcPattern), dest_pattern=(self.destPattern))