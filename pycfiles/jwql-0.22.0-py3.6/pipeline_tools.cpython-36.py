# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/instrument_monitors/pipeline_tools.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 8842 bytes
"""Various utility functions related to the JWST calibration pipeline

Authors
-------

    - Bryan Hilbert

Use
---

    This module can be imported as such:
    ::

        from jwql.instrument_monitors import pipeline_tools
        pipeline_steps = pipeline_tools.completed_pipeline_steps(filename)
 """
from collections import OrderedDict
import copy, numpy as np
from astropy.io import fits
from jwst.dq_init import DQInitStep
from jwst.dark_current import DarkCurrentStep
from jwst.firstframe import FirstFrameStep
from jwst.group_scale import GroupScaleStep
from jwst.ipc import IPCStep
from jwst.jump import JumpStep
from jwst.lastframe import LastFrameStep
from jwst.linearity import LinearityStep
from jwst.persistence import PersistenceStep
from jwst.ramp_fitting import RampFitStep
from jwst.refpix import RefPixStep
from jwst.rscd import RSCD_Step
from jwst.saturation import SaturationStep
from jwst.superbias import SuperBiasStep
from jwql.utils.constants import JWST_INSTRUMENT_NAMES_UPPERCASE
PIPE_KEYWORDS = {'S_GRPSCL':'group_scale', 
 'S_DQINIT':'dq_init',  'S_SATURA':'saturation',  'S_IPC':'ipc', 
 'S_REFPIX':'refpix',  'S_SUPERB':'superbias',  'S_PERSIS':'persistence', 
 'S_DARK':'dark_current',  'S_LINEAR':'linearity',  'S_FRSTFR':'firstframe', 
 'S_LASTFR':'lastframe',  'S_RSCD':'rscd',  'S_JUMP':'jump', 
 'S_RAMP':'rate'}
PIPELINE_STEP_MAPPING = {'dq_init':DQInitStep, 
 'dark_current':DarkCurrentStep,  'firstframe':FirstFrameStep, 
 'group_scale':GroupScaleStep,  'ipc':IPCStep, 
 'jump':JumpStep,  'lastframe':LastFrameStep,  'linearity':LinearityStep, 
 'persistence':PersistenceStep,  'rate':RampFitStep, 
 'refpix':RefPixStep,  'rscd':RSCD_Step,  'saturation':SaturationStep, 
 'superbias':SuperBiasStep}
GROUPSCALE_READOUT_PATTERNS = [
 'NRSIRS2']

def completed_pipeline_steps(filename):
    """Return a list of the completed pipeline steps for a given file.

    Parameters
    ----------
    filename : str
        File to examine

    Returns
    -------
    completed : collections.OrderedDict
        Dictionary with boolean entry for each pipeline step,
        indicating which pipeline steps have been run on filename
    """
    completed = OrderedDict({})
    for key in PIPE_KEYWORDS.values():
        completed[key] = False

    header = fits.getheader(filename)
    for key in PIPE_KEYWORDS.keys():
        try:
            value = header.get(key)
        except KeyError:
            value == 'NOT DONE'

        if value == 'COMPLETE':
            completed[PIPE_KEYWORDS[key]] = True

    return completed


def get_pipeline_steps(instrument):
    """Get the names and order of the ``calwebb_detector1`` pipeline
    steps for a given instrument. Use values that match up with the
    values in the ``PIPE_STEP`` defintion in ``definitions.py``

    Parameters
    ----------
    instrument : str
        Name of JWST instrument

    Returns
    -------
    steps : collections.OrderedDict
        Dictionary of step names
    """
    instrument = instrument.upper()
    if instrument not in JWST_INSTRUMENT_NAMES_UPPERCASE.values():
        raise ValueError('WARNING: {} is not a valid instrument name.'.format(instrument))
    else:
        if instrument == 'MIRI':
            steps = [
             'group_scale', 'dq_init', 'saturation', 'ipc', 'firstframe', 'lastframe',
             'linearity', 'rscd', 'dark_current', 'refpix', 'persistence', 'jump', 'rate']
            steps.remove('persistence')
            steps.remove('group_scale')
        else:
            steps = [
             'group_scale', 'dq_init', 'saturation', 'ipc', 'superbias', 'refpix', 'linearity',
             'persistence', 'dark_current', 'jump', 'rate']
            if instrument == 'NIRSPEC':
                steps.remove('persistence')
            else:
                steps.remove('group_scale')
    steps.remove('ipc')
    required_steps = OrderedDict({})
    for key in steps:
        required_steps[key] = True

    for key in PIPE_KEYWORDS.values():
        if key not in required_steps.keys():
            required_steps[key] = False

    return required_steps


def image_stack(file_list):
    """Given a list of fits files containing 2D images, read in all data
    and place into a 3D stack

    Parameters
    ----------
    file_list : list
        List of fits file names

    Returns
    -------
    cube : numpy.ndarray
        3D stack of the 2D images
    """
    exptimes = []
    for i, input_file in enumerate(file_list):
        with fits.open(input_file) as (hdu):
            image = hdu[1].data
            exptime = hdu[0].header['EFFINTTM']
            num_ints = hdu[0].header['NINTS']
        if i == 0:
            ndim_base = image.shape
            if len(ndim_base) == 3:
                cube = copy.deepcopy(image)
            elif len(ndim_base) == 2:
                cube = np.expand_dims(image, 0)
        else:
            ndim = image.shape
            if ndim_base[-2:] == ndim[-2:]:
                if len(ndim) == 2:
                    image = np.expand_dims(image, 0)
                else:
                    if len(ndim) > 3:
                        raise ValueError('4-dimensional input slope images not supported.')
                cube = np.vstack((cube, image))
            else:
                raise ValueError('Input images are of inconsistent size in x/y dimension.')
        exptimes.append([exptime] * num_ints)

    return (cube, exptimes)


def run_calwebb_detector1_steps(input_file, steps):
    """Run the steps of ``calwebb_detector1`` specified in the steps
    dictionary on the input file

    Parameters
    ----------
    input_file : str
        File on which to run the pipeline steps

    steps : collections.OrderedDict
        Keys are the individual pipeline steps (as seen in the
        ``PIPE_KEYWORDS`` values above). Boolean values indicate whether
        a step should be run or not. Steps are run in the official
        ``calwebb_detector1`` order.
    """
    first_step_to_be_run = True
    for step_name in steps:
        if steps[step_name]:
            if first_step_to_be_run:
                model = PIPELINE_STEP_MAPPING[step_name].call(input_file)
                first_step_to_be_run = False
            else:
                model = PIPELINE_STEP_MAPPING[step_name].call(model)
            suffix = step_name

    output_filename = input_file.replace('.fits', '_{}.fits'.format(suffix))
    if suffix != 'rate':
        model.save(output_filename)
    else:
        model[0].save(output_filename)
    return output_filename


def steps_to_run(all_steps, finished_steps):
    """Given a list of pipeline steps that need to be completed as well
    as a list of steps that have already been completed, return a list
    of steps remaining to be done.

    Parameters
    ----------
    all_steps : collections.OrderedDict
        A dictionary of all steps that need to be completed

    finished_steps : collections.OrderedDict
        A dictionary with keys equal to the pipeline steps and boolean
        values indicating whether a particular step has been completed
        or not (i.e. output from ``completed_pipeline_steps``)

    Returns
    -------
    steps_to_run : collections.OrderedDict
        A dictionaru with keys equal to the pipeline steps and boolean
        values indicating whether a particular step has yet to be run.
    """
    torun = copy.deepcopy(finished_steps)
    for key in all_steps:
        if all_steps[key] == finished_steps[key]:
            torun[key] = False
        else:
            if (all_steps[key] is True) & (finished_steps[key] is False):
                torun[key] = True
            else:
                if (all_steps[key] is False) & (finished_steps[key] is True):
                    print('WARNING: {} step has been run but the requirements say that it should not be. Need a new input file.'.format(key))

    return torun