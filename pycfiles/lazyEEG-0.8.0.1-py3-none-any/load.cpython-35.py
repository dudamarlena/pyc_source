# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Coding\py\IPython Notebooks\experiment\chunking\LazyEEG\io\load.py
# Compiled at: 2017-04-14 17:44:00
# Size of source mod 2**32: 3739 bytes
from ..default import *
import pickle
from scipy.io import loadmat

def load_pickle(filename, path='data'):
    if path != '':
        path += '/'
    with open(path + filename, 'rb') as (f):
        return pickle.load(f)


def load_mat(subIDs, paths, raw_epoch_time, epoch_time, baseline_time, markers=[]):
    epoches = []
    for subjID, path in zip(subjIDs, paths):
        mat_file = loadmat(path)['EEG'][0][0]
        eeg_data = mat_file[15]
        sr = mat_file[11][0][0]
        trial_count = mat_file[15].shape[2]
        events = [i[4][0] for i in mat_file[25][0]]
        if markers == []:
            markers = {m:m for m in set(events)}
        channels = dict()
        for ind, i in enumerate(mat_file[21][0]):
            channels[i[0][0]] = ind
            channels[ind] = i[0][0]

        channel_count = mat_file[15].shape[0]
        channel_names = [i[0][0] for i in mat_file[21][0]]
        span = pd.timedelta_range(start='%d ms' % epoch_time[0], end='%d ms' % (epoch_time[1] - 1), freq='%d ms' % (1000 / sr))
        epoch_start = (epoch_time[0] - raw_epoch_time[0]) * sr // 1000
        epoch_end = (epoch_time[1] - raw_epoch_time[1]) * sr // 1000
        baseline_start = (baseline_time[0] - epoch_time[0]) * sr // 1000
        baseline_end = (baseline_time[1] - epoch_time[1]) * sr // 1000
        baseline_end_new = -baseline_time[0] * sr // 1000
        count = 0
        epoches_each_subj = []
        indexs_each_subj = []
        for T in range(trial_count):
            reject = False
            epoches_each_trial = []
            indexs_each_trial = []
            for C in range(channel_count):
                eeg = eeg_data[C, epoch_start:epoch_end, T]
                eeg -= eeg[baseline_start:baseline_end].mean()
                if min(eeg) > -60 and max(eeg) < 60 and max(eeg[:baseline_end_new]) - min(eeg[:baseline_end_new]) < 60:
                    epoches_each_trial.append(np.array(eeg))
                    indexs_each_trial.append([subID, markers[events[T]], T, channels[C]])
                else:
                    reject = True

            if not reject:
                epoches_each_subj += epoches_each_trial
                indexs_each_subj += indexs_each_trial
                count += 1

        index = pd.MultiIndex.from_tuples(indexs_each_subj, names=['subject', 'condition', 'trial', 'channel'])
        epoches.append(pd.DataFrame(epoches_each_subj, index=index))
        print(subjID, ': ', round(count / trial_count, 2), ' in ', trial_count)

    epoches = pd.concat(epoches)
    epoches.columns = pd.MultiIndex.from_tuples([('data', ts) for ts in span], names=['', 'time'])
    epoches.sort_index(inplace=True)
    return (
     epoches, {'sample rate': sr, 'channel name': channel_names, 'channels': channels})