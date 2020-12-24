# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanghunkang/dev/aascraw/venv/lib/python3.7/site-packages/aascraw/kernels.py
# Compiled at: 2019-08-28 10:35:45
# Size of source mod 2**32: 6406 bytes
import numpy as np
from functools import reduce
import ctypes
SIZE_XPATH_SET = 4
c_kernels = ctypes.CDLL('./aascraw/c_kernels.so')
c_kernels.rank_tuple_vicinity.argtypes = (
 ctypes.c_wchar_p * SIZE_XPATH_SET,)
c_kernels.rank_tuple_vicinity.restype = ctypes.c_int
arr = ctypes.c_wchar_p * SIZE_XPATH_SET
parameter_array = arr(*['array', 'of', 'strings', 'asdasd'])

def rank_tuple_vicinity(xpath_set, existing_records):
    filterer_actions = [xpath['filterer_action'] for xpath in xpath_set]
    c_xpath_set = (ctypes.c_wchar_p * SIZE_XPATH_SET)(*filterer_actions)
    print(len(filterer_actions))
    print(c_xpath_set)
    rank = c_kernels.rank_tuple_vicinity(c_xpath_set)
    print(rank)
    return rank


def rank_tuple_consistency(new_record, existing_records):
    """
    This function returns an integer which indicates how much the relative sizes of contents is preserved.
    It is 0 if relative sizes of contents are perfectly different from previous records, 
    and it is 1 if relative sizes of contents are at exact average of previous records.
    """
    rank = 0
    return rank


def rank_consistency_by_datatype(new_record, existing_records):
    rank = 0
    for element in new_record:
        element_type = str
        try:
            int()
        except Error:
            pass

    return rank


def rank_content_variance(new_record, existing_records, element_index, record_length):
    """
    This functions measures how much a new record is variant from previously collected records.
    It is 0 if it the new record is exactly the same with one of previously collected records,
    and it is 1 if the new record is completly different from previously collected records.
    """
    rank = np.zeros(record_length)
    rank[element_index] = 1
    for existing_record in existing_records:
        if existing_record['crawled_data'] == new_record['crawled_data']:
            rank[element_index] = 0

    return rank


def rank_content_length(new_record, existing_records, element_id, record_length):
    arr_existing_elements = [np.log(len(record['crawled_data'])) for record in existing_records if record['index'] == element_id]
    score_mean_existing_elements = np.mean(arr_existing_elements)
    score_new_record = np.log(len(new_record['crawled_data']))
    rank = np.zeros(record_length)
    rank[element_id] = np.square(score_new_record - score_mean_existing_elements)
    return rank