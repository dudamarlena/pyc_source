# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/datasets/imdb_unsup.py
# Compiled at: 2017-11-28 10:47:30
# Size of source mod 2**32: 1045 bytes
"""
Processing of the imdb_unsup dataset.

URL:
http://ai.stanford.edu/~amaas/data/sentiment/    
REF:
Maas, A. L., Daly, R. E., Pham, P. T., Huang, D., Ng, A. Y., & Potts, C. (2011, June). 
Learning word vectors for sentiment analysis. 
In Proceedings of the 49th Annual Meeting of the Association for Computational Linguistics: Human Language Technologies-Volume 1 (pp. 142-150). Association for Computational Linguistics.
"""
import os, logging, pandas as pd, numpy as np
from glob import glob
from itertools import islice
from gsitk.datasets import utils
from gsitk.datasets.datasets import Dataset
from gsitk.preprocess import normalize
from gsitk.datasets.imdb import Imdb
logger = logging.getLogger(__name__)

class Imdb_unsup(Imdb):

    def normalize_data(self):
        dataset = pd.DataFrame(columns=['id', 'text', 'polarity'])
        data_path = os.path.join(self.data_path, self.info['properties']['data_file'])
        self.populate_data(path=data_path, dataframe=dataset, unsup=True)
        return dataset