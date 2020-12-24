# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/generate_full_multiperiod_set.py
# Compiled at: 2018-10-21 08:00:46
# Size of source mod 2**32: 3526 bytes
""" Example of using the transitionMatrix generator methods to generate a full multi-period matrix set
The input data are processed Standard and Poor's matrices for a selection of cumulative observation points
NB: This example requires a substantial amount of custom code!

"""
from scipy.linalg import expm
import transitionMatrix as tm
from transitionMatrix import source_path
dataset_path = source_path + 'datasets/'
print('> Loading multi-period transitional matrices (cumulative mode) from json file')
SnP_Set0 = tm.TransitionMatrixSet(json_file=dataset_path + 'sp_NR_adjusted.json', temporal_type='Cumulative')
print('> Validate')
print(SnP_Set0.validate())
print('> Set the timesteps at which we have matrix observations')
SnP_Set0.timesteps = [
 1, 2, 3, 5, 7, 10]
print(SnP_Set0.timesteps)
timesteps = SnP_Set0.timesteps[(len(SnP_Set0.timesteps) - 1)]
SnP = tm.TransitionMatrixSet(dimension=8, periods=timesteps)
print('> Fill in the gaps between periods')
t_list = SnP_Set0.timesteps
ts = 1
SnP.entries[ts - 1] = SnP_Set0.entries[0]
for k in t_list:
    i = t_list.index(k)
    if i < len(t_list) - 1:
        gap = t_list[(i + 1)] - t_list[i]
        if gap > 1:
            lm = SnP_Set0.entries[i]
            lm.fix_rowsums()
            rm = SnP_Set0.entries[(i + 1)]
            rm.fix_rowsums()
            q = rm * lm.I
            q.fix_rowsums()
            q.fix_negativerates()
            G = q.generator(t=gap)
            for gap_period in range(1, gap + 1):
                gm = expm(gap_period * G)
                cm = gm * lm
                cm.fix_negativerates()
                ts += 1
                SnP.entries[ts - 1] = cm

        else:
            ts += 1
            SnP.entries[ts - 1] = SnP_Set0.entries[(i + 1)]
    else:
        ts = timesteps
        SnP.entries[ts - 1] = SnP_Set0.entries[i]

SnP.timesteps = t_list
SnP.temporal_type = 'Cumulative'
SnP.print(accuracy=4)
SnP.to_json(dataset_path + 'sp_multiperiod.json', accuracy=8)