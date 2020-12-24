# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/oaraque/git/gsi/gsitk/gsitk/datasets/semeval13.py
# Compiled at: 2017-03-21 06:14:47
# Size of source mod 2**32: 1657 bytes
"""
Processing of the semeval2013 dataset.

URL:
https://www.cs.york.ac.uk/semeval-2013/accepted/101_Paper.pdf

REF:
HLTCOE, J. (2013). SemEval-2013 Task 2: Sentiment Analysis in Twitter. Atlanta, Georgia, USA, 312.
"""
import os, logging, pandas as pd
from gsitk import config
from gsitk.datasets import utils
from gsitk.datasets.datasets import Dataset
from gsitk.preprocess import normalize
logger = logging.getLogger(__name__)
NAME = os.path.splitext(os.path.basename(__file__))[0]

class Semeval13(Dataset):

    def __init__(self, info=None):
        if info is None:
            info = utils.load_info(NAME)
        super(Semeval13, self).__init__(info)

    def normalize_data(self):
        data_path = os.path.join(config.DATA_PATH, self.name)
        raw_data_path = os.path.join(data_path, self.info['properties']['data_file'])
        data = pd.read_csv(raw_data_path, header=None, encoding='utf-8', sep='\t', index_col=False, names=[
         'tweet_id',
         'user_id',
         'polarity',
         'text'])
        pol_conv = {'negative': -1, 
         'neutral': 0, 
         'positive': 1}
        data['polarity'].replace(pol_conv, inplace=True)
        text_data = normalize.normalize_text(data)
        data = pd.concat([data['polarity'], text_data], axis=1)
        data.columns = [
         'polarity', 'text']
        return data