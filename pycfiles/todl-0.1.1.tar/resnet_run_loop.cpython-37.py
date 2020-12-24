# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/r1/resnet/resnet_run_loop.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 35377 bytes
"""Contains utility and supporting functions for ResNet.

  This module contains ResNet code which does not directly build layers. This
includes dataset management, hyperparameter and optimizer code, and argument
parsing. Code for defining the ResNet layers can be found in resnet_model.py.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools, math, multiprocessing, os
from absl import flags
from absl import logging
import tensorflow as tf
from official.r1.resnet import imagenet_preprocessing
from official.r1.resnet import resnet_model
from official.r1.utils import export
import official.utils.flags as flags_core
from official.utils.logs import hooks_helper
from official.utils.logs import logger
from official.utils.misc import distribution_utils
from official.utils.misc import model_helpers

def process_record_dataset(dataset, is_training, batch_size, shuffle_buffer, parse_record_fn, num_epochs=1, dtype=tf.float32, datasets_num_private_threads=None, drop_remainder=False, tf_data_experimental_slack=False):
    """Given a Dataset with raw records, return an iterator over the records.

  Args:
    dataset: A Dataset representing raw records
    is_training: A boolean denoting whether the input is for training.
    batch_size: The number of samples per batch.
    shuffle_buffer: The buffer size to use when shuffling records. A larger
      value results in better randomness, but smaller values reduce startup
      time and use less memory.
    parse_record_fn: A function that takes a raw record and returns the
      corresponding (image, label) pair.
    num_epochs: The number of epochs to repeat the dataset.
    dtype: Data type to use for images/features.
    datasets_num_private_threads: Number of threads for a private
      threadpool created for all datasets computation.
    drop_remainder: A boolean indicates whether to drop the remainder of the
      batches. If True, the batch dimension will be static.
    tf_data_experimental_slack: Whether to enable tf.data's
      `experimental_slack` option.

  Returns:
    Dataset of (image, label) pairs ready for iteration.
  """
    if datasets_num_private_threads:
        options = tf.data.Options()
        options.experimental_threading.private_threadpool_size = datasets_num_private_threads
        dataset = dataset.with_options(options)
        logging.info('datasets_num_private_threads: %s', datasets_num_private_threads)
    options = tf.data.Options()
    options.experimental_threading.max_intra_op_parallelism = 1
    dataset = dataset.with_options(options)
    dataset = dataset.prefetch(buffer_size=batch_size)
    if is_training:
        dataset = dataset.shuffle(buffer_size=shuffle_buffer)
    dataset = dataset.repeat(num_epochs)
    dataset = dataset.map((lambda value: parse_record_fn(value, is_training, dtype)),
      num_parallel_calls=(tf.data.experimental.AUTOTUNE))
    dataset = dataset.batch(batch_size, drop_remainder=drop_remainder)
    dataset = dataset.prefetch(buffer_size=(tf.data.experimental.AUTOTUNE))
    if tf_data_experimental_slack:
        options = tf.data.Options()
        options.experimental_slack = True
        dataset = dataset.with_options(options)
    return dataset


def get_synth_input_fn(height, width, num_channels, num_classes, dtype=tf.float32):
    """Returns an input function that returns a dataset with random data.

  This input_fn returns a data set that iterates over a set of random data and
  bypasses all preprocessing, e.g. jpeg decode and copy. The host to device
  copy is still included. This used to find the upper throughput bound when
  tunning the full input pipeline.

  Args:
    height: Integer height that will be used to create a fake image tensor.
    width: Integer width that will be used to create a fake image tensor.
    num_channels: Integer depth that will be used to create a fake image tensor.
    num_classes: Number of classes that should be represented in the fake labels
      tensor
    dtype: Data type for features/images.

  Returns:
    An input_fn that can be used in place of a real one to return a dataset
    that can be used for iteration.
  """

    def input_fn(is_training, data_dir, batch_size, *args, **kwargs):
        inputs = tf.random.truncated_normal(([
         batch_size] + [height, width, num_channels]),
          dtype=dtype,
          mean=127,
          stddev=60,
          name='synthetic_inputs')
        labels = tf.random.uniform([
         batch_size],
          minval=0,
          maxval=(num_classes - 1),
          dtype=(tf.int32),
          name='synthetic_labels')
        data = tf.data.Dataset.from_tensors((inputs, labels)).repeat()
        data = data.prefetch(buffer_size=(tf.data.experimental.AUTOTUNE))
        return data

    return input_fn


def image_bytes_serving_input_fn(image_shape, dtype=tf.float32):
    """Serving input fn for raw jpeg images."""

    def _preprocess_image(image_bytes):
        bbox = tf.constant([0.0, 0.0, 1.0, 1.0], dtype=dtype, shape=[1, 1, 4])
        height, width, num_channels = image_shape
        image = imagenet_preprocessing.preprocess_image(image_bytes,
          bbox, height, width, num_channels, is_training=False)
        return image

    image_bytes_list = tf.compat.v1.placeholder(shape=[
     None],
      dtype=(tf.string),
      name='input_tensor')
    images = tf.map_fn(_preprocess_image,
      image_bytes_list, back_prop=False, dtype=dtype)
    return tf.estimator.export.TensorServingInputReceiver(images, {'image_bytes': image_bytes_list})


def override_flags_and_set_envars_for_gpu_thread_pool(flags_obj):
    """Override flags and set env_vars for performance.

  These settings exist to test the difference between using stock settings
  and manual tuning. It also shows some of the ENV_VARS that can be tweaked to
  squeeze a few extra examples per second.  These settings are defaulted to the
  current platform of interest, which changes over time.

  On systems with small numbers of cpu cores, e.g. under 8 logical cores,
  setting up a gpu thread pool with `tf_gpu_thread_mode=gpu_private` may perform
  poorly.

  Args:
    flags_obj: Current flags, which will be adjusted possibly overriding
    what has been set by the user on the command-line.
  """
    cpu_count = multiprocessing.cpu_count()
    logging.info('Logical CPU cores: %s', cpu_count)
    per_gpu_thread_count = 1
    total_gpu_thread_count = per_gpu_thread_count * flags_obj.num_gpus
    os.environ['TF_GPU_THREAD_MODE'] = flags_obj.tf_gpu_thread_mode
    os.environ['TF_GPU_THREAD_COUNT'] = str(per_gpu_thread_count)
    logging.info('TF_GPU_THREAD_COUNT: %s', os.environ['TF_GPU_THREAD_COUNT'])
    logging.info('TF_GPU_THREAD_MODE: %s', os.environ['TF_GPU_THREAD_MODE'])
    main_thread_count = cpu_count - total_gpu_thread_count
    flags_obj.inter_op_parallelism_threads = main_thread_count
    num_monitoring_threads = 2 * flags_obj.num_gpus
    flags_obj.datasets_num_private_threads = cpu_count - total_gpu_thread_count - num_monitoring_threads


def learning_rate_with_decay(batch_size, batch_denom, num_images, boundary_epochs, decay_rates, base_lr=0.1, warmup=False):
    """Get a learning rate that decays step-wise as training progresses.

  Args:
    batch_size: the number of examples processed in each training batch.
    batch_denom: this value will be used to scale the base learning rate.
      `0.1 * batch size` is divided by this number, such that when
      batch_denom == batch_size, the initial learning rate will be 0.1.
    num_images: total number of images that will be used for training.
    boundary_epochs: list of ints representing the epochs at which we
      decay the learning rate.
    decay_rates: list of floats representing the decay rates to be used
      for scaling the learning rate. It should have one more element
      than `boundary_epochs`, and all elements should have the same type.
    base_lr: Initial learning rate scaled based on batch_denom.
    warmup: Run a 5 epoch warmup to the initial lr.
  Returns:
    Returns a function that takes a single argument - the number of batches
    trained so far (global_step)- and returns the learning rate to be used
    for training the next batch.
  """
    initial_learning_rate = base_lr * batch_size / batch_denom
    batches_per_epoch = num_images / batch_size
    boundaries = [int(batches_per_epoch * epoch) for epoch in boundary_epochs]
    vals = [initial_learning_rate * decay for decay in decay_rates]

    def learning_rate_fn(global_step):
        lr = tf.compat.v1.train.piecewise_constant(global_step, boundaries, vals)
        if warmup:
            warmup_steps = int(batches_per_epoch * 5)
            warmup_lr = initial_learning_rate * tf.cast(global_step, tf.float32) / tf.cast(warmup_steps, tf.float32)
            return tf.cond(pred=(global_step < warmup_steps), true_fn=(lambda : warmup_lr),
              false_fn=(lambda : lr))
        return lr

    def poly_rate_fn(global_step):
        if flags.FLAGS.batch_size < 8192:
            plr = 5.0
            w_epochs = 5
        else:
            if flags.FLAGS.batch_size < 16384:
                plr = 10.0
                w_epochs = 5
            else:
                if flags.FLAGS.batch_size < 32768:
                    plr = 25.0
                    w_epochs = 5
                else:
                    plr = 32.0
                    w_epochs = 14
        w_steps = int(w_epochs * batches_per_epoch)
        wrate = plr * tf.cast(global_step, tf.float32) / tf.cast(w_steps, tf.float32)
        num_epochs = 90
        train_steps = batches_per_epoch * num_epochs
        min_step = tf.constant(1, dtype=(tf.int64))
        decay_steps = tf.maximum(min_step, tf.subtract(global_step, w_steps))
        poly_rate = tf.train.polynomial_decay(plr,
          decay_steps,
          (train_steps - w_steps + 1),
          power=2.0)
        return tf.where(global_step <= w_steps, wrate, poly_rate)

    if flags.FLAGS.enable_lars:
        return poly_rate_fn
    return learning_rate_fn


def per_replica_batch_size(batch_size, num_gpus):
    """For multi-gpu, batch-size must be a multiple of the number of GPUs.

  Note that distribution strategy handles this automatically when used with
  Keras. For using with Estimator, we need to get per GPU batch.

  Args:
    batch_size: Global batch size to be divided among devices. This should be
      equal to num_gpus times the single-GPU batch_size for multi-gpu training.
    num_gpus: How many GPUs are used with DistributionStrategies.

  Returns:
    Batch size per device.

  Raises:
    ValueError: if batch_size is not divisible by number of devices
  """
    if num_gpus <= 1:
        return batch_size
    remainder = batch_size % num_gpus
    if remainder:
        err = 'When running with multiple GPUs, batch size must be a multiple of the number of available GPUs. Found {} GPUs with a batch size of {}; try --batch_size={} instead.'.format(num_gpus, batch_size, batch_size - remainder)
        raise ValueError(err)
    return int(batch_size / num_gpus)


def resnet_model_fn(features, labels, mode, model_class, resnet_size, weight_decay, learning_rate_fn, momentum, data_format, resnet_version, loss_scale, loss_filter_fn=None, dtype=resnet_model.DEFAULT_DTYPE, fine_tune=False, label_smoothing=0.0):
    """Shared functionality for different resnet model_fns.

  Initializes the ResnetModel representing the model layers
  and uses that model to build the necessary EstimatorSpecs for
  the `mode` in question. For training, this means building losses,
  the optimizer, and the train op that get passed into the EstimatorSpec.
  For evaluation and prediction, the EstimatorSpec is returned without
  a train op, but with the necessary parameters for the given mode.

  Args:
    features: tensor representing input images
    labels: tensor representing class labels for all input images
    mode: current estimator mode; should be one of
      `tf.estimator.ModeKeys.TRAIN`, `EVALUATE`, `PREDICT`
    model_class: a class representing a TensorFlow model that has a __call__
      function. We assume here that this is a subclass of ResnetModel.
    resnet_size: A single integer for the size of the ResNet model.
    weight_decay: weight decay loss rate used to regularize learned variables.
    learning_rate_fn: function that returns the current learning rate given
      the current global_step
    momentum: momentum term used for optimization
    data_format: Input format ('channels_last', 'channels_first', or None).
      If set to None, the format is dependent on whether a GPU is available.
    resnet_version: Integer representing which version of the ResNet network to
      use. See README for details. Valid values: [1, 2]
    loss_scale: The factor to scale the loss for numerical stability. A detailed
      summary is present in the arg parser help text.
    loss_filter_fn: function that takes a string variable name and returns
      True if the var should be included in loss calculation, and False
      otherwise. If None, batch_normalization variables will be excluded
      from the loss.
    dtype: the TensorFlow dtype to use for calculations.
    fine_tune: If True only train the dense layers(final layers).
    label_smoothing: If greater than 0 then smooth the labels.

  Returns:
    EstimatorSpec parameterized according to the input params and the
    current mode.
  """
    tf.compat.v1.summary.image('images', features, max_outputs=6)
    if not features.dtype == dtype:
        raise AssertionError
    else:
        model = model_class(resnet_size, data_format, resnet_version=resnet_version, dtype=dtype)
        logits = model(features, mode == tf.estimator.ModeKeys.TRAIN)
        logits = tf.cast(logits, tf.float32)
        predictions = {'classes':tf.argmax(input=logits, axis=1), 
         'probabilities':tf.nn.softmax(logits, name='softmax_tensor')}
        if mode == tf.estimator.ModeKeys.PREDICT:
            return tf.estimator.EstimatorSpec(mode=mode,
              predictions=predictions,
              export_outputs={'predict': tf.estimator.export.PredictOutput(predictions)})
            if label_smoothing != 0.0:
                one_hot_labels = tf.one_hot(labels, 1001)
                cross_entropy = tf.losses.softmax_cross_entropy(logits=logits,
                  onehot_labels=one_hot_labels,
                  label_smoothing=label_smoothing)
            else:
                cross_entropy = tf.compat.v1.losses.sparse_softmax_cross_entropy(logits=logits,
                  labels=labels)
            tf.identity(cross_entropy, name='cross_entropy')
            tf.compat.v1.summary.scalar('cross_entropy', cross_entropy)

            def exclude_batch_norm(name):
                return 'batch_normalization' not in name

            loss_filter_fn = loss_filter_fn or exclude_batch_norm
            l2_loss = weight_decay * tf.add_n([tf.nn.l2_loss(tf.cast(v, tf.float32)) for v in tf.compat.v1.trainable_variables() if loss_filter_fn(v.name)])
            tf.compat.v1.summary.scalar('l2_loss', l2_loss)
            loss = cross_entropy + l2_loss
            if mode == tf.estimator.ModeKeys.TRAIN:
                global_step = tf.compat.v1.train.get_or_create_global_step()
                learning_rate = learning_rate_fn(global_step)
                tf.identity(learning_rate, name='learning_rate')
                tf.compat.v1.summary.scalar('learning_rate', learning_rate)
                if flags.FLAGS.enable_lars:
                    import tensorflow.contrib as contrib_opt
                    optimizer = contrib_opt.LARSOptimizer(learning_rate,
                      momentum=momentum,
                      weight_decay=weight_decay,
                      skip_list=[
                     'batch_normalization', 'bias'])
        else:
            optimizer = tf.compat.v1.train.MomentumOptimizer(learning_rate=learning_rate,
              momentum=momentum)
    fp16_implementation = getattr(flags.FLAGS, 'fp16_implementation', None)
    if fp16_implementation == 'graph_rewrite':
        optimizer = tf.compat.v1.train.experimental.enable_mixed_precision_graph_rewrite(optimizer,
          loss_scale=loss_scale)

    def _dense_grad_filter(gvs):
        """Only apply gradient updates to the final layer.

      This function is used for fine tuning.

      Args:
        gvs: list of tuples with gradients and variable info
      Returns:
        filtered gradients so that only the dense layer remains
      """
        return [(g, v) for g, v in gvs if 'dense' in v.name]

    if loss_scale != 1:
        if fp16_implementation != 'graph_rewrite':
            scaled_grad_vars = optimizer.compute_gradients(loss * loss_scale)
            if fine_tune:
                scaled_grad_vars = _dense_grad_filter(scaled_grad_vars)
            unscaled_grad_vars = [(grad / loss_scale, var) for grad, var in scaled_grad_vars]
            minimize_op = optimizer.apply_gradients(unscaled_grad_vars, global_step)
        else:
            grad_vars = optimizer.compute_gradients(loss)
            if fine_tune:
                grad_vars = _dense_grad_filter(grad_vars)
            minimize_op = optimizer.apply_gradients(grad_vars, global_step)
        update_ops = tf.compat.v1.get_collection(tf.compat.v1.GraphKeys.UPDATE_OPS)
        train_op = tf.group(minimize_op, update_ops)
    else:
        train_op = None
    accuracy = tf.compat.v1.metrics.accuracy(labels, predictions['classes'])
    accuracy_top_5 = tf.compat.v1.metrics.mean(tf.nn.in_top_k(predictions=logits, targets=labels, k=5, name='top_5_op'))
    metrics = {'accuracy':accuracy,  'accuracy_top_5':accuracy_top_5}
    tf.identity((accuracy[1]), name='train_accuracy')
    tf.identity((accuracy_top_5[1]), name='train_accuracy_top_5')
    tf.compat.v1.summary.scalar('train_accuracy', accuracy[1])
    tf.compat.v1.summary.scalar('train_accuracy_top_5', accuracy_top_5[1])
    return tf.estimator.EstimatorSpec(mode=mode,
      predictions=predictions,
      loss=loss,
      train_op=train_op,
      eval_metric_ops=metrics)


def resnet_main--- This code section failed: ---

 L. 576         0  LOAD_GLOBAL              model_helpers
                2  LOAD_METHOD              apply_clean
                4  LOAD_GLOBAL              flags
                6  LOAD_ATTR                FLAGS
                8  CALL_METHOD_1         1  '1 positional argument'
               10  POP_TOP          

 L. 579        12  LOAD_DEREF               'flags_obj'
               14  LOAD_ATTR                tf_gpu_thread_mode
               16  POP_JUMP_IF_FALSE    26  'to 26'

 L. 580        18  LOAD_GLOBAL              override_flags_and_set_envars_for_gpu_thread_pool
               20  LOAD_DEREF               'flags_obj'
               22  CALL_FUNCTION_1       1  '1 positional argument'
               24  POP_TOP          
             26_0  COME_FROM            16  '16'

 L. 583        26  LOAD_GLOBAL              distribution_utils
               28  LOAD_METHOD              configure_cluster
               30  LOAD_DEREF               'flags_obj'
               32  LOAD_ATTR                worker_hosts

 L. 584        34  LOAD_DEREF               'flags_obj'
               36  LOAD_ATTR                task_index
               38  CALL_METHOD_2         2  '2 positional arguments'
               40  STORE_FAST               'num_workers'

 L. 588        42  LOAD_GLOBAL              tf
               44  LOAD_ATTR                compat
               46  LOAD_ATTR                v1
               48  LOAD_ATTR                ConfigProto

 L. 589        50  LOAD_DEREF               'flags_obj'
               52  LOAD_ATTR                inter_op_parallelism_threads

 L. 590        54  LOAD_DEREF               'flags_obj'
               56  LOAD_ATTR                intra_op_parallelism_threads

 L. 591        58  LOAD_CONST               True
               60  LOAD_CONST               ('inter_op_parallelism_threads', 'intra_op_parallelism_threads', 'allow_soft_placement')
               62  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               64  STORE_FAST               'session_config'

 L. 593        66  LOAD_GLOBAL              distribution_utils
               68  LOAD_ATTR                get_distribution_strategy

 L. 594        70  LOAD_DEREF               'flags_obj'
               72  LOAD_ATTR                distribution_strategy

 L. 595        74  LOAD_GLOBAL              flags_core
               76  LOAD_METHOD              get_num_gpus
               78  LOAD_DEREF               'flags_obj'
               80  CALL_METHOD_1         1  '1 positional argument'

 L. 596        82  LOAD_DEREF               'flags_obj'
               84  LOAD_ATTR                all_reduce_alg

 L. 597        86  LOAD_DEREF               'flags_obj'
               88  LOAD_ATTR                num_packs
               90  LOAD_CONST               ('distribution_strategy', 'num_gpus', 'all_reduce_alg', 'num_packs')
               92  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               94  STORE_FAST               'distribution_strategy'

 L. 601        96  LOAD_GLOBAL              tf
               98  LOAD_ATTR                estimator
              100  LOAD_ATTR                RunConfig

 L. 602       102  LOAD_FAST                'distribution_strategy'

 L. 603       104  LOAD_FAST                'session_config'

 L. 604       106  LOAD_CONST               86400

 L. 605       108  LOAD_CONST               None
              110  LOAD_CONST               ('train_distribute', 'session_config', 'save_checkpoints_secs', 'save_checkpoints_steps')
              112  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              114  STORE_FAST               'run_config'

 L. 608       116  LOAD_DEREF               'flags_obj'
              118  LOAD_ATTR                pretrained_model_checkpoint_path
              120  LOAD_CONST               None
              122  COMPARE_OP               is-not
              124  POP_JUMP_IF_FALSE   146  'to 146'

 L. 609       126  LOAD_GLOBAL              tf
              128  LOAD_ATTR                estimator
              130  LOAD_ATTR                WarmStartSettings

 L. 610       132  LOAD_DEREF               'flags_obj'
              134  LOAD_ATTR                pretrained_model_checkpoint_path

 L. 611       136  LOAD_STR                 '^(?!.*dense)'
              138  LOAD_CONST               ('vars_to_warm_start',)
              140  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              142  STORE_FAST               'warm_start_settings'
              144  JUMP_FORWARD        150  'to 150'
            146_0  COME_FROM           124  '124'

 L. 613       146  LOAD_CONST               None
              148  STORE_FAST               'warm_start_settings'
            150_0  COME_FROM           144  '144'

 L. 615       150  LOAD_GLOBAL              tf
              152  LOAD_ATTR                estimator
              154  LOAD_ATTR                Estimator

 L. 616       156  LOAD_FAST                'model_function'
              158  LOAD_DEREF               'flags_obj'
              160  LOAD_ATTR                model_dir
              162  LOAD_FAST                'run_config'

 L. 617       164  LOAD_FAST                'warm_start_settings'

 L. 618       166  LOAD_GLOBAL              int
              168  LOAD_DEREF               'flags_obj'
              170  LOAD_ATTR                resnet_size
              172  CALL_FUNCTION_1       1  '1 positional argument'

 L. 619       174  LOAD_DEREF               'flags_obj'
              176  LOAD_ATTR                data_format

 L. 620       178  LOAD_DEREF               'flags_obj'
              180  LOAD_ATTR                batch_size

 L. 621       182  LOAD_GLOBAL              int
              184  LOAD_DEREF               'flags_obj'
              186  LOAD_ATTR                resnet_version
              188  CALL_FUNCTION_1       1  '1 positional argument'

 L. 622       190  LOAD_GLOBAL              flags_core
              192  LOAD_ATTR                get_loss_scale
              194  LOAD_DEREF               'flags_obj'

 L. 623       196  LOAD_CONST               128
              198  LOAD_CONST               ('default_for_fp16',)
              200  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 624       202  LOAD_GLOBAL              flags_core
              204  LOAD_METHOD              get_tf_dtype
              206  LOAD_DEREF               'flags_obj'
              208  CALL_METHOD_1         1  '1 positional argument'

 L. 625       210  LOAD_DEREF               'flags_obj'
              212  LOAD_ATTR                fine_tune

 L. 626       214  LOAD_FAST                'num_workers'
              216  LOAD_CONST               ('resnet_size', 'data_format', 'batch_size', 'resnet_version', 'loss_scale', 'dtype', 'fine_tune', 'num_workers')
              218  BUILD_CONST_KEY_MAP_8     8 
              220  LOAD_CONST               ('model_fn', 'model_dir', 'config', 'warm_start_from', 'params')
              222  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
              224  STORE_FAST               'classifier'

 L. 630       226  LOAD_DEREF               'flags_obj'
              228  LOAD_ATTR                batch_size

 L. 631       230  LOAD_GLOBAL              flags_core
              232  LOAD_METHOD              get_tf_dtype
              234  LOAD_DEREF               'flags_obj'
              236  CALL_METHOD_1         1  '1 positional argument'

 L. 632       238  LOAD_DEREF               'flags_obj'
              240  LOAD_ATTR                resnet_size

 L. 633       242  LOAD_DEREF               'flags_obj'
              244  LOAD_ATTR                resnet_version

 L. 634       246  LOAD_DEREF               'flags_obj'
              248  LOAD_ATTR                use_synthetic_data

 L. 635       250  LOAD_DEREF               'flags_obj'
              252  LOAD_ATTR                train_epochs

 L. 636       254  LOAD_FAST                'num_workers'
              256  LOAD_CONST               ('batch_size', 'dtype', 'resnet_size', 'resnet_version', 'synthetic_data', 'train_epochs', 'num_workers')
              258  BUILD_CONST_KEY_MAP_7     7 
              260  STORE_FAST               'run_params'

 L. 638       262  LOAD_DEREF               'flags_obj'
              264  LOAD_ATTR                use_synthetic_data
          266_268  POP_JUMP_IF_FALSE   278  'to 278'

 L. 639       270  LOAD_FAST                'dataset_name'
              272  LOAD_STR                 '-synthetic'
              274  BINARY_ADD       
              276  STORE_FAST               'dataset_name'
            278_0  COME_FROM           266  '266'

 L. 641       278  LOAD_GLOBAL              logger
              280  LOAD_METHOD              get_benchmark_logger
              282  CALL_METHOD_0         0  '0 positional arguments'
              284  STORE_FAST               'benchmark_logger'

 L. 642       286  LOAD_FAST                'benchmark_logger'
              288  LOAD_ATTR                log_run_info
              290  LOAD_STR                 'resnet'
              292  LOAD_FAST                'dataset_name'
              294  LOAD_FAST                'run_params'

 L. 643       296  LOAD_DEREF               'flags_obj'
              298  LOAD_ATTR                benchmark_test_id
              300  LOAD_CONST               ('test_id',)
              302  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              304  POP_TOP          

 L. 645       306  LOAD_GLOBAL              hooks_helper
              308  LOAD_ATTR                get_train_hooks

 L. 646       310  LOAD_DEREF               'flags_obj'
              312  LOAD_ATTR                hooks

 L. 647       314  LOAD_DEREF               'flags_obj'
              316  LOAD_ATTR                model_dir

 L. 648       318  LOAD_DEREF               'flags_obj'
              320  LOAD_ATTR                batch_size
              322  LOAD_CONST               ('model_dir', 'batch_size')
              324  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              326  STORE_FAST               'train_hooks'

 L. 650       328  LOAD_CONST               (None,)
              330  LOAD_CLOSURE             'flags_obj'
              332  LOAD_CLOSURE             'input_function'
              334  BUILD_TUPLE_2         2 
              336  LOAD_CODE                <code_object input_fn_train>
              338  LOAD_STR                 'resnet_main.<locals>.input_fn_train'
              340  MAKE_FUNCTION_9          'default, closure'
              342  STORE_DEREF              'input_fn_train'

 L. 661       344  LOAD_CLOSURE             'flags_obj'
              346  LOAD_CLOSURE             'input_function'
              348  BUILD_TUPLE_2         2 
              350  LOAD_CODE                <code_object input_fn_eval>
              352  LOAD_STR                 'resnet_main.<locals>.input_fn_eval'
              354  MAKE_FUNCTION_8          'closure'
              356  STORE_FAST               'input_fn_eval'

 L. 670       358  LOAD_DEREF               'flags_obj'
              360  LOAD_ATTR                eval_only
          362_364  POP_JUMP_IF_TRUE    374  'to 374'
              366  LOAD_DEREF               'flags_obj'
              368  LOAD_ATTR                train_epochs
          370_372  POP_JUMP_IF_TRUE    378  'to 378'
            374_0  COME_FROM           362  '362'
              374  LOAD_CONST               0
              376  JUMP_FORWARD        382  'to 382'
            378_0  COME_FROM           370  '370'

 L. 671       378  LOAD_DEREF               'flags_obj'
              380  LOAD_ATTR                train_epochs
            382_0  COME_FROM           376  '376'
              382  STORE_DEREF              'train_epochs'

 L. 673       384  LOAD_DEREF               'flags_obj'
              386  LOAD_ATTR                use_train_and_evaluate
          388_390  JUMP_IF_TRUE_OR_POP   398  'to 398'
              392  LOAD_FAST                'num_workers'
              394  LOAD_CONST               1
              396  COMPARE_OP               >
            398_0  COME_FROM           388  '388'
              398  STORE_FAST               'use_train_and_evaluate'

 L. 674       400  LOAD_FAST                'use_train_and_evaluate'
          402_404  POP_JUMP_IF_FALSE   484  'to 484'

 L. 675       406  LOAD_GLOBAL              tf
              408  LOAD_ATTR                estimator
              410  LOAD_ATTR                TrainSpec

 L. 676       412  LOAD_CONST               (None,)
              414  LOAD_CLOSURE             'input_fn_train'
              416  LOAD_CLOSURE             'train_epochs'
              418  BUILD_TUPLE_2         2 
              420  LOAD_LAMBDA              '<code_object <lambda>>'
              422  LOAD_STR                 'resnet_main.<locals>.<lambda>'
              424  MAKE_FUNCTION_9          'default, closure'

 L. 678       426  LOAD_FAST                'train_hooks'

 L. 679       428  LOAD_DEREF               'flags_obj'
              430  LOAD_ATTR                max_train_steps
              432  LOAD_CONST               ('input_fn', 'hooks', 'max_steps')
              434  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              436  STORE_FAST               'train_spec'

 L. 680       438  LOAD_GLOBAL              tf
              440  LOAD_ATTR                estimator
              442  LOAD_ATTR                EvalSpec
              444  LOAD_FAST                'input_fn_eval'
              446  LOAD_CONST               ('input_fn',)
              448  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              450  STORE_FAST               'eval_spec'

 L. 681       452  LOAD_GLOBAL              logging
              454  LOAD_METHOD              info
              456  LOAD_STR                 'Starting to train and evaluate.'
              458  CALL_METHOD_1         1  '1 positional argument'
              460  POP_TOP          

 L. 682       462  LOAD_GLOBAL              tf
              464  LOAD_ATTR                estimator
              466  LOAD_METHOD              train_and_evaluate
              468  LOAD_FAST                'classifier'
              470  LOAD_FAST                'train_spec'
              472  LOAD_FAST                'eval_spec'
              474  CALL_METHOD_3         3  '3 positional arguments'
              476  POP_TOP          

 L. 685       478  BUILD_MAP_0           0 
              480  STORE_FAST               'eval_results'
              482  JUMP_FORWARD        710  'to 710'
            484_0  COME_FROM           402  '402'

 L. 687       484  LOAD_DEREF               'train_epochs'
              486  LOAD_CONST               0
              488  COMPARE_OP               ==
          490_492  POP_JUMP_IF_FALSE   508  'to 508'

 L. 689       494  LOAD_CONST               0
              496  BUILD_LIST_1          1 
              498  LOAD_CONST               1
              500  ROT_TWO          
              502  STORE_FAST               'schedule'
              504  STORE_FAST               'n_loops'
              506  JUMP_FORWARD        574  'to 574'
            508_0  COME_FROM           490  '490'

 L. 699       508  LOAD_GLOBAL              math
              510  LOAD_METHOD              ceil
              512  LOAD_DEREF               'train_epochs'
              514  LOAD_DEREF               'flags_obj'
              516  LOAD_ATTR                epochs_between_evals
              518  BINARY_TRUE_DIVIDE
              520  CALL_METHOD_1         1  '1 positional argument'
              522  STORE_FAST               'n_loops'

 L. 700       524  LOAD_CLOSURE             'flags_obj'
              526  BUILD_TUPLE_1         1 
              528  LOAD_LISTCOMP            '<code_object <listcomp>>'
              530  LOAD_STR                 'resnet_main.<locals>.<listcomp>'
              532  MAKE_FUNCTION_8          'closure'
              534  LOAD_GLOBAL              range
              536  LOAD_GLOBAL              int
              538  LOAD_FAST                'n_loops'
              540  CALL_FUNCTION_1       1  '1 positional argument'
              542  CALL_FUNCTION_1       1  '1 positional argument'
              544  GET_ITER         
              546  CALL_FUNCTION_1       1  '1 positional argument'
              548  STORE_FAST               'schedule'

 L. 701       550  LOAD_DEREF               'train_epochs'
              552  LOAD_GLOBAL              sum
              554  LOAD_FAST                'schedule'
              556  LOAD_CONST               None
              558  LOAD_CONST               -1
              560  BUILD_SLICE_2         2 
              562  BINARY_SUBSCR    
              564  CALL_FUNCTION_1       1  '1 positional argument'
              566  BINARY_SUBTRACT  
              568  LOAD_FAST                'schedule'
              570  LOAD_CONST               -1
              572  STORE_SUBSCR     
            574_0  COME_FROM           506  '506'

 L. 703       574  SETUP_LOOP          710  'to 710'
              576  LOAD_GLOBAL              enumerate
              578  LOAD_FAST                'schedule'
              580  CALL_FUNCTION_1       1  '1 positional argument'
              582  GET_ITER         
            584_0  COME_FROM           698  '698'
              584  FOR_ITER            708  'to 708'
              586  UNPACK_SEQUENCE_2     2 
              588  STORE_FAST               'cycle_index'
              590  STORE_DEREF              'num_train_epochs'

 L. 704       592  LOAD_GLOBAL              logging
              594  LOAD_METHOD              info
              596  LOAD_STR                 'Starting cycle: %d/%d'
              598  LOAD_FAST                'cycle_index'
              600  LOAD_GLOBAL              int
              602  LOAD_FAST                'n_loops'
              604  CALL_FUNCTION_1       1  '1 positional argument'
              606  CALL_METHOD_3         3  '3 positional arguments'
              608  POP_TOP          

 L. 706       610  LOAD_DEREF               'num_train_epochs'
          612_614  POP_JUMP_IF_FALSE   646  'to 646'

 L. 711       616  LOAD_FAST                'classifier'
              618  LOAD_ATTR                train

 L. 712       620  LOAD_CONST               (None,)
              622  LOAD_CLOSURE             'input_fn_train'
              624  LOAD_CLOSURE             'num_train_epochs'
              626  BUILD_TUPLE_2         2 
              628  LOAD_LAMBDA              '<code_object <lambda>>'
              630  LOAD_STR                 'resnet_main.<locals>.<lambda>'
              632  MAKE_FUNCTION_9          'default, closure'

 L. 714       634  LOAD_FAST                'train_hooks'

 L. 715       636  LOAD_DEREF               'flags_obj'
              638  LOAD_ATTR                max_train_steps
              640  LOAD_CONST               ('input_fn', 'hooks', 'max_steps')
              642  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              644  POP_TOP          
            646_0  COME_FROM           612  '612'

 L. 723       646  LOAD_GLOBAL              logging
              648  LOAD_METHOD              info
              650  LOAD_STR                 'Starting to evaluate.'
              652  CALL_METHOD_1         1  '1 positional argument'
              654  POP_TOP          

 L. 724       656  LOAD_FAST                'classifier'
              658  LOAD_ATTR                evaluate
              660  LOAD_FAST                'input_fn_eval'

 L. 725       662  LOAD_DEREF               'flags_obj'
              664  LOAD_ATTR                max_train_steps
              666  LOAD_CONST               ('input_fn', 'steps')
              668  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              670  STORE_FAST               'eval_results'

 L. 727       672  LOAD_FAST                'benchmark_logger'
              674  LOAD_METHOD              log_evaluation_result
              676  LOAD_FAST                'eval_results'
              678  CALL_METHOD_1         1  '1 positional argument'
              680  POP_TOP          

 L. 729       682  LOAD_GLOBAL              model_helpers
              684  LOAD_METHOD              past_stop_threshold

 L. 730       686  LOAD_DEREF               'flags_obj'
              688  LOAD_ATTR                stop_threshold
              690  LOAD_FAST                'eval_results'
              692  LOAD_STR                 'accuracy'
              694  BINARY_SUBSCR    
              696  CALL_METHOD_2         2  '2 positional arguments'
          698_700  POP_JUMP_IF_FALSE   584  'to 584'

 L. 731       702  BREAK_LOOP       
          704_706  JUMP_BACK           584  'to 584'
              708  POP_BLOCK        
            710_0  COME_FROM_LOOP      574  '574'
            710_1  COME_FROM           482  '482'

 L. 733       710  LOAD_DEREF               'flags_obj'
              712  LOAD_ATTR                export_dir
              714  LOAD_CONST               None
              716  COMPARE_OP               is-not
          718_720  POP_JUMP_IF_FALSE   794  'to 794'

 L. 735       722  LOAD_GLOBAL              flags_core
              724  LOAD_METHOD              get_tf_dtype
              726  LOAD_DEREF               'flags_obj'
              728  CALL_METHOD_1         1  '1 positional argument'
              730  STORE_FAST               'export_dtype'

 L. 736       732  LOAD_DEREF               'flags_obj'
              734  LOAD_ATTR                image_bytes_as_serving_input
          736_738  POP_JUMP_IF_FALSE   758  'to 758'

 L. 737       740  LOAD_GLOBAL              functools
              742  LOAD_ATTR                partial

 L. 738       744  LOAD_GLOBAL              image_bytes_serving_input_fn
              746  LOAD_FAST                'shape'
              748  LOAD_FAST                'export_dtype'
              750  LOAD_CONST               ('dtype',)
              752  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              754  STORE_FAST               'input_receiver_fn'
              756  JUMP_FORWARD        776  'to 776'
            758_0  COME_FROM           736  '736'

 L. 740       758  LOAD_GLOBAL              export
              760  LOAD_ATTR                build_tensor_serving_input_receiver_fn

 L. 741       762  LOAD_FAST                'shape'
              764  LOAD_DEREF               'flags_obj'
              766  LOAD_ATTR                batch_size
              768  LOAD_FAST                'export_dtype'
              770  LOAD_CONST               ('batch_size', 'dtype')
              772  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              774  STORE_FAST               'input_receiver_fn'
            776_0  COME_FROM           756  '756'

 L. 742       776  LOAD_FAST                'classifier'
              778  LOAD_ATTR                export_savedmodel
              780  LOAD_DEREF               'flags_obj'
              782  LOAD_ATTR                export_dir
              784  LOAD_FAST                'input_receiver_fn'

 L. 743       786  LOAD_CONST               True
              788  LOAD_CONST               ('strip_default_attrs',)
              790  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              792  POP_TOP          
            794_0  COME_FROM           718  '718'

 L. 745       794  BUILD_MAP_0           0 
              796  STORE_FAST               'stats'

 L. 746       798  LOAD_FAST                'eval_results'
              800  LOAD_FAST                'stats'
              802  LOAD_STR                 'eval_results'
              804  STORE_SUBSCR     

 L. 747       806  LOAD_FAST                'train_hooks'
              808  LOAD_FAST                'stats'
              810  LOAD_STR                 'train_hooks'
              812  STORE_SUBSCR     

 L. 749       814  LOAD_FAST                'stats'
              816  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `MAKE_FUNCTION_9' instruction at offset 424


def define_resnet_flags(resnet_size_choices=None, dynamic_loss_scale=False, fp16_implementation=False):
    """Add flags and validators for ResNet."""
    flags_core.define_base(clean=True, train_epochs=True, epochs_between_evals=True,
      stop_threshold=True,
      num_gpu=True,
      hooks=True,
      export_dir=True,
      distribution_strategy=True)
    flags_core.define_performance(num_parallel_calls=False, inter_op=True,
      intra_op=True,
      synthetic_data=True,
      dtype=True,
      all_reduce_alg=True,
      num_packs=True,
      tf_gpu_thread_mode=True,
      datasets_num_private_threads=True,
      dynamic_loss_scale=dynamic_loss_scale,
      fp16_implementation=fp16_implementation,
      loss_scale=True,
      tf_data_experimental_slack=True,
      max_train_steps=True)
    flags_core.define_image()
    flags_core.define_benchmark()
    flags_core.define_distribution()
    flags.adopt_module_key_flags(flags_core)
    flags.DEFINE_enum(name='resnet_version',
      short_name='rv',
      default='1',
      enum_values=[
     '1', '2'],
      help=(flags_core.help_wrap('Version of ResNet. (1 or 2) See README.md for details.')))
    flags.DEFINE_bool(name='fine_tune',
      short_name='ft',
      default=False,
      help=(flags_core.help_wrap('If True do not train any parameters except for the final layer.')))
    flags.DEFINE_string(name='pretrained_model_checkpoint_path',
      short_name='pmcp',
      default=None,
      help=(flags_core.help_wrap('If not None initialize all the network except the final layer with these values')))
    flags.DEFINE_boolean(name='eval_only',
      default=False,
      help=(flags_core.help_wrap('Skip training and only perform evaluation on the latest checkpoint.')))
    flags.DEFINE_boolean(name='image_bytes_as_serving_input',
      default=False,
      help=(flags_core.help_wrap('If True exports savedmodel with serving signature that accepts JPEG image bytes instead of a fixed size [HxWxC] tensor that represents the image. The former is easier to use for serving at the expense of image resize/cropping being done as part of model inference. Note, this flag only applies to ImageNet and cannot be used for CIFAR.')))
    flags.DEFINE_boolean(name='use_train_and_evaluate',
      default=False,
      help=(flags_core.help_wrap('If True, uses `tf.estimator.train_and_evaluate` for the training and evaluation loop, instead of separate calls to `classifier.train and `classifier.evaluate`, which is the default behavior.')))
    flags.DEFINE_bool(name='enable_lars',
      default=False,
      help=(flags_core.help_wrap('Enable LARS optimizer for large batch training.')))
    flags.DEFINE_float(name='label_smoothing',
      default=0.0,
      help=(flags_core.help_wrap('Label smoothing parameter used in the softmax_cross_entropy')))
    flags.DEFINE_float(name='weight_decay',
      default=0.0001,
      help=(flags_core.help_wrap('Weight decay coefficiant for l2 regularization.')))
    choice_kwargs = dict(name='resnet_size',
      short_name='rs',
      default='50',
      help=(flags_core.help_wrap('The size of the ResNet model to use.')))
    if resnet_size_choices is None:
        (flags.DEFINE_string)(**choice_kwargs)
    else:
        (flags.DEFINE_enum)(enum_values=resnet_size_choices, **choice_kwargs)