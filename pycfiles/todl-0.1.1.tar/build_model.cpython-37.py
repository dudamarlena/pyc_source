# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/seq2species/build_model.py
# Compiled at: 2020-04-05 19:50:58
# Size of source mod 2**32: 18567 bytes
"""Defines convolutional model graph for Seq2Species.

Builds TensorFlow computation graph for predicting the given taxonomic target
labels from short reads of DNA using convolutional filters, followed by
fully-connected layers and a softmax output layer.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import collections, math, tensorflow as tf, input as seq2species_input, seq2label_utils

class ConvolutionalNet(object):
    __doc__ = "Class to build and store the model's computational graph and operations.\n\n  Attributes:\n    read_length: int; the length in basepairs of the input reads of DNA.\n    placeholders: dict; mapping from name to tf.Placeholder.\n    global_step: tf.Variable tracking number of training iterations performed.\n    train_op: operation to perform one training step by gradient descent.\n    summary_op: operation to log model's performance metrics to TF event files.\n    accuracy: tf.Variable giving the model's read-level accuracy for the\n      current inputs.\n    weighted_accuracy: tf.Variable giving the model's read-level weighted\n      accuracy for the current inputs.\n    loss: tf.Variable giving the model's current cross entropy loss.\n    logits: tf.Variable containing the model's logits for the current inputs.\n    predictions: tf.Variable containing the model's current predicted\n      probability distributions for the current inputs.\n    possible_labels: a dict of possible label values (list of strings), keyed by\n      target name.  Labels in the lists are the order used for integer encoding.\n    use_tpu: whether model is to be run on TPU.\n  "

    def __init__(self, hparams, dataset_info, targets, use_tpu=False):
        """Initializes the ConvolutionalNet according to provided hyperparameters.

    Does not build the graph---this is done by calling `build_graph` on the
    constructed object or using `model_fn`.

    Args:
      hparams: tf.contrib.training.Hparams object containing the model's
        hyperparamters; see configuration.py for hyperparameter definitions.
      dataset_info: a `Seq2LabelDatasetInfo` message reflecting the dataset
        metadata.
      targets: list of strings: the names of the prediction targets.
      use_tpu: whether we are running on TPU; if True, summaries will be
        disabled.
    """
        self._placeholders = {}
        self._targets = targets
        self._dataset_info = dataset_info
        self._hparams = hparams
        all_label_values = seq2label_utils.get_all_label_values(self.dataset_info)
        self._possible_labels = {target:all_label_values[target] for target in self.targets}
        self._use_tpu = use_tpu

    @property
    def hparams(self):
        return self._hparams

    @property
    def dataset_info(self):
        return self._dataset_info

    @property
    def possible_labels(self):
        return self._possible_labels

    @property
    def bases(self):
        return seq2species_input.DNA_BASES

    @property
    def n_bases(self):
        return seq2species_input.NUM_DNA_BASES

    @property
    def targets(self):
        return self._targets

    @property
    def read_length(self):
        return self.dataset_info.read_length

    @property
    def placeholders(self):
        return self._placeholders

    @property
    def global_step(self):
        return self._global_step

    @property
    def train_op(self):
        return self._train_op

    @property
    def summary_op(self):
        return self._summary_op

    @property
    def accuracy(self):
        return self._accuracy

    @property
    def weighted_accuracy(self):
        return self._weighted_accuracy

    @property
    def loss(self):
        return self._loss

    @property
    def total_loss(self):
        return self._total_loss

    @property
    def logits(self):
        return self._logits

    @property
    def predictions(self):
        return self._predictions

    @property
    def use_tpu(self):
        return self._use_tpu

    def _summary_scalar(self, name, scalar):
        """Adds a summary scalar, if the platform supports summaries."""
        if not self.use_tpu:
            return tf.summary.scalar(name, scalar)
        return

    def _summary_histogram(self, name, values):
        """Adds a summary histogram, if the platform supports summaries."""
        if not self.use_tpu:
            return tf.summary.histogram(name, values)
        return

    def _init_weights(self, shape, scale=1.0, name='weights'):
        """Randomly initializes a weight Tensor of the given shape.

    Args:
      shape: list; desired Tensor dimensions.
      scale: float; standard deviation scale with which to initialize weights.
      name: string name for the variable.

    Returns:
      TF Variable contining truncated random Normal initialized weights.
    """
        num_inputs = shape[0] if len(shape) < 3 else shape[0] * shape[1] * shape[2]
        stddev = scale / math.sqrt(num_inputs)
        return tf.get_variable(name,
          shape=shape,
          initializer=(tf.truncated_normal_initializer(0.0, stddev)))

    def _init_bias(self, size):
        """Initializes bias vector of given shape as zeros.

    Args:
      size: int; desired size of bias Tensor.

    Returns:
      TF Variable containing the initialized biases.
    """
        return tf.get_variable(name=('b_{}'.format(size)),
          shape=[
         size],
          initializer=(tf.zeros_initializer()))

    def _add_summaries(self, mode, gradient_norm, parameter_norm):
        """Defines TensorFlow operation for logging summaries to event files.

    Args:
      mode: the ModeKey string.
      gradient_norm: Tensor; norm of gradients produced during the current
        training operation.
      parameter_norm: Tensor; norm of the model parameters produced during the
        current training operation.
    """
        if mode == tf.estimator.ModeKeys.TRAIN:
            self._summary_scalar('norm_of_gradients', gradient_norm)
            self._summary_scalar('norm_of_parameters', parameter_norm)
            self._summary_scalar('total_loss', self.total_loss)
            self._summary_scalar('learning_rate', self._learn_rate)
            for target in self.targets:
                self._summary_scalar('per_read_weighted_accuracy/{}'.format(target), self.weighted_accuracy[target])
                self._summary_scalar('per_read_accuracy/{}'.format(target), self.accuracy[target])
                self._summary_histogram('prediction_frequency/{}'.format(target), self._predictions[target])
                self._summary_scalar('cross_entropy_loss/{}'.format(target), self._loss[target])

            self._summary_op = tf.summary.merge_all()
        else:
            summaries = []
            for target in self.targets:
                accuracy_ph = tf.placeholder((tf.float32), shape=())
                weighted_accuracy_ph = tf.placeholder((tf.float32), shape=())
                cross_entropy_ph = tf.placeholder((tf.float32), shape=())
                self._placeholders.update({'accuracy/{}'.format(target): accuracy_ph, 
                 'weighted_accuracy/{}'.format(target): weighted_accuracy_ph, 
                 'cross_entropy/{}'.format(target): cross_entropy_ph})
                summaries += [
                 self._summary_scalar('cross_entropy_loss/{}'.format(target), cross_entropy_ph),
                 self._summary_scalar('per_read_accuracy/{}'.format(target), accuracy_ph),
                 self._summary_scalar('per_read_weighted_accuracy/{}'.format(target), weighted_accuracy_ph)]

            self._summary_op = tf.summary.merge(summaries)

    def _convolution(self, inputs, filter_dim, pointwise_dim=None, scale=1.0, padding='SAME'):
        """Applies convolutional filter of given dimensions to given input Tensor.

    If a pointwise dimension is specified, a depthwise separable convolution is
    performed.

    Args:
      inputs: 4D Tensor of shape (# reads, 1, # basepairs, # bases).
      filter_dim: integer tuple of the form (width, depth).
      pointwise_dim: int; output dimension for pointwise convolution.
      scale: float; standard deviation scale with which to initialize weights.
      padding: string; type of padding to use. One of "SAME" or "VALID".

    Returns:
      4D Tensor result of applying the convolutional filter to the inputs.
    """
        in_channels = inputs.get_shape()[3].value
        filter_width, filter_depth = filter_dim
        filters = self._init_weights([1, filter_width, in_channels, filter_depth], scale)
        self._summary_histogram(filters.name.split(':')[0].split('/')[1], filters)
        if pointwise_dim is None:
            return tf.nn.conv2d(inputs,
              filters,
              strides=[
             1, 1, 1, 1],
              padding=padding,
              name='weights')
        pointwise_filters = self._init_weights([
         1, 1, filter_depth * in_channels, pointwise_dim],
          scale,
          name='pointwise_weights')
        self._summary_histogram(pointwise_filters.name.split(':')[0].split('/')[1], pointwise_filters)
        return tf.nn.separable_conv2d(inputs,
          filters,
          pointwise_filters,
          strides=[
         1, 1, 1, 1],
          padding=padding)

    def _pool(self, inputs, pooling_type):
        """Performs pooling across width and height of the given inputs.

    Args:
      inputs: Tensor shaped (batch, height, width, channels) over which to pool.
        In our case, height is a unitary dimension and width can be thought of
        as the read dimension.
      pooling_type: string; one of "avg" or "max".

    Returns:
      Tensor result of performing pooling of the given pooling_type over the
      height and width dimensions of the given inputs.
    """
        if pooling_type == 'max':
            return tf.reduce_max(inputs, axis=[1, 2])
        if pooling_type == 'avg':
            return tf.reduce_sum(inputs,
              axis=[1, 2]) / tf.to_float(tf.shape(inputs)[2])

    def _leaky_relu(self, lrelu_slope, inputs):
        """Applies leaky ReLu activation to the given inputs with the given slope.

    Args:
      lrelu_slope: float; slope value for the activation function.
        A slope of 0.0 defines a standard ReLu activation, while a positive
        slope defines a leaky ReLu.
      inputs: Tensor upon which to apply the activation function.

    Returns:
      Tensor result of applying the activation function to the given inputs.
    """
        with tf.variable_scope('leaky_relu_activation'):
            return tf.maximum(lrelu_slope * inputs, inputs)

    def _dropout(self, inputs, keep_prob):
        """Applies dropout to the given inputs.

    Args:
      inputs: Tensor upon which to apply dropout.
      keep_prob: float; probability with which to randomly retain values in
        the given input.

    Returns:
      Tensor result of applying dropout to the given inputs.
    """
        with tf.variable_scope('dropout'):
            if keep_prob < 1.0:
                return tf.nn.dropout(inputs, keep_prob)
            return inputs

    def build_graph(self, features, labels, mode, batch_size):
        """Creates TensorFlow model graph.

    Args:
      features: a dict of input features Tensors.
      labels: a dict (by target name) of prediction labels.
      mode: the ModeKey string.
      batch_size: the integer batch size.

    Side Effect:
      Adds the following key Tensors and operations as class attributes:
        placeholders, global_step, train_op, summary_op, accuracy,
        weighted_accuracy, loss, logits, and predictions.
    """
        is_train = mode == tf.estimator.ModeKeys.TRAIN
        read = features['sequence']
        read = tf.expand_dims(read, 1)
        prev_out = read
        filters = zip(self.hparams.filter_widths, self.hparams.filter_depths)
        for i, f in enumerate(filters):
            with tf.variable_scope('convolution_' + str(i)):
                if self.hparams.use_depthwise_separable:
                    p = self.hparams.pointwise_depths[i]
                else:
                    p = None
                conv_out = self._convolution(prev_out,
                  f, pointwise_dim=p, scale=(self.hparams.weight_scale))
                conv_act_out = self._leaky_relu(self.hparams.lrelu_slope, conv_out)
                prev_out = self._dropout(conv_act_out, self.hparams.keep_prob) if is_train else conv_act_out

        for i in xrange(self.hparams.num_fc_layers):
            with tf.variable_scope('fully_connected_' + str(i)):
                biases = self._init_bias(self.hparams.num_fc_units)
                if i == 0:
                    filter_dimensions = (
                     self.hparams.min_read_length,
                     self.hparams.num_fc_units)
                else:
                    filter_dimensions = (
                     1, self.hparams.num_fc_units)
                fc_out = biases + self._convolution(prev_out,
                  filter_dimensions,
                  scale=(self.hparams.weight_scale),
                  padding='VALID')
                self._summary_histogram(biases.name.split(':')[0].split('/')[1], biases)
                fc_act_out = self._leaky_relu(self.hparams.lrelu_slope, fc_out)
                prev_out = self._dropout(fc_act_out, self.hparams.keep_prob) if is_train else fc_act_out

        with tf.variable_scope('pool'):
            pool_out = self._pool(prev_out, self.hparams.pooling_type)
        with tf.variable_scope('output'):
            self._logits = {}
            self._predictions = {}
            self._weighted_accuracy = {}
            self._accuracy = {}
            self._loss = collections.OrderedDict()
            for target in self.targets:
                with tf.variable_scope(target):
                    label = labels[target]
                    possible_labels = self.possible_labels[target]
                    weights = self._init_weights([
                     pool_out.get_shape()[1].value,
                     len(possible_labels)],
                      (self.hparams.weight_scale),
                      name='weights')
                    biases = self._init_bias(len(possible_labels))
                    self._summary_histogram(weights.name.split(':')[0].split('/')[1], weights)
                    self._summary_histogram(biases.name.split(':')[0].split('/')[1], biases)
                    logits = tf.matmul(pool_out, weights) + biases
                    predictions = tf.nn.softmax(logits)
                    gather_inds = tf.stack([tf.range(batch_size), label], axis=1)
                    self._weighted_accuracy[target] = tf.reduce_mean(tf.gather_nd(predictions, gather_inds))
                    argmax_prediction = tf.cast(tf.argmax(predictions, axis=1), tf.int32)
                    self._accuracy[target] = tf.reduce_mean(tf.to_float(tf.equal(label, argmax_prediction)))
                    losses = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=label,
                      logits=logits)
                    self._loss[target] = tf.reduce_mean(losses)
                    self._logits[target] = logits
                    self._predictions[target] = predictions

        self._total_loss = tf.add_n(self._loss.values())
        self._global_step = tf.train.get_or_create_global_step()
        if self.hparams.lr_decay < 0:
            self._learn_rate = self.hparams.lr_init
        else:
            self._learn_rate = tf.train.exponential_decay((self.hparams.lr_init),
              (self._global_step),
              (int(self.hparams.train_steps)),
              (self.hparams.lr_decay),
              staircase=False)
        if self.hparams.optimizer == 'adam':
            opt = tf.train.AdamOptimizer(self._learn_rate, self.hparams.optimizer_hp)
        else:
            if self.hparams.optimizer == 'momentum':
                opt = tf.train.MomentumOptimizer(self._learn_rate, self.hparams.optimizer_hp)
            else:
                if self.use_tpu:
                    opt = tf.contrib.tpu.CrossShardOptimizer(opt)
                gradients, variables = zip(*opt.compute_gradients(self._total_loss))
                clipped_gradients, _ = tf.clip_by_global_norm(gradients, self.hparams.grad_clip_norm)
                with tf.control_dependencies(tf.get_collection(tf.GraphKeys.UPDATE_OPS)):
                    self._train_op = opt.apply_gradients((zip(clipped_gradients, variables)),
                      global_step=(self._global_step))
                grad_norm = self.use_tpu or (tf.global_norm(gradients) if is_train else None)
                param_norm = tf.global_norm(variables) if is_train else None
                self._add_summaries(mode, grad_norm, param_norm)

    def model_fn(self, features, labels, mode, params):
        """Function fulfilling the tf.estimator model_fn interface.

    Args:
      features: a dict containing the input features for prediction.
      labels: a dict from target name to Tensor-value prediction.
      mode: the ModeKey string.
      params: a dictionary of parameters for building the model; current params
        are params["batch_size"]: the integer batch size.

    Returns:
      A tf.estimator.EstimatorSpec object ready for use in training, inference.
      or evaluation.
    """
        self.build_graph(features, labels, mode, params['batch_size'])
        return tf.estimator.EstimatorSpec(mode,
          predictions=(self.predictions),
          loss=(self.total_loss),
          train_op=(self.train_op),
          eval_metric_ops={})