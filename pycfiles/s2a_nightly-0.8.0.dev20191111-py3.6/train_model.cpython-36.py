# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/trainer/train_model.py
# Compiled at: 2019-09-18 06:01:42
# Size of source mod 2**32: 6435 bytes
import copy, os, tensorflow as tf
from seq2annotation import utils
from seq2annotation.utils import class_from_module_path
from tokenizer_tools.hooks import TensorObserveHook
tf.logging.set_verbosity(tf.logging.INFO)
observer_hook = TensorObserveHook({'fake_golden':'fake_golden:0', 
 'fake_prediction':'fake_prediction:0'}, {'predictions_id':'predictions:0', 
 'predict_str':'predict_Lookup:0', 
 'labels_id':'labels:0', 
 'labels_str':'IteratorGetNext:2'}, {'word_str':lambda x: x.decode(), 
 'predict_str':lambda x: x.decode(), 
 'labels_str':lambda x: x.decode()})

def train_model(train_inpf, eval_inpf, config, model_fn, model_name):
    estimator_params = copy.deepcopy(config)
    indices = [idx for idx, tag in enumerate(config['tags_data']) if tag.strip() != 'O']
    num_tags = len(indices) + 1
    estimator_params['_indices'] = indices
    estimator_params['_num_tags'] = num_tags
    cfg = tf.estimator.RunConfig(save_checkpoints_secs=(config['save_checkpoints_secs']))
    model_specific_name = '{model_name}-{batch_size}-{learning_rate}-{max_steps}-{max_steps_without_increase}'.format(model_name=model_name,
      batch_size=(config['batch_size']),
      learning_rate=(config['learning_rate']),
      max_steps=(config['max_steps']),
      max_steps_without_increase=(config['max_steps_without_increase']))
    instance_model_dir = os.path.join(config['model_dir'], model_specific_name)
    if config['use_tpu']:
        tpu_cluster_resolver = tf.contrib.cluster_resolver.TPUClusterResolver(tpu=(config['tpu_name']),
          zone=(config['tpu_zone']),
          project=(config['gcp_project']))
        run_config = tf.contrib.tpu.RunConfig(cluster=tpu_cluster_resolver,
          model_dir=instance_model_dir,
          session_config=tf.ConfigProto(allow_soft_placement=True,
          log_device_placement=True),
          tpu_config=(tf.contrib.tpu.TPUConfig()))
        tpu_estimator_params = copy.deepcopy(estimator_params)
        del tpu_estimator_params['batch_size']
        estimator = tf.contrib.tpu.TPUEstimator(model_fn=model_fn,
          params=tpu_estimator_params,
          config=run_config,
          use_tpu=True,
          train_batch_size=(estimator_params['batch_size']),
          eval_batch_size=(estimator_params['batch_size']),
          predict_batch_size=(estimator_params['batch_size']))
    else:
        estimator = tf.estimator.Estimator(model_fn, instance_model_dir, cfg, estimator_params)
    utils.create_dir_if_needed(estimator.eval_dir())
    train_hook = []
    for i in config.get('train_hook', []):
        class_ = class_from_module_path(i['class'])
        params = i['params']
        if i.get('inject_whole_config', False):
            params['config'] = config
        train_hook.append(class_(**params))

    eval_hook = []
    for i in config.get('eval_hook', []):
        class_ = class_from_module_path(i['class'])
        params = i['params']
        if i.get('inject_whole_config', False):
            params['config'] = config
        eval_hook.append(class_(**params))

    if eval_inpf:
        train_spec = tf.estimator.TrainSpec(input_fn=train_inpf,
          hooks=train_hook,
          max_steps=(config['max_steps']))
        eval_spec = tf.estimator.EvalSpec(input_fn=eval_inpf,
          throttle_secs=(config['throttle_secs']),
          hooks=eval_hook)
        evaluate_result, export_results = tf.estimator.train_and_evaluate(estimator, train_spec, eval_spec)
    else:
        estimator.train(input_fn=train_inpf,
          hooks=train_hook,
          max_steps=(config['max_steps']))
        evaluate_result, export_results = {}, None
    feature_spec = {'words':tf.placeholder(tf.string, [None, None]), 
     'words_len':tf.placeholder(tf.int32, [None])}
    if config.get('forced_saved_model_dir'):
        instance_saved_dir = config.get('forced_saved_model_dir')
    else:
        instance_saved_dir = os.path.join(config['saved_model_dir'], model_specific_name)
    utils.create_dir_if_needed(instance_saved_dir)
    serving_input_receiver_fn = tf.estimator.export.build_raw_serving_input_receiver_fn(feature_spec)
    raw_final_saved_model = estimator.export_saved_model(instance_saved_dir, serving_input_receiver_fn)
    final_saved_model = raw_final_saved_model.decode('utf-8')
    return (
     evaluate_result, export_results, final_saved_model)