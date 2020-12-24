# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mdiazmel/code/aramis/clinica/clinica/lib/nipype/interfaces/mrtrix/preprocess.py
# Compiled at: 2019-10-10 04:46:12
# Size of source mod 2**32: 6761 bytes
from __future__ import print_function, division, unicode_literals, absolute_import
import os.path as op
from nipype.utils.filemanip import split_filename
from nipype.interfaces.base import CommandLineInputSpec, CommandLine, traits, TraitedSpec, File, InputMultiPath, isdefined

class DWI2TensorInputSpec(CommandLineInputSpec):
    in_file = InputMultiPath(File(exists=True),
      argstr='%s',
      mandatory=True,
      position=(-2),
      desc='Diffusion-weighted images')
    out_filename = File(name_template='%s_tensor.mif',
      name_source='in_file',
      output_name='tensor',
      argstr='%s',
      desc='Output tensor filename',
      position=(-1))
    encoding_file = File(argstr='-grad %s',
      position=2,
      desc='Encoding file supplied as a 4xN text file with each line is in the format [ X Y Z b ], where [ X Y Z ] describe the direction of the applied gradient, and b gives the b-value in units (1000 s/mm^2). See FSL2MRTrix()')
    ignore_slice_by_volume = traits.List((traits.Int),
      argstr='-ignoreslices %s',
      sep=' ',
      position=2,
      minlen=2,
      maxlen=2,
      desc='Requires two values (i.e. [34 1] for [Slice Volume] Ignores the image slices specified when computing the tensor. Slice here means the z coordinate of the slice to be ignored.')
    ignore_volumes = traits.List((traits.Int),
      argstr='-ignorevolumes %s',
      sep=' ',
      position=2,
      minlen=1,
      desc='Requires two values (i.e. [2 5 6] for [Volumes] Ignores the image volumes specified when computing the tensor.')
    quiet = traits.Bool(argstr='-quiet',
      position=1,
      desc='Do not display information messages or progress status.')
    debug = traits.Bool(argstr='-debug',
      position=1,
      desc='Display debugging messages.')
    in_mask = File(exists=True,
      argstr='-mask %s',
      desc='only perform computation within the specified binary brain mask image')


class DWI2TensorOutputSpec(TraitedSpec):
    tensor = File(exists=True,
      desc='path/name of output diffusion tensor image')


class DWI2Tensor(CommandLine):
    __doc__ = "\n    Converts diffusion-weighted images to tensor images.\n\n    Example\n    -------\n\n    >>> import nipype.interfaces.mrtrix as mrt\n    >>> dwi2tensor = mrt.DWI2Tensor()\n    >>> dwi2tensor.inputs.in_file = 'dwi.mif'\n    >>> dwi2tensor.inputs.encoding_file = 'encoding.txt'\n    >>> dwi2tensor.cmdline\n    'dwi2tensor -grad encoding.txt dwi.mif dwi_tensor.mif'\n    >>> dwi2tensor.run()                                   # doctest: +SKIP\n    "
    _cmd = 'dwi2tensor'
    input_spec = DWI2TensorInputSpec
    output_spec = DWI2TensorOutputSpec


class MRTransformInputSpec(CommandLineInputSpec):
    in_files = InputMultiPath(File(exists=True),
      argstr='%s',
      mandatory=True,
      position=(-2),
      desc='Input images to be transformed')
    out_filename = File(genfile=True,
      argstr='%s',
      position=(-1),
      desc='Output image')
    invert = traits.Bool(argstr='-inverse',
      position=1,
      desc='Invert the specified transform before using it')
    replace_transform = traits.Bool(argstr='-replace',
      position=1,
      desc='replace the current transform by that specified, rather than applying it to the current transform')
    transformation_file = File(exists=True,
      argstr='-transform %s',
      position=1,
      desc='The transform to apply, in the form of a 4x4 ascii file.')
    linear_transform = File(exists=True,
      argstr='-linear %s',
      position=1,
      desc='specify a linear transform to apply, in the form of a 3x4 or 4x4 ascii file. Note the standard reverse convention is used, where the transform maps points in the template image to the moving image. Note that the reverse convention is still assumed even if no -template image is supplied')
    template_image = File(exists=True,
      argstr='-template %s',
      position=1,
      desc='Reslice the input image to match the specified template image.')
    reference_image = File(exists=True,
      argstr='-reference %s',
      position=1,
      desc='in case the transform supplied maps from the input image onto a reference image, use this option to specify the reference. Note that this implicitly sets the -replace option.')
    flip_x = traits.Bool(argstr='-flipx',
      position=1,
      desc="assume the transform is supplied assuming a coordinate system with the x-axis reversed relative to the MRtrix convention (i.e. x increases from right to left). This is required to handle transform matrices produced by FSL's FLIRT command. This is only used in conjunction with the -reference option.")
    quiet = traits.Bool(argstr='-quiet',
      position=1,
      desc='Do not display information messages or progress status.')
    debug = traits.Bool(argstr='-debug',
      position=1,
      desc='Display debugging messages.')


class MRTransformOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc='the output image of the transformation')


class MRTransform(CommandLine):
    __doc__ = "\n    Apply spatial transformations or reslice images\n\n    Example\n    -------\n\n    >>> MRxform = MRTransform()\n    >>> MRxform.inputs.in_files = 'anat_coreg.mif'\n    >>> MRxform.run()                                   # doctest: +SKIP\n    "
    _cmd = 'mrtransform'
    input_spec = MRTransformInputSpec
    output_spec = MRTransformOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = self.inputs.out_filename
        if not isdefined(outputs['out_file']):
            outputs['out_file'] = op.abspath(self._gen_outfilename())
        else:
            outputs['out_file'] = op.abspath(outputs['out_file'])
        return outputs

    def _gen_filename(self, name):
        if name == 'out_filename':
            return self._gen_outfilename()
        else:
            return

    def _gen_outfilename(self):
        _, name, _ = split_filename(self.inputs.in_files[0])
        return name + '_MRTransform.mif'