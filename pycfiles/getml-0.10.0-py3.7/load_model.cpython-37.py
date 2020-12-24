# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/models/load_model.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 9784 bytes
import getml.communication as comm
from getml import predictors
import json
from getml.data import Placeholder, _decode_placeholder, _decode_joined_tables
from .loss_functions import _decode_loss_function
from .multirel_model import MultirelModel
from .relboost_model import RelboostModel

def load_model(name):
    """Returns a handler for a model in the engine.

    The model has to be held in memory and thus be present in the
    current project. :func:`~getml.models.list_models` can be used to
    list all of them. In order to load a model from a different
    project, you have to switch projects first. See
    :func:`~getml.engine.set_project` and :mod:`~getml.models` for
    more details about the lifecycles of the models.

    Args:
        name (str): Name of a model in the current project.

    Raises:
        KeyError: If the model loaded from the engine is ill-formatted
            (should not be happen. Please report such a problem.)
        IOError: If the response of the engine did not contain a valid
            model.
        TypeError: If `name` is not of type str or its value does not
            correspond to the class name of a model in `getml.models`.

    Returns:
        Union[:class:`~getml.models.MultirelModel`, :class:`~getml.models.RelboostModel`]:
            Handler for the model called `name`.

    """
    if type(name) is not str:
        raise TypeError("'name' must be of type str")
    else:
        cmd_get_model = dict()
        cmd_get_model['type_'] = 'get_model'
        cmd_get_model['name_'] = name
        s_get_model = comm.send_and_receive_socket(cmd_get_model)
        msg_get_model = comm.recv_string(s_get_model)
        s_get_model.close()
        if msg_get_model != 'MultirelModel':
            if msg_get_model != 'RelboostModel':
                comm.engine_exception_handler(msg, 'Unknown model class: ' + msg)
        else:
            cmd_load_model = dict()
            if msg_get_model == 'MultirelModel':
                cmd_load_model['type_'] = 'MultirelModel.refresh'
            else:
                cmd_load_model['type_'] = 'RelboostModel.refresh'
        cmd_load_model['name_'] = name
        s_load_model = comm.send_and_receive_socket(cmd_load_model)
        msg_load_model = comm.recv_string(s_load_model)
        s_load_model.close()
        if msg_load_model[0] != '{':
            comm.engine_exception_handler(msg, 'Message to load model does not contain a proper JSON: ' + msg)
        else:
            json_obj = json.loads(msg_load_model)
            if len(json_obj['peripheral_']) != len(json_obj['peripheral_schema_']):
                ValueError('Mismatch in the information concerning the peripheral tables')
            population = _decode_placeholder(json_obj['population_schema_'])
            joined_tables = _decode_joined_tables(json_obj['placeholder_']['joined_tables_'])
            population.set_relations(join_keys_used=(json_obj['placeholder_']['join_keys_used_']),
              other_join_keys_used=(json_obj['placeholder_']['other_join_keys_used_']),
              time_stamps_used=(json_obj['placeholder_']['time_stamps_used_']),
              other_time_stamps_used=(json_obj['placeholder_']['other_time_stamps_used_']),
              upper_time_stamps_used=(json_obj['placeholder_']['upper_time_stamps_used_']),
              joined_tables=joined_tables)
            peripheral_placeholders = list()
            for pp in range(0, len(json_obj['peripheral_'])):
                pperipheral = Placeholder(name=(json_obj['peripheral_'][pp]),
                  categorical=(json_obj['peripheral_schema_'][pp]['categoricals_']),
                  numerical=(json_obj['peripheral_schema_'][pp]['numericals_']),
                  join_keys=(json_obj['peripheral_schema_'][pp]['join_keys_']),
                  time_stamps=(json_obj['peripheral_schema_'][pp]['time_stamps_']),
                  targets=(json_obj['peripheral_schema_'][pp]['targets_']))
                peripheral_placeholders.append(pperipheral)

            peripheral = peripheral_placeholders
            if json_obj['type_'] == 'MultirelModel':
                model = MultirelModel(name=name, population=population,
                  peripheral=peripheral)
            else:
                if json_obj['type_'] == 'RelboostModel':
                    model = RelboostModel(name=name, population=population,
                      peripheral=peripheral)
                else:
                    raise KeyError('Unknown model class in loaded model!')
    for kkey in json_obj['hyperparameters_']:
        if kkey not in ('feature_selector_', 'loss_function_', 'peripheral_', 'peripheral_schema_',
                        'placeholder_', 'population_schema_', 'predictor_'):
            model.__dict__[kkey[:len(kkey) - 1]] = json_obj['hyperparameters_'][kkey]

    if 'predictor_' in json_obj['hyperparameters_']:
        model.predictor = predictors._decode_predictor(json_obj['hyperparameters_']['predictor_'])
    if 'feature_selector_' in json_obj['hyperparameters_']:
        model.feature_selector = predictors._decode_predictor(json_obj['hyperparameters_']['feature_selector_'])
    model.loss_function = _decode_loss_function(json_obj['hyperparameters_']['loss_function_'])
    multithreaded = False
    if model.num_threads > 1:
        multithreaded = True
    if model.predictor is not None and not isinstance(model.predictor, predictors.XGBoostClassifier):
        if isinstance(model.predictor, predictors.XGBoostRegressor):
            if model.predictor.n_jobs > 1:
                multithreaded = True
        if model.feature_selector is not None and not isinstance(model.feature_selector, predictors.XGBoostClassifier):
            if isinstance(model.feature_selector, predictors.XGBoostRegressor):
                if model.feature_selector.n_jobs > 1:
                    multithreaded = True
        if multithreaded:
            model.seed = None
    return model