# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mdiazmel/code/aramis/clinica/clinica/lib/nipype/interfaces/mrtrix3/reconst.py
# Compiled at: 2019-10-10 04:46:12
# Size of source mod 2**32: 5492 bytes
from __future__ import print_function, division, unicode_literals, absolute_import
import os.path as op
from nipype.interfaces.base import traits, TraitedSpec, File, Undefined
from nipype.interfaces.mrtrix3.base import MRTrix3BaseInputSpec, MRTrix3Base

class FitTensorInputSpec(MRTrix3BaseInputSpec):
    in_file = File(exists=True,
      argstr='%s',
      mandatory=True,
      position=(-2),
      desc='input diffusion weighted images')
    out_file = File('dti.mif',
      argstr='%s',
      mandatory=True,
      position=(-1),
      usedefault=True,
      desc='the output diffusion tensor image')
    in_mask = File(exists=True,
      argstr='-mask %s',
      desc='only perform computation within the specified binary brain mask image')
    method = traits.Enum('nonlinear',
      'loglinear',
      'sech',
      'rician',
      argstr='-method %s',
      desc='select method used to perform the fitting')
    reg_term = traits.Float(5000.0,
      usedefault=True, argstr='-regularisation %f',
      desc='specify the strength of the regularisation term on the magnitude of the tensor elements (default = 5000). This only applies to the non-linear methods')


class FitTensorOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc='the output DTI file')


class FitTensor(MRTrix3Base):
    __doc__ = "\n    Convert diffusion-weighted images to tensor images\n\n\n    Example\n    -------\n\n    >>> import nipype.interfaces.mrtrix3 as mrt\n    >>> tsr = mrt.FitTensor()\n    >>> tsr.inputs.in_file = 'dwi.mif'\n    >>> tsr.inputs.in_mask = 'mask.nii.gz'\n    >>> tsr.inputs.grad_fsl = ('bvecs', 'bvals')\n    >>> tsr.cmdline                               # doctest: +ELLIPSIS\n    'dwi2tensor -fslgrad bvecs bvals -mask mask.nii.gz -regularisation 5000.000000 dwi.mif dti.mif'\n    >>> tsr.run()                                 # doctest: +SKIP\n    "
    _cmd = 'dwi2tensor'
    input_spec = FitTensorInputSpec
    output_spec = FitTensorOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = op.abspath(self.inputs.out_file)
        return outputs


class EstimateFODInputSpec(MRTrix3BaseInputSpec):
    algorithm = traits.Enum('csd',
      'msmt_csd',
      argstr='%s',
      position=(-8),
      mandatory=True,
      desc='FOD algorithm')
    in_file = File(exists=True,
      argstr='%s',
      position=(-7),
      mandatory=True,
      desc='input DWI image')
    wm_txt = File(argstr='%s',
      position=(-6),
      mandatory=True,
      desc='WM response text file')
    wm_odf = File('wm.mif',
      argstr='%s',
      position=(-5),
      usedefault=True,
      mandatory=True,
      desc='output WM ODF')
    mask_file = File(exists=True, argstr='-mask %s', desc='mask image')
    shell = traits.List((traits.Float),
      sep=',',
      argstr='-shell %s',
      desc='specify one or more dw gradient shells')
    max_sh = traits.Int(8,
      usedefault=True, argstr='-lmax %d',
      desc='maximum harmonic degree of response function')
    in_dirs = File(exists=True,
      argstr='-directions %s',
      desc='specify the directions over which to apply the non-negativity constraint (by default, the built-in 300 direction set is used). These should be supplied as a text file containing the [ az el ] pairs for the directions.')


class EstimateFODOutputSpec(TraitedSpec):
    wm_odf = File(argstr='%s', desc='output WM ODF')
    gm_odf = File(argstr='%s', desc='output GM ODF')
    csf_odf = File(argstr='%s', desc='output CSF ODF')


class EstimateFOD(MRTrix3Base):
    __doc__ = "\n    Estimate fibre orientation distributions from diffusion data using spherical deconvolution\n\n    Example\n    -------\n\n    >>> import nipype.interfaces.mrtrix3 as mrt\n    >>> fod = mrt.EstimateFOD()\n    >>> fod.inputs.algorithm = 'csd'\n    >>> fod.inputs.in_file = 'dwi.mif'\n    >>> fod.inputs.wm_txt = 'wm.txt'\n    >>> fod.inputs.grad_fsl = ('bvecs', 'bvals')\n    >>> fod.cmdline                               # doctest: +ELLIPSIS\n    'dwi2fod -fslgrad bvecs bvals -lmax 8 csd dwi.mif wm.txt wm.mif gm.mif csf.mif'\n    >>> fod.run()                                 # doctest: +SKIP\n    "
    _cmd = 'dwi2fod'
    input_spec = EstimateFODInputSpec
    output_spec = EstimateFODOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['wm_odf'] = op.abspath(self.inputs.wm_odf)
        return outputs