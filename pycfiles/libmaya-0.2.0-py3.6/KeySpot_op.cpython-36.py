# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/maya/KeySpot_op.py
# Compiled at: 2019-06-13 05:22:46
# Size of source mod 2**32: 6120 bytes
from exp_runner.from_template import edit_file, edit_file_with_dict, rewrite_file
from exp_runner.command_runner import run_command, run_command_with_id
from exp_runner.result_processor import result_print, result_to_file_raw, result_to_file_read
from exp_runner.utils import clean_dir, force_copy_tree, check_exist
from exp_runner.dataset_processor import sample_to_new_dir
import os
from multiprocessing import Pool
import shutil, glob

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


class KeySpot(object):

    def __init__(self, template_dict, default_dataset):
        self.template_dict = template_dict
        self.default_dataset = default_dataset

    def key_with_id(self, input_tuple):
        teamplate1 = './audio_super/StreamingAccuracy.h.template'
        teamplate2 = './audio_super/StreamingKeyWordSpotting.h.template'
        teamplate3 = './audio_super/StreamingKeyWordSpotting.cc'
        command_id, mode, avg_window, window_stride, threshold, pb = input_tuple
        base_dir = os.path.abspath('./')
        dummy_path = '../' + str(command_id) + '/'
        clean_dir(dummy_path)
        shutil.copytree('./', dummy_path)
        os.chdir(dummy_path)
        print('working in', dummy_path)
        rewrite_file(teamplate1, mode)
        rewrite_file(teamplate2, mode)
        rewrite_file(teamplate3, mode)
        if '16000' in pb:
            time_sample = 16000
        else:
            time_sample = 24000
        replace_dict = {'PB_PH':pb, 
         'AVG_PH':str(avg_window),  'TH_PH':str(threshold),  'TIME_PH':str(time_sample)}
        edit_file_with_dict(teamplate1, replace_dict)
        replace_dict2 = {'STRIDE_PH':str(window_stride), 
         'TIME_PH':str(time_sample)}
        edit_file_with_dict(teamplate2, replace_dict2)
        os.system('rm CMakeCache.txt')
        result = run_command('cmake ./ && make && ./demo')
        os.chdir(base_dir)
        shutil.rmtree(dummy_path)
        return result

    def default_train(self):
        input_tuple = (
         [
          self.default_dataset], [])
        result = self.train(input_tuple)
        return result

    def default_test(self):
        assert 'not implement yet.'
        return result

    def train(self, input_tuple):
        dataset_list, pre_processing_list = input_tuple
        check_exist(dataset_list)
        print(pre_processing_list)
        command_id = ''.join(dataset_list + pre_processing_list)
        base_dir = os.path.abspath('./')
        dummy_path = os.path.abspath('../' + str(command_id) + '/')
        assert len(command_id) != 0
        print('dummy_path', dummy_path)
        clean_dir(dummy_path)
        force_copy_tree('./', dummy_path)
        os.chdir(dummy_path)
        print('working in', dummy_path)
        for pre_processing in pre_processing_list:
            rewrite_file(self.template_dict[pre_processing], pre_processing)

        clean_dir('./dataset/')
        for dataset in dataset_list:
            force_copy_tree('./' + dataset, './dataset/')

        result = run_command('python keyspot_train/train_easy.py')
        os.chdir(base_dir)
        print(dummy_path + '/output.pb', base_dir + '/' + command_id + '.pb')
        shutil.copyfile(dummy_path + '/output.pb', base_dir + '/' + command_id + '.pb')
        shutil.rmtree(dummy_path)
        return result

    def keyspot_runner_acc(self, input_tuple):
        print('Running with: ', input_tuple)
        result = self.key_with_id(input_tuple)
        correct_triggle_percentage_TP_T, false_triggle_percentage_FP_P, delay, max_delay = result[(-8)].split(' ')
        result_tuple = (correct_triggle_percentage_TP_T, false_triggle_percentage_FP_P, delay, max_delay)
        return (input_tuple, result_tuple)

    def keyspot_runner_n_mos(self, input_tuple):
        print('Running with: ', input_tuple)
        result = self.key_with_id(input_tuple)
        _, n_mos = result[(-1)].split(':')
        return n_mos


if __name__ == '__main__':
    default_dataset = 'half_plus_data_1225_4'
    ks = KeySpot({}, default_dataset)
    result = ks.default_train()
    print(result)
    result_to_file_raw(result)