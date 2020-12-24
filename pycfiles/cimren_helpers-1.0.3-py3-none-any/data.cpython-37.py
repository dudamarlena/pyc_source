# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\cvrptw_optimization\data\data.py
# Compiled at: 2020-04-05 01:50:25
# Size of source mod 2**32: 1159 bytes
import pandas as pd, os
current_dir, this_filename = os.path.split(__file__)
customers_unit_test = pd.read_pickle(os.path.join(current_dir, 'customers_unit_test.pkl'))
depots_unit_test = pd.read_pickle(os.path.join(current_dir, 'depots_unit_test.pkl'))
transportation_matrix_unit_test = pd.read_pickle(os.path.join(current_dir, 'transportation_matrix_unit_test.pkl'))
vehicles_unit_test = pd.read_pickle(os.path.join(current_dir, 'vehicles_unit_test.pkl'))
customers0 = pd.read_pickle(os.path.join(current_dir, 'customers0.pkl'))
depots0 = pd.read_pickle(os.path.join(current_dir, 'depots0.pkl'))
transportation_matrix0 = pd.read_pickle(os.path.join(current_dir, 'transportation_matrix0.pkl'))
vehicles0 = pd.read_pickle(os.path.join(current_dir, 'vehicles0.pkl'))
customers1 = pd.read_pickle(os.path.join(current_dir, 'customers1.pkl'))
depots1 = pd.read_pickle(os.path.join(current_dir, 'depots1.pkl'))
transportation_matrix1 = pd.read_pickle(os.path.join(current_dir, 'transportation_matrix1.pkl'))
vehicles1 = pd.read_pickle(os.path.join(current_dir, 'vehicles1.pkl'))