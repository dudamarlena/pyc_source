# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/hcpre/interfaces.py
# Compiled at: 2014-06-10 20:28:57
import os, sys, math
from nipype.interfaces.traits_extension import isdefined
from nipype.interfaces.base import BaseInterface, InputMultiPath, OutputMultiPath, BaseInterfaceInputSpec, traits, File, TraitedSpec, CommandLineInputSpec, CommandLine, Directory
from traits.trait_errors import TraitError
import nipype.interfaces.dcm2nii as d2n
from duke_siemens.util_dicom_siemens import read as read_siemens_shadow
from hcpre.util import *
from hcpre.config import *

class HCDcm2nii(d2n.Dcm2nii):
    """ We override to fix a bug in output listing... """

    def _parse_stdout(self, stdout):
        import re, os
        files = []
        reoriented_files = []
        reoriented_and_cropped_files = []
        bvecs = []
        bvals = []
        skip = False
        last_added_file = None
        for line in stdout.split('\n'):
            if not skip:
                file = None
                if line.startswith('Saving '):
                    file = line[len('Saving '):]
                elif line.startswith('GZip...'):
                    if isdefined(self.inputs.output_dir):
                        output_dir = self.inputs.output_dir
                    else:
                        output_dir = self._gen_filename('output_dir')
                    file = os.path.abspath(os.path.join(output_dir, line[len('GZip...'):]))
                elif line.startswith('Number of diffusion directions '):
                    if last_added_file:
                        base, filename, ext = split_filename(last_added_file)
                        bvecs.append(os.path.join(base, filename + '.bvec'))
                        bvals.append(os.path.join(base, filename + '.bval'))
                elif re.search('.*->(.*)', line):
                    val = re.search('.*->(.*)', line)
                    val = val.groups()[0]
                    if isdefined(self.inputs.output_dir):
                        output_dir = self.inputs.output_dir
                    else:
                        output_dir = self._gen_filename('output_dir')
                    val = os.path.join(output_dir, val)
                    file = val
                if file:
                    if last_added_file and os.path.exists(file) and last_added_file not in file:
                        files.append(file)
                    last_added_file = file
                    continue
                if line.startswith('Reorienting as '):
                    reoriented_files.append(line[len('Reorienting as '):])
                    skip = True
                    continue
                elif line.startswith('Cropping NIfTI/Analyze image '):
                    base, filename = os.path.split(line[len('Cropping NIfTI/Analyze image '):])
                    filename = 'c' + filename
                    reoriented_and_cropped_files.append(os.path.join(base, filename))
                    skip = True
                    continue
            skip = False

        return (
         files, reoriented_files, reoriented_and_cropped_files, bvecs, bvals)


class DicomInfoInputSpec(BaseInterfaceInputSpec):
    files = InputMultiPath(traits.Either(traits.List(File(exists=True)), File(exists=True)), mandatory=True, desc='a list of dicom files from which to extract data', copyfile=False)


class DicomInfoOutputSpec(TraitedSpec):
    info = traits.List(traits.Dict(), desc='an ordered list of dicts, all in the same directory.')


class DicomInfo(BaseInterface):
    input_spec = DicomInfoInputSpec
    output_spec = DicomInfoOutputSpec

    def __init__(self, *args, **kwargs):
        super(DicomInfo, self).__init__(*args, **kwargs)
        self.info = []

    def _run_interface(self, runtime):
        import dicom
        files = self.inputs.files
        by_series = {}
        self.info = []
        for f in files:
            d = dicom.read_file(f)
            try:
                s_num = d.SeriesNumber
                s_num = int(s_num)
            except Exception as e:
                raise e

            if s_num not in by_series:
                by_series[s_num] = {'series_num': s_num, 'series_desc': getattr(d, 'SeriesDescription', None), 
                   'protocol_name': getattr(d, 'ProtocolName', None)}
                if [
                 25, 4120] in d and 'description' in dir(d[(25, 4120)]) and 'RealDwellTime' in d[(25,
                                                                                                  4120)].description():
                    try:
                        by_series[s_num]['RealDwellTime'] = float(d[(25, 4120)].value)
                    except Exception as e:
                        pass

                it = getattr(d, 'ImageType', None)
                if it:
                    if not isinstance(it, str):
                        it = list(it)
                    by_series[s_num]['image_type'] = it
                ipped = getattr(d, 'InPlanePhaseEncodingDirection', None)
                if ipped:
                    by_series[s_num]['ipp_encoding_direction'] = ipped
                bpppe = d.get((25, 4136), None)
                if bpppe:
                    try:
                        bpppe = float(bpppe.value)
                    except Exception as e:
                        pass
                    else:
                        by_series[s_num]['bw_per_pix_phase_encode'] = bpppe

                acq_mat = getattr(d, 'AcquisitionMatrix', None)
                if acq_mat and len(acq_mat) == 4:
                    by_series[s_num]['acq_matrix_n'] = acq_mat[0] or acq_mat[1]
                    by_series[s_num]['acq_matrix_m'] = acq_mat[2] or acq_mat[3]
                orient = orientation_from_dcm_header(d)
                if orient:
                    by_series[s_num]['orientation'] = orient
                try:
                    ss = read_siemens_shadow(f)[0]
                except Exception as e:
                    pass
                else:
                    siemens_keys = [
                     'in_plane_rotation', 'polarity_swap']
                    by_series[s_num].update(dict([ (k, v) for k, v in ss.iteritems() if k in siemens_keys ]))

            bs = by_series[s_num]
            try:
                et = getattr(d, 'EchoTime', None)
                if et:
                    et = float(et)
                    if 'echo_times' not in bs:
                        bs['echo_times'] = []
                    if et not in bs['echo_times']:
                        bs['echo_times'].append(et)
            except Exception as e:
                pass

        for s_num, s_info in by_series.iteritems():
            if 'echo_times' in s_info:
                etc = len(s_info['echo_times'])
                if etc == 0:
                    del s_info['echo_times']
                elif etc == 1:
                    s_info['echo_time'] = s_info['echo_times'][0]
                    del s_info['echo_times']
                elif etc == 2:
                    s_info['delta_te'] = abs(s_info['echo_times'][0] - s_info['echo_times'][1])

        for k in sorted(by_series.keys()):
            self.info.append(by_series[k])

        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['info'] = self.info
        return outputs


class NiiWranglerInputSpec(BaseInterfaceInputSpec):
    nii_files = InputMultiPath(traits.Either(traits.List(File(exists=True)), File(exists=True)), mandatory=True, desc='a list of nifti files to be categorized, matched up, etc.', copyfile=False)
    series_map = traits.Dict(key_trait=traits.Str(), value_trait=traits.List(), value={}, mandatory=False, usedefault=True, desc='keys are any member of SCAN_TYPES, values are lists of series                  descriptions as recorded in DICOM headers.')
    dicom_info = traits.List(mandatory=True, desc='one dict for each series in the session, in the order they were                  run. each dict should contain at least the series_num (int) and                  the series_desc (str).')
    ep_echo_spacing = traits.Either(traits.Enum('NONE'), traits.Float(), desc="\n            The effective echo spacing of your BOLD images. Already accounts\n            for whether or not iPAT (acceleration in the phase direction) was\n            used. If you're using acceleration, then the EES is not going to\n            match the 'Echo Spacing' that Siemen's reports in the console.\n\n            Setting this value will prevent any attempt to derive it.")
    ep_unwarp_dir = traits.Enum('x', 'x-', '-x', 'y', 'y-', '-y', 'z', 'z-', '-z', desc='Setting this value will prevent any attempt to derive it.')
    block_struct_averaging = traits.Bool(False, mandatory=False, usedefault=True, desc='\n            Causes us to only use the first t1 and t2 images. A kludge for\n            some data that fails during structural averaging.')
    ep_fieldmap_selection = traits.Enum('first', 'most_recent', mandatory=False, usedefault=True, desc="\n            If you have more than one set of ep fieldmaps, then you can either\n            use the first set during preprocessing of all bold images\n            ('first'), or you can select the se fieldmap set that was taken\n            most recently prior to acquisition of a given bold image, or -\n            failing that - the first available se fieldmap thereafter\n            ('most_recent').")


class NiiWranglerOutputSpec(TraitedSpec):
    t1_structs = OutputMultiPath(traits.List(File(exists=True)), mandatory=True, desc='a list of t1 niftis in chronological order.')
    t2_structs = OutputMultiPath(traits.List(File(exists=True)), mandatory=True, desc='a list of t2 niftis in chronological order.')
    bolds = OutputMultiPath(traits.List(File(exists=True)), mandatory=True, desc='a list of BOLD niftis in chronological order.')
    bold_names = traits.List(traits.Str(), mandatory=True, desc='a list of names for the bold images. Length must match number of bold images.')
    sb_refs = OutputMultiPath(traits.List(File(exists=True)), mandatory=True, desc='a list of BOLD_SBRef niftis in chronological order. Length must match number of bold images.')
    pos_fieldmaps = OutputMultiPath(traits.List(File(exists=True)), mandatory=True, desc='a list of positive fieldmap niftis. Length must match number of bold images.')
    neg_fieldmaps = OutputMultiPath(traits.List(File(exists=True)), mandatory=True, desc='a list of negative fieldmap niftis. Length must match number of bold images.')
    mag_fieldmap = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, desc='magnitude fieldmap image for structural images. first matching image will be used.')
    phase_fieldmap = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, desc='phase fieldmap image for structural images. first matching image will be used.')
    t1_sample_spacing = traits.Either(traits.Float(), traits.Enum('NONE'), mandatory=False, usedefault=True, desc="DICOM field (0019,1018) * 10e-9 in s or 'NONE' if not used. (float) seconds.")
    t2_sample_spacing = traits.Either(traits.Float(), traits.Enum('NONE'), mandatory=False, usedefault=True, desc="DICOM field (0019,1018) * 10e-9 in s or 'NONE' if not used. (float) seconds.")
    fieldmap_te = traits.Either(traits.Enum('NONE'), traits.Float(), default='NONE', mandatory=False, usedefault=True, desc="delta TE in ms for magnitude fieldmap or 'NONE' if not used.")
    ep_echo_spacings = traits.List(traits.Either(traits.Enum('NONE'), traits.Float()), value=[
     'NONE'], mandatory=False, usedefault=True, desc="\n            The effective echo spacing of your BOLD images. Already accounts\n            for whether or not iPAT (acceleration in the phase direction) was\n            used. If you're using acceleration, then the EES is not going to\n            match the 'Echo Spacing' that Siemen's reports in the console.\n\n            This value will be derived, if not overridden by the input of the\n            same name. Please inspect the value after your initial run of the\n            pipeline to ensure that it's sane.\n\n            Length must match number of bold images.")
    ep_unwarp_dirs = traits.List(traits.Enum('x', 'x-', '-x', 'y', 'y-', '-y', 'z', 'z-', '-z'), mandatory=True, desc='Length must match number of bold images.')


class NiiWrangler(BaseInterface):
    input_spec = NiiWranglerInputSpec
    output_spec = NiiWranglerOutputSpec

    def __init__(self, *args, **kwargs):
        super(NiiWrangler, self).__init__(*args, **kwargs)
        self.t1_files = []
        self.t2_files = []
        self.bolds = []
        self.bold_names = []
        self.sbrefs = []
        self.fieldmap_pos = []
        self.fieldmap_neg = []
        self.fieldmap_mag = []
        self.fieldmap_ph = []
        self.fieldmap_mag_delta_te = 'NONE'
        self.t1_sample_spacing = 0.0
        self.t2_sample_spacing = 0.0
        self.ep_e_spaces = None
        self.ep_unwarp_dirs = None
        return

    def _run_interface(self, runtime):
        import re, operator
        nii_files = self.inputs.nii_files
        smap = self.inputs.series_map
        dinfo = self.inputs.dicom_info
        block_averaging = self.inputs.block_struct_averaging
        s_num_reg = re.compile('.*s(\\d+)a(?!.*/)')
        nii_by_series = {}
        fails = []
        extras = []
        for fn in nii_files:
            try:
                sn = int(s_num_reg.match(fn).groups()[0])
                if sn in nii_by_series:
                    extras.append(fn)
                    continue
                nii_by_series[sn] = fn
            except Exception as e:
                fails.append(fn)

        if fails:
            raise ValueError('Could not derive series number from file names: %s.' % str(fails))
        if extras:
            print >> sys.stderr, '\nWARNING: Ignoring extra niftis: %s\n' % str(extras)
        m_count = 0
        for sn, fn in nii_by_series.iteritems():
            m = filter(lambda x: x.get('series_num', -1) == sn, dinfo)
            if not m:
                continue
            m_count += 1
            m[0]['nifti_file'] = fn

        if not m_count == len(dinfo):
            raise ValueError('incorrect number of nifti->series matches (%d/%d)' % (m_count, len(dinfo)))
        nf = 'nifti_file'
        sd = 'series_desc'
        it = 'image_type'
        t1fs = [ d for d in filter(lambda x: sd in x and x[sd] in smap.get('t1', []), dinfo) if nf in d ]
        t2fs = [ d for d in filter(lambda x: sd in x and x[sd] in smap.get('t2', []), dinfo) if nf in d ]
        if block_averaging:
            t1fs = [
             t1fs[0]]
            t2fs = [t2fs[0]]
        self.t1_files = [ d[nf] for d in t1fs ]
        self.t2_files = [ d[nf] for d in t2fs ]
        bs = [ d for d in filter(lambda x: sd in x and x[sd] in smap.get('bold', []), dinfo) if nf in d
             ]
        self.bolds = [ d[nf] for d in bs ]
        self.sbrefs = [ d[nf] for d in filter(lambda x: sd in x and x[sd] in smap.get('bold_sbref', []), dinfo) if nf in d ]
        s_policy = self.inputs.ep_fieldmap_selection
        pos_types = reduce(operator.add, [ smap.get(k, []) for k in POS_FIELDMAPS ])
        neg_types = reduce(operator.add, [ smap.get(k, []) for k in NEG_FIELDMAPS ])
        pos = [ d for d in filter(lambda x: sd in x and x[sd] in pos_types, dinfo) if nf in d ]
        neg = [ d for d in filter(lambda x: sd in x and x[sd] in neg_types, dinfo) if nf in d ]
        both = zip(pos, neg)
        if s_policy == 'most_recent':
            pfs = []
            nfs = []
            for bold in bs:
                sn = bold['series_num']
                earlier = filter(lambda x: x[0]['series_num'] < sn and x[1]['series_num'] < sn, both)
                later = filter(lambda x: x[0]['series_num'] < sn and x[1]['series_num'] < sn, both)
                if earlier:
                    pfs.append(earlier[(-1)][0][nf])
                    nfs.append(earlier[(-1)][1][nf])
                elif later:
                    pfs.append(later[0][0][nf])
                    nfs.append(later[0][1][nf])
                else:
                    print 'This... should never happen.'

            self.fieldmaps_pos = pfs
            self.fieldmaps_neg = nfs
        else:
            self.fieldmaps_pos = [ pos[0][nf] for n in self.bolds ] if pos else []
            self.fieldmaps_neg = [ neg[0][nf] for n in self.bolds ] if pos else []
        mag_fs = filter(lambda x: sd in x and x[sd] in smap.get('fieldmap_magnitude', []) and it in x and isinstance(x[it], list) and len(x[it]) > 2 and x[it][2].strip().lower() == 'm', dinfo)
        phase_fs = filter(lambda x: sd in x and x[sd] in smap.get('fieldmap_phase', []) and it in x and isinstance(x[it], list) and len(x[it]) > 2 and x[it][2].strip().lower() == 'p', dinfo)
        self.fieldmap_mag = [ d[nf] for d in mag_fs if nf in d ]
        self.fieldmap_ph = [ d[nf] for d in phase_fs if nf in d ]
        ep_calc_fail = False
        if isdefined(self.inputs.ep_echo_spacing):
            self.ep_e_spaces = [ self.inputs.ep_echo_spacing for n in self.bolds ]
        elif bs and any([ 'bw_per_pix_phase_encode' in d and 'acq_matrix_n' in d for d in bs ]):
            if not all([ 'bw_per_pix_phase_encode' in d and 'acq_matrix_n' in d for d in bs ]):
                ep_calc_fail = True
            else:
                self.ep_e_spaces = [ 1 / (d['bw_per_pix_phase_encode'] * d['acq_matrix_n']) for d in bs ]
        else:
            self.ep_e_spaces = [ 'NONE' for n in self.bolds ]
        if mag_fs and self.fieldmap_mag and self.fieldmap_ph:
            self.fieldmap_mag_delta_te = mag_fs[0].get('delta_te', 'NONE')
        else:
            self.fieldmap_mag_delta_te = 'NONE'
        self.bold_names = [ 'bold_%d' % n for n in xrange(len(self.bolds)) ]
        if isdefined(self.inputs.ep_unwarp_dir):
            self.ep_unwarp_dirs = [ self.inputs.ep_unwarp_dir for n in self.bolds ]
            pswaps = smap.get('polarity_swapped', [])
            if pswaps:
                for b_idx, uw_dir in enumerate(self.ep_unwarp_dirs):
                    if bs[b_idx].get('series_desc', None) in pswaps:
                        raw_dir = uw_dir.replace('-', '')
                        self.ep_unwarp_dirs[b_idx] = '-' + raw_dir if '-' not in uw_dir else raw_dir

        else:
            raise ValueError("We can't derive ep_unwarp_dir yet. Please set it in the nii wrangler config section.")
        if not (len(self.fieldmap_mag) and len(self.fieldmap_ph)):
            print >> sys.stderr, '\nWARNING: found %d magnitude fieldmaps and %d phase fieldmaps.\n' % (len(self.fieldmap_mag), len(self.fieldmap_ph))
        if self.sbrefs and len(self.sbrefs) != len(self.bolds):
            raise ValueError('Had %d bolds, but %d SBRefs. If there are any SBRefs, there must be one for each BOLD image' % (
             len(self.bolds), len(self.sbrefs)))
        if not self.sbrefs:
            self.sbrefs = [ 'NONE' for n in self.bolds ]
        if len(self.fieldmaps_pos) != len(self.fieldmaps_neg):
            raise ValueError('Mismatched number of pos and neg fieldmaps (%d/%d)' % (len(self.fieldmaps_pos), len(self.fieldmaps_neg)))
        if len(self.fieldmaps_pos) != len(self.bolds):
            raise ValueError('Mismatched number of pos/neg fieldmaps and bolds (%d/%d)' % (len(self.fieldmaps_pos), len(self.bolds)))
        if t1fs and 'RealDwellTime' in t1fs[0].keys():
            self.t1_sample_spacing = t1fs[0]['RealDwellTime'] * math.pow(10, -9)
        else:
            self.t1_sample_spacing = 'NONE'
        if t2fs and 'RealDwellTime' in t2fs[0].keys():
            self.t2_sample_spacing = t2fs[0]['RealDwellTime'] * math.pow(10, -9)
        else:
            self.t2_sample_spacing = 'NONE'
        if ep_calc_fail:
            raise ValueError('Unabel to calculate ep echo spacing. Try specifying manually in nii wrangler config section.')
        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['t1_structs'] = self.t1_files
        outputs['t2_structs'] = self.t2_files
        outputs['bolds'] = self.bolds
        outputs['bold_names'] = self.bold_names
        outputs['sb_refs'] = self.sbrefs
        outputs['pos_fieldmaps'] = self.fieldmaps_pos
        outputs['neg_fieldmaps'] = self.fieldmaps_neg
        fm = self.fieldmap_mag
        fp = self.fieldmap_ph
        outputs['mag_fieldmap'] = fm[0] if fm and fp else 'NONE'
        outputs['phase_fieldmap'] = fp[0] if fm and fp else 'NONE'
        if not (fm and fp):
            print >> sys.stderr, '\nWARNING: not using magnitude or phase fieldmaps.\n'
        outputs['t1_sample_spacing'] = self.t1_sample_spacing
        outputs['t2_sample_spacing'] = self.t2_sample_spacing
        outputs['fieldmap_te'] = self.fieldmap_mag_delta_te
        outputs['ep_echo_spacings'] = self.ep_e_spaces
        outputs['ep_unwarp_dirs'] = self.ep_unwarp_dirs
        return outputs


class HCPCommandInputSpec(CommandLineInputSpec):
    full_command = traits.Str('PreFreeSurferPipeline.sh', mandatory=False, usedefault=True, desc='Full path to the relevant HCP script.')


class HCPCommandOutputSpec(TraitedSpec):
    subject = traits.Str(mandatory=True, desc='subject id or number, as a string')


class HCPCommand(CommandLine):
    """ Handles setting of _cmd to full path.

    Input spec must be a subclass of HCPCommandInputSpec.
    """

    def _run_interface(self, runtime):
        import os
        self._cmd = self.inputs.full_command
        return super(HCPCommand, self)._run_interface(runtime)


class PreFSInputSpec(HCPCommandInputSpec):
    full_command = traits.Str('PreFreeSurferPipeline.sh', mandatory=False, usedefault=True, desc='Full path to the relevant HCP script.')
    study_dir = traits.Either(traits.Enum(None), Directory(exists=True), default=None, mandatory=False, usedefault=True, position=0, argstr='--path="%s"', desc='Leave as None to have the interface make a new dir in its working dir.')
    subject = traits.Str(mandatory=True, position=1, argstr='--subject="%s"', desc='')
    t1_files = InputMultiPath(traits.Either(traits.List(File(exists=True)), File(exists=True)), mandatory=True, sep='@', position=2, argstr='--t1="%s"', desc='t1 files.')
    t2_files = InputMultiPath(traits.Either(traits.List(File(exists=True)), File(exists=True)), mandatory=True, sep='@', position=3, argstr='--t2="%s"', desc='t2 files.')
    t1_template = InputMultiPath(File(exists=True), mandatory=True, position=4, argstr='--t1template="%s"', desc='MNI0.7mm template')
    t1_template_brain = InputMultiPath(File(exists=True), mandatory=True, position=5, argstr='--t1templatebrain="%s"', desc='Brain extracted MNI0.7mm template')
    t1_template_2mm = InputMultiPath(File(exists=True), mandatory=True, position=6, argstr='--t1template2mm="%s"', desc='MNI2mm template')
    t2_template = InputMultiPath(File(exists=True), mandatory=True, position=7, argstr='--t2template="%s"', desc='MNI0.7mm T2wTemplate')
    t2_template_brain = InputMultiPath(File(exists=True), mandatory=True, position=8, argstr='--t2templatebrain="%s"', desc='Brain extracted MNI0.7mm T2wTemplate')
    t2_template_2mm = InputMultiPath(File(exists=True), mandatory=True, position=9, argstr='--t2template2mm="%s"', desc='MNI2mm T2wTemplate')
    template_mask = InputMultiPath(File(exists=True), mandatory=True, position=10, argstr='--templatemask="%s"', desc='Brain mask MNI0.7mm template')
    template_2mm_mask = InputMultiPath(File(exists=True), mandatory=True, position=11, argstr='--template2mmmask="%s"', desc='MNI2mm template')
    brain_size = traits.Int(150, mandatory=False, usedefault=True, position=12, argstr='--brainsize="%d"', desc='brain size in mm')
    fnirt_config = InputMultiPath(File(exists=True), mandatory=True, position=13, argstr='--fnirtconfig="%s"', desc='FNIRT 2mm T1w Config')
    fieldmap_magnitude = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=14, argstr='--fmapmag="%s"', xor=[
     'se_fieldmap_neg', 'se_fieldmap_pos', 'se_echo_spacing', 'se_unwarp_dir'], desc="Expects 4D magitude volume with two 3D timepoints or 'NONE' if not used")
    fieldmap_phase = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=15, argstr='--fmapphase="%s"', xor=[
     'se_fieldmap_neg', 'se_fieldmap_pos', 'se_echo_spacing', 'se_unwarp_dir'], desc="Expects 3D phase difference volume or 'NONE' if not used")
    fieldmap_te = traits.Either(traits.Enum('NONE'), traits.Float(), default='NONE', mandatory=False, usedefault=True, position=16, argstr='--echodiff="%s"', xor=[
     'se_fieldmap_neg', 'se_fieldmap_pos', 'se_echo_spacing', 'se_unwarp_dir'], desc="delta TE in ms for magnitude field map or 'NONE' if not used.")
    se_fieldmap_neg = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=17, argstr='--SEPhaseNeg="%s"', xor=[
     'fieldmap_magnitude', 'fieldmap_phase', 'fieldmap_te'], desc='\n            For the spin echo field map volume with a negative phase encoding\n            direction (LR in HCP data), set to NONE if using regular\n            FIELDMAP')
    se_fieldmap_pos = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=18, argstr='--SEPhasePos="%s"', xor=[
     'fieldmap_magnitude', 'fieldmap_phase', 'fieldmap_te'], desc='\n            For the spin echo field map volume with a positive phase encoding\n            direction (RL in HCP data), set to NONE if using regular\n            FIELDMAP')
    se_echo_spacing = traits.Either(traits.Enum('NONE'), traits.Float(), default='NONE', mandatory=False, usedefault=True, position=19, argstr='--echospacing="%s"', xor=[
     'fieldmap_magnitude', 'fieldmap_phase', 'fieldmap_te'], desc="Echo Spacing or Dwelltime of Spin Echo Field Map or 'NONE' if not used")
    se_unwarp_dir = traits.Enum('NONE', 'x', 'y', defaut='NONE', mandatory=False, usedefault=True, position=20, argstr='--seunwarpdir="%s"', xor=[
     'fieldmap_magnitude', 'fieldmap_phase', 'fieldmap_te'], desc="x or y (minus or not does not matter) 'NONE' if not used")
    t1_sample_spacing = traits.Either(traits.Enum('NONE'), traits.Float(), default='NONE', mandatory=False, usedefault=True, position=21, argstr='--t1samplespacing="%s"', desc="DICOM field (0019,1018) * 10e-9 in s or 'NONE' if not used.")
    t2_sample_spacing = traits.Either(traits.Enum('NONE'), traits.Float(), default='NONE', mandatory=False, usedefault=True, position=22, argstr='--t2samplespacing="%s"', desc="DICOM field (0019,1018) * 10e-9 in s or 'NONE' if not used.")
    unwarp_dir = traits.Enum('z', 'z-', '-z', 'x', 'x-', '-x', 'y', 'y-', '-y', 'NONE', mandatory=False, usedefault=True, position=23, argstr='--unwarpdir="%s"', desc="z appears to be best or 'NONE' if not used")
    grad_distort_coeffs = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=24, argstr='--gdcoeffs="%s"', desc="Location of Coeffs file or 'NONE' to skip")
    avg_rcd_method = traits.Enum('FIELDMAP', 'TOPUP', 'NONE', mandatory=False, usedefault=True, position=25, argstr='--avgrdcmethod="%s"', desc='\n    Averaging and readout distortion correction methods: "NONE" = average any\n    repeats with no readout correction "FIELDMAP" = average any repeats and use\n    field map for readout correction "TOPUP" = average and distortion correct at\n    the same time with topup/applytopup only works for 2 images currently')
    top_up_config = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=26, argstr='--topupconfig="%s"', desc="Config for topup or 'NONE' if not used")
    print_com = traits.Enum('', 'echo', mandatory=False, usedefault=True, position=27, argstr='--printcom=%s', desc='')


class PreFSOutputSpec(HCPCommandOutputSpec):
    study_dir = Directory(mandatory=True, exists=True, desc='the study dir')
    subject_dir = Directory(mandatory=False, exists=True, desc='the subject dir')
    subject_t1_dir = Directory(mandatory=False, exists=True, desc='the subject dir')
    t1_acpc_dc_restore = traits.File(mandatory=True, exists=True, desc='The resulting T1w_acpc_dc_restore.nii.gz')
    t1_acpc_dc_restore_brain = traits.File(mandatory=True, exists=True, desc='The resulting T1w_acpc_dc_restore_brain.nii.gz')
    t2_acpc_dc_restore = traits.File(mandatory=True, exists=True, desc='The resulting T2w_acpc_dc_restore.nii.gz')


class PreFS(HCPCommand):
    input_spec = PreFSInputSpec
    output_spec = PreFSOutputSpec
    _cmd = 'PreFreeSurferPipeline.sh'

    def _format_arg(self, name, spec, value):
        if name not in ('t1_sample_spacing', 't2_sample_spacing', 'fieldmap_te'):
            return super(PreFS, self)._format_arg(name, spec, value)
        st = value
        if isinstance(st, float):
            st = '%.9f' % st if name in ('t1_sample_spacing', 't2_sample_spacing') else str(st)
        st = (isinstance(st, str) or str)(st) if 1 else st
        return spec.argstr % st

    def _run_interface(self, runtime):
        import os
        sf = self.inputs.study_dir
        if not sf:
            sf = './study_dir'
        sf = os.path.abspath(sf)
        if not os.path.exists(sf):
            os.mkdir(sf)
        self.inputs.study_dir = sf
        return super(PreFS, self)._run_interface(runtime)

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['study_dir'] = self.inputs.study_dir
        outputs['subject'] = self.inputs.subject
        subj_d = os.path.join(self.inputs.study_dir, self.inputs.subject)
        if os.path.exists(subj_d):
            outputs['subject_dir'] = subj_d
        subj_t1_d = os.path.join(subj_d, 'T1w')
        if os.path.exists(subj_t1_d):
            outputs['subject_t1_dir'] = subj_t1_d
            files = {'T1w_acpc_dc_restore.nii.gz': 't1_acpc_dc_restore', 'T1w_acpc_dc_restore_brain.nii.gz': 't1_acpc_dc_restore_brain', 
               'T2w_acpc_dc_restore.nii.gz': 't2_acpc_dc_restore'}
            for f_name, v_name in files.iteritems():
                p = os.path.join(subj_t1_d, f_name)
                if not os.path.exists(p):
                    continue
                outputs[v_name] = p

        return outputs


class FSInputSpec(HCPCommandInputSpec):
    full_command = traits.Str('FreeSurferPipeline.sh', mandatory=True, desc='Full path to the relevant HCP script.')
    subject = traits.Str(mandatory=True, position=0, argstr='--subject="%s"', desc='')
    subject_t1_dir = InputMultiPath(Directory(exists=True), mandatory=True, position=1, argstr='--subjectDIR="%s"', desc='path to T1w dir created by the pre_freesurfer node.')
    t1_acpc_dc_restore = InputMultiPath(File(exists=True), mandatory=True, position=2, argstr='--t1="%s"', desc='')
    t1_acpc_dc_restore_brain = InputMultiPath(File(exists=True), mandatory=True, position=3, argstr='--t1brain="%s"', desc='')
    t2_acpc_dc_restore = InputMultiPath(File(exists=True), mandatory=True, position=4, argstr='--t2="%s"', desc='')
    print_com = traits.Enum('', 'echo', mandatory=False, usedefault=True, position=5, argstr='--printcom=%s', desc='')


class FSOutputSpec(HCPCommandOutputSpec):
    pass


class FS(HCPCommand):
    input_spec = FSInputSpec
    output_spec = FSOutputSpec
    _cmd = 'FreeSurferPipeline.sh'

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['subject'] = self.inputs.subject
        return outputs


class PostFSInputSpec(HCPCommandInputSpec):
    full_command = traits.Str('PostFreeSurferPipeline.sh', mandatory=True, desc='Full path to the relevant HCP script.')
    study_dir = Directory(mandatory=True, exists=True, position=0, argstr='--path="%s"', desc='The study dir. Should contain a subdir named after the subject.')
    subject = traits.Str(mandatory=True, position=1, argstr='--subject="%s"', desc='')
    surf_atlas_dir = Directory(mandatory=True, exists=True, position=2, argstr='--surfatlasdir="%s"', desc='')
    grayordinates_dir = Directory(mandatory=True, exists=True, position=3, argstr='--grayordinatesdir="%s"', desc='')
    grayordinates_res = traits.Int(2, mandatory=False, usedefault=True, position=4, argstr='--grayordinatesres="%d"', desc='\n            Usually 2mm.')
    high_res_mesh = traits.Int(164, mandatory=False, usedefault=True, position=5, argstr='--hiresmesh="%d"', desc='Usually 164k vertices')
    low_res_mesh = traits.Int(32, mandatory=False, usedefault=True, position=6, argstr='--lowresmesh="%d"', desc='Usually 32k vertices')
    subcort_gray_labels = InputMultiPath(File(exists=True), mandatory=True, position=7, argstr='--subcortgraylabels="%s"', desc='')
    freesurfer_labels = InputMultiPath(File(exists=True), mandatory=True, position=8, argstr='--freesurferlabels="%s"', desc='')
    ref_myelin_maps = InputMultiPath(File(exists=True), mandatory=True, position=9, argstr='--refmyelinmaps="%s"', desc='')
    reg_name = traits.Enum('FS', 'MSMSulc', 'MSMAll', default='FS', mandatory=False, usedefault=True, position=10, argstr='--regname=%s', desc='MSMSulc is recommended, if binary is not available use FS (FreeSurfer)')
    print_com = traits.Enum('', 'echo', mandatory=False, usedefault=True, position=11, argstr='--printcom=%s', desc='')


class PostFSOutputSpec(HCPCommandOutputSpec):
    grayordinates_res = traits.Int(desc='Usually 2mm.')
    high_res_mesh = traits.Int(desc='Usually 164k vertices')
    low_res_mesh = traits.Int(desc='Usually 32k vertices')


class PostFS(HCPCommand):
    input_spec = PostFSInputSpec
    output_spec = PostFSOutputSpec
    _cmd = 'PostFreeSurferPipeline.sh'

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['subject'] = self.inputs.subject
        outputs['grayordinates_res'] = self.inputs.grayordinates_res
        outputs['high_res_mesh'] = self.inputs.high_res_mesh
        outputs['low_res_mesh'] = self.inputs.low_res_mesh
        return outputs


class VolumeProcessingInputSpec(HCPCommandInputSpec):
    full_command = traits.Str('PostFreeSurferPipeline.sh', mandatory=True, desc='Full path to the relevant HCP script.')
    study_dir = Directory(mandatory=True, exists=True, position=0, argstr='--path="%s"', desc='The study dir. Should contain a subdir named after the subject.')
    subject = traits.Str(mandatory=True, position=1, argstr='--subject="%s"', desc='')
    bold_name = traits.Str(mandatory=True, position=2, argstr='--fmriname="%s"', desc='For some reason, we need a unique name for each BOLD series. Whatever. Provide.')
    bold_img = InputMultiPath(File(exists=True), mandatory=True, position=3, argstr='--fmritcs="%s"', desc='A 4D BOLD image.')
    bold_scout = traits.Either(traits.Enum('NONE'), traits.File(exists=True), mandatory=True, position=4, argstr='--fmriscout="%s"', desc='\n            A single band reference image (SBRef) is recommended if using\n            multiband, set to NONE if you want to use the first volume of the\n            timeseries for motion correction')
    se_fieldmap_neg = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=5, argstr='--SEPhaseNeg="%s"', requires=[
     'se_fieldmap_pos', 'fieldmap_echo_spacing'], desc='')
    se_fieldmap_pos = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=6, argstr='--SEPhasePos="%s"', requires=[
     'se_fieldmap_neg', 'fieldmap_echo_spacing'], desc='')
    fieldmap_mag = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=7, argstr='--fmapmag="%s"', requires=[
     'fieldmap_phase', 'fieldmap_delta_te'], desc='')
    fieldmap_phase = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=8, argstr='--fmapphase="%s"', requires=[
     'fieldmap_mag', 'fieldmap_delta_te'], desc='')
    fieldmap_echo_spacing = traits.Either(traits.Enum('NONE'), traits.Float(), default='NONE', mandatory=False, usedefault=True, position=9, argstr='--echospacing="%s"', requires=[
     'se_fieldmap_neg', 'se_fieldmap_pos'], desc='(seconds) Spacing or Dwelltime of fMRI image.')
    fieldmap_delta_te = traits.Either(traits.Enum('NONE'), traits.Float(), default='NONE', mandatory=False, usedefault=True, position=10, argstr='--echodiff="%s"', requires=[
     'fieldmap_mag', 'fieldmap_phase'], desc='(ms) 2.46ms for 3T, 1.02ms for 7T, set to NONE if using TOPUP')
    unwarp_dir = traits.Enum('x', 'x-', '-x', 'y', 'y-', '-y', 'z', 'z-', '-z', mandatory=False, usedefault=True, position=11, argstr='--unwarpdir="%s"', desc='')
    fmri_res = traits.Int(2, mandatory=False, usedefault=True, position=12, argstr='--fmrires="%d"', desc='Needs to match what is in PostFS. Target final resolution of fMRI data. 2mm is recommended.')
    distortion_correction_method = traits.Enum('TOPUP', 'FIELDMAP', mandatory=False, usedefault=True, position=13, argstr='--dcmethod="%s"', desc='FIELDMAP or TOPUP, distortion correction is required for accurate processing')
    grad_distort_coeffs = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=14, argstr='--gdcoeffs="%s"', desc='Gradient distortion correction coefficents, set to NONE to turn off.')
    top_up_config = traits.Either(traits.Enum('NONE'), traits.File(exists=True), default='NONE', mandatory=False, usedefault=True, position=15, argstr='--topupconfig="%s"', desc='Topup config if using TOPUP, set to NONE if using FIELDMAP as distortion_correction_method.')
    print_com = traits.Enum('', 'echo', mandatory=False, usedefault=True, position=16, argstr='--printcom=%s', desc='')


class VolumeProcessingOutputSpec(HCPCommandOutputSpec):
    bold_name = traits.Str(mandatory=True, desc='A unique name for the BOLD series. We only handle one at a time, so use a mapnode if you have more.')


class VolumeProcessing(HCPCommand):
    input_spec = VolumeProcessingInputSpec
    output_spec = VolumeProcessingOutputSpec
    _cmd = 'GenericfMRIVolumeProcessingPipeline.sh'

    def _format_arg(self, name, spec, value):
        if name in ('fieldmap_echo_spacing', 'fieldmap_delta_te'):
            st = value
            if isinstance(st, float):
                st = '%.7f' % st if name in ('fieldmap_echo_spacing', ) else str(st)
            st = (isinstance(st, str) or str)(st) if 1 else st
            return spec.argstr % st
        return super(VolumeProcessing, self)._format_arg(name, spec, value)

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['subject'] = self.inputs.subject
        outputs['bold_name'] = self.inputs.bold_name
        return outputs


class SurfaceProcessingInputSpec(HCPCommandInputSpec):
    full_command = traits.Str('GenericfMRISurfaceProcessingPipeline.sh', mandatory=True, desc='Full path to the relevant HCP script.')
    study_dir = Directory(mandatory=True, exists=True, position=0, argstr='--path="%s"', desc='The study dir. Should contain a subdir named after the subject.')
    subject = traits.Str(mandatory=True, position=1, argstr='--subject="%s"', desc='')
    bold_name = traits.Str(mandatory=True, position=2, argstr='--fmriname="%s"', desc='For some reason, we need a unique name for each BOLD series. Whatever. Provide.')
    low_res_mesh = traits.Int(32, mandatory=False, usedefault=True, position=3, argstr='--lowresmesh="%d"', desc='Needs to match what is in PostFS. Usually 32k vertices.')
    fmri_res = traits.Int(2, mandatory=False, usedefault=True, position=4, argstr='--fmrires="%d"', desc='Needs to match what is in PostFS. Target final resolution of fMRI data. 2mm is recommended.')
    smoothing_fwhm = traits.Int(2, mandatory=False, usedefault=True, position=5, argstr='--smoothingFWHM="%d"', desc='Recommended to be roughly the voxel size.')
    grayordinates_res = traits.Int(2, mandatory=False, usedefault=True, position=6, argstr='--grayordinatesres="%d"', desc='\n            Needs to match what is in PostFS. Usually 2mm. Could be the same\n            as FinalfRMIResolution or something different, which will call a\n            different module for subcortical processing.')
    reg_name = traits.Enum('FS', 'MSMSulc', 'MSMAll', default='FS', mandatory=False, usedefault=True, position=7, argstr='--regname=%s', desc='MSMSulc is recommended, if binary is not available use FS (FreeSurfer)')


class SurfaceProcessingOutputSpec(HCPCommandOutputSpec):
    study_dir = Directory(desc='The study dir. Should contain a subdir named after the subject.')


class SurfaceProcessing(HCPCommand):
    input_spec = SurfaceProcessingInputSpec
    output_spec = SurfaceProcessingOutputSpec
    _cmd = 'GenericfMRISurfaceProcessingPipeline.sh'

    def _list_outputs(self):
        outputs = self._outputs().get()
        outputs['subject'] = self.inputs.subject
        outputs['study_dir'] = self.inputs.study_dir
        return outputs


class OutputSelectorInputSpec(BaseInterfaceInputSpec):
    study_dir = Directory(desc='The study dir. Should contain a subdir named after the subject.')
    output_mni_only = traits.Bool(True, mandatory=False, usedefault=True, desc="\n            To save space, by default we only output the pipeline's final\n            product. If you need to look at the precursor files, then just set\n            this to false... and prepare your drives to go to that big server\n            farm in the sky.\n            ")


class OutputSelectorOutputSpec(TraitedSpec):
    output_dir = Directory(desc='Either the full study dir, or just the MNINonLinear dir (default).')


class OutputSelector(BaseInterface):
    input_spec = OutputSelectorInputSpec
    output_spec = OutputSelectorOutputSpec

    def __init__(self, *args, **kwargs):
        super(OutputSelector, self).__init__(*args, **kwargs)
        self.out_dir = None
        return

    def _run_interface(self, runtime):
        from glob import glob
        od = self.inputs.study_dir
        if not self.inputs.output_mni_only:
            self.out_dir = od
        else:
            glob_str = os.path.join(od, '*', 'MNINonLinear')
            mni_dirs = glob(glob_str)
            if not mni_dirs:
                raise ValueError('Could not find MNINonLinear output dir in %s' % glob_str)
            self.out_dir = mni_dirs[0]
        return runtime

    def _list_outputs(self):
        from glob import glob
        outputs = self._outputs().get()
        outputs['output_dir'] = self.out_dir
        return outputs