# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/global_objectives/loss_layers.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 41217 bytes
"""Loss functions for learning global objectives.

These functions have two return values: a Tensor with the value of
the loss, and a dictionary of internal quantities for customizability.
"""
import numpy, tensorflow as tf
from global_objectives import util

def precision_recall_auc_loss(labels, logits, precision_range=(0.0, 1.0), num_anchors=20, weights=1.0, dual_rate_factor=0.1, label_priors=None, surrogate_type='xent', lambdas_initializer=tf.constant_initializer(1.0), reuse=None, variables_collections=None, trainable=True, scope=None):
    """Computes precision-recall AUC loss.

  The loss is based on a sum of losses for recall at a range of
  precision values (anchor points). This sum is a Riemann sum that
  approximates the area under the precision-recall curve.

  The per-example `weights` argument changes not only the coefficients of
  individual training examples, but how the examples are counted toward the
  constraint. If `label_priors` is given, it MUST take `weights` into account.
  That is,
      label_priors = P / (P + N)
  where
      P = sum_i (wt_i on positives)
      N = sum_i (wt_i on negatives).

  Args:
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    logits: A `Tensor` with the same shape as `labels`.
    precision_range: A length-two tuple, the range of precision values over
      which to compute AUC. The entries must be nonnegative, increasing, and
      less than or equal to 1.0.
    num_anchors: The number of grid points used to approximate the Riemann sum.
    weights: Coefficients for the loss. Must be a scalar or `Tensor` of shape
      [batch_size] or [batch_size, num_labels].
    dual_rate_factor: A floating point value which controls the step size for
      the Lagrange multipliers.
    label_priors: None, or a floating point `Tensor` of shape [num_labels]
      containing the prior probability of each label (i.e. the fraction of the
      training data consisting of positive examples). If None, the label
      priors are computed from `labels` with a moving average. See the notes
      above regarding the interaction with `weights` and do not set this unless
      you have a good reason to do so.
    surrogate_type: Either 'xent' or 'hinge', specifying which upper bound
      should be used for indicator functions.
    lambdas_initializer: An initializer for the Lagrange multipliers.
    reuse: Whether or not the layer and its variables should be reused. To be
      able to reuse the layer scope must be given.
    variables_collections: Optional list of collections for the variables.
    trainable: If `True` also add variables to the graph collection
      `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).
    scope: Optional scope for `variable_scope`.

  Returns:
    loss: A `Tensor` of the same shape as `logits` with the component-wise
      loss.
    other_outputs: A dictionary of useful internal quantities for debugging. For
      more details, see http://arxiv.org/pdf/1608.04802.pdf.
      lambdas: A Tensor of shape [1, num_labels, num_anchors] consisting of the
        Lagrange multipliers.
      biases: A Tensor of shape [1, num_labels, num_anchors] consisting of the
        learned bias term for each.
      label_priors: A Tensor of shape [1, num_labels, 1] consisting of the prior
        probability of each label learned by the loss, if not provided.
      true_positives_lower_bound: Lower bound on the number of true positives
        given `labels` and `logits`. This is the same lower bound which is used
        in the loss expression to be optimized.
      false_positives_upper_bound: Upper bound on the number of false positives
        given `labels` and `logits`. This is the same upper bound which is used
        in the loss expression to be optimized.

  Raises:
    ValueError: If `surrogate_type` is not `xent` or `hinge`.
  """
    with tf.variable_scope(scope, 'precision_recall_auc',
      [
     labels, logits, label_priors],
      reuse=reuse):
        labels, logits, weights, original_shape = _prepare_labels_logits_weights(labels, logits, weights)
        num_labels = util.get_num_labels(logits)
        dual_rate_factor = util.convert_and_cast(dual_rate_factor, 'dual_rate_factor', logits.dtype)
        precision_values, delta = _range_to_anchors_and_delta(precision_range, num_anchors, logits.dtype)
        lambdas, lambdas_variable = _create_dual_variable('lambdas',
          shape=[
         1, num_labels, num_anchors],
          dtype=(logits.dtype),
          initializer=lambdas_initializer,
          collections=variables_collections,
          trainable=trainable,
          dual_rate_factor=dual_rate_factor)
        biases = tf.contrib.framework.model_variable(name='biases',
          shape=[
         1, num_labels, num_anchors],
          dtype=(logits.dtype),
          initializer=(tf.zeros_initializer()),
          collections=variables_collections,
          trainable=trainable)
        label_priors = maybe_create_label_priors(label_priors, labels, weights, variables_collections)
        label_priors = tf.reshape(label_priors, [1, num_labels, 1])
        logits = tf.expand_dims(logits, 2)
        labels = tf.expand_dims(labels, 2)
        weights = tf.expand_dims(weights, 2)
        loss = weights * util.weighted_surrogate_loss(labels,
          (logits + biases),
          surrogate_type=surrogate_type,
          positive_weights=(1.0 + lambdas * (1.0 - precision_values)),
          negative_weights=(lambdas * precision_values))
        maybe_log2 = tf.log(2.0) if surrogate_type == 'xent' else 1.0
        maybe_log2 = tf.cast(maybe_log2, logits.dtype.base_dtype)
        lambda_term = lambdas * (1.0 - precision_values) * label_priors * maybe_log2
        per_anchor_loss = loss - lambda_term
        per_label_loss = delta * tf.reduce_sum(per_anchor_loss, 2)
        scaled_loss = tf.div(per_label_loss, (precision_range[1] - precision_range[0] - delta),
          name='AUC_Normalize')
        scaled_loss = tf.reshape(scaled_loss, original_shape)
        other_outputs = {'lambdas':lambdas_variable, 
         'biases':biases, 
         'label_priors':label_priors, 
         'true_positives_lower_bound':true_positives_lower_bound(labels, logits, weights, surrogate_type), 
         'false_positives_upper_bound':false_positives_upper_bound(labels, logits, weights, surrogate_type)}
        return (
         scaled_loss, other_outputs)


def roc_auc_loss(labels, logits, weights=1.0, surrogate_type='xent', scope=None):
    """Computes ROC AUC loss.

  The area under the ROC curve is the probability p that a randomly chosen
  positive example will be scored higher than a randomly chosen negative
  example. This loss approximates 1-p by using a surrogate (either hinge loss or
  cross entropy) for the indicator function. Specifically, the loss is:

    sum_i sum_j w_i*w_j*loss(logit_i - logit_j)

  where i ranges over the positive datapoints, j ranges over the negative
  datapoints, logit_k denotes the logit (or score) of the k-th datapoint, and
  loss is either the hinge or log loss given a positive label.

  Args:
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    logits: A `Tensor` with the same shape and dtype as `labels`.
    weights: Coefficients for the loss. Must be a scalar or `Tensor` of shape
      [batch_size] or [batch_size, num_labels].
    surrogate_type: Either 'xent' or 'hinge', specifying which upper bound
      should be used for the indicator function.
    scope: Optional scope for `name_scope`.

  Returns:
    loss: A `Tensor` of the same shape as `logits` with the component-wise loss.
    other_outputs: An empty dictionary, for consistency.

  Raises:
    ValueError: If `surrogate_type` is not `xent` or `hinge`.
  """
    with tf.name_scope(scope, 'roc_auc', [labels, logits, weights]):
        labels, logits, weights, original_shape = _prepare_labels_logits_weights(labels, logits, weights)
        logits_difference = tf.expand_dims(logits, 0) - tf.expand_dims(logits, 1)
        labels_difference = tf.expand_dims(labels, 0) - tf.expand_dims(labels, 1)
        weights_product = tf.expand_dims(weights, 0) * tf.expand_dims(weights, 1)
        signed_logits_difference = labels_difference * logits_difference
        raw_loss = util.weighted_surrogate_loss(labels=(tf.ones_like(signed_logits_difference)),
          logits=signed_logits_difference,
          surrogate_type=surrogate_type)
        weighted_loss = weights_product * raw_loss
        loss = tf.reduce_mean(tf.abs(labels_difference) * weighted_loss, 0) * 0.5
        loss = tf.reshape(loss, original_shape)
        return (loss, {})


def recall_at_precision_loss(labels, logits, target_precision, weights=1.0, dual_rate_factor=0.1, label_priors=None, surrogate_type='xent', lambdas_initializer=tf.constant_initializer(1.0), reuse=None, variables_collections=None, trainable=True, scope=None):
    """Computes recall at precision loss.

  The loss is based on a surrogate of the form
      wt * w(+) * loss(+) + wt * w(-) * loss(-) - c * pi,
  where:
  - w(+) =  1 + lambdas * (1 - target_precision)
  - loss(+) is the cross-entropy loss on the positive examples
  - w(-) = lambdas * target_precision
  - loss(-) is the cross-entropy loss on the negative examples
  - wt is a scalar or tensor of per-example weights
  - c = lambdas * (1 - target_precision)
  - pi is the label_priors.

  The per-example weights change not only the coefficients of individual
  training examples, but how the examples are counted toward the constraint.
  If `label_priors` is given, it MUST take `weights` into account. That is,
      label_priors = P / (P + N)
  where
      P = sum_i (wt_i on positives)
      N = sum_i (wt_i on negatives).

  Args:
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    logits: A `Tensor` with the same shape as `labels`.
    target_precision: The precision at which to compute the loss. Can be a
      floating point value between 0 and 1 for a single precision value, or a
      `Tensor` of shape [num_labels], holding each label's target precision
      value.
    weights: Coefficients for the loss. Must be a scalar or `Tensor` of shape
      [batch_size] or [batch_size, num_labels].
    dual_rate_factor: A floating point value which controls the step size for
      the Lagrange multipliers.
    label_priors: None, or a floating point `Tensor` of shape [num_labels]
      containing the prior probability of each label (i.e. the fraction of the
      training data consisting of positive examples). If None, the label
      priors are computed from `labels` with a moving average. See the notes
      above regarding the interaction with `weights` and do not set this unless
      you have a good reason to do so.
    surrogate_type: Either 'xent' or 'hinge', specifying which upper bound
      should be used for indicator functions.
    lambdas_initializer: An initializer for the Lagrange multipliers.
    reuse: Whether or not the layer and its variables should be reused. To be
      able to reuse the layer scope must be given.
    variables_collections: Optional list of collections for the variables.
    trainable: If `True` also add variables to the graph collection
      `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).
    scope: Optional scope for `variable_scope`.

  Returns:
    loss: A `Tensor` of the same shape as `logits` with the component-wise
      loss.
    other_outputs: A dictionary of useful internal quantities for debugging. For
      more details, see http://arxiv.org/pdf/1608.04802.pdf.
      lambdas: A Tensor of shape [num_labels] consisting of the Lagrange
        multipliers.
      label_priors: A Tensor of shape [num_labels] consisting of the prior
        probability of each label learned by the loss, if not provided.
      true_positives_lower_bound: Lower bound on the number of true positives
        given `labels` and `logits`. This is the same lower bound which is used
        in the loss expression to be optimized.
      false_positives_upper_bound: Upper bound on the number of false positives
        given `labels` and `logits`. This is the same upper bound which is used
        in the loss expression to be optimized.

  Raises:
    ValueError: If `logits` and `labels` do not have the same shape.
  """
    with tf.variable_scope(scope, 'recall_at_precision',
      [
     logits, labels, label_priors],
      reuse=reuse):
        labels, logits, weights, original_shape = _prepare_labels_logits_weights(labels, logits, weights)
        num_labels = util.get_num_labels(logits)
        target_precision = util.convert_and_cast(target_precision, 'target_precision', logits.dtype)
        dual_rate_factor = util.convert_and_cast(dual_rate_factor, 'dual_rate_factor', logits.dtype)
        lambdas, lambdas_variable = _create_dual_variable('lambdas',
          shape=[
         num_labels],
          dtype=(logits.dtype),
          initializer=lambdas_initializer,
          collections=variables_collections,
          trainable=trainable,
          dual_rate_factor=dual_rate_factor)
        label_priors = maybe_create_label_priors(label_priors, labels, weights, variables_collections)
        weighted_loss = weights * util.weighted_surrogate_loss(labels,
          logits,
          surrogate_type=surrogate_type,
          positive_weights=(1.0 + lambdas * (1.0 - target_precision)),
          negative_weights=(lambdas * target_precision))
        maybe_log2 = tf.log(2.0) if surrogate_type == 'xent' else 1.0
        maybe_log2 = tf.cast(maybe_log2, logits.dtype.base_dtype)
        lambda_term = lambdas * (1.0 - target_precision) * label_priors * maybe_log2
        loss = tf.reshape(weighted_loss - lambda_term, original_shape)
        other_outputs = {'lambdas':lambdas_variable, 
         'label_priors':label_priors, 
         'true_positives_lower_bound':true_positives_lower_bound(labels, logits, weights, surrogate_type), 
         'false_positives_upper_bound':false_positives_upper_bound(labels, logits, weights, surrogate_type)}
        return (
         loss, other_outputs)


def precision_at_recall_loss(labels, logits, target_recall, weights=1.0, dual_rate_factor=0.1, label_priors=None, surrogate_type='xent', lambdas_initializer=tf.constant_initializer(1.0), reuse=None, variables_collections=None, trainable=True, scope=None):
    """Computes precision at recall loss.

  The loss is based on a surrogate of the form
     wt * loss(-) + lambdas * (pi * (b - 1) + wt * loss(+))
  where:
  - loss(-) is the cross-entropy loss on the negative examples
  - loss(+) is the cross-entropy loss on the positive examples
  - wt is a scalar or tensor of per-example weights
  - b is the target recall
  - pi is the label_priors.

  The per-example weights change not only the coefficients of individual
  training examples, but how the examples are counted toward the constraint.
  If `label_priors` is given, it MUST take `weights` into account. That is,
      label_priors = P / (P + N)
  where
      P = sum_i (wt_i on positives)
      N = sum_i (wt_i on negatives).

  Args:
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    logits: A `Tensor` with the same shape as `labels`.
    target_recall: The recall at which to compute the loss. Can be a floating
      point value between 0 and 1 for a single target recall value, or a
      `Tensor` of shape [num_labels] holding each label's target recall value.
    weights: Coefficients for the loss. Must be a scalar or `Tensor` of shape
      [batch_size] or [batch_size, num_labels].
    dual_rate_factor: A floating point value which controls the step size for
      the Lagrange multipliers.
    label_priors: None, or a floating point `Tensor` of shape [num_labels]
      containing the prior probability of each label (i.e. the fraction of the
      training data consisting of positive examples). If None, the label
      priors are computed from `labels` with a moving average. See the notes
      above regarding the interaction with `weights` and do not set this unless
      you have a good reason to do so.
    surrogate_type: Either 'xent' or 'hinge', specifying which upper bound
      should be used for indicator functions.
    lambdas_initializer: An initializer for the Lagrange multipliers.
    reuse: Whether or not the layer and its variables should be reused. To be
      able to reuse the layer scope must be given.
    variables_collections: Optional list of collections for the variables.
    trainable: If `True` also add variables to the graph collection
      `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).
    scope: Optional scope for `variable_scope`.

  Returns:
    loss: A `Tensor` of the same shape as `logits` with the component-wise
      loss.
    other_outputs: A dictionary of useful internal quantities for debugging. For
      more details, see http://arxiv.org/pdf/1608.04802.pdf.
      lambdas: A Tensor of shape [num_labels] consisting of the Lagrange
        multipliers.
      label_priors: A Tensor of shape [num_labels] consisting of the prior
        probability of each label learned by the loss, if not provided.
      true_positives_lower_bound: Lower bound on the number of true positives
        given `labels` and `logits`. This is the same lower bound which is used
        in the loss expression to be optimized.
      false_positives_upper_bound: Upper bound on the number of false positives
        given `labels` and `logits`. This is the same upper bound which is used
        in the loss expression to be optimized.
  """
    with tf.variable_scope(scope, 'precision_at_recall',
      [
     logits, labels, label_priors],
      reuse=reuse):
        labels, logits, weights, original_shape = _prepare_labels_logits_weights(labels, logits, weights)
        num_labels = util.get_num_labels(logits)
        target_recall = util.convert_and_cast(target_recall, 'target_recall', logits.dtype)
        dual_rate_factor = util.convert_and_cast(dual_rate_factor, 'dual_rate_factor', logits.dtype)
        lambdas, lambdas_variable = _create_dual_variable('lambdas',
          shape=[
         num_labels],
          dtype=(logits.dtype),
          initializer=lambdas_initializer,
          collections=variables_collections,
          trainable=trainable,
          dual_rate_factor=dual_rate_factor)
        label_priors = maybe_create_label_priors(label_priors, labels, weights, variables_collections)
        weighted_loss = weights * util.weighted_surrogate_loss(labels,
          logits,
          surrogate_type,
          positive_weights=lambdas,
          negative_weights=1.0)
        maybe_log2 = tf.log(2.0) if surrogate_type == 'xent' else 1.0
        maybe_log2 = tf.cast(maybe_log2, logits.dtype.base_dtype)
        lambda_term = lambdas * label_priors * (target_recall - 1.0) * maybe_log2
        loss = tf.reshape(weighted_loss + lambda_term, original_shape)
        other_outputs = {'lambdas':lambdas_variable, 
         'label_priors':label_priors, 
         'true_positives_lower_bound':true_positives_lower_bound(labels, logits, weights, surrogate_type), 
         'false_positives_upper_bound':false_positives_upper_bound(labels, logits, weights, surrogate_type)}
        return (
         loss, other_outputs)


def false_positive_rate_at_true_positive_rate_loss(labels, logits, target_rate, weights=1.0, dual_rate_factor=0.1, label_priors=None, surrogate_type='xent', lambdas_initializer=tf.constant_initializer(1.0), reuse=None, variables_collections=None, trainable=True, scope=None):
    """Computes false positive rate at true positive rate loss.

  Note that `true positive rate` is a synonym for Recall, and that minimizing
  the false positive rate and maximizing precision are equivalent for a fixed
  Recall. Therefore, this function is identical to precision_at_recall_loss.

  The per-example weights change not only the coefficients of individual
  training examples, but how the examples are counted toward the constraint.
  If `label_priors` is given, it MUST take `weights` into account. That is,
      label_priors = P / (P + N)
  where
      P = sum_i (wt_i on positives)
      N = sum_i (wt_i on negatives).

  Args:
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    logits: A `Tensor` with the same shape as `labels`.
    target_rate: The true positive rate at which to compute the loss. Can be a
      floating point value between 0 and 1 for a single true positive rate, or
      a `Tensor` of shape [num_labels] holding each label's true positive rate.
    weights: Coefficients for the loss. Must be a scalar or `Tensor` of shape
      [batch_size] or [batch_size, num_labels].
    dual_rate_factor: A floating point value which controls the step size for
      the Lagrange multipliers.
    label_priors: None, or a floating point `Tensor` of shape [num_labels]
      containing the prior probability of each label (i.e. the fraction of the
      training data consisting of positive examples). If None, the label
      priors are computed from `labels` with a moving average. See the notes
      above regarding the interaction with `weights` and do not set this unless
      you have a good reason to do so.
    surrogate_type: Either 'xent' or 'hinge', specifying which upper bound
      should be used for indicator functions. 'xent' will use the cross-entropy
      loss surrogate, and 'hinge' will use the hinge loss.
    lambdas_initializer: An initializer op for the Lagrange multipliers.
    reuse: Whether or not the layer and its variables should be reused. To be
      able to reuse the layer scope must be given.
    variables_collections: Optional list of collections for the variables.
    trainable: If `True` also add variables to the graph collection
      `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).
    scope: Optional scope for `variable_scope`.

  Returns:
    loss: A `Tensor` of the same shape as `logits` with the component-wise
      loss.
    other_outputs: A dictionary of useful internal quantities for debugging. For
      more details, see http://arxiv.org/pdf/1608.04802.pdf.
      lambdas: A Tensor of shape [num_labels] consisting of the Lagrange
        multipliers.
      label_priors: A Tensor of shape [num_labels] consisting of the prior
        probability of each label learned by the loss, if not provided.
      true_positives_lower_bound: Lower bound on the number of true positives
        given `labels` and `logits`. This is the same lower bound which is used
        in the loss expression to be optimized.
      false_positives_upper_bound: Upper bound on the number of false positives
        given `labels` and `logits`. This is the same upper bound which is used
        in the loss expression to be optimized.

  Raises:
    ValueError: If `surrogate_type` is not `xent` or `hinge`.
  """
    return precision_at_recall_loss(labels=labels, logits=logits,
      target_recall=target_rate,
      weights=weights,
      dual_rate_factor=dual_rate_factor,
      label_priors=label_priors,
      surrogate_type=surrogate_type,
      lambdas_initializer=lambdas_initializer,
      reuse=reuse,
      variables_collections=variables_collections,
      trainable=trainable,
      scope=scope)


def true_positive_rate_at_false_positive_rate_loss(labels, logits, target_rate, weights=1.0, dual_rate_factor=0.1, label_priors=None, surrogate_type='xent', lambdas_initializer=tf.constant_initializer(1.0), reuse=None, variables_collections=None, trainable=True, scope=None):
    """Computes true positive rate at false positive rate loss.

  The loss is based on a surrogate of the form
      wt * loss(+) + lambdas * (wt * loss(-) - r * (1 - pi))
  where:
  - loss(-) is the loss on the negative examples
  - loss(+) is the loss on the positive examples
  - wt is a scalar or tensor of per-example weights
  - r is the target rate
  - pi is the label_priors.

  The per-example weights change not only the coefficients of individual
  training examples, but how the examples are counted toward the constraint.
  If `label_priors` is given, it MUST take `weights` into account. That is,
      label_priors = P / (P + N)
  where
      P = sum_i (wt_i on positives)
      N = sum_i (wt_i on negatives).

  Args:
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    logits: A `Tensor` with the same shape as `labels`.
    target_rate: The false positive rate at which to compute the loss. Can be a
      floating point value between 0 and 1 for a single false positive rate, or
      a `Tensor` of shape [num_labels] holding each label's false positive rate.
    weights: Coefficients for the loss. Must be a scalar or `Tensor` of shape
      [batch_size] or [batch_size, num_labels].
    dual_rate_factor: A floating point value which controls the step size for
      the Lagrange multipliers.
    label_priors: None, or a floating point `Tensor` of shape [num_labels]
      containing the prior probability of each label (i.e. the fraction of the
      training data consisting of positive examples). If None, the label
      priors are computed from `labels` with a moving average. See the notes
      above regarding the interaction with `weights` and do not set this unless
      you have a good reason to do so.
    surrogate_type: Either 'xent' or 'hinge', specifying which upper bound
      should be used for indicator functions. 'xent' will use the cross-entropy
      loss surrogate, and 'hinge' will use the hinge loss.
    lambdas_initializer: An initializer op for the Lagrange multipliers.
    reuse: Whether or not the layer and its variables should be reused. To be
      able to reuse the layer scope must be given.
    variables_collections: Optional list of collections for the variables.
    trainable: If `True` also add variables to the graph collection
      `GraphKeys.TRAINABLE_VARIABLES` (see `tf.Variable`).
    scope: Optional scope for `variable_scope`.

  Returns:
    loss: A `Tensor` of the same shape as `logits` with the component-wise
      loss.
    other_outputs: A dictionary of useful internal quantities for debugging. For
      more details, see http://arxiv.org/pdf/1608.04802.pdf.
      lambdas: A Tensor of shape [num_labels] consisting of the Lagrange
        multipliers.
      label_priors: A Tensor of shape [num_labels] consisting of the prior
        probability of each label learned by the loss, if not provided.
      true_positives_lower_bound: Lower bound on the number of true positives
        given `labels` and `logits`. This is the same lower bound which is used
        in the loss expression to be optimized.
      false_positives_upper_bound: Upper bound on the number of false positives
        given `labels` and `logits`. This is the same upper bound which is used
        in the loss expression to be optimized.

  Raises:
    ValueError: If `surrogate_type` is not `xent` or `hinge`.
  """
    with tf.variable_scope(scope, 'tpr_at_fpr',
      [
     labels, logits, label_priors],
      reuse=reuse):
        labels, logits, weights, original_shape = _prepare_labels_logits_weights(labels, logits, weights)
        num_labels = util.get_num_labels(logits)
        target_rate = util.convert_and_cast(target_rate, 'target_rate', logits.dtype)
        dual_rate_factor = util.convert_and_cast(dual_rate_factor, 'dual_rate_factor', logits.dtype)
        lambdas, lambdas_variable = _create_dual_variable('lambdas',
          shape=[
         num_labels],
          dtype=(logits.dtype),
          initializer=lambdas_initializer,
          collections=variables_collections,
          trainable=trainable,
          dual_rate_factor=dual_rate_factor)
        label_priors = maybe_create_label_priors(label_priors, labels, weights, variables_collections)
        weighted_loss = weights * util.weighted_surrogate_loss(labels,
          logits,
          surrogate_type=surrogate_type,
          positive_weights=1.0,
          negative_weights=lambdas)
        maybe_log2 = tf.log(2.0) if surrogate_type == 'xent' else 1.0
        maybe_log2 = tf.cast(maybe_log2, logits.dtype.base_dtype)
        lambda_term = lambdas * target_rate * (1.0 - label_priors) * maybe_log2
        loss = tf.reshape(weighted_loss - lambda_term, original_shape)
        other_outputs = {'lambdas':lambdas_variable, 
         'label_priors':label_priors, 
         'true_positives_lower_bound':true_positives_lower_bound(labels, logits, weights, surrogate_type), 
         'false_positives_upper_bound':false_positives_upper_bound(labels, logits, weights, surrogate_type)}
    return (loss, other_outputs)


def _prepare_labels_logits_weights(labels, logits, weights):
    """Validates labels, logits, and weights.

  Converts inputs to tensors, checks shape compatibility, and casts dtype if
  necessary.

  Args:
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    logits: A `Tensor` with the same shape as `labels`.
    weights: Either `None` or a `Tensor` with shape broadcastable to `logits`.

  Returns:
    labels: Same as `labels` arg after possible conversion to tensor, cast, and
      reshape.
    logits: Same as `logits` arg after possible conversion to tensor and
      reshape.
    weights: Same as `weights` arg after possible conversion, cast, and reshape.
    original_shape: Shape of `labels` and `logits` before reshape.

  Raises:
    ValueError: If `labels` and `logits` do not have the same shape.
  """
    logits = tf.convert_to_tensor(logits, name='logits')
    labels = util.convert_and_cast(labels, 'labels', logits.dtype.base_dtype)
    weights = util.convert_and_cast(weights, 'weights', logits.dtype.base_dtype)
    try:
        labels.get_shape().merge_with(logits.get_shape())
    except ValueError:
        raise ValueError('logits and labels must have the same shape (%s vs %s)' % (
         logits.get_shape(), labels.get_shape()))

    original_shape = labels.get_shape().as_list()
    if labels.get_shape().ndims > 0:
        original_shape[0] = -1
    if labels.get_shape().ndims <= 1:
        labels = tf.reshape(labels, [-1, 1])
        logits = tf.reshape(logits, [-1, 1])
    if weights.get_shape().ndims == 1:
        weights = tf.reshape(weights, [-1, 1])
    if weights.get_shape().ndims == 0:
        weights *= tf.ones_like(logits)
    return (labels, logits, weights, original_shape)


def _range_to_anchors_and_delta--- This code section failed: ---

 L. 779         0  LOAD_CONST               0
                2  LOAD_FAST                'precision_range'
                4  LOAD_CONST               0
                6  BINARY_SUBSCR    
                8  DUP_TOP          
               10  ROT_THREE        
               12  COMPARE_OP               <=
               14  POP_JUMP_IF_FALSE    38  'to 38'
               16  LOAD_FAST                'precision_range'
               18  LOAD_CONST               -1
               20  BINARY_SUBSCR    
               22  DUP_TOP          
               24  ROT_THREE        
               26  COMPARE_OP               <=
               28  POP_JUMP_IF_FALSE    38  'to 38'
               30  LOAD_CONST               1
               32  COMPARE_OP               <=
               34  POP_JUMP_IF_TRUE     64  'to 64'
               36  JUMP_FORWARD         40  'to 40'
             38_0  COME_FROM            28  '28'
             38_1  COME_FROM            14  '14'
               38  POP_TOP          
             40_0  COME_FROM            36  '36'

 L. 780        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 'precision values must obey 0 <= %f <= %f <= 1'

 L. 781        44  LOAD_FAST                'precision_range'
               46  LOAD_CONST               0
               48  BINARY_SUBSCR    
               50  LOAD_FAST                'precision_range'
               52  LOAD_CONST               -1
               54  BINARY_SUBSCR    
               56  BUILD_TUPLE_2         2 
               58  BINARY_MODULO    
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  RAISE_VARARGS_1       1  'exception instance'
             64_0  COME_FROM            34  '34'

 L. 782        64  LOAD_CONST               0
               66  LOAD_GLOBAL              len
               68  LOAD_FAST                'precision_range'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  DUP_TOP          
               74  ROT_THREE        
               76  COMPARE_OP               <
               78  POP_JUMP_IF_FALSE    88  'to 88'
               80  LOAD_CONST               3
               82  COMPARE_OP               <
               84  POP_JUMP_IF_TRUE    106  'to 106'
               86  JUMP_FORWARD         90  'to 90'
             88_0  COME_FROM            78  '78'
               88  POP_TOP          
             90_0  COME_FROM            86  '86'

 L. 783        90  LOAD_GLOBAL              ValueError
               92  LOAD_STR                 'length of precision_range (%d) must be 1 or 2'

 L. 784        94  LOAD_GLOBAL              len
               96  LOAD_FAST                'precision_range'
               98  CALL_FUNCTION_1       1  '1 positional argument'
              100  BINARY_MODULO    
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  RAISE_VARARGS_1       1  'exception instance'
            106_0  COME_FROM            84  '84'

 L. 787       106  LOAD_GLOBAL              numpy
              108  LOAD_ATTR                linspace
              110  LOAD_FAST                'precision_range'
              112  LOAD_CONST               0
              114  BINARY_SUBSCR    

 L. 788       116  LOAD_FAST                'precision_range'
              118  LOAD_CONST               1
              120  BINARY_SUBSCR    

 L. 789       122  LOAD_FAST                'num_anchors'
              124  LOAD_CONST               2
              126  BINARY_ADD       
              128  LOAD_CONST               ('start', 'stop', 'num')
              130  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              132  LOAD_CONST               1
              134  LOAD_CONST               -1
              136  BUILD_SLICE_2         2 
              138  BINARY_SUBSCR    
              140  STORE_FAST               'values'

 L. 790       142  LOAD_GLOBAL              util
              144  LOAD_METHOD              convert_and_cast

 L. 791       146  LOAD_FAST                'values'
              148  LOAD_STR                 'precision_values'
              150  LOAD_FAST                'dtype'
              152  CALL_METHOD_3         3  '3 positional arguments'
              154  STORE_FAST               'precision_values'

 L. 792       156  LOAD_GLOBAL              util
              158  LOAD_METHOD              convert_and_cast

 L. 793       160  LOAD_FAST                'values'
              162  LOAD_CONST               0
              164  BINARY_SUBSCR    
              166  LOAD_FAST                'precision_range'
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  BINARY_SUBTRACT  
              174  LOAD_STR                 'delta'
              176  LOAD_FAST                'dtype'
              178  CALL_METHOD_3         3  '3 positional arguments'
              180  STORE_FAST               'delta'

 L. 795       182  LOAD_GLOBAL              util
              184  LOAD_METHOD              expand_outer
              186  LOAD_FAST                'precision_values'
              188  LOAD_CONST               3
              190  CALL_METHOD_2         2  '2 positional arguments'
              192  STORE_FAST               'precision_values'

 L. 796       194  LOAD_FAST                'precision_values'
              196  LOAD_FAST                'delta'
              198  BUILD_TUPLE_2         2 
              200  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def _create_dual_variable(name, shape, dtype, initializer, collections, trainable, dual_rate_factor):
    """Creates a new dual variable.

  Dual variables are required to be nonnegative. If trainable, their gradient
  is reversed so that they are maximized (rather than minimized) by the
  optimizer.

  Args:
    name: A string, the name for the new variable.
    shape: Shape of the new variable.
    dtype: Data type for the new variable.
    initializer: Initializer for the new variable.
    collections: List of graph collections keys. The new variable is added to
      these collections. Defaults to `[GraphKeys.GLOBAL_VARIABLES]`.
    trainable: If `True`, the default, also adds the variable to the graph
      collection `GraphKeys.TRAINABLE_VARIABLES`. This collection is used as
      the default list of variables to use by the `Optimizer` classes.
    dual_rate_factor: A floating point value or `Tensor`. The learning rate for
      the dual variable is scaled by this factor.

  Returns:
    dual_value: An op that computes the absolute value of the dual variable
      and reverses its gradient.
    dual_variable: The underlying variable itself.
  """
    partitioner = tf.get_variable_scope().partitioner
    try:
        tf.get_variable_scope().set_partitioner(None)
        dual_variable = tf.contrib.framework.model_variable(name=name,
          shape=shape,
          dtype=dtype,
          initializer=initializer,
          collections=collections,
          trainable=trainable)
    finally:
        tf.get_variable_scope().set_partitioner(partitioner)

    dual_value = tf.abs(dual_variable)
    if trainable:
        dual_value = tf.stop_gradient((1.0 + dual_rate_factor) * dual_value) - dual_rate_factor * dual_value
    return (
     dual_value, dual_variable)


def maybe_create_label_priors(label_priors, labels, weights, variables_collections):
    """Creates moving average ops to track label priors, if necessary.

  Args:
    label_priors: As required in e.g. precision_recall_auc_loss.
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    weights: As required in e.g. precision_recall_auc_loss.
    variables_collections: Optional list of collections for the variables, if
      any must be created.

  Returns:
    label_priors: A Tensor of shape [num_labels] consisting of the
      weighted label priors, after updating with moving average ops if created.
  """
    if label_priors is not None:
        label_priors = util.convert_and_cast(label_priors,
          name='label_priors', dtype=(labels.dtype.base_dtype))
        return tf.squeeze(label_priors)
    label_priors = util.build_label_priors(labels,
      weights,
      variables_collections=variables_collections)
    return label_priors


def true_positives_lower_bound(labels, logits, weights, surrogate_type):
    """Calculate a lower bound on the number of true positives.

  This lower bound on the number of true positives given `logits` and `labels`
  is the same one used in the global objectives loss functions.

  Args:
    labels: A `Tensor` of shape [batch_size] or [batch_size, num_labels].
    logits: A `Tensor` of shape [batch_size, num_labels] or
      [batch_size, num_labels, num_anchors]. If the third dimension is present,
      the lower bound is computed on each slice [:, :, k] independently.
    weights: Per-example loss coefficients, with shape broadcast-compatible with
        that of `labels`.
    surrogate_type: Either 'xent' or 'hinge', specifying which upper bound
      should be used for indicator functions.

  Returns:
    A `Tensor` of shape [num_labels] or [num_labels, num_anchors].
  """
    maybe_log2 = tf.log(2.0) if surrogate_type == 'xent' else 1.0
    maybe_log2 = tf.cast(maybe_log2, logits.dtype.base_dtype)
    if logits.get_shape().ndims == 3:
        if labels.get_shape().ndims < 3:
            labels = tf.expand_dims(labels, 2)
    loss_on_positives = util.weighted_surrogate_loss(labels,
      logits, surrogate_type, negative_weights=0.0) / maybe_log2
    return tf.reduce_sum(weights * (labels - loss_on_positives), 0)


def false_positives_upper_bound(labels, logits, weights, surrogate_type):
    """Calculate an upper bound on the number of false positives.

  This upper bound on the number of false positives given `logits` and `labels`
  is the same one used in the global objectives loss functions.

  Args:
    labels: A `Tensor` of shape [batch_size, num_labels]
    logits: A `Tensor` of shape [batch_size, num_labels]  or
      [batch_size, num_labels, num_anchors]. If the third dimension is present,
      the lower bound is computed on each slice [:, :, k] independently.
    weights: Per-example loss coefficients, with shape broadcast-compatible with
        that of `labels`.
    surrogate_type: Either 'xent' or 'hinge', specifying which upper bound
      should be used for indicator functions.

  Returns:
    A `Tensor` of shape [num_labels] or [num_labels, num_anchors].
  """
    maybe_log2 = tf.log(2.0) if surrogate_type == 'xent' else 1.0
    maybe_log2 = tf.cast(maybe_log2, logits.dtype.base_dtype)
    loss_on_negatives = util.weighted_surrogate_loss(labels,
      logits, surrogate_type, positive_weights=0.0) / maybe_log2
    return tf.reduce_sum(weights * loss_on_negatives, 0)