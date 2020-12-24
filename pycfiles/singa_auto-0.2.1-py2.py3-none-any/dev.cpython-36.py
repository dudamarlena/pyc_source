# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/model/dev.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 18596 bytes
import json, traceback, inspect, argparse, time
from datetime import datetime
from typing import Dict, Type, List, Any
from singa_auto.constants import ModelDependency, Budget
from singa_auto.advisor import ParamsType, Proposal, TrialResult, make_advisor
from singa_auto.predictor import get_ensemble_method, Query, Prediction
from singa_auto.param_store import FileParamStore, ParamStore
from singa_auto.redis import ParamCache, TrainCache, InferenceCache
from .model import BaseModel, BaseKnob, Params
from .utils import serialize_knob_config, deserialize_knob_config, parse_model_install_command, load_model_class

def tune_model(py_model_class: Type[BaseModel], train_dataset_path: str, val_dataset_path: str, test_dataset_path: str=None, budget: Budget=None, train_args: Dict[(str, any)]=None) -> (Dict[(str, Any)], float, Params):
    worker_id = 'local'
    start_time = time.time()
    _print_header('Checking model configuration...')
    knob_config = py_model_class.get_knob_config()
    _check_knob_config(knob_config)
    _print_header('Starting trials...')
    knobs_from_args = _maybe_read_knobs_from_args(knob_config)
    budget_from_args = _maybe_read_budget_from_args()
    budget = {**(budget or {}), **budget_from_args}
    inform_user(f"Using budget {budget}...")
    advisor = make_advisor(knob_config, budget)
    inform_user(f'Using advisor "{type(advisor).__name__}"...')
    param_store = FileParamStore()
    param_cache = ParamCache()
    train_cache = TrainCache()
    best_model_score = -1
    best_trial_no = 0
    best_model_test_score = None
    best_proposal = None
    best_store_params_id = None
    train_cache.add_worker(worker_id)
    trial_no = 0
    while True:
        trial_no += 1
        worker_ids = train_cache.get_workers()
        assert worker_id in worker_ids
        proposal = train_cache.get_proposal(worker_id)
        assert proposal is None
        proposal = advisor.propose(worker_id, trial_no)
        if proposal is None:
            print('No more proposals from advisor - to stop training')
            break
        proposal.knobs = {**(proposal.knobs), **knobs_from_args}
        train_cache.create_proposal(worker_id, proposal)
        proposal = train_cache.get_proposal(worker_id)
        assert proposal is not None
        _print_header(f"Trial #{trial_no}")
        print('Proposal from advisor:', proposal)
        model_inst = py_model_class(**proposal.knobs)
        shared_params = _pull_shared_params(proposal, param_cache)
        print('Training model...')
        (model_inst.train)(train_dataset_path, shared_params=shared_params, **train_args or {})
        result = _evaluate_model(model_inst, proposal, val_dataset_path)
        store_params_id = _save_model(model_inst, proposal, result, param_cache, param_store)
        if result.score is not None:
            if store_params_id is not None:
                if result.score > best_model_score:
                    inform_user('Best saved model so far! Beats previous best of score {}!'.format(best_model_score))
                    best_store_params_id = store_params_id
                    best_proposal = proposal
                    best_model_score = result.score
                    best_trial_no = trial_no
                    if test_dataset_path is not None:
                        print('Evaluating new best model on test dataset...')
                        best_model_test_score = model_inst.evaluate(test_dataset_path)
                        inform_user('Score on test dataset: {}'.format(best_model_test_score))
        print('Giving feedback to advisor...')
        train_cache.create_result(worker_id, result)
        train_cache.delete_proposal(worker_id)
        result = train_cache.take_result(worker_id)
        assert result is not None
        advisor.feedback(worker_id, result)
        model_inst.destroy()

    train_cache.delete_worker(worker_id)
    if best_proposal is not None:
        inform_user('Best trial #{} has knobs {} with score of {}'.format(best_trial_no, best_proposal.knobs, best_model_score))
        if best_model_test_score is not None:
            inform_user('...with test score of {}'.format(best_model_test_score))
    best_params = None
    if best_store_params_id is not None:
        best_params = param_store.load(best_store_params_id)
    print('Running model class teardown...')
    py_model_class.teardown()
    duration = time.time() - start_time
    print('Tuning took a total of {}s'.format(duration))
    return (
     best_proposal, best_model_test_score, best_params)


def make_predictions(queries: List[Any], task: str, py_model_class: Type[BaseModel], proposal: Proposal, params: Params) -> List[Any]:
    inference_cache = InferenceCache()
    worker_id = 'local'
    model_inst = None
    _print_header('Loading trained model...')
    model_inst = py_model_class(**proposal.knobs)
    model_inst.load_parameters(params)
    inference_cache.add_worker(worker_id)
    queries = [Query(x) for x in queries]
    worker_ids = inference_cache.get_workers()
    if not worker_id in worker_ids:
        raise AssertionError
    else:
        inference_cache.add_queries_for_worker(worker_id, queries)
        queries_at_worker = inference_cache.pop_queries_for_worker(worker_id, len(queries))
        assert len(queries_at_worker) == len(queries)
    _print_header('Making predictions with trained model...')
    predictions = model_inst.predict([x.query for x in queries_at_worker])
    predictions = [Prediction(x, query.id, worker_id) for x, query in zip(predictions, queries_at_worker)]
    inference_cache.add_predictions_for_worker(worker_id, predictions)
    predictions_at_predictor = []
    for query in queries:
        prediction = inference_cache.take_prediction_for_worker(worker_id, query.id)
        assert prediction is not None
        predictions_at_predictor.append(prediction)

    ensemble_method = get_ensemble_method(task)
    print(f"Ensemble method: {ensemble_method}")
    out_predictions = []
    for prediction in predictions_at_predictor:
        prediction = prediction.prediction
        _assert_jsonable(prediction, Exception('Each `prediction` should be JSON serializable'))
        out_prediction = ensemble_method([prediction])
        out_predictions.append(out_prediction)

    print('Predictions: {}'.format(out_predictions))
    return (
     out_predictions, model_inst)


def test_model_class(model_file_path: str, model_class: str, task: str, dependencies: Dict[(str, str)], train_dataset_path: str, val_dataset_path: str, test_dataset_path: str=None, budget: Budget=None, train_args: Dict[(str, any)]=None, queries: List[Any]=None) -> (List[Any], BaseModel):
    """
    Tests whether a model class is *more likely* to be correctly defined by *locally* simulating a full train-inference flow on your model
    on a given dataset. The model's methods will be called in an manner similar to that in Rafiki.

    This method assumes that your model's Python dependencies have already been installed.

    This method also reads knob values and budget options from CLI arguments.
    For example, you can pass e.g. ``--TIME_HOURS=0.01`` to configure the budget, or ``--learning_rate=0.01`` to fix a knob's value.

    :param model_file_path: Path to a single Python file that contains the definition for the model class
    :param model_class: The name of the model class inside the Python file. This class should implement :class:`singa_auto.model.BaseModel`
    :param task: Task type of model
    :param dependencies: Model's dependencies
    :param train_dataset_path: File path of the train dataset for training of the model
    :param val_dataset_path: File path of the validation dataset for evaluating trained models
    :param test_dataset_path: File path of the test dataset for testing the final best trained model, if provided
    :param budget: Budget for model training
    :param train_args: Additional arguments to pass to models during training, if any
    :param queries: List of queries for testing predictions with the trained model
    :returns: (<predictions of best trained model>, <best trained model>)

    """
    _print_header('Installing & checking model dependencies...')
    _check_dependencies(dependencies)
    _print_header('Checking loading of model & model definition...')
    with open(model_file_path, 'rb') as (f):
        model_file_bytes = f.read()
    py_model_class = load_model_class(model_file_bytes, model_class, temp_mod_name=model_class)
    _check_model_class(py_model_class)
    best_proposal, _, best_params = tune_model(py_model_class, train_dataset_path, val_dataset_path, test_dataset_path=test_dataset_path,
      budget=budget,
      train_args=train_args)
    model_inst = None
    predictions = None
    if best_proposal is not None:
        if best_params is not None:
            if queries is not None:
                predictions, model_inst = make_predictions(queries, task, py_model_class, best_proposal, best_params)
    py_model_class.teardown()
    inform_user('No errors encountered while testing model!')
    return (
     predictions, model_inst)


def warn_user(msg):
    print(f"\x1b[93mWARNING: {msg}\x1b[0m")


def inform_user(msg):
    print(f"\x1b[94m{msg}\x1b[0m")


def _pull_shared_params(proposal: Proposal, param_cache: ParamCache):
    if proposal.params_type == ParamsType.NONE:
        return
    else:
        print('Retrieving shared params from cache...')
        shared_params = param_cache.retrieve_params(proposal.params_type)
        return shared_params


def _evaluate_model(model_inst: BaseModel, proposal: Proposal, val_dataset_path: str) -> TrialResult:
    if not proposal.to_eval:
        return TrialResult(proposal)
    else:
        print('Evaluating model...')
        score = model_inst.evaluate(val_dataset_path)
        if not isinstance(score, float):
            raise Exception('`evaluate()` should return a float!')
        print('Score on validation dataset:', score)
        return TrialResult(proposal, score=score)


def _save_model(model_inst: BaseModel, proposal: Proposal, result: TrialResult, param_cache: ParamCache, param_store: ParamStore):
    if not proposal.to_cache_params:
        if not proposal.to_save_params:
            return
    else:
        print('Dumping model parameters...')
        params = model_inst.dump_parameters()
        if proposal.to_cache_params:
            print('Storing shared params in cache...')
            param_cache.store_params(params, score=(result.score), time=(datetime.now()))
        store_params_id = None
        if proposal.to_save_params:
            print('Saving shared params...')
            store_params_id = param_store.save(params)
    return store_params_id


def _maybe_read_knobs_from_args(knob_config):
    parser = argparse.ArgumentParser()
    for name, knob in knob_config.items():
        if knob.value_type in [int, float, str]:
            parser.add_argument(('--{}'.format(name)), type=(knob.value_type))
        else:
            if knob.value_type in [list, bool]:
                parser.add_argument(('--{}'.format(name)), type=str)

    args_namespace = vars(parser.parse_known_args()[0])
    knobs_from_args = {}
    for name, knob in knob_config.items():
        if name in args_namespace:
            if args_namespace[name] is not None:
                value = args_namespace[name]
                if knob.value_type in [list, bool]:
                    value = eval(value)
            knobs_from_args[name] = value
            inform_user('Setting knob "{}" to be fixed value of "{}"...'.format(name, value))

    return knobs_from_args


def _maybe_read_budget_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--GPU_COUNT', type=int, default=0)
    parser.add_argument('--TIME_HOURS', type=float, default=0.01)
    parser.add_argument('--MODEL_TRIAL_COUNT', type=int, default=(-1))
    budget_from_args = vars(parser.parse_known_args()[0])
    return budget_from_args


def _check_model_class(py_model_class):
    if not issubclass(py_model_class, BaseModel):
        raise Exception('Model should extend `singa_auto.model.BaseModel`')
    else:
        if inspect.isfunction(getattr(py_model_class, 'init', None)):
            warn_user("`init` has been deprecated - use `__init__` for your model's initialization logic instead")
        if inspect.isfunction(getattr(py_model_class, 'get_knob_config', None)):
            if not isinstance(py_model_class.__dict__.get('get_knob_config', None), staticmethod):
                warn_user('`get_knob_config` has been changed to a `@staticmethod`')


def _check_dependencies(dependencies):
    if not isinstance(dependencies, dict):
        raise Exception('`dependencies` should be a dict[str, str]')
    for dep, ver in dependencies.items():
        if dep == ModelDependency.KERAS:
            inform_user('Keras models can enable GPU usage with by adding a `tensorflow` dependency.')
        else:
            if dep in [ModelDependency.TORCH, ModelDependency.TORCHVISION]:
                pass
            else:
                if dep == ModelDependency.SCIKIT_LEARN:
                    pass
                else:
                    if dep == ModelDependency.TENSORFLOW:
                        warn_user('TensorFlow models must cater for GPU-sharing with `config.gpu_options.allow_growth = True` (ref: https://www.tensorflow.org/guide/using_gpu#allowing_gpu_memory_growth).')
                    elif dep == ModelDependency.SINGA:
                        pass

    install_command = parse_model_install_command(dependencies, enable_gpu=False)
    install_command_with_gpu = parse_model_install_command(dependencies, enable_gpu=True)
    inform_user(f"Install command (without GPU): `{install_command}`")
    inform_user(f"Install command (with GPU): `{install_command_with_gpu}`")


def _check_knob_config(knob_config):
    if not isinstance(knob_config, dict) or any([not isinstance(name, str) or not isinstance(knob, BaseKnob) for name, knob in knob_config.items()]):
        raise Exception('Static method `get_knob_config()` should return a dict[str, BaseKnob]')
    knob_config_bytes = serialize_knob_config(knob_config)
    knob_config = deserialize_knob_config(knob_config_bytes)


def _assert_jsonable--- This code section failed: ---

 L. 408         0  SETUP_EXCEPT         16  'to 16'

 L. 409         2  LOAD_GLOBAL              json
                4  LOAD_ATTR                dumps
                6  LOAD_FAST                'jsonable'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  POP_TOP          
               12  POP_BLOCK        
               14  JUMP_FORWARD         66  'to 66'
             16_0  COME_FROM_EXCEPT      0  '0'

 L. 410        16  DUP_TOP          
               18  LOAD_GLOBAL              Exception
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    64  'to 64'
               24  POP_TOP          
               26  STORE_FAST               'e'
               28  POP_TOP          
               30  SETUP_FINALLY        54  'to 54'

 L. 411        32  LOAD_GLOBAL              traceback
               34  LOAD_ATTR                print_stack
               36  CALL_FUNCTION_0       0  '0 positional arguments'
               38  POP_TOP          

 L. 412        40  LOAD_FAST                'exception'
               42  JUMP_IF_TRUE_OR_POP    46  'to 46'
               44  LOAD_FAST                'e'
             46_0  COME_FROM            42  '42'
               46  RAISE_VARARGS_1       1  'exception'
               48  POP_BLOCK        
               50  POP_EXCEPT       
               52  LOAD_CONST               None
             54_0  COME_FROM_FINALLY    30  '30'
               54  LOAD_CONST               None
               56  STORE_FAST               'e'
               58  DELETE_FAST              'e'
               60  END_FINALLY      
               62  JUMP_FORWARD         66  'to 66'
               64  END_FINALLY      
             66_0  COME_FROM            62  '62'
             66_1  COME_FROM            14  '14'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 46


def _check_model_inst(model_inst):

    def deprecated_func(desc):

        def throw_error(*args, **kwargs):
            raise AttributeError(desc)

        return throw_error

    class DeprecatedModelUtils:
        log = deprecated_func('`self.utils.log(...)` has been moved to `logger.log(...)`')
        log_metrics = deprecated_func('`self.utils.log_metrics(...)` has been moved to `logger.log(...)`')
        define_plot = deprecated_func('`self.utils.define_plot(...)` has been moved to `logger.define_plot(...)`')
        define_loss_plot = deprecated_func('`self.utils.define_loss_plot(...)` has been moved to `logger.define_loss_plot(...)`')
        log_loss_metric = deprecated_func('`self.utils.log_loss_metric(...)` has been moved to `logger.log_loss(...)`')
        load_dataset_of_image_files = deprecated_func('`self.utils.load_dataset_of_image_files(...)` has been moved to `dataset_utils.load_dataset_of_image_files(...)`')
        load_dataset_of_corpus = deprecated_func('`self.utils.load_dataset_of_corpus(...)` has been moved to `dataset_utils.load_dataset_of_corpus(...)`')
        resize_as_images = deprecated_func('`self.utils.resize_as_images(...)` has been moved to `dataset_utils.resize_as_images(...)`')
        download_dataset_from_uri = deprecated_func('`self.utils.download_dataset_from_uri(...)` has been moved to `dataset_utils.download_dataset_from_uri(...)`')

    model_inst.utils = DeprecatedModelUtils()


def _print_header(msg):
    print('-' * (len(msg) + 4))
    print('| {} |'.format(msg))
    print('-' * (len(msg) + 4))