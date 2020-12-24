# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Zeras/data_parallelism.py
# Compiled at: 2020-03-15 07:46:43
# Size of source mod 2**32: 3459 bytes
"""
Created on Sat Sep 29 04:11:16 2018

@author: limingfan
"""
import os, pickle

def save_data_to_pkl(data, file_path):
    with open(file_path, 'wb') as (fp):
        pickle.dump(data, fp)


def load_data_from_pkl(file_path):
    with open(file_path, 'rb') as (fp):
        data = pickle.load(fp)
    return data


def get_files_with_ext(path, str_ext, flag_walk=False):
    """
    """
    list_all = []
    if flag_walk:
        for root, dirs, files in os.walk(path):
            for filename in files:
                file_path = os.path.join(root, filename)
                list_all.append(file_path)

    else:
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            list_all.append(file_path)

    file_list = [item for item in list_all if item.endswith(str_ext)]
    return file_list


def split_data_list(list_data, num_split):
    """
    """
    num_data_all = len(list_data)
    num_per_worker = num_data_all // num_split
    print('num_data_all: %d' % num_data_all)
    data_split = []
    posi_start = 0
    posi_end = num_per_worker
    for idx in range(num_split):
        list_curr = list_data[posi_start:posi_end]
        data_split.append(list_curr)
        posi_start = posi_end
        posi_end += num_per_worker

    if posi_start < num_data_all:
        data_split[(-1)].extend(list_data[posi_start:])
    list_num_data = [len(item) for item in data_split]
    print('list_files split: {}'.format(list_num_data))
    return data_split


class DataParallelism(object):
    __doc__ = '\n    '

    def __init__(self, num_workers, worker_type='thread'):
        """
        """
        self.num_workers = num_workers
        self.worker_type = worker_type

    def do_processing(self, list_data, process_pipeline, args_rem):
        """
        """
        data_split = split_data_list(list_data, self.num_workers)
        if self.worker_type == 'process':
            from multiprocessing import Process
        else:
            from multiprocessing.dummy import Process
        self.worker = Process
        print('parent process: %s.' % os.getpid())
        self._workers = []
        for idx in range(self.num_workers):
            p_curr = self.worker(target=process_pipeline, args=(
             data_split[idx], idx, args_rem))
            p_curr.daemon = True
            self._workers.append(p_curr)
            print('worker %d created' % idx)

        for idx in range(self.num_workers):
            self._workers[idx].start()

        for idx in range(self.num_workers):
            self._workers[idx].join()

        print('data processing all finished')


if __name__ == '__main__':
    pass