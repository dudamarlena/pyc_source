# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/generate_synthetic_data.py
# Compiled at: 2018-10-22 07:16:35
# Size of source mod 2**32: 6307 bytes
"""
Example workflows using transitionMatrix to generate synthetic data

The first three examples produce "duration" type data. Estimating transitions
for duration data is done directly with duration type estimators or after
cohorting (binning) the data for cohort (frequency) type estimators

The subsequent three examples product cohort type data using markov chain simulation

"""
import transitionMatrix as tm
from datasets import Generic
from transitionMatrix import source_path
from transitionMatrix.utils import dataset_generators
dataset_path = source_path + 'datasets/'
dataset = 7
if dataset == 1:
    myState = tm.StateSpace([('0', 'A'), ('1', 'B'), ('2', 'C'), ('3', 'D')])
    data = dataset_generators.exponential_transitions(myState, n=1, sample=100, rate=0.1)
    sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
    sorted_data.to_csv(dataset_path + 'synthetic_data1.csv', index=False)
else:
    if dataset == 2:
        myState = tm.StateSpace([('0', 'Basic'), ('1', 'Default')])
        data = dataset_generators.exponential_transitions(myState, n=1000, sample=10, rate=0.1)
        sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
        sorted_data.to_csv(dataset_path + 'synthetic_data2.csv', index=False)
    else:
        if dataset == 3:
            myState = tm.StateSpace([('0', 'A'), ('1', 'B'), ('2', 'C'), ('3', 'D'), ('4', 'E'), ('5', 'F'), ('6', 'G')])
            data = dataset_generators.exponential_transitions(myState, n=100, sample=20, rate=0.1)
            sorted_data = data.sort_values(['ID', 'Time'], ascending=[True, True])
            sorted_data.to_csv(dataset_path + 'synthetic_data3.csv', index=False)
        else:
            if dataset == 4:
                description = [
                 ('0', 'AAA'), ('1', 'AA'), ('2', 'A'), ('3', 'BBB'),
                 ('4', 'BB'), ('5', 'B'), ('6', 'CCC'), ('7', 'D')]
                matrix = Generic
                myState = tm.StateSpace(description)
                data = dataset_generators.markov_chain(myState, matrix, n=1000, timesteps=10)
                sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
                sorted_data.to_csv(dataset_path + 'synthetic_data4.csv', index=False)
            else:
                if dataset == 5:
                    description = [('0', 'Stage 1'), ('1', 'Stage 2'), ('2', 'Stage 3')]
                    matrix = [
                     [
                      0.8, 0.15, 0.05],
                     [
                      0.1, 0.7, 0.2],
                     [
                      0.0, 0.0, 1.0]]
                    myState = tm.StateSpace(description)
                    data = dataset_generators.markov_chain(myState, transitionmatrix=matrix, n=10000, timesteps=5)
                    sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
                    sorted_data.to_csv(dataset_path + 'synthetic_data5.csv', index=False)
                else:
                    if dataset == 6:
                        myState = tm.StateSpace()
                        myState.generic(2)
                        myState.describe()
                        matrix = [[0.5, 0.5],
                         [
                          0.0, 1.0]]
                        data = dataset_generators.markov_chain(myState, transitionmatrix=matrix, n=1000, timesteps=20)
                        sorted_data = data.sort_values(['ID', 'Timestep'], ascending=[True, True])
                        data.to_csv(dataset_path + 'synthetic_data6.csv', index=False)
                    else:
                        if dataset == 7:
                            description = [('0', 'AAA'), ('1', 'AA'), ('2', 'A'), ('3', 'BBB'),
                             ('4', 'BB'), ('5', 'B'), ('6', 'CCC'), ('7', 'D')]
                            myState = tm.StateSpace(description)
                            matrix = Generic
                            data = dataset_generators.long_format(myState, transitionmatrix=matrix, n=1000, timesteps=10)
                            sorted_data = data.sort_values(['Time', 'ID', 'From'], ascending=[True, True, True])
                            sorted_data.to_csv(dataset_path + 'synthetic_data7.csv', index=False)
                        elif dataset == 8:
                            description = [
                             ('0', 'G'), ('1', 'B')]
                            myState = tm.StateSpace()
                            myState.generic(2)
                            myState.describe()
                            matrix = [[0.5, 0.5],
                             [
                              0.0, 1.0]]
                            data = dataset_generators.long_format(myState, transitionmatrix=matrix, n=10000, timesteps=2)
                            sorted_data = data.sort_values(['Time', 'ID', 'From'], ascending=[True, True, True])
                            data.to_csv(dataset_path + 'synthetic_data8.csv', index=False)
print('> Synthetic Dataset:', dataset, ' has been created and stored in the filesystem.')