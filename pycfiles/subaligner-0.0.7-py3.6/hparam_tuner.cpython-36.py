# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/subaligner/hparam_tuner.py
# Compiled at: 2020-05-06 18:46:53
# Size of source mod 2**32: 4039 bytes
import hyperopt, numpy as np
from hyperopt import hp
from hyperopt.pyll.base import scope
from .trainer import Trainer
from .embedder import FeatureEmbedder
from .hyperparameters import Hyperparameters

class HyperParameterTuner(object):
    __doc__ = 'Hyper parameter tuning using the Bayesian Optimizer'
    SEARCH_SPACE = {'learning_rate':hp.loguniform('learning_rate', np.log(1e-05), np.log(0.1)), 
     'front_hidden_size':hp.choice('front_hidden_size', [[16], [32], [64]]), 
     'back_hidden_size':hp.choice('back_hidden_size', [[16, 8], [32, 16]]), 
     'batch_size':scope.int(hp.qloguniform('batch_size', np.log(8), np.log(4096), 1)), 
     'optimizer':hp.choice('optimizer', ['adam', 'sgd', 'rms', 'adagrad']), 
     'dropout':hp.loguniform('dropout', np.log(0.1), np.log(0.3)), 
     'validation_split':hp.loguniform('validation_split', np.log(0.2), np.log(0.4))}

    def __init__(self, av_file_paths, subtitle_file_paths, training_dump_dir, num_of_trials=5, tuning_epochs=5):
        """Hyper parameter tuner initialiser

        Arguments:
            av_file_paths {list} -- A list of paths to the input audio/video files.
            subtitle_file_paths {list} -- A list of paths to the subtitle files.
            training_dump_dir {string} --  The directory of the training data dump file.

        Keyword Arguments:
            num_of_trials {int} -- The number of trials for tuning (default: {5}).
            tuning_epochs {int} -- The number of training epochs for each trial (default: {5}).
        """
        self._HyperParameterTuner__trainer = Trainer(FeatureEmbedder())
        self._HyperParameterTuner__av_file_paths = av_file_paths
        self._HyperParameterTuner__subtitle_file_paths = subtitle_file_paths
        self._HyperParameterTuner__training_dump_dir = training_dump_dir
        self._HyperParameterTuner__hyperparameters = Hyperparameters()
        self._HyperParameterTuner__num_of_trials = num_of_trials
        self._HyperParameterTuner__tuning_epochs = tuning_epochs
        self._HyperParameterTuner__original_epochs = self._HyperParameterTuner__hyperparameters.epochs

    @property
    def hyperparameters(self):
        self._HyperParameterTuner__hyperparameters.epochs = self._HyperParameterTuner__original_epochs
        return self._HyperParameterTuner__hyperparameters.clone()

    def tune_hyperparameters(self):
        """Tune the hyper parameters"""
        trials = hyperopt.Trials()
        minimised = hyperopt.fmin(fn=(self._HyperParameterTuner__get_val_loss), space=(self.SEARCH_SPACE),
          trials=trials,
          algo=(hyperopt.tpe.suggest),
          max_evals=(self._HyperParameterTuner__num_of_trials),
          show_progressbar=False)
        turned_hps = hyperopt.space_eval(self.SEARCH_SPACE, minimised)
        for key, value in turned_hps.items():
            if key == 'front_hidden_size':
                self._HyperParameterTuner__hyperparameters.front_hidden_size = list(value)
            else:
                if key == 'back_hidden_size':
                    self._HyperParameterTuner__hyperparameters.back_hidden_size = list(value)
                else:
                    setattr(self._HyperParameterTuner__hyperparameters, key, value)

    def __get_val_loss(self, params):
        for key, value in params.items():
            if key == 'front_hidden_size':
                self._HyperParameterTuner__hyperparameters.front_hidden_size = list(value)
            else:
                if key == 'back_hidden_size':
                    self._HyperParameterTuner__hyperparameters.back_hidden_size = list(value)
                else:
                    setattr(self._HyperParameterTuner__hyperparameters, key, value)

        self._HyperParameterTuner__hyperparameters.epochs = self._HyperParameterTuner__tuning_epochs
        val_loss, _ = self._HyperParameterTuner__trainer.pre_train(self._HyperParameterTuner__av_file_paths, self._HyperParameterTuner__subtitle_file_paths, self._HyperParameterTuner__training_dump_dir, self._HyperParameterTuner__hyperparameters)
        if not val_loss:
            raise ValueError('Cannot get training loss during hyper parameter tuning')
        return {'loss':sum(val_loss) / len(val_loss),  'status':hyperopt.STATUS_OK}