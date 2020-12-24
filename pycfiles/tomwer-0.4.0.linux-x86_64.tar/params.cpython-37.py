# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/reconstruction/darkref/params.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 8713 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '07/03/2019'
import enum
from tomwer.core.process.reconstruction.darkref.settings import DARKHST_PREFIX, REFHST_PREFIX
from tomwer.core.process.reconstruction.ftseries.params.base import _ReconsParam

@enum.unique
class When(enum.Enum):
    never = (0, )
    before = (1, )
    after = (2, )


@enum.unique
class Method(enum.Enum):
    none = (0, )
    average = (1, )
    median = 2


class DKRFRP(_ReconsParam):

    def __init__(self):
        _ReconsParam.__init__(self)
        self._DKRFRP__do_when = When.before
        self._DKRFRP__dark_calc = Method.average
        self._DKRFRP__overwrite_dark = False
        self._DKRFRP__remove_dark = False
        self._DKRFRP__dark_pattern = 'darkend[0-9]{3,4}'
        self._DKRFRP__ref_calc = Method.median
        self._DKRFRP__overwrite_ref = False
        self._DKRFRP__remove_ref = False
        self._DKRFRP__ref_pattern = 'ref*.*[0-9]{3,4}_[0-9]{3,4}'
        self._DKRFRP__dark_prefix = DARKHST_PREFIX
        self._DKRFRP__ref_prefix = REFHST_PREFIX
        self._managed_params = {'DOWHEN':self.__class__.do_when, 
         'DARKCAL':self.__class__.dark_calc_method, 
         'DARKOVE':self.__class__.overwrite_dark, 
         'DARKRMV':self.__class__.remove_dark, 
         'DKFILE':self.__class__.dark_pattern, 
         'REFSCAL':self.__class__.ref_calc_method, 
         'REFSOVE':self.__class__.overwrite_ref, 
         'REFSRMV':self.__class__.remove_ref, 
         'RFFILE':self.__class__.ref_pattern}

    @property
    def do_when(self):
        """When should we process calculation. Should be removed now that DKRF
        process exists. Was needed for fastomo3"""
        return self._DKRFRP__do_when

    @do_when.setter
    def do_when(self, when):
        assert isinstance(when, (int, When))
        when = When(when)
        if when != self._DKRFRP__do_when:
            self._DKRFRP__do_when = when
            self.changed()

    @property
    def dark_calc_method(self):
        """Dark calculation Method"""
        return self._DKRFRP__dark_calc

    @dark_calc_method.setter
    def dark_calc_method(self, method):
        if not isinstance(method, (int, Method, str)):
            raise AssertionError
        elif isinstance(method, str):
            _dark_calc = getattr(Method, method.lower())
        else:
            _dark_calc = Method(method)
        if self._DKRFRP__dark_calc != _dark_calc:
            self._DKRFRP__dark_calc = _dark_calc
            self.changed()

    @property
    def overwrite_dark(self):
        """Overwrite Dark results if already exists"""
        return self._DKRFRP__overwrite_dark

    @overwrite_dark.setter
    def overwrite_dark(self, overwrite):
        assert isinstance(overwrite, (int, bool, float))
        _overwrite_dark = bool(overwrite)
        if self._DKRFRP__overwrite_dark != _overwrite_dark:
            self._DKRFRP__overwrite_dark = _overwrite_dark
            self.changed()

    @property
    def remove_dark(self):
        """Remove original Darks files when done"""
        return self._DKRFRP__remove_dark

    @remove_dark.setter
    def remove_dark(self, remove):
        assert isinstance(remove, (int, bool, float))
        _remove_dark = bool(remove)
        if _remove_dark != self._DKRFRP__remove_dark:
            self._DKRFRP__remove_dark = _remove_dark
            self.changed()

    @property
    def dark_pattern(self):
        """ File pattern to detect edf Dark field"""
        return self._DKRFRP__dark_pattern

    @dark_pattern.setter
    def dark_pattern(self, pattern):
        _dark_pattern = pattern
        if self._DKRFRP__dark_pattern != _dark_pattern:
            self._DKRFRP__dark_pattern = _dark_pattern
            self.changed()

    @property
    def ref_calc_method(self):
        """Dark calculation method (None, Average, Median)"""
        return self._DKRFRP__ref_calc

    @ref_calc_method.setter
    def ref_calc_method(self, method):
        if not isinstance(method, (int, Method, str)):
            raise AssertionError
        elif isinstance(method, str):
            _ref_calc = getattr(Method, method.lower())
        else:
            _ref_calc = Method(method)
        if self._DKRFRP__ref_calc != _ref_calc:
            self._DKRFRP__ref_calc = _ref_calc
            self.changed()

    @property
    def overwrite_ref(self):
        """Overwrite Dark results if already exists"""
        return self._DKRFRP__overwrite_ref

    @overwrite_ref.setter
    def overwrite_ref(self, overwrite):
        assert isinstance(overwrite, (int, bool, float))
        _overwrite_ref = bool(overwrite)
        if self._DKRFRP__overwrite_ref != _overwrite_ref:
            self._DKRFRP__overwrite_ref = _overwrite_ref
            self.changed()

    @property
    def remove_ref(self):
        """Remove original ref files when done"""
        return self._DKRFRP__remove_ref

    @remove_ref.setter
    def remove_ref(self, remove):
        assert isinstance(remove, (int, bool, float))
        _remove_ref = remove
        if self._DKRFRP__remove_ref != _remove_ref:
            self._DKRFRP__remove_ref = _remove_ref
            self.changed()

    @property
    def ref_pattern(self):
        """File pattern to detect references"""
        return self._DKRFRP__ref_pattern

    @ref_pattern.setter
    def ref_pattern(self, pattern):
        if pattern != self._DKRFRP__ref_pattern:
            self._DKRFRP__ref_pattern = pattern
            self.changed()

    @property
    def ref_prefix(self):
        return self._DKRFRP__ref_prefix

    @ref_prefix.setter
    def ref_prefix(self, prefix):
        if prefix != self._DKRFRP__ref_prefix:
            self._DKRFRP__ref_prefix = prefix
            self.changed()

    @property
    def dark_prefix(self):
        return self._DKRFRP__dark_prefix

    @dark_prefix.setter
    def dark_prefix(self, prefix):
        if prefix != self._DKRFRP__dark_prefix:
            self._DKRFRP__dark_prefix = prefix
            self.changed()

    def _set_remove_opt(self, rm):
        self.remove_ref = rm
        self.remove_dark = rm

    def _set_skip_if_exist(self, skip):
        self.overwrite_ref = not skip
        self.overwrite_dark = not skip

    def to_dict(self):
        _dict = {'DOWHEN':self.do_when.name, 
         'DARKCAL':self.dark_calc_method.name.split('.')[(-1)].title(), 
         'DARKOVE':int(self.overwrite_dark), 
         'DARKRMV':int(self.remove_dark), 
         'DKFILE':self.dark_pattern, 
         'REFSCAL':self.ref_calc_method.name.split('.')[(-1)].title(), 
         'REFSOVE':int(self.overwrite_ref), 
         'REFSRMV':int(self.remove_ref), 
         'RFFILE':self.ref_pattern}
        _dict.update(self.unmanaged_params)
        return _dict

    @staticmethod
    def from_dict(_dict):
        params = DKRFRP()
        params.load_from_dict(_dict)
        return params

    def load_from_dict(self, _dict):
        self._load_unmanaged_params(_dict=_dict)
        self.do_when = getattr(When, _dict['DOWHEN'])
        self.dark_calc_method = getattr(Method, _dict['DARKCAL'].lower())
        self.overwrite_dark = _dict['DARKOVE']
        self.remove_dark = _dict['DARKRMV']
        self.dark_pattern = _dict['DKFILE']
        self.ref_calc_method = getattr(Method, _dict['REFSCAL'].lower())
        self.overwrite_ref = _dict['REFSOVE']
        self.remove_ref = _dict['REFSRMV']
        self.ref_pattern = _dict['RFFILE']