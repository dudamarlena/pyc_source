# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/axon_conabio/datasets/tf_dataset.py
# Compiled at: 2018-12-10 18:39:09
from abc import ABCMeta
import os, json, tensorflow as tf
from .basedataset import Dataset
CONFIG_FIELDS = {'cross_validation': [
                      (
                       'folds', int, None),
                      (
                       'train_folds', int, None),
                      (
                       'test_folds', int, None),
                      (
                       'validation_folds', int, None)], 
   'partition': [
               (
                'train_size', float, 0.7),
               (
                'validation_size', float, 0.1),
               (
                'test_size', float, 0.2)]}

class ConfigError(Exception):
    pass


class TFDatasetConfig(object):

    def __init__(self, dictionary):
        self.dict = dictionary
        self._parse_config(dictionary)
        self._check_config()

    def __repr__(self):
        return repr(self.dict)

    def _check_config(self):
        if self.partition and self.cross_validation:
            msg = 'partition and cross_validation fields cannot be set'
            msg += ' simultaneously.'
            raise ConfigError(msg)

    def _parse_config(self, dictionary):
        for key in CONFIG_FIELDS:
            key_conf = CONFIG_FIELDS[key]
            if isinstance(key_conf, tuple):
                dtype, default = key_conf
                value = dictionary.get(key, default)
                if value is not None:
                    if not isinstance(value, dtype):
                        msg = '{key} configuration is not of the right type: '
                        msg += '{type}.'
                        msg = msg.format(key=key, type=dtype)
                        raise ConfigError(msg)
                setattr(self, key, value)
            elif isinstance(key_conf, list):
                if key in dictionary:
                    setattr(self, key, True)
                    subdict = dictionary[key]
                    for subkey, dtype, default in key_conf:
                        value = subdict.get(subkey, default)
                        if value is not None:
                            if not isinstance(value, dtype):
                                msg = '{key} configuration is not of the '
                                msg += 'right type: {type}.'
                                msg = msg.format(key=key, type=dtype)
                                raise ConfigError(msg)
                        setattr(self, subkey, value)

                else:
                    setattr(self, key, False)

        return

    @classmethod
    def from_path(cls, path, name='config'):
        config_file = os.path.join(path, name)
        json_exists = os.path.exists(config_file + '.json')
        if not json_exists:
            msg = 'No configuration file for TFDataset was found at {path}'
            msg = msg.format(path=path)
            raise IOError(msg)
        if json_exists:
            with open(config_file + '.json', 'r') as (jfile):
                config = json.load(jfile)
        return cls(config)


class TFDataset(Dataset):
    __metaclass__ = ABCMeta

    def __init__(self, path):
        self.path = path
        self.config = self._load_config()
        super(TFDataset, self).__init__()

    def _build_from_folds(self, fold_nums):
        n_folds = len(fold_nums)
        categories = set()
        for n in fold_nums:
            fold_path = os.path.join(self.path, ('fold_{}').format(n))
            tfrecords_files = [ os.path.splitext(tf_file)[0] for tf_file in os.listdir(fold_path) if 'tfrecords' in tf_file
                              ]
            categories.update(tfrecords_files)

        datasets = []
        for category in categories:
            files = [ ('{}/fold_{}/{}.tfrecords').format(self.path, n, category) for n in fold_nums
                    ]
            category_dataset = tf.data.Dataset.from_tensor_slices(files).interleave(lambda filename: tf.data.TFRecordDataset(filename), cycle_length=n_folds, block_length=1)
            datasets.append(category_dataset)

        def flatten(*samples):
            base = tf.data.Dataset.from_tensors(samples[0])
            for k in range(1, len(samples)):
                base = base.concatenate(tf.data.Dataset.from_tensors(samples[k]))

            return base

        merged = tf.data.Dataset.zip(tuple(datasets)).flat_map(flatten)
        return merged

    def build_data(self):
        if self.config.cross_validation:
            data = self._build_from_folds([0, 1, 2, 3, 4])
        return data

    def _load_config(self, name='config'):
        config = TFDatasetConfig.from_path(self.path, name=name)
        return config