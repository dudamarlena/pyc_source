# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\IPython Notebooks\experiment\lazyEEG\algorithms\erp.py
# Compiled at: 2017-12-22 20:50:57
# Size of source mod 2**32: 4540 bytes
from ..default import *
from .. import structure
from .basic import *
from ..statistics import stats_methods
comparison_params = dict(test=(stats_methods.t_test), win='20ms', method='mean', sig_limit=0.05, need_fdr=False)

def ERP(self, compare=False, comparison_params=comparison_params):

    @self.iter('average')
    def to_erp(case_raw_data):
        check_availability(case_raw_data, single_value_level=['condition_group', 'trial_group', 'channel_group'])
        return case_raw_data.mean(level=['subject', 'condition_group', 'channel_group'])

    erp_collection = to_erp()
    if compare:
        stats_data = [stats_compare(erp_batch, comparison_params, levels='time', between='condition_group', in_group='subject') for erp_batch in erp_collection]
    else:
        stats_data = None
    default_plot_params = dict(plot_type=['direct', 'waveform'], y_title='Amplitude(uV)', err_style='ci_band', color='Set1', style='darkgrid', win=(comparison_params['win']), sig_limit=0.05)
    return structure.Analyzed_data('ERP', erp_collection, stats_data, default_plot_params)


structure.Extracted_epochs.ERP = ERP

def topo_ERPs(self, compare=False, comparison_params=comparison_params):

    @self.iter('average')
    def to_erp(case_raw_data):
        check_availability(case_raw_data, single_value_level=['condition_group', 'trial_group', 'channel_group'])
        return case_raw_data.mean(level=['subject', 'condition_group', 'channel_group'])

    erp_collection = to_erp()
    if compare:
        stats_data = [stats_compare(erp_batch, comparison_params, levels=['time', 'channel_group'], between='condition_group', in_group='subject') for erp_batch in erp_collection]
    else:
        stats_data = None
    default_plot_params = dict(plot_type=['float', 'waveform'], y_title='Amplitude(uV)', err_style='ci_band', color='Set1', style='darkgrid', win=(comparison_params['win']),
      sig_limit=0.05,
      xy_locs=(self.info['xy_locs']))
    return structure.Analyzed_data('topo_ERPs', erp_collection, stats_data, default_plot_params)


structure.Extracted_epochs.topo_ERPs = topo_ERPs

def ERPs(self):

    @self.iter('average')
    def to_erp(case_raw_data):
        check_availability(case_raw_data, single_value_level=['condition_group', 'trial_group', 'channel_group'])
        return case_raw_data.mean(level=['subject', 'condition_group', 'channel_group'])

    erp_collection = to_erp()
    stats_data = None
    default_plot_params = dict(plot_type=['direct', 'waveform'], y_title='Amplitude(uV)', err_style=None, color=['#34495e'], style='darkgrid', legend=False)
    return structure.Analyzed_data('ERPs', erp_collection, stats_data, default_plot_params)


structure.Extracted_epochs.ERPs = ERPs

def RMS(self, compare=False, comparison_params=comparison_params):

    def calc_rms(x):
        return np.sqrt(np.mean(x ** 2))

    @self.iter('average')
    def to_rms(case_raw_data):
        check_availability(case_raw_data, single_value_level=['condition_group', 'trial_group', 'channel_group'])
        erp = case_raw_data.mean(level=['subject', 'condition_group', 'channel', 'channel_group'])
        RMS_df = []
        for name, data in erp.groupby(level=['subject', 'condition_group', 'channel_group']):
            data = pd.DataFrame(data.apply(calc_rms)).T
            data.index = pd.MultiIndex.from_tuples([name], names=['subject', 'condition_group', 'channel_group'])
            RMS_df.append(data)

        RMS_df = pd.concat(RMS_df)
        return RMS_df

    rms_collection = to_rms()
    if compare:
        stats_data = [stats_compare(rms_batch, comparison_params, levels='time', between='condition_group', in_group='subject') for rms_batch in rms_collection]
    else:
        stats_data = None
    default_plot_params = dict(plot_type=['direct', 'waveform'], y_title='RMS', err_style='ci_band', color='Set1', style='darkgrid', win=(comparison_params['win']), sig_limit=0.05)
    return structure.Analyzed_data('RMS', rms_collection, stats_data, default_plot_params)


structure.Extracted_epochs.RMS = RMS