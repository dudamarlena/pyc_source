# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maya/andrew_exp.py
# Compiled at: 2019-06-13 05:22:46
# Size of source mod 2**32: 1319 bytes
from KeySpot_op import KeySpot
from exp_runner.dataset_processor import sample_to_new_dir
from exp_runner.result_processor import result_to_file_raw
import os
from multiprocessing import Pool

class Andrew(object):

    def __init__(self, exp_op):
        print('Running experiments following <Machine Learning Yearning>')
        print('For more detail: https://accepteddoge.github.io/machine-learning-yearning-cn/docs/home/')
        self.exp_op = exp_op

    def draw_learn_curve(self, num):
        exp_list = []
        assert num >= 2
        for i in range(1, num):
            percentage = i / float(num)
            new_dir = os.path.abspath(sample_to_new_dir('half_plus_data_1225_4', percentage))
            print(new_dir)
            basename = os.path.basename(new_dir)
            dataset_list = [basename]
            exp_list.append((dataset_list, []))

        p = Pool()
        result = p.map(self.exp_op.train, exp_list)
        return result

    def show_fail_case(self):
        result = self.exp_op.default_train()

    def get_eyeball(self):
        pass


if __name__ == '__main__':
    default_dataset = 'half_plus_data_1225_4'
    ks_op = KeySpot({}, default_dataset)
    ng = Andrew(ks_op)
    result = ng.draw_learn_curve(10)
    print(result)
    result_to_file_raw(result)