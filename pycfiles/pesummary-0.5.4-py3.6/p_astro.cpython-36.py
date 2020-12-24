# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/gw/p_astro.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 4883 bytes
try:
    from ligo.computeDiskMass import computeDiskMass
    PASTRO = True
except ImportError:
    PASTRO = False

import numpy as np
from pesummary.utils.utils import logger

def get_probabilities(samples):
    """Return `HasNS` and `HasRemnant` probabilities from a dictionary of
    samples

    Parameters
    ----------
    samples: dict
        dictionary of samples
    """
    from pesummary.utils.utils import RedirectLogger
    default_error = 'Failed to generate `HasNS` and `HasRemnant` probabilities because {}'
    try:
        with RedirectLogger('p_astro', level='DEBUG') as (redirector):
            data = PAstro.classifications(samples)
    except ImportError:
        logger.warn(default_error.format("'p_astro' is not installed"))
        data = None
    except Exception as e:
        logger.warn(default_error.format('%s' % e))
        data = None

    return data


class PAstro(object):
    __doc__ = 'Class to handle the p_astro package\n    '

    @staticmethod
    def check_for_install():
        """Check that p_astro is installed
        """
        if not PASTRO:
            raise ImportError("Failed to import 'p_astro' packages and therefore unable to calculate `HasNS` and `HasRemnant` probabilities")

    @staticmethod
    def _classifications(samples):
        """
        """
        required_params = [
         'mass_1_source', 'mass_2_source', 'a_1', 'a_2']
        parameters = list(samples.keys())
        if not all(i in parameters for i in required_params):
            raise Exception('Failed to generate `HasNS` and `HasRemnant` probabilities because not all required parameters have been provided.')
        M_rem = computeDiskMass(samples['mass_1_source'], samples['mass_2_source'], samples['a_1'], samples['a_2'])
        prediction_ns = float(np.sum(samples['mass_2_source'] <= 3.0) / len(samples['mass_2_source']))
        prediction_em = float(np.sum(M_rem > 0) / len(M_rem))
        return {'HasNS':np.round(prediction_ns, 5), 
         'HasRemnant':np.round(prediction_em, 5)}

    @staticmethod
    def default_classification(samples):
        """
        """
        return PAstro._classifications(samples)

    @staticmethod
    def population_classification(samples):
        """
        """
        import pandas as pd, copy
        from pepredicates import rewt_approx_massdist_redshift
        p_astro_samples = copy.deepcopy(samples)
        mapping = {'mass_1_source':'m1_source',  'mass_2_source':'m2_source', 
         'luminosity_distance':'dist', 
         'redshift':'redshift', 
         'a_1':'a1', 
         'a_2':'a2'}
        reverse_mapping = dict((value, key) for key, value in mapping.items())
        keys = list(p_astro_samples.keys())
        for key in keys:
            if key in list(mapping.keys()):
                p_astro_samples[mapping[key]] = p_astro_samples[key]

        p_astro_samples = rewt_approx_massdist_redshift(pd.DataFrame.from_dict(p_astro_samples))
        for key, item in p_astro_samples.items():
            if key in list(reverse_mapping.keys()):
                p_astro_samples[reverse_mapping[key]] = item

        try:
            return PAstro._classifications(p_astro_samples)
        except KeyError:
            logger.warn("Failed to generate 'em_bright' probabilities after reweighting to a population prior because there were no samples after reweighting")
            return {'HasNS':'-', 
             'HasRemnant':'-'}

    @staticmethod
    def classifications(samples):
        """Return the source classification probabilities using both the default
        prior used in the analysis and the population prior
        """
        pop = PAstro.population_classification(samples)
        default = PAstro.default_classification(samples)
        return (default, pop)