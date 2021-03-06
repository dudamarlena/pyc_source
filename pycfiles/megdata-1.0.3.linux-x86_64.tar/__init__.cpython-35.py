# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/megdata/__init__.py
# Compiled at: 2018-10-24 06:01:48
# Size of source mod 2**32: 1812 bytes
from .bti_pdf import BTIPDF
from .bti_elecfile import BTIElectrodeFile, BTI_ELEC_STATE_NOT_COLLECTED, BTI_ELEC_STATE_COLLECTED, BTI_ELEC_STATE_SKIPPED, BTI_ELEC_STATE_NOT_APPLICABLE, BTI_ELEC_STATES
from .bti_config import BTIConfigFile
from .bti_hsfile import BTIHSFile
from .bti_channel import BTI_CHANTYPE_MEG, BTI_CHANTYPE_EEG, BTI_CHANTYPE_REFERENCE, BTI_CHANTYPE_EXTERNAL, BTI_CHANTYPE_TRIGGER, BTI_CHANTYPE_UTILITY, BTI_CHANTYPE_DERIVED, BTI_CHANTYPE_SHORTED, BTI_CHANTYPES
from .bti_dipolefile import BTIDipoleFile, BTIDipole, BTIDipoleTextFile
from .ctf_res4 import CTFRes4File, CTF_CHAN_REF_MAG, CTF_CHAN_REF_GRAD1, CTF_CHAN_REF_GRAD2, CTF_CHAN_REF_GRAD3, CTF_CHAN_MAG, CTF_CHAN_GRAD1, CTF_CHAN_GRAD2, CTF_CHAN_GRAD3, CTF_CHAN_REF_EEG, CTF_CHAN_EEG, CTF_CHAN_ADC, CTF_CHAN_STIM, CTF_CHAN_TIME, CTF_CHAN_POS, CTF_CHAN_DAC, CTF_CHAN_OTHER, CTF_CHAN_VIRTUAL, CTF_CHAN_SYSTIME, CTF_CHANTYPES, CTF_COILSHAPE_CIRCULAR, CTF_COILSHAPE_SQUARE, CTF_COILSHAPES
from .ctf_dataset import CTFDataset
from .ctf_polhemus import CTFPolhemus
from .ctf_mri import CTFMRIFile
from .ctf_hc import CTFHCFile
from .meghdf import HMEGSubjectData, HMEGChannel, HMEGADChannel, HMEGMegChannel, HMEGWeightTable, HMEGSystemConfig, HMEGGeomFiducials, HMEGGeomCoils, HMEGGeomHeadshape, HMEGAcquisitions, HMEGAcquisition, HDF5Meg, bti_to_meghdf_data