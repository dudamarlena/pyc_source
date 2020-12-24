# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\py3\experiments\easyEEG_dist\easyEEG\algorithms\erp.py
# Compiled at: 2018-05-22 18:33:32
# Size of source mod 2**32: 3916 bytes
from ..default import *
from .. import structure
from .basic import *
from ..statistics import stats_methods
comparison_params = dict(test=(stats_methods.t_test), win='20ms', method='mean', sig_limit=0.05, need_fdr=False)

def ERP(self, compare=False, comparison_params=comparison_params):

    @self.iter('average')
    def to_erp(case_raw_data):
        return case_raw_data.mean(level=['subject', 'condition_group', 'channel_group'])

    erp_batch = to_erp()
    if compare:
        stats_data = stats_compare(erp_batch, comparison_params, levels='time', between='condition_group', in_group='subject')
    else:
        stats_data = None
    default_plot_params = dict(plot_type=['direct', 'waveform'], y_title='Amplitude(uV)', err_style='ci_band', color='Set1',
      style='darkgrid',
      compare=compare,
      win=(comparison_params['win']),
      sig_limit=0.05)
    return structure.Analyzed_data('ERP', erp_batch, stats_data, default_plot_params=default_plot_params)


def topo_ERPs(self, compare=False, comparison_params=comparison_params):

    @self.iter('average')
    def to_erp(case_raw_data):
        return case_raw_data.mean(level=['subject', 'condition_group', 'channel_group'])

    erp_batch = to_erp()
    if compare:
        stats_data = stats_compare(erp_batch, comparison_params, levels=['time', 'channel_group'], between='condition_group', in_group='subject')
    else:
        stats_data = None
    default_plot_params = dict(plot_type=['float', 'waveform'], y_title='Amplitude(uV)', err_style='ci_band', color='Set1', style='darkgrid', compare=compare, win=(comparison_params['win']),
      sig_limit=0.05,
      xy_locs=(self.info['xy_locs']))
    return structure.Analyzed_data('topo_ERPs', erp_batch, stats_data, default_plot_params=default_plot_params)


def ERPs(self):

    @self.iter('average')
    def to_erp(case_raw_data):
        return case_raw_data.mean(level=['subject', 'condition_group', 'channel_group'])

    erp_batch = to_erp()
    stats_data = None
    default_plot_params = dict(plot_type=['direct', 'waveform'], y_title='Amplitude(uV)', err_style=None, color=['#34495e'], style='darkgrid', legend=False)
    return structure.Analyzed_data('ERPs', erp_batch, stats_data, default_plot_params=default_plot_params)


def GFP(self, compare=False, comparison_params=comparison_params):

    def calc_gfp(x):
        return np.sqrt(np.mean(x ** 2))

    @self.iter('average')
    def to_gfp(case_raw_data):
        erp = case_raw_data.mean(level=['subject', 'condition_group', 'channel', 'channel_group'])
        GFP_df = []
        for name, data in erp.groupby(level=['subject', 'condition_group', 'channel_group']):
            data = pd.DataFrame(data.apply(calc_gfp)).T
            data.index = pd.MultiIndex.from_tuples([name], names=['subject', 'condition_group', 'channel_group'])
            GFP_df.append(data)

        GFP_df = pd.concat(GFP_df)
        return GFP_df

    gfp_batch = to_gfp()
    if compare:
        stats_data = stats_compare(gfp_batch, comparison_params, levels='time', between='condition_group', in_group='subject')
    else:
        stats_data = None
    default_plot_params = dict(plot_type=['direct', 'waveform'], y_title='GFP', err_style='ci_band', color='Set1',
      style='darkgrid',
      compare=compare,
      win=(comparison_params['win']),
      sig_limit=0.05)
    return structure.Analyzed_data('GFP', gfp_batch, stats_data, default_plot_params=default_plot_params)