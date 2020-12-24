# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/file/formats/GWTC1.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 3805 bytes
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

class GWTC1(GWRead):
    __doc__ = 'PESummary wrapper of the GWTC1 sample release\n\n    Attributes\n    ----------\n    path_to_results_file: str\n        path to the results file you wish to load in with `GWTC1`\n    '

    def __init__(self, path_to_results_file, injection_file=None):
        super(GWTC1, self).__init__(path_to_results_file)
        self.load(self._grab_data_from_GWTC1_file)

    @classmethod
    def load_file(cls, path, injection_file=None):
        if not os.path.isfile(path):
            raise IOError('%s does not exist' % path)
        if injection_file:
            if not os.path.isfile(injection_file):
                raise IOError('%s does not exist' % path)
        return cls(path, injection_file=injection_file)

    @staticmethod
    def grab_extra_kwargs(path):
        """
        """
        return {'sampler':{},  'meta_data':{}}

    @staticmethod
    def grab_priors(obj):
        """
        """
        from pesummary.utils.samples_dict import SamplesDict
        keys = list(obj.keys())
        if 'prior' in keys or 'priors' in keys:
            data = obj['prior'] if 'prior' in keys else obj['priors']
            parameters = list(data.dtype.names)
            samples = [list(i) for i in data]
            return SamplesDict(parameters, np.array(samples).T)
        else:
            logger.warn("Failed to draw prior samples because there is not an entry for 'prior' or 'priors' in the result file")
            return {}

    @staticmethod
    def _grab_data_from_GWTC1_file(path):
        """
        """
        f = h5py.File(path, 'r')
        keys = list(f.keys())
        if 'Overall_posterior' in keys or 'overall_posterior' in keys:
            data = f['overall_posterior'] if 'overall_posterior' in keys else f['Overall_posterior']
        else:
            f.close()
            raise Exception("Failed to read in result file because there was no group called 'Overall_posterior' or 'overall_posterior'")
        parameters = list(data.dtype.names)
        samples = [list(i) for i in data]
        extra_kwargs = GWTC1.grab_extra_kwargs(path)
        extra_kwargs['sampler']['nsamples'] = len(samples)
        prior_samples = GWTC1.grab_priors(f)
        version = None
        f.close()
        return {'parameters':parameters, 
         'samples':samples, 
         'injection':None, 
         'version':version, 
         'kwargs':extra_kwargs, 
         'prior':prior_samples}

    @property
    def calibration_data_in_results_file(self):
        """
        """
        pass