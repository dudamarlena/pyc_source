# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/fix_multiperiod_matrix.py
# Compiled at: 2018-10-21 07:33:15
# Size of source mod 2**32: 2238 bytes
""" Example of using transitionMatrix to detect and solve various pathologies that might be affecting transition
matrix data

"""
import transitionMatrix as tm, numpy as np
from transitionMatrix import dataset_path
print('> Loading historical multi-period transitional matrices (cumulative mode) from csv file')
SnP_Set0 = tm.TransitionMatrixSet(csv_file=dataset_path + 'sp_1981-2016.csv', temporal_type='Cumulative')
print('> Validate')
print(SnP_Set0.validate())
print('> We detect dimensionality problems. The matrices are not square (missing the trivial Default and NR transitions)')
print('> We must fix that to proceed. Augment matrices in set by fixing Default and NR transitions')
C_Vals = []
for matrix in SnP_Set0.entries:
    C = tm.TransitionMatrix(values=np.resize(matrix, (9, 9)))
    C[7, 0:9] = 0.0
    C[8, 0:9] = 0.0
    C[(7, 7)] = 100.0
    C[(8, 8)] = 100.0
    C_Vals.append(C)

SnP_Set1 = tm.TransitionMatrixSet(values=C_Vals)
print('> Validate Again')
print(SnP_Set1.validate())
print('> Now we have square matrices but the format is not in probabilities!')
print('> Divide all entries by 100')
SnP_Set2 = SnP_Set1 * 0.01
print('> Validate Again')
print(SnP_Set2.validate())
print('> Hurrah, we have a probability matrix set. Lets save it')
SnP_Set2.to_json(dataset_path + 'sp_1981-2016.json', accuracy=5)