# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\IPython Notebooks\experiment\lazyEEG\io\save.py
# Compiled at: 2017-12-17 17:15:35
# Size of source mod 2**32: 942 bytes
from ..default import *

def save_epochs(epochs, filepath, append=False):
    if append:
        mode = 'a'
    else:
        mode = 'w'
    if not filepath.endswith('.h5'):
        print('Your file have been added ".h5" as the extension name.')
        filepath += '.h5'
    t = epochs.info['trials']
    del epochs.info['trials']
    with pd.HDFStore(filepath, mode) as (store):
        for subj_id, subj_data in epochs.all.groupby(level=['subject']):
            subj_id = str(subj_id)
            print('saving', subj_id, '...')
            store[subj_id] = subj_data
            store.get_storer(subj_id).attrs['info'] = epochs.info

    epochs.info['trials'] = t
    print('Done.')