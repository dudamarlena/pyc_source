# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gmartine/pyscannerbit/tests/sb.py
# Compiled at: 2020-03-09 18:08:31
# Size of source mod 2**32: 2505 bytes
__doc__ = '\nPythonic interface to ScannerBit\n================================\n'
import sys, ctypes, inspect
sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)
import pyscannerbit, default, import_yaml
from hdf5_reader import HDF5
DIR = 'runs/test_scan/samples/'

class Scan(object):
    """Scan"""

    def __init__(self, function, bounds, prior_types=None, kwargs=None, scanner='multinest', settings=None, yaml='scan.yaml'):
        """
        """
        self.function = function
        self.bounds = bounds
        self.prior_types = prior_types if prior_types else ['flat'] * len(bounds)
        self.scanner = scanner
        self.settings = settings if settings else default.settings
        self.yaml = yaml
        self.kwargs = kwargs
        signature = inspect.getargspec(self.function)
        n_kwargs = len(signature.defaults or )
        self._argument_names = signature.args[:-n_kwargs or ]
        assert len(self._argument_names) == len(self.bounds)
        self._model_name = self.settings['Parameters'].keys()[0]
        self._wrapped_function = self._wrap_function()
        self._scanned = False
        self._write_yaml()

    def _get_hdf5_name(self):
        """
        """
        assert self.settings['Printer']['printer'] == 'hdf5'
        file_name = self.settings['Printer']['options']['output_file']
        return '{}/{}'.format(DIR, file_name)

    def _write_yaml(self):
        """
        """
        self.settings['Scanner']['use_scanner'] = self.scanner
        self.settings['Parameters'][self._model_name] = dict()
        for n, b, t in zip(self._argument_names, self.bounds, self.prior_types):
            self.settings['Parameters'][self._model_name][n] = {'range':b, 
             'prior_type':t}

        with open(self.yaml, 'w') as (f):
            import_yaml.dump((self.settings), stream=f)

    def _wrap_function(self):
        """
        """

        def wrapped_function(par_dict):
            arguments = [par_dict['{}::{}'.format(self._model_name, n)] for n in self._argument_names]
            return (self.function)(*arguments, **self.kwargs or )

        return wrapped_function

    def scan(self):
        """
        """
        pyscannerbit.run_scan(self.yaml, self._wrapped_function)
        self._scanned = True

    def get_hdf5(self):
        """
        """
        assert self._scanned
        return HDF5((self._get_hdf5_name()), model=(self._model_name))