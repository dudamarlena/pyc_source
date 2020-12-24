# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/steven/Documents/Projects/radio/EOR/OthersCodes/21cmFAST/21cmFAST/src/py21cmfast/outputs.py
# Compiled at: 2020-02-13 17:38:14
# Size of source mod 2**32: 10273 bytes
"""
Output class objects.

The classes provided by this module exist to simplify access to large datasets created within C.
Fundamentally, ownership of the data belongs to these classes, and the C functions merely accesses
this and fills it. The various boxes and quantities associated with each output are available as
instance attributes. Along with the output data, each output object contains the various input
parameter objects necessary to define it.

.. warning:: These should not be instantiated or filled by the user, but always handled
             as output objects from the various functions contained here. Only the data
             within the objects should be accessed.
"""
import numpy as np
from cached_property import cached_property
from ._utils import OutputStruct as _BaseOutputStruct
from .c_21cmfast import ffi
from .inputs import AstroParams
from .inputs import CosmoParams
from .inputs import FlagOptions
from .inputs import UserParams
from .inputs import global_params

class _OutputStruct(_BaseOutputStruct):
    _global_params = global_params

    def __init__(self, *, user_params=None, cosmo_params=None, **kwargs):
        if cosmo_params is None:
            cosmo_params = CosmoParams()
        if user_params is None:
            user_params = UserParams()
        (super().__init__)(user_params=user_params, cosmo_params=cosmo_params, **kwargs)

    _ffi = ffi


class _OutputStructZ(_OutputStruct):
    _meta = False
    _inputs = _OutputStruct._inputs + ['redshift']


class InitialConditions(_OutputStruct):
    __doc__ = 'A class containing all initial conditions boxes.'
    _filter_params = _OutputStruct._filter_params + [
     'ALPHA_UVB',
     'EVOLVE_DENSITY_LINEARLY',
     'SMOOTH_EVOLVED_DENSITY_FIELD',
     'R_smooth_density',
     'HII_ROUND_ERR',
     'FIND_BUBBLE_ALGORITHM',
     'N_POISSON',
     'T_USE_VELOCITIES',
     'MAX_DVDR',
     'DELTA_R_HII_FACTOR',
     'HII_FILTER',
     'INITIAL_REDSHIFT',
     'HEAT_FILTER',
     'CLUMPING_FACTOR',
     'Z_HEAT_MAX',
     'R_XLy_MAX',
     'NUM_FILTER_STEPS_FOR_Ts',
     'ZPRIME_STEP_FACTOR',
     'TK_at_Z_HEAT_MAX',
     'XION_at_Z_HEAT_MAX',
     'Pop',
     'Pop2_ion',
     'Pop3_ion',
     'NU_X_BAND_MAX',
     'NU_X_MAX']

    def _init_arrays(self):
        self.lowres_density = np.zeros((self.user_params.HII_tot_num_pixels),
          dtype=(np.float32))
        self.lowres_vx = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.lowres_vy = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.lowres_vz = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.lowres_vx_2LPT = np.zeros((self.user_params.HII_tot_num_pixels),
          dtype=(np.float32))
        self.lowres_vy_2LPT = np.zeros((self.user_params.HII_tot_num_pixels),
          dtype=(np.float32))
        self.lowres_vz_2LPT = np.zeros((self.user_params.HII_tot_num_pixels),
          dtype=(np.float32))
        self.hires_density = np.zeros((self.user_params.tot_fft_num_pixels),
          dtype=(np.float32))
        self.hires_vcb = np.zeros((self.user_params.tot_fft_num_pixels), dtype=(np.float32))
        self.lowres_vcb = np.zeros((self.user_params.HII_tot_num_pixels),
          dtype=(np.float32))
        shape = (
         self.user_params.HII_DIM,
         self.user_params.HII_DIM,
         self.user_params.HII_DIM)
        hires_shape = (
         self.user_params.DIM, self.user_params.DIM, self.user_params.DIM)
        self.lowres_density.shape = shape
        self.lowres_vx.shape = shape
        self.lowres_vy.shape = shape
        self.lowres_vz.shape = shape
        self.lowres_vx_2LPT.shape = shape
        self.lowres_vy_2LPT.shape = shape
        self.lowres_vz_2LPT.shape = shape
        self.hires_density.shape = hires_shape
        self.lowres_vcb.shape = shape
        self.hires_vcb.shape = hires_shape


class PerturbedField(_OutputStructZ):
    __doc__ = 'A class containing all perturbed field boxes.'
    _filter_params = _OutputStruct._filter_params + [
     'ALPHA_UVB',
     'HII_ROUND_ERR',
     'FIND_BUBBLE_ALGORITHM',
     'N_POISSON',
     'T_USE_VELOCITIES',
     'MAX_DVDR',
     'DELTA_R_HII_FACTOR',
     'HII_FILTER',
     'HEAT_FILTER',
     'CLUMPING_FACTOR',
     'Z_HEAT_MAX',
     'R_XLy_MAX',
     'NUM_FILTER_STEPS_FOR_Ts',
     'ZPRIME_STEP_FACTOR',
     'TK_at_Z_HEAT_MAX',
     'XION_at_Z_HEAT_MAX',
     'Pop',
     'Pop2_ion',
     'Pop3_ion',
     'NU_X_BAND_MAX',
     'NU_X_MAX']

    def _init_arrays(self):
        self.density = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.velocity = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.density.shape = (
         self.user_params.HII_DIM,
         self.user_params.HII_DIM,
         self.user_params.HII_DIM)
        self.velocity.shape = (
         self.user_params.HII_DIM,
         self.user_params.HII_DIM,
         self.user_params.HII_DIM)


class _AllParamsBox(_OutputStructZ):
    _meta = True
    _inputs = _OutputStructZ._inputs + ['flag_options', 'astro_params']
    _filter_params = _OutputStruct._filter_params + [
     'T_USE_VELOCITIES',
     'MAX_DVDR']

    def __init__(self, astro_params=None, flag_options=None, first_box=False, **kwargs):
        if flag_options is None:
            flag_options = FlagOptions()
        if astro_params is None:
            astro_params = AstroParams(INHOMO_RECO=(flag_options.INHOMO_RECO))
        self.first_box = first_box
        (super().__init__)(astro_params=astro_params, flag_options=flag_options, **kwargs)


class IonizedBox(_AllParamsBox):
    __doc__ = 'A class containing all ionized boxes.'
    _meta = False

    def _init_arrays(self):
        self.xH_box = np.ones((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.Gamma12_box = np.zeros((self.user_params.HII_tot_num_pixels),
          dtype=(np.float32))
        self.z_re_box = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.dNrec_box = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        shape = (
         self.user_params.HII_DIM,
         self.user_params.HII_DIM,
         self.user_params.HII_DIM)
        self.xH_box.shape = shape
        self.Gamma12_box.shape = shape
        self.z_re_box.shape = shape
        self.dNrec_box.shape = shape

    @cached_property
    def global_xH(self):
        """Global (mean) neutral fraction."""
        if not self.filled:
            raise AttributeError('global_xH is not defined until the ionization calculation has been performed')
        else:
            return np.mean(self.xH_box)


class TsBox(_AllParamsBox):
    __doc__ = 'A class containing all spin temperature boxes.'
    _meta = False

    def _init_arrays(self):
        self.Ts_box = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.x_e_box = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.Tk_box = np.zeros((self.user_params.HII_tot_num_pixels), dtype=(np.float32))
        self.Ts_box.shape = (
         self.user_params.HII_DIM,
         self.user_params.HII_DIM,
         self.user_params.HII_DIM)
        self.x_e_box.shape = (
         self.user_params.HII_DIM,
         self.user_params.HII_DIM,
         self.user_params.HII_DIM)
        self.Tk_box.shape = (
         self.user_params.HII_DIM,
         self.user_params.HII_DIM,
         self.user_params.HII_DIM)

    @cached_property
    def global_Ts(self):
        """Global (mean) spin temperature."""
        if not self.filled:
            raise AttributeError('global_Ts is not defined until the ionization calculation has been performed')
        else:
            return np.mean(self.Ts_box)

    @cached_property
    def global_Tk(self):
        """Global (mean) Tk."""
        if not self.filled:
            raise AttributeError('global_Tk is not defined until the ionization calculation has been performed')
        else:
            return np.mean(self.Tk_box)

    @cached_property
    def global_x_e(self):
        """Global (mean) x_e."""
        if not self.filled:
            raise AttributeError('global_x_e is not defined until the ionization calculation has been performed')
        else:
            return np.mean(self.x_e_box)


class BrightnessTemp(_AllParamsBox):
    __doc__ = 'A class containing the brightness temperature box.'
    _meta = False
    _filter_params = _OutputStructZ._filter_params

    def _init_arrays(self):
        self.brightness_temp = np.zeros((self.user_params.HII_tot_num_pixels),
          dtype=(np.float32))
        self.brightness_temp.shape = (
         self.user_params.HII_DIM,
         self.user_params.HII_DIM,
         self.user_params.HII_DIM)

    @cached_property
    def global_Tb(self):
        """Global (mean) brightness temperature."""
        if not self.filled:
            raise AttributeError('global_Tb is not defined until the ionization calculation has been performed')
        else:
            return np.mean(self.brightness_temp)