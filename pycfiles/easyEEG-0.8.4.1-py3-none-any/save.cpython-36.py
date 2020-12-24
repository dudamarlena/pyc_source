# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\py3\experiments\easyEEG_dist\easyEEG\io\save.py
# Compiled at: 2018-05-22 18:30:22
# Size of source mod 2**32: 2425 bytes
from ..default import *
import pickle

def save_epochs(epochs, filepath, append=False, all_in_one=False):
    if append:
        mode = 'a'
    else:
        mode = 'w'
    if not filepath.endswith('.h5'):
        print('Your file have been added ".h5" as the extension name.')
        filepath += '.h5'
    info_t = epochs.info.copy()
    del info_t['subjects']
    del info_t['timepoints']
    del info_t['conditions']
    del info_t['channels']
    del info_t['trials']
    with pd.HDFStore(filepath, mode) as (store):
        if all_in_one:
            store.put('all', epochs.all)
            store.get_storer('all').attrs['info'] = info_t
        else:
            store.put('supplementary', pd.DataFrame([0]))
            store.get_storer('supplementary').attrs['info'] = info_t
            for subj_id, subj_data in epochs.all.groupby(level=['subject']):
                subj_id = str(subj_id)
                print('saving', subj_id, '...')
                store.put(subj_id, subj_data)

    print('Done.')


def save_result(result, filepath):
    if not filepath.endswith('.pickle'):
        print('Your file have been added ".pickle" as the extension name.')
        filepath += '.pickle'
    with open(filepath, 'wb') as (f):
        pickle.dump(result.analysis_name, f)
        pickle.dump(result.data, f)
        pickle.dump(result.annotation, f)
        pickle.dump(result.supplement, f)
        pickle.dump(result.default_plot_params, f)
        if hasattr(result.data, 'name'):
            pickle.dump(result.data.name, f)
        else:
            pickle.dump('', f)
        if hasattr(result.annotation, 'name'):
            pickle.dump(result.annotation.name, f)
        else:
            pickle.dump('', f)
    print('Result saved.')