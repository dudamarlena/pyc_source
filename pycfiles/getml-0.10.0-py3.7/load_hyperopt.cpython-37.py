# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/hyperopt/load_hyperopt.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 10728 bytes
import json
import getml.communication as comm
import getml.models as models
from .hyperopt import RandomSearch, LatinHypercubeSearch, GaussianHyperparameterSearch

def _decode_hyperopt(rawStr):
    """A custom decoder function for
    :class:`~getml.hyperopt.RandomSearch`,
    :class:`~getml.hyperopt.LatinHypercubeSearch`, and
    :class:`~getml.hyperopt.GaussianHyperparameterSearch`.

    Args:
        rawStr (str): string containing a valid JSON message.

    Raises:
        KeyError: If not all required fields are present in `rawStr`
            to reconstruct a hyperparameter optimization search.
        ValueError: If not all keys in `rawStr` have a trailing
            underscore.
        TypeError: If `rawStr` is not of type :py:class:`dict`.

    Returns: 
        Union[:class:`~getml.hyperopt.RandomSearch`,:class:`~getml.hyperopt.LatinHypercubeSearch`,:class:`~getml.hyperopt.GaussianHyperparameterSearch`]
    """
    if type(rawStr) is not str:
        raise TypeError('_decode_hyperopt is expecting a str containing a valid JSON as input')
    else:
        rawDict = json.loads(rawStr)
        requiredFields = {
         'name_', 'param_space_', 'session_name_',
         'n_iter_', 'ratio_iter_',
         'optimization_algorithm_',
         'optimization_burn_in_algorithm_',
         'optimization_burn_ins_',
         'seed_',
         'surrogate_burn_in_algorithm_',
         'gaussian_kernel_',
         'gaussian_optimization_algorithm_',
         'gaussian_optimization_burn_in_algorithm_',
         'gaussian_optimization_burn_ins_'}
        if set(rawDict.keys()).intersection(requiredFields) != requiredFields:
            raise KeyError('Not enough information contained in the response to reconstruct the hyperparameter optimization: ' + str(rawDict.keys()))
        decodingDict = dict()
        for kkey in rawDict:
            if kkey[(len(kkey) - 1)] != '_':
                raise ValueError('All keys in the JSON must have a trailing underscore.')
            elif kkey == 'name_':
                decodingDict['model'] = models.load_model(rawDict[kkey])
            elif kkey == 'param_space_':
                param_space = dict()
                for ddimension in rawDict[kkey]:
                    param_space[ddimension[:len(ddimension) - 1]] = rawDict[kkey][ddimension]

                decodingDict['param_space'] = param_space
            else:
                if kkey in ('peripheral_names_', 'population_training_name_', 'population_validation_name_'):
                    continue
                decodingDict[kkey[:len(kkey) - 1]] = rawDict[kkey]

        if decodingDict['ratio_iter'] == 1 and decodingDict['surrogate_burn_in_algorithm'] == 'latinHypercube':
            h = LatinHypercubeSearch(model=(decodingDict['model']), param_space=(decodingDict['param_space']),
              seed=(decodingDict['seed']),
              session_name=(decodingDict['session_name']),
              n_iter=(decodingDict['n_iter']))
        else:
            if decodingDict['ratio_iter'] == 1 and decodingDict['surrogate_burn_in_algorithm'] == 'random':
                h = RandomSearch(model=(decodingDict['model']), param_space=(decodingDict['param_space']),
                  seed=(decodingDict['seed']),
                  session_name=(decodingDict['session_name']),
                  n_iter=(decodingDict['n_iter']))
            else:
                h = GaussianHyperparameterSearch(model=(decodingDict['model']), param_space=(decodingDict['param_space']),
                  session_name=(decodingDict['session_name']),
                  ratio_iter=(decodingDict['ratio_iter']),
                  n_iter=(decodingDict['n_iter']),
                  optimization_algorithm=(decodingDict['optimization_algorithm']),
                  optimization_burn_in_algorithm=(decodingDict['optimization_burn_in_algorithm']),
                  optimization_burn_ins=(decodingDict['optimization_burn_ins']),
                  seed=(decodingDict['seed']),
                  surrogate_burn_in_algorithm=(decodingDict['surrogate_burn_in_algorithm']),
                  gaussian_kernel=(decodingDict['gaussian_kernel']),
                  gaussian_optimization_algorithm=(decodingDict['gaussian_optimization_algorithm']),
                  gaussian_optimization_burn_in_algorithm=(decodingDict['gaussian_optimization_burn_in_algorithm']),
                  gaussian_optimization_burn_ins=(decodingDict['gaussian_optimization_burn_ins']))
    if 'score' in decodingDict:
        h.score = decodingDict['score']
    return h


def load_hyperopt(session_name):
    """Loads a hyperparameter optimization run into the Python API.

    Args:
        session_name (string): Unique identifier of a particular
            hyperparameter optimization run.

    Returns:
        Union[:class:`~getml.hyperopt.RandomSearch`, :class:`~getml.hyperopt.LatinHypercubeSearch`, :class:`~getml.hyperopt.GaussianHyperparameterSearch`]

    Raises:
        IOError: If the messages received from the engine is not a
            valid JSON.
        TypeError: if `session_name` is not a string.
        ValueError: if `session_name` is an empty string.

    """
    if type(session_name) is not string:
        raise TypeError('Only strings are allowed as session_name!')
    elif session_name == '':
        raise ValueError('The session_name must not be empty!')
    else:
        print('Not supported yet!')
        return
        h = _decode_hyperopt(msg)
        multithreaded = False
        if h.model.num_threads > 1:
            multithreaded = True
        if h.model.predictor is not None:
            if isinstance(h.model.predictor, predictors.XGBoostClassifier) or isinstance(h.model.predictor, predictors.XGBoostRegressor):
                if h.model.predictor.n_jobs > 1:
                    multithreaded = True
        if not h.model.feature_selector is not None or isinstance(h.model.feature_selector, predictors.XGBoostClassifier) or isinstance(h.model.feature_selector, predictors.XGBoostRegressor):
            if h.model.feature_selector.n_jobs > 1:
                multithreaded = True
    if multithreaded:
        h.model.seed = None