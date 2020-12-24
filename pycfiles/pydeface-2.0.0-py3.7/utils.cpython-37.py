# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pydeface/utils.py
# Compiled at: 2019-10-31 04:42:23
# Size of source mod 2**32: 4644 bytes
"""Utility scripts for pydeface."""
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
    return (
     template, facemask)


def output_checks(infile, outfile=None, force=False):
    """Determine output file name."""
    if force is None:
        force = False
    if outfile is None:
        outfile = infile.replace('.nii', '_defaced.nii')
    if os.path.exists(outfile) and force:
        print('Previous output will be overwritten.')
    else:
        if os.path.exists(outfile):
            raise Exception("%s already exists. Remove it first or use '--force' flag to overwrite." % outfile)
        else:
            return outfile


def generate_tmpfiles(verbose=True):
    _, template_reg_mat = tempfile.mkstemp(suffix='.mat')
    _, warped_mask = tempfile.mkstemp(suffix='.nii.gz')
    if verbose:
        print('Temporary files:\n  %s\n  %s' % (template_reg_mat, warped_mask))
    _, template_reg = tempfile.mkstemp(suffix='.nii.gz')
    _, warped_mask_mat = tempfile.mkstemp(suffix='.mat')
    return (template_reg, template_reg_mat, warped_mask, warped_mask_mat)


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
    return (warped_mask_img, warped_mask, template_reg, template_reg_mat)