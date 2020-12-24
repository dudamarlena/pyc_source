# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/adlib/tests/adversaries/data_transform_test.py
# Compiled at: 2018-07-17 12:56:28
# Size of source mod 2**32: 1640 bytes
from adlib.adversaries.datatransform.data_transform import DataTransform
from adlib.adversaries.datatransform.poisoning.poison import open_dataset
import time

def test_data_transform():
    print()
    print('###################################################################')
    print('START data transform attack.\n')
    begin = time.time()
    args = {'beta':0.1, 
     'dataset':'./data_reader/data/raw/data-transform/house-processed.csv', 
     'epsilon':0.001, 
     'eta':0.5, 
     'initialization':'randflip', 
     'lambd':1, 
     'logdir':'./results', 
     'logind':0, 
     'model':'ridge', 
     'multiproc':False, 
     'numinit':1, 
     'objective':1, 
     'optimizey':False, 
     'partct':4, 
     'poisct':75, 
     'rounding':False, 
     'seed':123, 
     'sigma':1.0, 
     'testct':500, 
     'trainct':300, 
     'validct':250, 
     'visualize':False}
    x, y = open_dataset(args['dataset'], args['visualize'])
    attacker = DataTransform(**args)
    poisoned_x, poisoned_y = attacker.attack((x, y))
    end = time.time()
    print('\nTotal time: ', (round(end - begin, 2)), 's', '\n', sep='')
    print('\nEND data transform attack.')
    print('###################################################################')
    print()


if __name__ == '__main__':
    test_data_transform()