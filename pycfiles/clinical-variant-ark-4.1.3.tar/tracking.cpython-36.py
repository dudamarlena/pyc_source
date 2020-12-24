# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mdiazmel/code/aramis/clinica/clinica/lib/nipype/interfaces/mrtrix3/tracking.py
# Compiled at: 2019-10-10 04:46:12
# Size of source mod 2**32: 13577 bytes
from __future__ import print_function, division, unicode_literals, absolute_import
import os.path as op
from nipype.interfaces.base import traits, TraitedSpec, File
from nipype.interfaces.mrtrix3.base import MRTrix3BaseInputSpec, MRTrix3Base

class TractographyInputSpec(MRTrix3BaseInputSpec):
    sph_trait = traits.Tuple((traits.Float),
      (traits.Float),
      (traits.Float),
      (traits.Float),
      argstr='%f,%f,%f,%f')
    in_file = File(exists=True,
      argstr='%s',
      mandatory=True,
      position=(-2),
      desc='input file to be processed')
    out_file = File('tracked.tck',
      argstr='%s',
      mandatory=True,
      position=(-1),
      usedefault=True,
      desc='output file containing tracks')
    algorithm = traits.Enum('iFOD2',
      'FACT',
      'iFOD1',
      'Nulldist',
      'SD_Stream',
      'Tensor_Det',
      'Tensor_Prob',
      usedefault=True,
      argstr='-algorithm %s',
      desc='tractography algorithm to be used')
    roi_incl = traits.Either(File(exists=True),
      sph_trait,
      argstr='-include %s',
      desc='specify an inclusion region of interest, streamlines must traverse ALL inclusion regions to be accepted')
    roi_excl = traits.Either(File(exists=True),
      sph_trait,
      argstr='-exclude %s',
      desc='specify an exclusion region of interest, streamlines that enter ANY exclude region will be discarded')
    roi_mask = traits.Either(File(exists=True),
      sph_trait,
      argstr='-mask %s',
      desc='specify a masking region of interest. If defined,streamlines exiting the mask will be truncated')
    step_size = traits.Float(argstr='-step %f',
      desc='set the step size of the algorithm in mm (default is 0.1 x voxelsize; for iFOD2: 0.5 x voxelsize)')
    angle = traits.Float(argstr='-angle %f',
      desc='set the maximum angle between successive steps (default is 90deg x stepsize / voxelsize)')
    n_tracks = traits.Int(argstr='-select %d',
      desc='set the desired number of tracks. The program will continue to generate tracks until this number of tracks have been selected and written to the output file')
    max_tracks = traits.Int(argstr='-maxnum %d',
      desc="set the maximum number of tracks to generate. The program will not generate more tracks than this number, even if the desired number of tracks hasn't yet been reached (default is 100 x number)")
    max_length = traits.Float(argstr='-maxlength %f',
      desc='set the maximum length of any track in mm (default is 100 x voxelsize)')
    min_length = traits.Float(argstr='-minlength %f',
      desc='set the minimum length of any track in mm (default is 5 x voxelsize)')
    cutoff = traits.Float(argstr='-cutoff %f',
      desc='set the FA or FOD amplitude cutoff for terminating tracks (default is 0.1)')
    cutoff_init = traits.Float(argstr='-initcutoff %f',
      desc='set the minimum FA or FOD amplitude for initiating tracks (default is the same as the normal cutoff)')
    n_trials = traits.Int(argstr='-trials %d',
      desc='set the maximum number of sampling trials at each point (only used for probabilistic tracking)')
    unidirectional = traits.Bool(argstr='-unidirectional',
      desc='track from the seed point in one direction only (default is to track in both directions)')
    init_dir = traits.Tuple((traits.Float),
      (traits.Float),
      (traits.Float),
      argstr='-initdirection %f,%f,%f',
      desc='specify an initial direction for the tracking (this should be supplied as a vector of 3 comma-separated values')
    noprecompt = traits.Bool(argstr='-noprecomputed',
      desc='do NOT pre-compute legendre polynomial values. Warning: this will slow down the algorithm by a factor of approximately 4')
    power = traits.Int(argstr='-power %d',
      desc='raise the FOD to the power specified (default is 1/nsamples)')
    n_samples = traits.Int(4,
      usedefault=True, argstr='-samples %d',
      desc='set the number of FOD samples to take per step for the 2nd order (iFOD2) method')
    use_rk4 = traits.Bool(argstr='-rk4',
      desc='use 4th-order Runge-Kutta integration (slower, but eliminates curvature overshoot in 1st-order deterministic methods)')
    stop = traits.Bool(argstr='-stop',
      desc='stop propagating a streamline once it has traversed all include regions')
    downsample = traits.Float(argstr='-downsample %f',
      desc='downsample the generated streamlines to reduce output file size')
    act_file = File(exists=True,
      argstr='-act %s',
      desc='use the Anatomically-Constrained Tractography framework during tracking; provided image must be in the 5TT (five - tissue - type) format')
    backtrack = traits.Bool(argstr='-backtrack',
      desc='allow tracks to be truncated')
    crop_at_gmwmi = traits.Bool(argstr='-crop_at_gmwmi',
      desc='crop streamline endpoints more precisely as they cross the GM-WM interface')
    seed_sphere = traits.Tuple((traits.Float),
      (traits.Float),
      (traits.Float),
      (traits.Float),
      argstr='-seed_sphere %f,%f,%f,%f',
      desc='spherical seed')
    seed_image = File(exists=True,
      argstr='-seed_image %s',
      desc='seed streamlines entirely at random within mask')
    seed_rnd_voxel = traits.Tuple(File(exists=True),
      (traits.Int()),
      argstr='-seed_random_per_voxel %s %d',
      xor=[
     'seed_image', 'seed_grid_voxel'],
      desc='seed a fixed number of streamlines per voxel in a mask image; random placement of seeds in each voxel')
    seed_grid_voxel = traits.Tuple(File(exists=True),
      (traits.Int()),
      argstr='-seed_grid_per_voxel %s %d',
      xor=[
     'seed_image', 'seed_rnd_voxel'],
      desc='seed a fixed number of streamlines per voxel in a mask image; place seeds on a 3D mesh grid (grid_size argument is per axis; so a grid_size of 3 results in 27 seeds per voxel)')
    seed_rejection = File(exists=True,
      argstr='-seed_rejection %s',
      desc='seed from an image using rejection sampling (higher values = more probable to seed from')
    seed_gmwmi = File(exists=True,
      argstr='-seed_gmwmi %s',
      requires=[
     'act_file'],
      desc='seed from the grey matter - white matter interface (only valid if using ACT framework)')
    seed_dynamic = File(exists=True,
      argstr='-seed_dynamic %s',
      desc='determine seed points dynamically using the SIFT model (must not provide any other seeding mechanism). Note that while this seeding mechanism improves the distribution of reconstructed streamlines density, it should NOT be used as a substitute for the SIFT method itself.')
    max_seed_attempts = traits.Int(argstr='-max_seed_attempts %d',
      desc='set the maximum number of times that the tracking algorithm should attempt to find an appropriate tracking direction from a given seed point')
    out_seeds = File('out_seeds.nii.gz',
      usedefault=True, argstr='-output_seeds %s',
      desc='output the seed location of all successful streamlines to a file')


class TractographyOutputSpec(TraitedSpec):
    out_file = File(exists=True, desc='the output filtered tracks')
    out_seeds = File(desc='output the seed location of all successful streamlines to a file')


class Tractography(MRTrix3Base):
    """Tractography"""
    _cmd = 'tckgen'
    input_spec = TractographyInputSpec
    output_spec = TractographyOutputSpec

    def _format_arg(self, name, trait_spec, value):
        if 'roi_' in name and isinstance(value, tuple):
            value = ['%f' % v for v in value]
            return trait_spec.argstr % ','.join(value)
        else:
            return super(Tractography, self)._format_arg(name, trait_spec, value)

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_file'] = op.abspath(self.inputs.out_file)
        return outputs


class TckSiftInputSpec(MRTrix3BaseInputSpec):
    in_tracks = File(exists=True,
      argstr='%s',
      mandatory=True,
      position=0,
      desc='the input track file')
    in_fod = File(exists=True,
      argstr='%s',
      mandatory=True,
      position=1,
      desc='input image containing the spherical harmonics of the fibre orientation distributions')
    out_tracks = File('out_tracks.tck',
      argstr='%s',
      mandatory=True,
      position=2,
      usedefault=True,
      desc='the output filtered tracks file')


class TckSiftOutputSpec(TraitedSpec):
    out_tracks = File(exists=True, desc='the output filtered tracks file')


class TckSift(MRTrix3Base):
    """TckSift"""
    _cmd = 'tcksift'
    input_spec = TckSiftInputSpec
    output_spec = TckSiftOutputSpec

    def _list_outputs(self):
        outputs = self.output_spec().get()
        outputs['out_tracks'] = op.abspath(self.inputs.out_tracks)
        return outputs