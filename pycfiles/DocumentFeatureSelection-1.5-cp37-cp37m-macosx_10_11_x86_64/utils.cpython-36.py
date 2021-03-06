# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /codes/DocumentFeatureSelection/common/utils.py
# Compiled at: 2018-10-24 07:45:14
# Size of source mod 2**32: 1896 bytes
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
from __future__ import division
from scipy.sparse.csr import csr_matrix
from typing import Union
from DocumentFeatureSelection import models
import sqlitedict, sys, tempfile, os
python_version = sys.version_info
__author__ = 'kensuke-mi'

def flatten(lis):
    for item in lis:
        if isinstance(item, list) and not isinstance(item, str):
            for x in flatten(item):
                yield x

        else:
            yield item


def __conv_into_dict_format(pmi_word_score_items):
    out_format_structure = {}
    for item in pmi_word_score_items:
        if out_format_structure not in item['label']:
            out_format_structure[item['label']] = [
             {'word':item['word'], 
              'score':item['score']}]
        else:
            out_format_structure[item['label']].append({'word':item['word'],  'score':item['score']})

    return out_format_structure


def extract_from_csr_matrix(weight_csr_matrix, vocabulary, label_id, row_id, col_id):
    if not isinstance(weight_csr_matrix, csr_matrix):
        raise AssertionError
    else:
        assert isinstance(vocabulary, dict)
        assert isinstance(label_id, dict)


def init_cache_object(file_name: str, path_work_dir: str=tempfile.mkdtemp(), cache_backend: str='PersistentDict') -> Union[(sqlitedict.SqliteDict, models.PersistentDict)]:
    """* What you can do
    - You initialize cached object.
    """
    if cache_backend == 'PersistentDict':
        cached_obj = models.PersistentDict(os.path.join(path_work_dir, file_name))
    else:
        if cache_backend == 'SqliteDict':
            cached_obj = sqlitedict.SqliteDict((os.path.join(path_work_dir, file_name)), autocommit=True)
        else:
            raise Exception('No cache backend named {}'.format(cache_backend))
    return cached_obj