# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/recommendation/constants.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 2979 bytes
"""Central location for NCF specific values."""
import sys, numpy as np
from official.recommendation import movielens
TRAIN_USER_KEY = 'train_{}'.format(movielens.USER_COLUMN)
TRAIN_ITEM_KEY = 'train_{}'.format(movielens.ITEM_COLUMN)
TRAIN_LABEL_KEY = 'train_labels'
MASK_START_INDEX = 'mask_start_index'
VALID_POINT_MASK = 'valid_point_mask'
EVAL_USER_KEY = 'eval_{}'.format(movielens.USER_COLUMN)
EVAL_ITEM_KEY = 'eval_{}'.format(movielens.ITEM_COLUMN)
USER_MAP = 'user_map'
ITEM_MAP = 'item_map'
USER_DTYPE = np.int32
ITEM_DTYPE = np.int32
MIN_NUM_RATINGS = 20
NUM_EVAL_NEGATIVES = 999
TOP_K = 10
HR_KEY = 'HR'
NDCG_KEY = 'NDCG'
DUPLICATE_MASK = 'duplicate_mask'
HR_METRIC_NAME = 'HR_METRIC'
NDCG_METRIC_NAME = 'NDCG_METRIC'
RAW_CACHE_FILE = 'raw_data_cache_py{}.pickle'.format(sys.version_info[0])
CACHE_INVALIDATION_SEC = 86400
CYCLES_TO_BUFFER = 3
SYNTHETIC_BATCHES_PER_EPOCH = 2000
NUM_FILE_SHARDS = 16
TRAIN_FOLDER_TEMPLATE = 'training_cycle_{}'
EVAL_FOLDER = 'eval_data'
SHARD_TEMPLATE = 'shard_{}.tfrecords'