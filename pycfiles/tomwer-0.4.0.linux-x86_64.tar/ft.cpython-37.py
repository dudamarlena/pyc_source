# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/process/reconstruction/ftseries/params/ft.py
# Compiled at: 2020-02-17 09:32:20
# Size of source mod 2**32: 17975 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '05/03/2019'
from .base import _ReconsParam
from ....utils import _assert_cast_to_boolean, _assert_param_instance
from collections.abc import Iterable
import silx.utils.enum as _Enum
import enum, numpy, typing, logging
_logger = logging.getLogger(__name__)

@enum.unique
class VolSelMode(_Enum):
    total = 0
    manual = 1
    graphics = 2


@enum.unique
class FixedSliceMode(_Enum):
    middle = -1
    row_n = -3

    @classmethod
    def from_value(cls, value):
        for val in FixedSliceMode:
            if val.name == value:
                return val

        return super(FixedSliceMode, cls).from_value(value)


class FTRP(_ReconsParam):
    __doc__ = 'Reconstruction parameters for ftseries (general parameters)'
    _UNSPLIT_KEYS = ('FIXEDSLICE', )

    def __init__(self):
        _ReconsParam.__init__(self)
        self._FTRP__show_proj = False
        self._FTRP__show_slice = True
        self._FTRP__fixed_slice = FixedSliceMode.middle
        self._FTRP__vol_out_file = False
        self._FTRP__half_acq = False
        self._FTRP__force_half_acq = False
        self._FTRP__angle_offset_value = 0.0
        self._FTRP__num_part = 4
        self._FTRP__fastomo3_version = 'fastomo3 3.2'
        self._FTRP__correct_spikes_threshold = 0.04
        self._FTRP__activate_database = False
        self._FTRP__do_test_slice = True
        self._FTRP__no_test = False
        self._FTRP__zero_off_mask = True
        self._FTRP__volume_selection_mode = VolSelMode.total
        self._FTRP__record_volume_selection = False
        self._FTRP__ring_correction = False
        self._FTRP__fix_header_size = False
        self._FTRP__head_directory_to_remove = '/lbsram'
        self._FTRP__axis_correction_file = 'correct.txt'
        self._FTRP__do_axis_correction = False
        self._FTRP__force_reconstruction = False
        self._managed_params = {'SHOWPROJ':self.__class__.show_proj, 
         'SHOWSLICE':self.__class__.show_slice, 
         'FIXEDSLICE':self.__class__.fixed_slice, 
         'VOLOUTFILE':self.__class__.vol_out_file, 
         'HALF_ACQ':self.__class__.half_acq, 
         'FORCE_HALF_ACQ':self.__class__.force_half_acq, 
         'ANGLE_OFFSET_VALUE':self.__class__.angle_offset_value, 
         'ANGLE_OFFSET':self.__class__.angle_offset, 
         'NUM_PART':self.__class__.num_part, 
         'VERSION':self.__class__.fastomo3_version, 
         'CORRECT_SPIKES_THRESHOLD':self.__class__.correct_spikes_threshold, 
         'DATABASE':self.__class__.activate_database, 
         'DO_TEST_SLICE':self.__class__.do_test_slice, 
         'NO_CHECK':self.__class__.skip_reconstruction_tests, 
         'ZEROOFFMASK':self.__class__.set_mask_outside_to_zero, 
         'VOLSELECT':self.__class__.volume_selection_mode, 
         'VOLSELECTION_REMEMBER':self.__class__.record_volume_selection, 
         'RINGSCORRECTION':self.__class__.ring_correction, 
         'FIXHD':self.__class__.fix_header_size, 
         'RM_HEAD_DIR':self.__class__.head_directory_to_rm, 
         'AXIS_CORRECTION_FILE':self.__class__.axis_correction_file, 
         'DO_AXIS_CORRECTION':self.__class__.do_axis_correction}

    @property
    def show_proj(self):
        """show graphical proj during reconstruction"""
        return self._FTRP__show_proj

    @show_proj.setter
    def show_proj(self, show):
        _assert_param_instance(show, (bool, int, float))
        _assert_cast_to_boolean(show)
        if self._FTRP__show_proj != bool(show):
            self._FTRP__show_proj = bool(show)
            self.changed()

    @property
    def show_slice(self):
        """"show graphical slice during reconstruction"""
        return self._FTRP__show_slice

    @show_slice.setter
    def show_slice(self, show):
        _assert_param_instance(show, (bool, int, float))
        _assert_cast_to_boolean(show)
        if self._FTRP__show_slice != bool(show):
            self._FTRP__show_slice = bool(show)
            self.changed()

    @property
    def fixed_slice(self):
        """which slice(s) to reconstruct"""
        return self._FTRP__fixed_slice

    @fixed_slice.setter
    def fixed_slice(self, fixed):
        _assert_param_instance(fixed, (int, str, FixedSliceMode, Iterable))
        if isinstance(fixed, str):
            try:
                fixed = FixedSliceMode.from_value(fixed)
            except Exception as e:
                try:
                    pass
                finally:
                    e = None
                    del e

        if self._FTRP__fixed_slice != fixed:
            self._FTRP__fixed_slice = fixed
            self.changed()

    def fixed_slice_as_list(self) -> typing.Union[(tuple, int)]:
        """Return fixed_slice as a list of int"""
        fixed_slice = self.fixed_slice
        if isinstance(fixed_slice, str):
            try:
                if fixed_slice.count(':') == 2:
                    _from, _to, _step = fixed_slice.split(':')
                    _from, _to, _step = int(_from), int(_to), int(_step)
                    if _from > _to:
                        tmp = _to
                        _to = _from
                        _from = tmp
                    res = []
                    while _from <= _to:
                        res.append(_from)
                        _from += _step

                    return tuple(res)
                vals = fixed_slice.replace(' ', '')
                vals = vals.replace('_', '')
                vals = vals.replace(';', ',').split(',')
                res = []
                [res.append(int(val)) for val in vals]
                if len(res) is 1:
                    return res[0]
                return tuple(res)
            except Exception as e:
                try:
                    _logger.error(e)
                finally:
                    e = None
                    del e

        else:
            return fixed_slice

    @property
    def vol_out_file(self):
        """single .vol instead of edf stack"""
        return self._FTRP__vol_out_file

    @vol_out_file.setter
    def vol_out_file(self, single_vol):
        _assert_param_instance(single_vol, (bool, int, float))
        _assert_cast_to_boolean(single_vol)
        if self._FTRP__vol_out_file != bool(single_vol):
            self._FTRP__vol_out_file = bool(single_vol)
            self.changed()

    @property
    def half_acq(self):
        """use half acquisition reconstruction"""
        return self._FTRP__half_acq

    @half_acq.setter
    def half_acq(self, half):
        _assert_param_instance(half, (bool, int, float))
        _assert_cast_to_boolean(half)
        if self._FTRP__half_acq != bool(half):
            self._FTRP__half_acq = bool(half)
            self.changed()

    @property
    def force_half_acq(self):
        """Force half acquisition even if angle is not 360 (from PyHST 2016c)"""
        return self._FTRP__force_half_acq

    @force_half_acq.setter
    def force_half_acq(self, force):
        _assert_param_instance(force, (bool, int, float))
        _assert_cast_to_boolean(force)
        self._FTRP__force_half_acq = bool(force)
        self.changed()

    @property
    def angle_offset_value(self):
        """finale image rotation angle in degrees"""
        return self._FTRP__angle_offset_value

    @angle_offset_value.setter
    def angle_offset_value(self, value):
        assert isinstance(value, (int, float))
        if self._FTRP__angle_offset_value != value:
            self._FTRP__angle_offset_value = value
            self.changed()

    @property
    def angle_offset(self):
        return self._FTRP__angle_offset_value != 0.0

    @angle_offset.setter
    def angle_offset(self, value):
        pass

    @property
    def num_part(self):
        return self._FTRP__num_part

    @num_part.setter
    def num_part(self, value):
        """length of the numerical part in the data filenames (for .edf files)
        """
        _assert_param_instance(value, (int, float))
        if self._FTRP__num_part != int(value):
            self._FTRP__num_part = int(value)
            self.changed()

    @property
    def fastomo3_version(self):
        return self._FTRP__fastomo3_version

    @fastomo3_version.setter
    def fastomo3_version(self, version):
        if self._FTRP__fastomo3_version != version:
            self._FTRP__fastomo3_version = version
            self.changed()

    @property
    def correct_spikes_threshold(self):
        """threshold above which we have spike"""
        return self._FTRP__correct_spikes_threshold

    @correct_spikes_threshold.setter
    def correct_spikes_threshold(self, correct):
        _assert_param_instance(correct, (bool, int, float, str))
        if self._FTRP__correct_spikes_threshold != correct:
            self._FTRP__correct_spikes_threshold = correct
            self.changed()

    @property
    def activate_database(self):
        """put scan in tomoDB"""
        return self._FTRP__activate_database

    @activate_database.setter
    def activate_database(self, activate):
        _assert_param_instance(activate, (bool, int, float))
        _assert_cast_to_boolean(activate)
        if self._FTRP__activate_database != bool(activate):
            self._FTRP__activate_database = bool(activate)
            self.changed()

    @property
    def do_test_slice(self):
        """reconstruct one test slice"""
        return self._FTRP__do_test_slice

    @do_test_slice.setter
    def do_test_slice(self, test):
        _assert_param_instance(test, (bool, int, float))
        _assert_cast_to_boolean(test)
        if self._FTRP__do_test_slice != bool(test):
            self._FTRP__do_test_slice = bool(test)
            self.changed()

    @property
    def skip_reconstruction_tests(self):
        """force or not reconst of slices in ftseries"""
        return self._FTRP__no_test

    @skip_reconstruction_tests.setter
    def skip_reconstruction_tests(self, skip):
        _assert_param_instance(skip, (bool, int, float))
        _assert_cast_to_boolean(skip)
        if self._FTRP__no_test != bool(skip):
            self._FTRP__no_test = bool(skip)
            self.changed()

    @property
    def force_reconstruction(self):
        """force or not reconst of slices in ftseries"""
        return self._FTRP__force_reconstruction

    @force_reconstruction.setter
    def force_reconstruction(self, force):
        _assert_param_instance(force, (bool, int, float))
        _assert_cast_to_boolean(force)
        if self._FTRP__force_reconstruction != bool(force):
            self._FTRP__force_reconstruction = bool(force)
            self.changed()

    @property
    def set_mask_outside_to_zero(self):
        """Sets to zero the region outside the reconstruction mask"""
        return self._FTRP__zero_off_mask

    @set_mask_outside_to_zero.setter
    def set_mask_outside_to_zero(self, set_to_zero):
        _assert_param_instance(set_to_zero, (bool, int, float))
        _assert_cast_to_boolean(set_to_zero)
        if self._FTRP__zero_off_mask != set_to_zero:
            self._FTRP__zero_off_mask = set_to_zero
            self.changed()

    @property
    def volume_selection_mode(self):
        """how to select volume: total, manual or graphic"""
        return self._FTRP__volume_selection_mode

    @volume_selection_mode.setter
    def volume_selection_mode(self, mode):
        _mode = mode
        if type(mode) is str:
            if hasattr(VolSelMode, _mode):
                _mode = getattr(VolSelMode, _mode)
        assert _mode in VolSelMode
        if self._FTRP__volume_selection_mode != _mode:
            self._FTRP__volume_selection_mode = _mode
            self.changed()

    @property
    def record_volume_selection(self):
        return self._FTRP__record_volume_selection

    @record_volume_selection.setter
    def record_volume_selection(self, record):
        _assert_param_instance(record, (bool, int, float))
        _assert_cast_to_boolean(record)
        if bool(record) != self._FTRP__record_volume_selection:
            self._FTRP__record_volume_selection = bool(record)
            self.changed()

    @property
    def ring_correction(self):
        return self._FTRP__ring_correction

    @ring_correction.setter
    def ring_correction(self, _apply):
        _assert_param_instance(_apply, (bool, int, float))
        _assert_cast_to_boolean(_apply)
        if self._FTRP__ring_correction != bool(_apply):
            self._FTRP__ring_correction = bool(_apply)
            self.changed()

    @property
    def fix_header_size(self):
        """If true, try fixed header size determination"""
        return self._FTRP__fix_header_size

    @fix_header_size.setter
    def fix_header_size(self, fix):
        if self._FTRP__fix_header_size != fix:
            self._FTRP__fix_header_size = fix
            self.changed()

    @property
    def head_directory_to_rm(self):
        return self._FTRP__head_directory_to_remove

    @head_directory_to_rm.setter
    def head_directory_to_rm(self, _dir):
        assert isinstance(_dir, str)
        if self._FTRP__head_directory_to_remove != _dir:
            self._FTRP__head_directory_to_remove = _dir
            self.changed()

    @property
    def axis_correction_file(self):
        return self._FTRP__axis_correction_file

    @axis_correction_file.setter
    def axis_correction_file(self, _file):
        assert isinstance(_file, str)
        if self._FTRP__axis_correction_file != _file:
            self._FTRP__axis_correction_file = _file
            self.changed()

    @property
    def do_axis_correction(self):
        return self._FTRP__do_axis_correction

    @do_axis_correction.setter
    def do_axis_correction(self, do):
        _assert_param_instance(do, (bool, int, float))
        _assert_cast_to_boolean(do)
        if self._FTRP__do_axis_correction != do:
            self._FTRP__do_axis_correction = do
            self.changed()

    def to_dict(self):
        _dict = {'SHOWPROJ':int(self.show_proj), 
         'SHOWSLICE':int(self.show_slice), 
         'FIXEDSLICE':self.fixed_slice.name.replace('_', ' ') if isinstance(self.fixed_slice, FixedSliceMode) else str(self.fixed_slice), 
         'VOLOUTFILE':int(self.vol_out_file), 
         'HALF_ACQ':int(self.half_acq), 
         'FORCE_HALF_ACQ':int(self.force_half_acq), 
         'ANGLE_OFFSET_VALUE':float(self.angle_offset_value), 
         'ANGLE_OFFSET':int(self.angle_offset), 
         'NUM_PART':self.num_part, 
         'VERSION':self.fastomo3_version, 
         'CORRECT_SPIKES_THRESHOLD':self.correct_spikes_threshold, 
         'DATABASE':int(self.activate_database), 
         'DO_TEST_SLICE':int(self.do_test_slice), 
         'NO_CHECK':int(self.skip_reconstruction_tests), 
         'ZEROOFFMASK':int(self.set_mask_outside_to_zero), 
         'VOLSELECT':self.volume_selection_mode.name, 
         'VOLSELECTION_REMEMBER':int(self.record_volume_selection), 
         'RINGSCORRECTION':int(self.ring_correction), 
         'FIXHD':int(self.fix_header_size), 
         'RM_HEAD_DIR':self.head_directory_to_rm, 
         'AXIS_CORRECTION_FILE':self.axis_correction_file, 
         'DO_AXIS_CORRECTION':int(self.do_axis_correction)}
        _dict.update(self.unmanaged_params)
        return _dict

    @staticmethod
    def from_dict(_dict):
        recons_param = FTRP()
        recons_param.load_from_dict(_dict)
        return recons_param

    def load_from_dict(self, _dict):
        self._load_unmanaged_params(_dict=_dict)
        self.show_proj = _dict['SHOWPROJ']
        self.show_slice = _dict['SHOWSLICE']
        self.fixed_slice = _dict['FIXEDSLICE']
        self.vol_out_file = _dict['VOLOUTFILE']
        self.half_acq = _dict['HALF_ACQ']
        self.force_half_acq = _dict['FORCE_HALF_ACQ']
        self.angle_offset_value = _dict['ANGLE_OFFSET_VALUE']
        self.num_part = _dict['NUM_PART']
        self.correct_spikes_threshold = _dict['CORRECT_SPIKES_THRESHOLD']
        self.activate_database = _dict['DATABASE']
        self.do_test_slice = _dict['DO_TEST_SLICE']
        self.skip_reconstruction_tests = _dict['NO_CHECK']
        self.set_mask_outside_to_zero = _dict['ZEROOFFMASK']
        self.volume_selection_mode = _dict['VOLSELECT']
        self.record_volume_selection = _dict['VOLSELECTION_REMEMBER']
        self.ring_correction = _dict['RINGSCORRECTION']
        self.fix_header_size = _dict['FIXHD']
        self.head_directory_to_rm = _dict['RM_HEAD_DIR']
        self.axis_correction_file = _dict['AXIS_CORRECTION_FILE']
        self.do_axis_correction = _dict['DO_AXIS_CORRECTION']