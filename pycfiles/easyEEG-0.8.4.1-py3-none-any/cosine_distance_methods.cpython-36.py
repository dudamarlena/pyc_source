# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\IPython Notebooks\experiment\lazyEEG_dist\lazyEEG\algorithms\cosine_distance_methods.py
# Compiled at: 2018-01-19 20:50:36
# Size of source mod 2**32: 6978 bytes
from ..default import *
from .. import structure
from .basic import *
from ..statistics import stats_methods
from scipy.spatial.distance import cosine

def tanova(self, step_size='1ms', win_size='1ms', sample='mean', shuffle=500, mode=1):

    def calc_cosD(df):
        cond_A, cond_B = [average(conditon_group_data, keep='channel').mean(axis=1) for conditon_group_id, conditon_group_data in df.groupby(level='condition_group')]
        return cosine(cond_A, cond_B)

    @self.iter('all')
    def to_tanova1(case_raw_data):
        case_raw_data = sampling(case_raw_data, step_size, win_size, sample)
        check_availability(case_raw_data, 'condition_group', 2)

        def sub_func(group_data):
            result_real = calc_cosD(group_data)
            dist_baseline = []
            for _ in range(shuffle):
                shuffle_on_level(group_data, 'condition_group', within_subject=False)
                dist_baseline.append(calc_cosD(group_data))

            pvalue = permutation_test_calc(result_real, dist_baseline)
            return pvalue

        return roll_on_levels(case_raw_data, sub_func, levels='time', prograssbar=True)

    @self.iter('all')
    def to_tanova2(case_raw_data):
        case_raw_data = sampling(case_raw_data, step_size, win_size, sample)
        check_availability(case_raw_data, 'condition_group', 2)

        def sub_func(group_data):
            result_real = calc_cosD(group_data)
            dist_baseline = []
            for _ in range(shuffle):
                shuffle_on_level(group_data, 'condition_group', within_subject=True)
                dist_baseline.append(calc_cosD(group_data))

            pvalue = permutation_test_calc(result_real, dist_baseline)
            return pvalue

        return roll_on_levels(case_raw_data, sub_func, levels='time', prograssbar=True)

    @self.iter('all')
    def to_tanova3(case_raw_data):
        case_raw_data = sampling(case_raw_data, step_size, win_size, sample)
        check_availability(case_raw_data, 'condition_group', 2)

        def sub_func(group_data):
            result_real = []
            baseline = []
            for subject_group_id, subject_group_data in group_data.groupby(level='subject'):
                result_real.append(calc_cosD(subject_group_data))
                dist_baseline = []
                for _ in range(shuffle):
                    shuffle_on_level(group_data, 'condition_group')
                    dist_baseline.append(calc_cosD(group_data))

                baseline.append(np.mean(dist_baseline))

            pvalue = scipy.stats.ttest_rel(result_real, baseline)[1]
            return pvalue

        return roll_on_levels(case_raw_data, sub_func, levels='time', prograssbar=True)

    @self.iter('average')
    def to_tanova4(case_raw_data):
        case_raw_data = sampling(case_raw_data, step_size, win_size, sample)
        check_availability(case_raw_data, 'condition_group', 2)

        def sub_func(group_data):
            result_real = calc_cosD(group_data)
            dist_baseline = []
            for _ in range(shuffle):
                shuffle_on_level(group_data, 'condition_group', within_subject=True)
                dist_baseline.append(calc_cosD(group_data))

            pvalue = permutation_test_calc(result_real, dist_baseline)
            return pvalue

        return roll_on_levels(case_raw_data, sub_func, levels='time', prograssbar=True)

    if mode == 1:
        tanova_collection = to_tanova1()
    else:
        if mode == 2:
            tanova_collection = to_tanova2()
        else:
            if mode == 3:
                tanova_collection = to_tanova3()
            else:
                if mode == 4:
                    tanova_collection = to_tanova4()
    default_plot_params = dict(title='TANOVA', plot_type=['direct', 'heatmap'], x_len=12, color=sns.cubehelix_palette(light=1, as_cmap=True),
      x_title='time',
      y_title='condition_group',
      cbar_title='pvalue')
    return structure.Analyzed_data('TANOVA', tanova_collection, default_plot_params=default_plot_params)


def Topo_CosD(data, container, step='1ms', err_style='ci_band', win='5ms', sample='mean', sig_limit=0):

    def calc(batch_data):

        def sub_task(scene_data):
            scene_data = mean_axis(scene_data, 'trial')
            if step != '1ms':
                scene_data = point_sample(scene_data, step)
            else:
                if win != '1ms':
                    scene_data = window_sample(scene_data, win, sample)
            distance = process.row_roll(scene_data, row=['subject', 'condition', 'time'], column=['channel'], func=calc_cosD)
            return distance['p'].unstack('time')

        map_result = [(scene_name, sub_task(scene_data)) for scene_name, scene_data in batch_data]
        result = pd.concat([result for name, result in map_result])
        result.sort_index(inplace=True)
        result = result.reindex([name for name, result in map_result], level='condition')
        return result

    container_data = group.extract(data, container, 'Topograph')
    diff_data = [(title, calc(batch_data)) for title, batch_data in container_data]
    diff_stat_data = [None for i in diff_data]
    note = [
     'Time(ms)', 'Distance', []]
    plot_put.block(diff_data, note, err_style, diff_stat_data, win, sig_limit=0)
    return (
     diff_data, diff_stat_data)


def CosineD_dynamics(data, container, step='1ms', win='20ms', sample='mean', shuffle=500):

    def calc_cosD_2(data):
        data_mean = mean_axis(data, 'trial')
        return calc_cosD(data_mean)

    def calc(batch_data):

        def sub_task(scene_data):
            if step != '1ms':
                scene_data = point_sample(scene_data, step)
            else:
                if win != '1ms':
                    scene_data = window_sample(scene_data, win, sample)
            result = (process.row_roll)(scene_data, row=['subject', 'condition', 'time'], column=['channel'], func=test.permutation_on_condition, **{'method':calc_cosD_2,  'shuffle_count':shuffle})
            return result['p']

        map_result = [(scene_name, sub_task(scene_data)) for scene_name, scene_data in batch_data]
        result = pd.concat([result for name, result in map_result])
        result.sort_index(inplace=True)
        result = result.reindex([name for name, result in map_result], level='condition')
        return result

    container_data = group.extract(data, container, 'Topograph')
    topo_data = [(title, calc(batch_data)) for title, batch_data in container_data]
    return topo_data