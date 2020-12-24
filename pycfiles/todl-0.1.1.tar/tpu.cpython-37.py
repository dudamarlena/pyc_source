# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/r1/utils/tpu.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 4656 bytes
"""Functions specific to running TensorFlow on TPUs."""
import tensorflow as tf
LOCAL = 'local'

def construct_scalar_host_call(metric_dict, model_dir, prefix=''):
    """Construct a host call to log scalars when training on TPU.

  Args:
    metric_dict: A dict of the tensors to be logged.
    model_dir: The location to write the summary.
    prefix: The prefix (if any) to prepend to the metric names.

  Returns:
    A tuple of (function, args_to_be_passed_to_said_function)
  """
    metric_names = list(metric_dict.keys())

    def host_call_fn(global_step, *args):
        step = global_step[0]
        with tf.compat.v1.summary.create_file_writer(logdir=model_dir,
          filename_suffix='.host_call').as_default():
            with tf.compat.v1.summary.always_record_summaries():
                for i, name in enumerate(metric_names):
                    tf.compat.v1.summary.scalar((prefix + name), (args[i][0]), step=step)

                return tf.compat.v1.summary.all_summary_ops()

    global_step_tensor = tf.reshape(tf.compat.v1.train.get_or_create_global_step(), [1])
    other_tensors = [tf.reshape(metric_dict[key], [1]) for key in metric_names]
    return (
     host_call_fn, [global_step_tensor] + other_tensors)


def embedding_matmul(embedding_table, values, mask, name='embedding_matmul'):
    """Performs embedding lookup via a matmul.

  The matrix to be multiplied by the embedding table Tensor is constructed
  via an implementation of scatter based on broadcasting embedding indices
  and performing an equality comparison against a broadcasted
  range(num_embedding_table_rows). All masked positions will produce an
  embedding vector of zeros.

  Args:
    embedding_table: Tensor of embedding table.
      Rank 2 (table_size x embedding dim)
    values: Tensor of embedding indices. Rank 2 (batch x n_indices)
    mask: Tensor of mask / weights. Rank 2 (batch x n_indices)
    name: Optional name scope for created ops

  Returns:
    Rank 3 tensor of embedding vectors.
  """
    with tf.name_scope(name):
        n_embeddings = embedding_table.get_shape().as_list()[0]
        batch_size, padded_size = values.shape.as_list()
        emb_idcs = tf.tile(tf.reshape(values, (batch_size, padded_size, 1)), (1, 1, n_embeddings))
        emb_weights = tf.tile(tf.reshape(mask, (batch_size, padded_size, 1)), (1, 1, n_embeddings))
        col_idcs = tf.tile(tf.reshape(tf.range(n_embeddings), (1, 1, n_embeddings)), (
         batch_size, padded_size, 1))
        one_hot = tf.where(tf.equal(emb_idcs, col_idcs), emb_weights, tf.zeros((batch_size, padded_size, n_embeddings)))
        return tf.tensordot(one_hot, embedding_table, 1)