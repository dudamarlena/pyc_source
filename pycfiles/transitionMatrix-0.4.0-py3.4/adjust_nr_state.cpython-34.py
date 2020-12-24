# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/adjust_nr_state.py
# Compiled at: 2018-10-22 16:10:48
# Size of source mod 2**32: 1540 bytes
""" Example of using transitionMatrix adjust the NR state (not-rated).

Input data are the Standard and Poor's historical data (1981 - 2016) for corporate credit rating migrations

"""
import transitionMatrix as tm
from transitionMatrix import source_path
dataset_path = source_path + 'datasets/'
print('> Load multi-period transitional matrices (cumulative mode) from json file')
SnP_Set0 = tm.TransitionMatrixSet(json_file=dataset_path + 'sp_1981-2016.json', temporal_type='Cumulative')
print('> Valid Input Matrix? ', SnP_Set0.validate())
print('> Remove NR transitions and redistribute to other states')
SnP_Set1 = SnP_Set0.remove(8, 'noninform')
print('> Valid Output Matrix? ', SnP_Set1.validate())
SnP_Set1.to_json(dataset_path + 'sp_NR_adjusted.json', accuracy=5)