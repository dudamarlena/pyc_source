# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pydeface/utils.py
# Compiled at: 2019-10-31 04:42:23
# Size of source mod 2**32: 4644 bytes
__doc__ = 'Utility scripts for pydeface.'
import os, shutil, sys
from pkg_resources import resource_filename, Requirement
import tempfile, numpy as np
from nipype.interfaces import fsl
from nibabel import load, Nifti1Image

def initial_checks(template=None, facemask=None):
    """Initial sanity checks."""
    if template is None:
        template = resource_filename(Requirement.parse('pydeface'), 'pydeface/data/mean_reg2mean.nii.gz')
    else:
        if facemask is None:
            facemask = resource_filename(Requirement.parse('pydeface'), 'pydeface/data/facemask.nii.gz')
        if not os.path.exists(template):
            raise Exception('Missing template: %s' % template)
        assert os.path.exists(facemask), 'Missing face mask: %s' % facemask
    if 'FSLDIR' not in os.environ:
        raise Exception('FSL must be installed and FSLDIR environment variable must be defined.')
        sys.exit(2)
    return (template, facemask)


def output_checks--- This code section failed: ---

 L.  36         0  LOAD_FAST                'force'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  37         8  LOAD_CONST               False
               10  STORE_FAST               'force'
             12_0  COME_FROM             6  '6'

 L.  38        12  LOAD_FAST                'outfile'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    32  'to 32'

 L.  39        20  LOAD_FAST                'infile'
               22  LOAD_METHOD              replace
               24  LOAD_STR                 '.nii'
               26  LOAD_STR                 '_defaced.nii'
               28  CALL_METHOD_2         2  ''
               30  STORE_FAST               'outfile'
             32_0  COME_FROM            18  '18'

 L.  41        32  LOAD_GLOBAL              os
               34  LOAD_ATTR                path
               36  LOAD_METHOD              exists
               38  LOAD_FAST                'outfile'
               40  CALL_METHOD_1         1  ''
               42  POP_JUMP_IF_FALSE    58  'to 58'
               44  LOAD_FAST                'force'
               46  POP_JUMP_IF_FALSE    58  'to 58'

 L.  42        48  LOAD_GLOBAL              print
               50  LOAD_STR                 'Previous output will be overwritten.'
               52  CALL_FUNCTION_1       1  ''
               54  POP_TOP          
               56  JUMP_FORWARD         84  'to 84'
             58_0  COME_FROM            46  '46'
             58_1  COME_FROM            42  '42'

 L.  43        58  LOAD_GLOBAL              os
               60  LOAD_ATTR                path
               62  LOAD_METHOD              exists
               64  LOAD_FAST                'outfile'
               66  CALL_METHOD_1         1  ''
               68  POP_JUMP_IF_FALSE    84  'to 84'

 L.  44        70  LOAD_GLOBAL              Exception
               72  LOAD_STR                 "%s already exists. Remove it first or use '--force' flag to overwrite."

 L.  45        74  LOAD_FAST                'outfile'
               76  BINARY_MODULO    
               78  CALL_FUNCTION_1       1  ''
               80  RAISE_VARARGS_1       1  ''
               82  JUMP_FORWARD         84  'to 84'
             84_0  COME_FROM            82  '82'
             84_1  COME_FROM            68  '68'
             84_2  COME_FROM            56  '56'

 L.  48        84  LOAD_FAST                'outfile'
               86  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 86


def generate_tmpfiles(verbose=True):
    _, template_reg_mat = tempfile.mkstemp(suffix='.mat')
    _, warped_mask = tempfile.mkstemp(suffix='.nii.gz')
    if verbose:
        print('Temporary files:\n  %s\n  %s' % (template_reg_mat, warped_mask))
    _, template_reg = tempfile.mkstemp(suffix='.nii.gz')
    _, warped_mask_mat = tempfile.mkstemp(suffix='.mat')
    return (
     template_reg, template_reg_mat, warped_mask, warped_mask_mat)


def cleanup_files(*args):
    print('Cleaning up...')
    for p in args:
        if os.path.exists(p):
            os.remove(p)


def get_outfile_type(outpath):
    if outpath.endswith('nii.gz'):
        return 'NIFTI_GZ'
    if outpath.endswith('nii'):
        return 'NIFTI'
    raise ValueError('outfile path should be have .nii or .nii.gz suffix')


def deface_image(infile=None, outfile=None, facemask=None, template=None, cost='mutualinfo', force=False, forcecleanup=False, verbose=True, **kwargs):
    if not infile:
        raise ValueError('infile must be specified')
    else:
        if shutil.which('fsl') is None:
            raise EnvironmentError('fsl cannot be found on the path')
        template, facemask = initial_checks(template, facemask)
        outfile = output_checks(infile, outfile, force)
        template_reg, template_reg_mat, warped_mask, warped_mask_mat = generate_tmpfiles()
        print('Defacing...\n  %s' % infile)
        outfile_type = get_outfile_type(template_reg)
        flirt = fsl.FLIRT()
        flirt.inputs.cost_func = cost
        flirt.inputs.in_file = template
        flirt.inputs.out_matrix_file = template_reg_mat
        flirt.inputs.out_file = template_reg
        flirt.inputs.output_type = outfile_type
        flirt.inputs.reference = infile
        flirt.run()
        outfile_type = get_outfile_type(warped_mask)
        flirt = fsl.FLIRT()
        flirt.inputs.in_file = facemask
        flirt.inputs.in_matrix_file = template_reg_mat
        flirt.inputs.apply_xfm = True
        flirt.inputs.reference = infile
        flirt.inputs.out_file = warped_mask
        flirt.inputs.output_type = outfile_type
        flirt.inputs.out_matrix_file = warped_mask_mat
        flirt.run()
        infile_img = load(infile)
        warped_mask_img = load(warped_mask)
        try:
            outdata = infile_img.get_data().squeeze() * warped_mask_img.get_data()
        except ValueError:
            tmpdata = np.stack(([warped_mask_img.get_data()] * infile_img.get_data().shape[(-1)]),
              axis=(-1))
            outdata = infile_img.get_data() * tmpdata

    masked_brain = Nifti1Image(outdata, infile_img.get_affine(), infile_img.get_header())
    masked_brain.to_filename(outfile)
    print('Defaced image saved as:\n  %s' % outfile)
    if forcecleanup:
        cleanup_files(warped_mask, template_reg, template_reg_mat)
        return warped_mask_img
    return (
     warped_mask_img, warped_mask, template_reg, template_reg_mat)