# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/reconstruction/ftseries/params/paganin.py
# Compiled at: 2020-02-10 09:12:42
# Size of source mod 2**32: 9248 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '05/03/2019'
from .base import _ReconsParam
from ....utils import _assert_param_instance, _assert_cast_to_boolean
import silx.utils.enum as _Enum
from collections.abc import Iterable

class PaganinMode(_Enum):
    off = 0
    on = 1
    both = 2
    multi = 3


class PaganinRP(_ReconsParam):
    __doc__ = '\n    Paganin parameters to use during ftseries process\n    '

    def __init__(self):
        _ReconsParam.__init__(self)
        self._PaganinRP__mode = PaganinMode.off
        self._PaganinRP__db = 500.0
        self._PaganinRP__db2 = 100.0
        self._PaganinRP__unsharp_sigma = 0.8
        self._PaganinRP__unsharp_coeff = 3.0
        self._PaganinRP__threshold = 500
        self._PaganinRP__dilate = 2
        self._PaganinRP__median_r = 4
        self._PaganinRP__keep_bone = False
        self._PaganinRP__keep_soft = False
        self._PaganinRP__keep_abs = False
        self._PaganinRP__keep_corr = False
        self._PaganinRP__keep_mask = False
        self._managed_params = {'MODE':self.__class__.mode, 
         'DB':self.__class__.db, 
         'DB2':self.__class__.db2, 
         'UNSHARP_SIGMA':self.__class__.unsharp_sigma, 
         'UNSHARP_COEFF':self.__class__.unsharp_coeff, 
         'THRESHOLD':self.__class__.threshold, 
         'DILATE':self.__class__.dilate, 
         'MEDIANR':self.__class__.median_r, 
         'MKEEP_BONE':self.__class__.mkeep_bone, 
         'MKEEP_SOFT':self.__class__.mkeep_soft, 
         'MKEEP_ABS':self.__class__.mkeep_abs, 
         'MKEEP_CORR':self.__class__.mkeep_corr, 
         'MKEEP_MASK':self.__class__.mkeep_mask}

    @property
    def mode(self):
        return self._PaganinRP__mode

    @mode.setter
    def mode(self, mode):
        _assert_param_instance(mode, (PaganinMode, int))
        _mode = mode
        if isinstance(_mode, int):
            _mode = PaganinMode(_mode)
        self._PaganinRP__mode = _mode
        self.changed()

    @property
    def db(self):
        """value of delta/beta"""
        return self._PaganinRP__db

    @db.setter
    def db(self, value):
        _assert_param_instance(value, (int, float, str))
        if isinstance(self._PaganinRP__db, str):
            _db = float(value)
        else:
            _db = value
        if _db != self._PaganinRP__db:
            self._PaganinRP__db = _db
            self.changed()

    @property
    def db2(self):
        return self._PaganinRP__db2

    @db2.setter
    def db2(self, value):
        _assert_param_instance(value, (int, float, str))
        if isinstance(self._PaganinRP__db2, str):
            _db2 = float(value)
        else:
            _db2 = value
        if _db2 != self._PaganinRP__db2:
            self._PaganinRP__db2 = _db2
            self.changed()

    @property
    def unsharp_sigma(self):
        """size of the mask of unsharp masking"""
        return self._PaganinRP__unsharp_sigma

    @unsharp_sigma.setter
    def unsharp_sigma(self, value):
        """coeff for unsharp masking"""
        _assert_param_instance(value, float)
        if self._PaganinRP__unsharp_sigma != value:
            self._PaganinRP__unsharp_sigma = value
            self.changed()

    @property
    def unsharp_coeff(self):
        return self._PaganinRP__unsharp_coeff

    @unsharp_coeff.setter
    def unsharp_coeff(self, value):
        _assert_param_instance(value, float)
        if self._PaganinRP__unsharp_coeff != value:
            self._PaganinRP__unsharp_coeff = value
            self.changed()

    @property
    def threshold(self):
        return self._PaganinRP__threshold

    @threshold.setter
    def threshold(self, value):
        _assert_param_instance(value, (int, float))
        if self._PaganinRP__threshold != float(value):
            self._PaganinRP__threshold = float(value)
            self.changed()

    @property
    def dilate(self):
        return self._PaganinRP__dilate

    @dilate.setter
    def dilate(self, value):
        if self._PaganinRP__dilate != value:
            self._PaganinRP__dilate = value
            self.changed()

    @property
    def median_r(self):
        return self._PaganinRP__median_r

    @median_r.setter
    def median_r(self, value):
        if self._PaganinRP__median_r != value:
            self._PaganinRP__median_r = value
            self.changed()

    @property
    def mkeep_bone(self):
        return self._PaganinRP__keep_bone

    @mkeep_bone.setter
    def mkeep_bone(self, keep):
        _assert_param_instance(keep, (int, bool, float))
        _assert_cast_to_boolean(keep)
        if self._PaganinRP__keep_bone != bool(keep):
            self._PaganinRP__keep_bone = bool(keep)
            self.changed()

    @property
    def mkeep_soft(self):
        return self._PaganinRP__keep_soft

    @mkeep_soft.setter
    def mkeep_soft(self, keep):
        _assert_param_instance(keep, (int, bool, float))
        _assert_cast_to_boolean(keep)
        if self._PaganinRP__keep_soft != bool(keep):
            self._PaganinRP__keep_soft = bool(keep)
            self.changed()

    @property
    def mkeep_abs(self):
        return self._PaganinRP__keep_abs

    @mkeep_abs.setter
    def mkeep_abs(self, keep):
        _assert_param_instance(keep, (int, bool, float))
        _assert_cast_to_boolean(keep)
        if self._PaganinRP__keep_abs != bool(keep):
            self._PaganinRP__keep_abs = bool(keep)
            self.changed()

    @property
    def mkeep_corr(self):
        return self._PaganinRP__keep_corr

    @mkeep_corr.setter
    def mkeep_corr(self, keep):
        _assert_param_instance(keep, (int, bool, float))
        _assert_cast_to_boolean(keep)
        if self._PaganinRP__keep_corr != bool(keep):
            self._PaganinRP__keep_corr = bool(keep)
            self.changed()

    @property
    def mkeep_mask(self):
        return self._PaganinRP__keep_mask

    @mkeep_mask.setter
    def mkeep_mask(self, keep):
        _assert_param_instance(keep, (int, bool, float))
        _assert_cast_to_boolean(keep)
        if self._PaganinRP__keep_mask != bool(keep):
            self._PaganinRP__keep_mask = bool(keep)
            self.changed()

    def to_dict(self):
        _dict = {'MODE':self.mode.value, 
         'DB':self.db, 
         'DB2':self.db2, 
         'UNSHARP_SIGMA':self.unsharp_sigma, 
         'UNSHARP_COEFF':self.unsharp_coeff, 
         'THRESHOLD':self.threshold, 
         'DILATE':self.dilate, 
         'MEDIANR':self.median_r, 
         'MKEEP_BONE':self.mkeep_bone, 
         'MKEEP_SOFT':self.mkeep_soft, 
         'MKEEP_ABS':self.mkeep_abs, 
         'MKEEP_CORR':self.mkeep_corr, 
         'MKEEP_MASK':self.mkeep_mask}
        _dict.update(self.unmanaged_params)
        return _dict

    @staticmethod
    def from_dict(_dict: dict):
        recons_param = PaganinRP()
        recons_param.load_from_dict(_dict)
        return recons_param

    def load_from_dict(self, _dict: dict) -> None:
        self._load_unmanaged_params(_dict)
        self.mode = PaganinMode(_dict['MODE'])
        self.db = _dict['DB']
        self.db2 = _dict['DB2']
        self.unsharp_sigma = _dict['UNSHARP_SIGMA']
        self.unsharp_coeff = _dict['UNSHARP_COEFF']
        self.threshold = _dict['THRESHOLD']
        self.dilate = _dict['DILATE']
        self.median_r = _dict['MEDIANR']
        self.mkeep_bone = _dict['MKEEP_BONE']
        self.mkeep_soft = _dict['MKEEP_SOFT']
        self.mkeep_abs = _dict['MKEEP_ABS']
        self.mkeep_corr = _dict['MKEEP_CORR']
        self.mkeep_mask = _dict['MKEEP_MASK']

    def has_several_db_param(self) -> bool:
        """

        :return: True if the reconstruction contains several delta/beta values.
                 If the paganin mode is off will return False by default,
                 No matter the values of db and db2
        """
        if self.mode is PaganinMode.off:
            return False
        else:
            if isinstance(self.db, Iterable):
                if len(self.db) > 1:
                    return True
            if isinstance(self.db2, Iterable) and len(self.db2) > 1:
                return True
        return False