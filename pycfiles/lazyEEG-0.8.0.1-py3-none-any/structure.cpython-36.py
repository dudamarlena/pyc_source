# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Coding\py\IPython Notebooks\experiment\lazyEEG\structure.py
# Compiled at: 2017-12-20 10:14:24
# Size of source mod 2**32: 7484 bytes
from .default import *
from . import io
from . import group

class Epochs:

    def __init__(self, epochs_data, montage_path='standard-10-5-cap385', info=dict()):
        if type(epochs_data) != pd.DataFrame:
            raise Exception('Unsupported input!')
        else:
            if 'sample_rate' not in info:
                info['sample_rate'] = 1000 // (epochs_data.columns[1] - epochs_data.columns[0])
            info['subjects'] = {'all': list(epochs_data.index.get_level_values('subject').unique())}
            info['timepoints'] = {'all': list(epochs_data.columns)}
            info['conditions'] = dict()
            info['conditions']['all'] = list(epochs_data.index.get_level_values('condition').unique())
            for subj_id, subj_data in epochs_data.groupby(level=['subject']):
                info['conditions'][str(subj_id)] = sorted(list(subj_data.index.get_level_values('condition').unique()))

            info['channels'] = dict()
            info['channels']['all'] = list(epochs_data.index.get_level_values('channel').unique())
            for subj_id, subj_data in epochs_data.groupby(level=['subject']):
                info['channels'][str(subj_id)] = sorted(list(subj_data.index.get_level_values('channel').unique()))

            info['trials'] = dict()
            info['trials']['all'] = list(epochs_data.index.get_level_values('trial').unique())
            for subj_id, subj_data in epochs_data.groupby(level=['subject']):
                info['trials'][str(subj_id)] = sorted(list(subj_data.index.get_level_values('trial').unique()))

            if 'channel&id' not in info:
                info['channel&id'] = dict()
                for ind, i in enumerate(info['channels']['all']):
                    info['channel&id'][str(i)] = ind
                    info['channel&id'][ind] = str(i)

            if 'xy_locs' not in info:
                info['xy_locs'] = io.load_topolocs(montage_path, info['channels']['all'])
        epochs_data_averaged = epochs_data.mean(level=(list(np.setdiff1d(epochs_data.index.names, ['trial']))))
        epochs_data_averaged.index = pd.MultiIndex.from_tuples([(subject, condition, info['conditions']['all'].index(condition), channel) for channel, condition, subject in epochs_data_averaged.index], names=[
         'subject', 'condition', 'trial', 'channel'])
        epochs_data_averaged.sort_index(inplace=True)
        self.all = epochs_data
        self.average = epochs_data_averaged
        self.info = info

    def extract(self, collection_script):
        collection_frame = group.parsing(collection_script, self)
        return Extracted_epochs(self, collection_frame)

    def save(self, filepath, append=False):
        io.save_epochs(self, filepath, append=False)


class Extracted_epochs:

    def __init__(self, epochs, collection_frame):
        self.data = epochs
        self.frame = collection_frame
        self.info = epochs.info

    def iter_batchs():
        for batch_name, batch_frame in self.frame:
            yield (batch_name, batch_frame)

    def iter_cases(batch_name, batch_frame):
        for case_frame in batch_frame:
            yield case_frame

    def get_batch_names(self, batch_id='all'):
        batch_names = [batch_name for batch_name, batch_frame in self.frame]
        if batch_id == 'all':
            return batch_names
        if type(batch_id) is list:
            return [batch_names[idx] for idx in batch_id]
        if type(batch_id) is int:
            return batch_names[batch_id]

    def get_case_name(self, batch_id=0, case_id=0):
        batch_name, batch_frame = self.frame[batch_id]
        case_frame = batch_frame[case_id]
        case_frame_dict = dict()
        for sub_case, sub_case_key in zip(case_frame, ['subject', 'condition', 'trial', 'channel', 'timepoint']):
            case_frame_dict[sub_case_key + '_name'] = sub_case[0]

        return case_frame_dict

    def get_dataframe(self, batch_id=0, case_id=0, average=True, to_print=False):
        batch_name, batch_frame = self.frame[batch_id]
        case_frame = batch_frame[case_id]
        if average:
            data_to_extracted = self.data.average
        else:
            data_to_extracted = self.data.all
        result = group.generate_case_data(case_frame, data_to_extracted)
        if to_print:
            print(f"batch_name: {batch_name}")
            print(f"case_name: {result.name}")
        return result

    def get_array(self, batch_id=0, case_id=0, average=True, to_print=False):
        df = self.dataframe(batch_id, case_id, average, to_print)
        return df.as_matrix()

    def get_index(self, batch_id=0, case_id=0, average=True, to_print=False):
        df = self.dataframe(batch_id, case_id, average, to_print)
        return (df.index, df.columns)

    def get_info(self, key):
        return self.info[key]

    def iter(self, mode='average'):

        def decorator(func):

            def wrapper(*args, **kw):
                data_to_extracted = getattr(self.data, mode)
                analyzed_collection = []
                for batch_name, batch_frame in self.frame:
                    analyzed_batch = []
                    all_case_names = []
                    for case_frame in batch_frame:
                        case_data = group.generate_case_data(case_frame, data_to_extracted)
                        all_case_names.append(case_data.name)
                        analyzed_batch.append(func(case_data, *args, **kw))

                    analyzed_batch = pd.concat(analyzed_batch)
                    all_case_names = np.array(all_case_names)
                    name = ''
                    for ind, i in enumerate(['subjects', 'conditions', 'trials', 'channels', 'timepoints']):
                        values = list(np.unique(all_case_names[:, ind]))
                        if values != ['All'] and set(values) != set(self.info[i]['all']):
                            name += ','.join(values) + ' '

                    analyzed_batch.name = name
                    analyzed_collection.append(analyzed_batch)

                return analyzed_collection

            return wrapper

        return decorator


class Analyzed_data:

    def __init__(self, analysis_name, data, annotation=None, default_plot_params=dict()):
        self.analysis_name = analysis_name
        self.data = data
        if annotation:
            self.annotation = annotation
        else:
            self.annotation = [
             None] * len(data)
        self.default_plot_params = default_plot_params

    def save(self, filepath, append=False):
        """Analyzed_data-like data"""
        pass