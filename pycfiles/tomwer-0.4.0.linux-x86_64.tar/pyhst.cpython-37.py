# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/reconstruction/ftseries/params/pyhst.py
# Compiled at: 2020-01-10 04:27:31
# Size of source mod 2**32: 5841 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '05/03/2019'
from .base import _ReconsParam
from ....utils import _assert_cast_to_boolean, _assert_param_instance
from collections.abc import Iterable
import logging
_logger = logging.getLogger(__name__)

class PyhstRP(_ReconsParam):
    OFFV = 'pyhst2'

    def __init__(self):
        _ReconsParam.__init__(self)
        self._PyhstRP__offv = PyhstRP.OFFV
        self._PyhstRP__pyhst_exe = PyhstRP.OFFV
        self._PyhstRP__verbose_file = 'pyhst_out.txt'
        self._PyhstRP__verbose = False
        self._PyhstRP__make_oar_file = False
        self._cuda_devices = None
        self._managed_params = {'OFFV':self.__class__._offv, 
         'EXE':self.__class__.pyhst_exe, 
         'VERBOSE_FILE':self.__class__.verbose_file, 
         'VERBOSE':self.__class__.verbose, 
         'MAKE_OAR_FILE':self.__class__.make_oar_file, 
         'CUDA_DEVICES':self.__class__.cuda_devices}

    @property
    def offv(self):
        return self._PyhstRP__offv

    @offv.setter
    def offv(self, offv):
        if self._PyhstRP__offv != offv:
            self._PyhstRP__offv = offv
            self.changed()

    @property
    def pyhst_exe(self):
        """name of the pyhste executable"""
        return self._PyhstRP__pyhst_exe

    @pyhst_exe.setter
    def pyhst_exe(self, exe_name):
        if self._PyhstRP__pyhst_exe != exe_name:
            self._PyhstRP__pyhst_exe = exe_name
            self.changed()

    @property
    def _offv(self):
        return self._PyhstRP__offv

    @_offv.setter
    def _offv(self, offv):
        if self._PyhstRP__offv != offv:
            self._PyhstRP__offv = offv
            self.changed()

    @property
    def verbose_file(self):
        """output file name if verbose is activated"""
        return self._PyhstRP__verbose_file

    @verbose_file.setter
    def verbose_file(self, file_name):
        if self._PyhstRP__verbose_file != file_name:
            self._PyhstRP__verbose_file = file_name
            self.changed()

    @property
    def verbose(self):
        return self._PyhstRP__verbose

    @verbose.setter
    def verbose(self, activate):
        assert isinstance(activate, (bool, int, float))
        if self._PyhstRP__verbose != bool(activate):
            self._PyhstRP__verbose = bool(activate)
            self.changed()

    @property
    def make_oar_file(self):
        return self._PyhstRP__make_oar_file

    @make_oar_file.setter
    def make_oar_file(self, make):
        _assert_param_instance(make, (bool, int, float))
        _assert_cast_to_boolean(make)
        if self._PyhstRP__make_oar_file != bool(make):
            self._PyhstRP__make_oar_file = bool(make)
            self.changed()

    @property
    def cuda_devices(self):
        """

        :return: list of cuda devices to use
        """
        return self._cuda_devices

    @cuda_devices.setter
    def cuda_devices(self, devices):
        """

        :param Union[list,None,str] devices: list of :class:`CudaDevice`
        :return: list of :class:`CudaDevice`
        """
        if isinstance(devices, Iterable) and len(devices) == 0:
            self._cuda_devices = None
        else:
            if devices == '':
                self._cuda_devices = None
            else:
                self._cuda_devices = devices

    def to_dict(self):
        if self._cuda_devices is not None:
            cuda_devices_id = [device.id for device in self._cuda_devices]
        else:
            cuda_devices_id = ''
        _dict = {'OFFV':self.offv,  'EXE':self.pyhst_exe, 
         'VERBOSE_FILE':self.verbose_file, 
         'VERBOSE':self.verbose, 
         'MAKE_OAR_FILE':self.make_oar_file, 
         'CUDA_DEVICES':cuda_devices_id}
        _dict.update(self.unmanaged_params)
        return _dict

    @staticmethod
    def from_dict(_dict):
        recons_param = PyhstRP()
        recons_param.load_from_dict(_dict)
        return recons_param

    def load_from_dict(self, _dict):
        self._load_unmanaged_params(_dict)
        self.offv = _dict['OFFV']
        self.pyhst_exe = _dict['EXE']
        self.verbose_file = _dict['VERBOSE_FILE']
        self.verbose = _dict['VERBOSE']
        self.make_oar_file = _dict['MAKE_OAR_FILE']
        try:
            self.cuda_devices = _dict['CUDA_DEVICES']
        except KeyError:
            _logger.info('no "CUDA_DEVICES" key')