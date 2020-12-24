# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/timer.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 2556 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '12/12/2018'
from tomwer.core.process.baseprocess import SingleProcess, _input_desc, _output_desc
from tomwer.core.scan.scanbase import TomoBase
from tomwer.core.scan.scanfactory import ScanFactory
import time
from tomwer.core.log import TomwerLogger
_logger = TomwerLogger(__name__)

class Timer(SingleProcess):
    __doc__ = '\n    Simple timer / time out - function'
    inputs = [
     _input_desc(name='data', type=TomoBase, handler='process', doc='scan object')]
    outputs = [
     _output_desc(name='data', type=TomoBase, doc='scan object')]

    def __init__(self, wait):
        SingleProcess.__init__(self)
        self.waiting_time = wait or 1

    @property
    def waiting_time(self):
        return self._waiting_time

    @waiting_time.setter
    def waiting_time(self, wait):
        self._waiting_time = wait

    def process(self, scan):
        if type(scan) is dict:
            _scan = ScanFactory.create_scan_object_frm_dict(scan)
        else:
            _scan = scan
        assert isinstance(scan, TomoBase)
        time.sleep(self.waiting_time)
        if self._return_dict:
            return _scan.to_dict()
        return _scan