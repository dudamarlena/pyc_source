# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/file/formats/default.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 6599 bytes
import os, numpy as np
from pesummary.gw.file.formats.base_read import GWRead
from pesummary.core.file.formats.default import Default as CoreDefault

class Default(GWRead):
    __doc__ = 'Class to handle the default loading options.\n\n    Parameters\n    ----------\n    path_to_results_file: str\n        path to the results file you wish to load\n\n    Attributes\n    ----------\n    parameters: list\n        list of parameters stored in the result file\n    samples: 2d list\n        list of samples stored in the result file\n    samples_dict: dict\n        dictionary of samples stored in the result file keyed by parameters\n    input_version: str\n        version of the result file passed.\n    extra_kwargs: dict\n        dictionary of kwargs that were extracted from the result file\n\n    Methods\n    -------\n    to_dat:\n        save the posterior samples to a .dat file\n    to_latex_table:\n        convert the posterior samples to a latex table\n    generate_latex_macros:\n        generate a set of latex macros for the stored posterior samples\n    to_lalinference:\n        convert the posterior samples to a lalinference result file\n    generate_all_posterior_samples:\n        generate all posterior distributions that may be derived from\n        sampled distributions\n    '

    def __init__(self, path_to_results_file):
        super(Default, self).__init__(path_to_results_file)
        func_map = {'json':self._grab_data_from_json_file, 
         'dat':self._grab_data_from_dat_file, 
         'txt':self._grab_data_from_dat_file, 
         'hdf5':self._grab_data_from_hdf5_file, 
         'h5':self._grab_data_from_hdf5_file, 
         'hdf':self._grab_data_from_hdf5_file}
        self.load_function = func_map[self.extension]
        try:
            self.load(self.load_function)
        except Exception as e:
            raise Exception('Failed to read data for file %s because: %s' % (
             self.path_to_results_file, e))

    @classmethod
    def load_file(cls, path):
        if not os.path.isfile(path):
            raise FileNotFoundError('%s does not exist' % path)
        return cls(path)

    @staticmethod
    def grab_extra_kwargs(parameters, samples):
        """Grab any additional information stored in the file
        """

        def find_parameter_given_alternatives(parameters, options):
            if any(i in options for i in parameters):
                parameter = [i for i in parameters if i in options]
                ind = parameters.index(parameter[0])
                return ind

        kwargs = {'sampler':{},  'meta_data':{}}
        possible_f_ref = ['f_ref', 'fRef', 'fref', 'fref_template']
        ind = find_parameter_given_alternatives(parameters, possible_f_ref)
        if ind is not None:
            kwargs['meta_data']['f_ref'] = samples[0][ind]
        possible_f_low = [
         'flow', 'f_low', 'fLow', 'flow_template']
        ind = find_parameter_given_alternatives(parameters, possible_f_low)
        if ind is not None:
            kwargs['meta_data']['f_low'] = samples[0][ind]
        return kwargs

    @staticmethod
    def _grab_data_from_dat_file(path):
        """Grab the data stored in a .dat file
        """
        data = CoreDefault._grab_data_from_dat_file(path)
        parameters, samples = data['parameters'], data['samples']
        parameters = GWRead._check_definition_of_inclination(parameters)
        condition1 = 'luminosity_distance' not in parameters
        condition2 = 'logdistance' in parameters
        if condition1:
            if condition2:
                parameters.append('luminosity_distance')
                for num, i in enumerate(samples):
                    samples[num].append(np.exp(i[parameters.index('logdistance')]))

        injection = {i:float('nan') for i in parameters}
        try:
            extra_kwargs = Default.grab_extra_kwargs(parameters, samples)
        except Exception:
            extra_kwargs = {'sampler':{},  'meta_data':{}}

        extra_kwargs['sampler']['nsamples'] = len(samples)
        return {'parameters':parameters, 
         'samples':samples,  'injection':injection, 
         'kwargs':extra_kwargs}

    @staticmethod
    def _grab_data_from_json_file(path):
        """Grab the data stored in a .json file
        """
        return CoreDefault._grab_data_from_json_file(path)

    @staticmethod
    def _grab_data_from_hdf5_file(path):
        """Grab the data stored in an hdf5 file
        """
        return CoreDefault._grab_data_from_hdf5_file(path, cls=Default)

    @staticmethod
    def _grab_data_with_deepdish(path):
        """Grab the data stored in a h5py file with `deepdish`.
        """
        return CoreDefault._grab_data_with_deepdish(path,
          remove_params=['waveform_approximant'])

    @staticmethod
    def _grab_data_with_h5py(path):
        """Grab the data stored in a hdf5 file with `h5py`.
        """
        return CoreDefault._grab_data_with_h5py(path,
          remove_params=['waveform_approximant'])

    @property
    def calibration_data_in_results_file(self):
        """
        """
        pass

    def add_injection_parameters_from_file(self, injection_file):
        """
        """
        self.injection_parameters = self._add_injection_parameters_from_file(injection_file, self._grab_injection_parameters_from_file)

    def add_marginalized_parameters_from_config_file(self, config_file):
        """Search the configuration file and add the marginalized parameters
        to the list of parameters and samples

        Parameters
        ----------
        config_file: str
            path to the configuration file
        """
        pass