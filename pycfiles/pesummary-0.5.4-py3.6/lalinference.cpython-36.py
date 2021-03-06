# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/file/formats/lalinference.py
# Compiled at: 2020-05-08 05:31:08
# Size of source mod 2**32: 20015 bytes
import os, h5py, numpy as np
try:
    from glue.ligolw import ligolw
    from glue.ligolw import lsctables
    from glue.ligolw import utils as ligolw_utils
    GLUE = True
except ImportError:
    GLUE = False

from pesummary.gw.file.formats.base_read import GWRead
from pesummary.gw.file import conversions as con
from pesummary.utils.utils import logger
from pesummary.utils.decorators import open_config
from pesummary import conf
SAMPLER_KWARGS = {'log_bayes_factor':conf.log_bayes_factor, 
 'bayes_factor':conf.bayes_factor, 
 'log_evidence':conf.log_evidence, 
 'evidence':conf.evidence, 
 'log_prior_volume':conf.log_prior_volume, 
 'sampleRate':'sample_rate', 
 'segmentLength':'segment_length'}
META_DATA = {'flow':'f_low', 
 'f_low':'f_low', 
 'fref':'f_ref', 
 'f_ref':'f_ref', 
 'LAL_PNORDER':'pn_order', 
 'LAL_APPROXIMANT':'approximant', 
 'number_of_live_points':'number_of_live_points', 
 'segmentLength':'segment_length', 
 'segmentStart':'segment_start', 
 'sampleRate':'sample_rate'}

class LALInference(GWRead):
    __doc__ = 'PESummary wrapper of `lalinference`\n    (https://git.ligo.org/lscsoft/lalsuite/lalinference).\n\n    Parameters\n    ----------\n    path_to_results_file: str\n        path to the results file you wish to load in with `LALInference`\n\n    Attributes\n    ----------\n    parameters: list\n        list of parameters stored in the result file\n    samples: 2d list\n        list of samples stored in the result file\n    samples_dict: dict\n        dictionary of samples stored in the result file keyed by parameters\n    input_version: str\n        version of the result file passed.\n    extra_kwargs: dict\n        dictionary of kwargs that were extracted from the result file\n\n    Methods\n    -------\n    to_dat:\n        save the posterior samples to a .dat file\n    to_latex_table:\n        convert the posterior samples to a latex table\n    generate_latex_macros:\n        generate a set of latex macros for the stored posterior samples\n    to_lalinference:\n        convert the posterior samples to a lalinference result file\n    generate_all_posterior_samples:\n        generate all posterior distributions that may be derived from\n        sampled distributions\n    '

    def __init__(self, path_to_results_file, injection_file=None):
        super(LALInference, self).__init__(path_to_results_file)
        self.load(self._grab_data_from_lalinference_file)

    @classmethod
    def load_file(cls, path, injection_file=None):
        if not os.path.isfile(path):
            raise IOError('%s does not exist' % path)
        if injection_file:
            if not os.path.isfile(injection_file):
                raise IOError('%s does not exist' % path)
        return cls(path, injection_file=injection_file)

    @staticmethod
    def guess_path_to_sampler(path):
        """Guess the path to the sampler group in a LALInference results file

        Parameters
        ----------
        path: str
            path to the LALInference results file
        """

        def _find_name(name):
            c1 = 'lalinference_nest' in name or 'lalinference_mcmc' in name
            c2 = 'lalinference_nest/' not in name and 'lalinference_mcmc/' not in name
            if c1:
                if c2:
                    return name

        f = h5py.File(path, 'r')
        _path = f.visit(_find_name)
        f.close()
        return _path

    @staticmethod
    def _parameters_in_lalinference_file(path):
        """Return the parameter names stored in the LALInference results file

        Parameters
        ----------
        """
        f = h5py.File(path, 'r')
        path_to_samples = GWRead.guess_path_to_samples(path)
        parameters = list(f[path_to_samples].dtype.names)
        f.close()
        return parameters

    @staticmethod
    def _samples_in_lalinference_file(path):
        """
        """
        f = h5py.File(path, 'r')
        path_to_samples = GWRead.guess_path_to_samples(path)
        samples = [list(i) for i in f[path_to_samples]]
        return samples

    @staticmethod
    def _check_for_calibration_data_in_lalinference_file(path):
        """
        """
        f = h5py.File(path, 'r')
        path_to_samples = GWRead.guess_path_to_samples(path)
        lalinference_names = list(f[path_to_samples].dtype.names)
        if any('_spcal_amp' in i for i in lalinference_names):
            return True
        else:
            return False

    @property
    def calibration_data_in_results_file(self):
        """
        """
        check = LALInference._check_for_calibration_data_in_lalinference_file
        grab = LALInference._grab_calibration_data_from_lalinference_file
        if self.check_for_calibration_data(check, self.path_to_results_file):
            return self.grab_calibration_data(grab, self.path_to_results_file)

    @staticmethod
    def grab_extra_kwargs(path):
        """Grab any additional information stored in the lalinference file
        """
        kwargs = {'sampler':{},  'meta_data':{},  'other':{}}
        path_to_samples = GWRead.guess_path_to_samples(path)
        path_to_sampler = LALInference.guess_path_to_sampler(path)
        f = h5py.File(path, 'r')
        attributes = dict(f[path_to_sampler].attrs.items())
        for kwarg, item in attributes.items():
            if kwarg in list(SAMPLER_KWARGS.keys()) and kwarg == 'evidence':
                kwargs['sampler'][conf.log_evidence] = np.round(np.log(item), 2)
            elif kwarg in list(SAMPLER_KWARGS.keys()) and kwarg == 'bayes_factor':
                kwargs['sampler'][conf.log_bayes_factor] = np.round(np.log(item), 2)
            else:
                if kwarg in list(SAMPLER_KWARGS.keys()):
                    kwargs['sampler'][SAMPLER_KWARGS[kwarg]] = np.round(item, 2)
                else:
                    kwargs['other'][kwarg] = item

        attributes = dict(f[path_to_samples].attrs.items())
        for kwarg, item in attributes.items():
            if kwarg in list(META_DATA.keys()):
                if kwarg == 'LAL_APPROXIMANT':
                    try:
                        from lalsimulation import GetStringFromApproximant
                        kwargs['meta_data']['approximant'] = GetStringFromApproximant(int(attributes['LAL_APPROXIMANT']))
                    except Exception:
                        kwargs['meta_data']['approximant'] = int(attributes['LAL_APPROXIMANT'])

            else:
                if kwarg in list(META_DATA.keys()):
                    kwargs['meta_data'][META_DATA[kwarg]] = item
                else:
                    kwargs['other'][kwarg] = item

        f.close()
        return kwargs

    @staticmethod
    def _grab_calibration_data_from_lalinference_file(path):
        """
        """
        f = h5py.File(path, 'r')
        path_to_samples = GWRead.guess_path_to_samples(path)
        attributes = f[path_to_samples].attrs.items()
        lalinference_names = list(f[path_to_samples].dtype.names)
        samples = [list(i) for i in f[path_to_samples]]
        keys_amp = np.sort([param for param in lalinference_names if '_spcal_amp' in param])
        keys_phase = np.sort([param for param in lalinference_names if '_spcal_phase' in param])
        log_frequencies = {key.split('_')[0]:[] for key, value in attributes if '_spcal_logfreq' in key or '_spcal_freq' in key if '_spcal_logfreq' in key or '_spcal_freq' in key}
        attribute_keys = [key for key, value in attributes]
        for key, value in attributes:
            if '_spcal_logfreq' in key:
                if key.replace('logfreq', 'freq') not in attribute_keys:
                    log_frequencies[key.split('_')[0]].append(float(value))
                else:
                    if '_spcal_freq' in key:
                        log_frequencies[key.split('_')[0]].append(np.log(float(value)))

        amp_params = {ifo:[] for ifo in log_frequencies.keys()}
        phase_params = {ifo:[] for ifo in log_frequencies.keys()}
        for key in keys_amp:
            ifo = key.split('_')[0]
            ind = lalinference_names.index(key)
            amp_params[ifo].append([float(i[ind]) for i in samples])

        for key in keys_phase:
            ifo = key.split('_')[0]
            ind = lalinference_names.index(key)
            phase_params[ifo].append([float(i[ind]) for i in samples])

        f.close()
        return (log_frequencies, amp_params, phase_params)

    @staticmethod
    def _grab_data_from_lalinference_file(path):
        """
        """
        f = h5py.File(path, 'r')
        path_to_samples = GWRead.guess_path_to_samples(path)
        lalinference_names = list(f[path_to_samples].dtype.names)
        samples = [list(i) for i in f[path_to_samples]]
        if 'logdistance' in lalinference_names:
            lalinference_names.append('luminosity_distance')
            for num, i in enumerate(samples):
                samples[num].append(np.exp(i[lalinference_names.index('logdistance')]))

        if 'costheta_jn' in lalinference_names:
            lalinference_names.append('theta_jn')
            for num, i in enumerate(samples):
                samples[num].append(np.arccos(i[lalinference_names.index('costheta_jn')]))

        extra_kwargs = LALInference.grab_extra_kwargs(path)
        extra_kwargs['sampler']['nsamples'] = len(samples)
        try:
            version = f[path_to_samples].attrs['VERSION'].decode('utf-8')
        except Exception as e:
            version = None

        return {'parameters':lalinference_names,  'samples':samples, 
         'injection':None, 
         'version':version, 
         'kwargs':extra_kwargs}

    def add_injection_parameters_from_file(self, injection_file):
        """
        """
        self.injection_parameters = self._add_injection_parameters_from_file(injection_file, self._grab_injection_parameters_from_file)

    def add_fixed_parameters_from_config_file(self, config_file):
        """Search the conifiguration file and add fixed parameters to the
        list of parameters and samples

        Parameters
        ----------
        config_file: str
            path to the configuration file
        """
        self._add_fixed_parameters_from_config_file(config_file, self._add_fixed_parameters)

    def add_marginalized_parameters_from_config_file(self, config_file):
        """Search the configuration file and add the marginalized parameters
        to the list of parameters and samples

        Parameters
        ----------
        config_file: str
            path to the configuration file
        """
        self._add_marginalized_parameters_from_config_file(config_file, self._add_marginalized_parameters)

    @staticmethod
    @open_config(index=2)
    def _add_fixed_parameters(parameters, samples, config_file):
        """Open a LALInference configuration file and add the fixed parameters
        to the list of parameters and samples

        Parameters
        ----------
        parameters: list
            list of existing parameters
        samples: list
            list of existing samples
        config_file: str
            path to the configuration file
        """
        from pesummary.gw.file.standard_names import standard_names
        config = config_file
        if not config.error:
            fixed_data = None
            if 'engine' in config.sections():
                fixed_data = {key.split('fix-')[1]:item for key, item in config.items('engine') if 'fix' in key if 'fix' in key}
            if fixed_data is not None:
                for i in fixed_data.keys():
                    fixed_parameter = i
                    fixed_value = fixed_data[i]
                    try:
                        param = standard_names[fixed_parameter]
                        if param in parameters:
                            pass
                        else:
                            parameters.append(param)
                            for num in range(len(samples)):
                                samples[num].append(float(fixed_value))

                    except Exception:
                        if fixed_parameter == 'logdistance':
                            if 'luminosity_distance' not in parameters:
                                parameters.append(standard_names['distance'])
                                for num in range(len(samples)):
                                    samples[num].append(float(fixed_value))

                        if fixed_parameter == 'costheta_jn':
                            if 'theta_jn' not in parameters:
                                parameters.append(standard_names['theta_jn'])
                                for num in range(len(samples)):
                                    samples[num].append(float(fixed_value))

        return (
         parameters, samples)

    @staticmethod
    @open_config(index=2)
    def _add_marginalized_parameters(parameters, samples, config_file):
        """Open a LALInference configuration file and add the marginalized
        parameters to the list of parameters and samples

        Parameters
        ----------
        parameters: list
            list of existing parameters
        samples: list
            list of existing samples
        config_file: str
            path to the configuration file
        """
        from pesummary.gw.file.standard_names import standard_names
        config = config_file
        if not config.error:
            fixed_data = None
            if 'engine' in config.sections():
                marg_par = {key.split('marg')[1]:item for key, item in config.items('engine') if 'marg' in key if 'marg' in key}
            for i in marg_par.keys():
                if 'time' in i and 'geocent_time' not in parameters:
                    if 'marginalized_geocent_time' in parameters:
                        ind = parameters.index('marginalized_geocent_time')
                        parameters.remove(parameters[ind])
                        parameters.append('geocent_time')
                        for num, j in enumerate(samples):
                            samples[num].append(float(j[ind]))
                            del j[ind]

                    else:
                        logger.warn('You have marginalized over time and there are no time samples. Manually setting time to 100000s')
                        parameters.append('geocent_time')
                        for num, j in enumerate(samples):
                            samples[num].append(float(100000))

                    if 'phi' in i:
                        if 'phase' not in parameters:
                            if 'marginalized_phase' in parameters:
                                ind = parameters.index('marginalized_phase')
                                parameters.remove(parameters[ind])
                                parameters.append('phase')
                                for num, j in enumerate(samples):
                                    samples[num].append(float(j[ind]))
                                    del j[ind]

                            else:
                                logger.warn('You have marginalized over phase and there are no phase samples. Manually setting the phase to be 0')
                                parameters.append('phase')
                                for num, j in enumerate(samples):
                                    samples[num].append(float(0))

                    if 'dist' in i and 'luminosity_distance' not in parameters:
                        if 'marginalized_distance' in parameters:
                            ind = parameters.index('marginalized_distance')
                            parameters.remove(parameters[ind])
                            parameters.append('luminosity_distance')
                            for num, j in enumerate(samples):
                                samples[num].append(float(j[ind]))
                                del j[ind]

                        else:
                            logger.warn('You have marginalized over distance and there are no distance samples. Manually setting distance to 100Mpc')
                            parameters.append('luminosity_distance')
                            for num, j in enumerate(samples):
                                samples[num].append(float(100.0))

            return (
             parameters, samples)
        else:
            return (
             parameters, samples)


def write_to_file(samples, outdir='./', label=None, filename=None, overwrite=False, sampler='lalinference_nest', dat=False):
    """Write a set of samples in LALInference file format

    Parameters
    ----------
    samples: pesummary.utils.utils.SamplesDict
        Dictionary containing the posterior samples
    outdir: str
        The directory where you would like to write the lalinference file
    label: str
        The label of the analysis. This is used in the filename if a filename
        if not specified
    filename: str
        The name of the file that you wish to write
    overwrite: Bool
        If True, an existing file of the same name will be overwritten
    sampler: str
        The sampler which you wish to store in the result file. This may either
        be 'lalinference_nest' or 'lalinference_mcmc'
    dat: Bool
        If True, a LALInference dat file is produced
    """
    from pesummary.gw.file.standard_names import lalinference_map
    import copy
    _samples = copy.deepcopy(samples)
    if not filename:
        if not label:
            from time import time
            label = round(time())
    if not filename:
        extension = 'dat' if dat else 'hdf5'
        filename = 'lalinference_{}.{}'.format(label, extension)
    else:
        if os.path.isfile(os.path.join(outdir, filename)):
            if not overwrite:
                raise FileExistsError("The file '{}' already exists in the directory {}".format(filename, outdir))
        reverse_map = {item:key for key, item in lalinference_map.items()}
        no_key = []
        for param in _samples.keys():
            if param in reverse_map.keys():
                _samples[reverse_map[param]] = _samples.pop(param)
            else:
                if param not in lalinference_map.keys():
                    no_key.append(param)

        if len(no_key):
            logger.info('Unable to find a LALInference name for the parameters: {}. Keeping the PESummary name.'.format(', '.join(no_key)))
        lalinference_samples = _samples.to_structured_array()
        if dat:
            np.savetxt((os.path.join(outdir, filename)),
              lalinference_samples, delimiter='\t',
              comments='',
              header=('\t'.join(lalinference_samples.dtype.names)))
        else:
            with h5py.File(os.path.join(outdir, filename), 'w') as (f):
                lalinference = f.create_group('lalinference')
                sampler = lalinference.create_group(sampler)
                samples = sampler.create_dataset('posterior_samples',
                  data=lalinference_samples)