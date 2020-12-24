# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Coding\py\IPython Notebooks\experiment\chunking\LazyEEG\algorithms\tanova.py
# Compiled at: 2017-04-18 04:16:01
# Size of source mod 2**32: 10554 bytes
from ..default import *
from .. import group
from .general import *
from ..graph import put as plot_put
from ..statistics import process
from ..statistics import test
from tqdm import tqdm
from scipy.spatial.distance import cosine

def Topo_Difference(data, container, step='1ms', err_style='ci_band', win='5ms', sample='mean', sig_limit=0):

    def calc_cosD(data):
        a, b = np.array(data)
        return cosine(a, b)

    def calc(batch_data):
        batch_data = mean_axis(batch_data, 'trial')
        if step != '1ms':
            batch_data = point_sample(batch_data, step)
        else:
            if win != '1ms':
                batch_data = window_sample(batch_data, win, sample)
        batch_data = condition_shuffled(batch_data)
        distance = process.row_roll(batch_data, row=['subject', 'condition', 'time'], column=['channel'], func=calc_cosD)
        return distance['p'].unstack('time')

    container_data = group.extract(data, container, 'Topograph')
    diff_data = [(title, calc(batch_data)) for title, batch_data in container_data]
    diff_stat_data = [None for i in diff_data]
    note = [
     'Time(ms)', 'Distance', []]
    plot_put.block(diff_data, note, err_style, diff_stat_data, win, sig_limit=0)
    return diff_data


def CosineD_dynamics(data, container, step='1ms', win='20ms', sample='mean', shuffle=500):

    def calc_cosD(data):
        data_mean = mean_axis(data, 'trial')
        a, b = np.array(data_mean)
        return (2 * cosine(a, b)) ** 0.5

    def calc(batch_data):
        if step != '1ms':
            batch_data = point_sample(batch_data, step)
        else:
            if win != '1ms':
                batch_data = window_sample(batch_data, win, sample)
        result = (process.row_roll)(batch_data, row=['subject', 'condition', 'time'], column=['channel'], func=test.permutation_on_condition, **{'method':calc_cosD,  'shuffle_count':shuffle})
        return result['p']

    container_data = group.extract(data, container, 'Topograph')
    topo_data = [(title, calc(batch_data)) for title, batch_data in container_data]
    return topo_data


def TANOVA1(data, container, step='1ms', win='1ms', sample='mean', shuffle=500, shuffleInSubj=True):

    def calc_cosD(data):
        a, b = np.array(data)
        return (2 * cosine(a, b)) ** 0.5

    def condition_shuffled(data):
        group_labels = list(data.index.get_level_values(level='cond_group'))
        random.shuffle(group_labels)
        data.index = data.index.set_labels(group_labels, level='cond_group')
        return data

    def calc(batch_data):
        if step != '1ms':
            batch_data = point_sample(batch_data, step)
        else:
            if win != '1ms':
                batch_data = window_sample(batch_data, win, sample)
        pvs = pd.DataFrame()
        pvs.columns.name = 'time'
        pvs.index.name = 'condition'
        for index, index_data in tqdm(batch_data.stack('time').unstack(['channel']).groupby(level=['condition', 'time']), ncols=0):
            dist_raw = calc_cosD(mean_axis(index_data, ['subject', 'trial']))
            dist_baseline = []
            for i in range(shuffle):
                if shuffleInSubj:
                    shuffled = pd.concat([condition_shuffled(subj_data) for subj_name, subj_data in index_data.groupby(level='subject')])
                else:
                    shuffled = condition_shuffled(index_data)
                t_baseline = mean_axis(shuffled, ['subject', 'trial'])
                dist_baseline.append(calc_cosD(t_baseline))

            dist_baseline.append(dist_raw)
            dist_baseline.append(2)
            dist_baseline.sort()
            pvs.set_value(index[0], index[1], 1 - dist_baseline.index(dist_raw) / shuffle)

        return pvs

    container_data = group.extract(data, container, 'Topograph')
    topo_data = [(title, calc(batch_data)) for title, batch_data in container_data]
    return {'p': topo_data}


def TANOVA2(data, container, step='1ms', win='1ms', sample='mean', shuffle=500, AvergThenCosD=True):

    def calc_cosD(data):
        a, b = np.array(data)
        return (2 * cosine(a, b)) ** 0.5

    def condition_shuffled(data):
        group_labels = list(data.index.get_level_values(level='cond_group'))
        random.shuffle(group_labels)
        data.index = data.index.set_labels(group_labels, level='cond_group')
        return data

    def calc(batch_data):
        if step != '1ms':
            batch_data = point_sample(batch_data, step)
        else:
            if win != '1ms':
                batch_data = window_sample(batch_data, win, sample)
        pvs = pd.DataFrame()
        pvs.columns.name = 'time'
        pvs.index.name = 'condition'
        for index, index_data in tqdm(batch_data.stack('time').unstack(['channel']).groupby(level=['condition', 'time']), ncols=0):
            dist_raw = []
            dist_baseline = []
            for subject_index, subject_data in index_data.groupby(level='subject'):
                dist_raw.append(calc_cosD(mean_axis(subject_data, 'trial')))
                if AvergThenCosD:
                    shuffled_baselines = []
                    for i in range(shuffle):
                        t_baseline = mean_axis(condition_shuffled(subject_data), 'trial')
                        shuffled_baselines.append(np.array(t_baseline))

                    shuffled_baseline = np.mean(shuffled_baselines, 0)
                    dist_baseline.append(calc_cosD(shuffled_baseline))
                else:
                    shuffled_baselines = [calc_cosD(mean_axis(condition_shuffled(subject_data), 'trial')) for i in range(shuffle)]
                    dist_baseline.append(np.mean(shuffled_baselines))

            pvs.set_value(index[0], index[1], test.t_test([dist_raw, dist_baseline])[0])

        return pvs

    container_data = group.extract(data, container, 'Topograph')
    topo_data = [(title, calc(batch_data)) for title, batch_data in container_data]
    return {'p': topo_data}