# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\bca4abm\processors\abm\abm_results.py
# Compiled at: 2020-02-14 01:16:04
# Size of source mod 2**32: 1945 bytes
import logging, os, pandas as pd
from activitysim.core import inject
from activitysim.core import pipeline
logger = logging.getLogger(__name__)

@inject.step()
def finalize_abm_results(coc_results, summary_results, settings):
    data_dict = inject.get_injectable('data_dictionary')
    coc_silos = pd.DataFrame()
    if coc_results.index.names != [None]:
        coc_column_names = coc_results.index.names
        assigned_column_names = coc_results.columns
        df = coc_results.to_frame().reset_index(drop=False)
        for coc in coc_column_names:
            coc_silos[coc] = df[(df[coc] != 0)][assigned_column_names].sum()

        coc_silos['any_coc'] = df[df[coc_column_names].any(axis=1)][assigned_column_names].sum()
        coc_silos.sort_index(inplace=True)
        coc_silos.index.name = 'Target'
        coc_silos.reset_index(inplace=True)
        coc_silos['Description'] = coc_silos['Target'].map(data_dict).fillna('')
    pipeline.replace_table('coc_silos', coc_silos)
    summary_results_t = summary_results.to_frame().T
    summary_results_t.sort_index(inplace=True)
    summary_results_t.reset_index(inplace=True)
    summary_results_t.columns = ['Target', 'Value']
    summary_results_t['Description'] = summary_results_t.Target.map(data_dict).fillna('')
    pipeline.replace_table('summary_results', summary_results_t)