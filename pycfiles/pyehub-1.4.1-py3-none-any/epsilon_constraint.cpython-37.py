# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/epsilon_constraint.py
# Compiled at: 2019-07-03 19:21:52
# Size of source mod 2**32: 2540 bytes
__doc__ = '\nProvides a function for the ehub_model using an epsilon constraint method\n\nfor input and output files - use config.yaml\n\nTo run: specify the number of intervals wanted for epsilon constraint method in the arguments\n\n            $ python epsilon_constraint.py --epsilon_n N\n'
from energy_hub import EHubModel
from run import CarbonEHubModel
import yaml
from outputter import pretty_print, output_excel
import argparse
with open('config.yaml', 'r') as (file_descriptor):
    data = yaml.safe_load(file_descriptor)

def main(epsilon_n):
    """
    Main function for running the EHub_Model using the epsilon constraint method

    :param epsilon_n: number of divisions wanted for the epsilon constraint method

    :outputs excel files with all the data (including the points in between)
    """
    outputFile = data['output_file']
    if epsilon_n is None:
        epsilon_n = 0
    cost_min_model = EHubModel(excel=(data['input_file']))
    cost_min = cost_min_model.solve(data['solver'])
    carbon_per_step = 0 if epsilon_n == 0 else cost_min['solution']['total_carbon'] / epsilon_n
    for n in range(epsilon_n + 1):
        carbon_min_model = CarbonEHubModel(excel=(data['input_file']), max_carbon=(carbon_per_step * n))
        carbon_min = carbon_min_model.solve(data['solver'])
        pretty_print(carbon_min)
        output_excel((carbon_min['solution']), (outputFile[:-5] + '_' + str(n) + '.xlsx'), time_steps=(len(carbon_min_model.time)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--epsilon_n', type=int, help='The number of steps to break into for the epsilon constraint.')
    arg = parser.parse_args()
    main(arg.epsilon_n)