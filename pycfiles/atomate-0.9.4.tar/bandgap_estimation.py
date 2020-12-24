# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/bandgap_estimation.py
# Compiled at: 2017-08-17 17:36:49
from __future__ import division
from tqdm import tqdm
import math
from atomate.utils.utils import get_logger
from matgendb.util import get_database
logger = get_logger(__name__)
__author__ = 'Anubhav Jain <ajain@lbl.gov>'

class BandgapEstimationBuilder:

    def __init__(self, materials_write):
        """
        Starting with an existing materials collection with dielectric constant data, adds
        estimated band gaps that may be more accurate than typical GGA calculations.

        Run the "DielectricBuilder" before running this builder.

        Args:
            materials_write: mongodb collection for materials (write access needed)
        """
        self._materials = materials_write

    def run(self):
        logger.info(('{} starting...').format(self.__class__.__name__))
        q = {'dielectric.epsilon_static_avg': {'$gt': 0}, 'bandgap_estimation': {'$exists': False}}
        for m in tqdm(self._materials.find(q, projection=['material_id', 'dielectric'])):
            try:
                eps = m['dielectric']['epsilon_static_avg']
                n = math.sqrt(eps)
                d = {}
                d['gap_moss'] = 95 / n ** 4 if n > 0 else None
                d['gap_gupta-ravindra'] = (4.16 - n) / 0.85 if n <= 4.16 else None
                d['gap_reddy-anjaneyulu'] = 36.3 / math.exp(n)
                d['gap_reddy-ahamed'] = 154 / n ** 4 + 0.365 if n > 0 else None
                d['gap_herve_vandamme'] = 13.47 / math.sqrt(n ** 2 - 1) - 3.47 if n > 1 else None
                d = {'bandgap_estimation': d}
                self._materials.update_one({'material_id': m['material_id']}, {'$set': d})
            except:
                import traceback
                logger.exception(traceback.format_exc())

        logger.info(('{} finished.').format(self.__class__.__name__))
        return

    def reset(self):
        logger.info(('Resetting {} starting!').format(self.__class__.__name__))
        self._materials.update_many({}, {'$unset': {'bandgap_estimation': 1}})
        logger.info(('Resetting {} finished!').format(self.__class__.__name__))

    @staticmethod
    def from_file(db_file, m='materials', **kwargs):
        """
        Get builder using only a db file.

        Args:
            db_file: (str) path to db file
            m: (str) name of "materials" collection
            **kwargs: other parameters to feed into the builder, e.g. mapi_key

        Returns:
            BandgapEstimationBuilder
        """
        db_write = get_database(db_file, admin=True)
        return BandgapEstimationBuilder(db_write[m], **kwargs)