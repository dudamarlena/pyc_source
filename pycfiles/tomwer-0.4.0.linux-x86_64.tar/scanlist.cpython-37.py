# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/scanlist.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 4012 bytes
"""
This module is used to define a set of folders to be emitted to the next box.
"""
__authors__ = [
 'H.Payno']
__license__ = 'MIT'
__date__ = '05/07/2017'
from tomwer.core.signal import Signal
from tomwer.core.process.baseprocess import BaseProcess, _output_desc
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.scan.scanfactory import ScanFactory
from tomwer.core.log import TomwerLogger
logger = TomwerLogger(__name__)

class _ScanList(BaseProcess):
    __doc__ = 'Simple class listing the scan ID to process'
    _scanIDs = dict()
    scanReady = Signal(TomoBase)
    outputs = [
     _output_desc(name='data', type=TomoBase, doc='scan path')]
    endless_process = True

    def __init__(self):
        BaseProcess.__init__(self)

    def process(self):
        """function to launch if is the first box to be executed
        """
        self._sendList()
        res = []
        for scanID, scan in self._scanIDs.items():
            if self._return_dict:
                res.append(scan.to_dict())
            else:
                res.append(scan)

        return res

    def setProperties(self, properties):
        if '_scanIDs' in properties:
            self.setScanIDs(properties['_scanIDs'])
        else:
            raise ValueError('scansID no included in the widget properties')

    def setScanIDs(self, list_of_scan):
        for folder in list_of_scan:
            self.add(folder)

    def add(self, folder):
        """Add a folder to the list

        :param folder: the path to the folder for the scan to add
        :type folder: Union[str, :class:`.TomoBase`]
        """
        if isinstance(folder, TomoBase):
            _scan_obj = folder
        else:
            try:
                _scan_obj = ScanFactory.create_scan_object(folder)
            except ValueError as e:
                try:
                    logger.warning(e)
                    return
                finally:
                    e = None
                    del e

            self._scanIDs[_scan_obj.path] = _scan_obj
            return _scan_obj

    def remove(self, folder):
        """Remove a folder to the list

        :param str folder: the path to the folder for the scan to add
        """
        if folder in self._scanIDs:
            del self._scanIDs[folder]

    def clear(self):
        """clear the list"""
        self._scanIDs.clear()

    def _sendList(self):
        for scanID, scan in self._scanIDs.items():
            self.scanReady.emit(scan)

    def length(self):
        return len(self._scanIDs)


class ScanList(_ScanList):
    __doc__ = 'For now to avoid multiple inheritance from QObject with the process widgets\n    we have to define two classes. One only for the QObject inheritance\n    '
    data = _ScanList.scanReady