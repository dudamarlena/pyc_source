# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/official/nlp/transformer/beam_search_v1.py
# Compiled at: 2020-04-05 19:50:57
# Size of source mod 2**32: 27301 bytes
"""Beam search to find the translated sequence with the highest probability.

Source implementation from Tensor2Tensor:
https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/utils/beam_search.py
"""
import numpy as np
import tensorflow.compat.v1 as tf
from tensorflow.python.util import nest

def inf(dtype):
    """Returns a value close to infinity, but is still finite in `dtype`.

  This is useful to get a very large value that is still zero when multiplied by
  zero. The floating-point "Inf" value is NaN when multiplied by zero.

  Args:
    dtype: A dtype. The returned value will be finite when casted to this dtype.

  Returns:
    A very large value.
  """
    if dtype == 'float32' or dtype == 'bfloat16':
        return 10000000.0
    if dtype == 'float16':
        return np.finfo(np.float16).max
    raise AssertionError('Invalid dtype: %s' % dtype)


class _StateKeys(object):
    __doc__ = 'Keys to dictionary storing the state of the beam search loop.'
    CUR_INDEX = 'CUR_INDEX'
    ALIVE_SEQ = 'ALIVE_SEQ'
    ALIVE_LOG_PROBS = 'ALIVE_LOG_PROBS'
    ALIVE_CACHE = 'ALIVE_CACHE'
    FINISHED_SEQ = 'FINISHED_SEQ'
    FINISHED_SCORES = 'FINISHED_SCORES'
    FINISHED_FLAGS = 'FINISHED_FLAGS'


class SequenceBeamSearch(object):
    __doc__ = 'Implementation of beam search loop.'

    def __init__(self, symbols_to_logits_fn, vocab_size, batch_size, beam_size, alpha, max_decode_length, eos_id, padded_decode, dtype=tf.float32):
        """Initialize sequence beam search.

    Args:
      symbols_to_logits_fn: A function to provide logits, which is the
        interface to the Transformer model. The passed in arguments are:
          ids -> A tensor with shape [batch_size * beam_size, index].
          index -> A scalar.
          cache -> A nested dictionary of tensors [batch_size * beam_size, ...].
        The function must return a tuple of logits and the updated cache:
          logits -> A tensor with shape [batch * beam_size, vocab_size].
          updated cache -> A nested dictionary with the same structure as the
            input cache.
      vocab_size: An integer, the size of the vocabulary, used for topk
        computation.
      batch_size: An integer, the decode batch size.
      beam_size: An integer, number of beams for beam search.
      alpha: A float, defining the strength of length normalization.
      max_decode_length: An integer, the maximum number of steps to decode
        a sequence.
      eos_id: An integer. ID of end of sentence token.
      padded_decode: A bool, indicating if max_sequence_length padding is used
        for beam search.
      dtype: A tensorflow data type used for score computation. The default is
        tf.float32.
    """
        self.symbols_to_logits_fn = symbols_to_logits_fn
        self.vocab_size = vocab_size
        self.batch_size = batch_size
        self.beam_size = beam_size
        self.alpha = alpha
        self.max_decode_length = max_decode_length
        self.eos_id = eos_id
        self.padded_decode = padded_decode
        self.dtype = tf.as_dtype(dtype)

    def search(self, initial_ids, initial_cache):
        """Beam search for sequences with highest scores."""
        state, state_shapes = self._create_initial_state(initial_ids, initial_cache)
        finished_state = tf.while_loop((self._continue_search),
          (self._search_step), loop_vars=[state], shape_invariants=[
         state_shapes],
          parallel_iterations=1,
          back_prop=False)
        finished_state = finished_state[0]
        alive_seq = finished_state[_StateKeys.ALIVE_SEQ]
        alive_log_probs = finished_state[_StateKeys.ALIVE_LOG_PROBS]
        finished_seq = finished_state[_StateKeys.FINISHED_SEQ]
        finished_scores = finished_state[_StateKeys.FINISHED_SCORES]
        finished_flags = finished_state[_StateKeys.FINISHED_FLAGS]
        finished_seq = tf.where(tf.reduce_any(finished_flags, 1), finished_seq, alive_seq)
        finished_scores = tf.where(tf.reduce_any(finished_flags, 1), finished_scores, alive_log_probs)
        return (finished_seq, finished_scores)

    def _create_initial_state(self, initial_ids, initial_cache):
        """Return initial state dictionary and its shape invariants.

    Args:
      initial_ids: initial ids to pass into the symbols_to_logits_fn.
        int tensor with shape [batch_size, 1]
      initial_cache: dictionary storing values to be passed into the
        symbols_to_logits_fn.

    Returns:
        state and shape invariant dictionaries with keys from _StateKeys
    """
        for key, value in initial_cache.items():
            for inner_value in nest.flatten(value):
                if inner_value.dtype != self.dtype:
                    raise TypeError("initial_cache element for key '%s' has dtype %s that does not match SequenceBeamSearch's dtype of %s. Value: %s" % (
                     key, value.dtype.name, self.dtype.name, inner_value))

        cur_index = tf.constant(0)
        alive_seq = _expand_to_beam_size(initial_ids, self.beam_size)
        alive_seq = tf.expand_dims(alive_seq, axis=2)
        if self.padded_decode:
            alive_seq = tf.tile(alive_seq, [1, 1, self.max_decode_length + 1])
        else:
            initial_log_probs = tf.constant([
             [
              0.0] + [-float('inf')] * (self.beam_size - 1)],
              dtype=(self.dtype))
            alive_log_probs = tf.tile(initial_log_probs, [self.batch_size, 1])
            alive_cache = nest.map_structure(lambda t: _expand_to_beam_size(t, self.beam_size), initial_cache)
            finished_seq = tf.zeros(tf.shape(alive_seq), tf.int32)
            finished_scores = tf.ones([self.batch_size, self.beam_size], dtype=(self.dtype)) * -inf(self.dtype)
            finished_flags = tf.zeros([self.batch_size, self.beam_size], tf.bool)
            state = {_StateKeys.CUR_INDEX: cur_index, 
             _StateKeys.ALIVE_SEQ: alive_seq, 
             _StateKeys.ALIVE_LOG_PROBS: alive_log_probs, 
             _StateKeys.ALIVE_CACHE: alive_cache, 
             _StateKeys.FINISHED_SEQ: finished_seq, 
             _StateKeys.FINISHED_SCORES: finished_scores, 
             _StateKeys.FINISHED_FLAGS: finished_flags}
            if self.padded_decode:
                state_shape_invariants = {_StateKeys.CUR_INDEX: tf.TensorShape([]), 
                 
                 _StateKeys.ALIVE_SEQ: tf.TensorShape([
                                        self.batch_size, self.beam_size,
                                        self.max_decode_length + 1]), 
                 
                 _StateKeys.ALIVE_LOG_PROBS: tf.TensorShape([self.batch_size, self.beam_size]), 
                 
                 _StateKeys.ALIVE_CACHE: nest.map_structure(_get_shape, alive_cache), 
                 
                 _StateKeys.FINISHED_SEQ: tf.TensorShape([
                                           self.batch_size, self.beam_size,
                                           self.max_decode_length + 1]), 
                 
                 _StateKeys.FINISHED_SCORES: tf.TensorShape([self.batch_size, self.beam_size]), 
                 
                 _StateKeys.FINISHED_FLAGS: tf.TensorShape([self.batch_size, self.beam_size])}
            else:
                state_shape_invariants = {_StateKeys.CUR_INDEX: tf.TensorShape([]), 
                 
                 _StateKeys.ALIVE_SEQ: tf.TensorShape([None, self.beam_size, None]), 
                 
                 _StateKeys.ALIVE_LOG_PROBS: tf.TensorShape([None, self.beam_size]), 
                 
                 _StateKeys.ALIVE_CACHE: nest.map_structure(_get_shape_keep_last_dim, alive_cache), 
                 
                 _StateKeys.FINISHED_SEQ: tf.TensorShape([None, self.beam_size, None]), 
                 
                 _StateKeys.FINISHED_SCORES: tf.TensorShape([None, self.beam_size]), 
                 
                 _StateKeys.FINISHED_FLAGS: tf.TensorShape([None, self.beam_size])}
        return (state, state_shape_invariants)

    def _continue_search(self, state):
        """Return whether to continue the search loop.

    The loops should terminate when
      1) when decode length has been reached, or
      2) when the worst score in the finished sequences is better than the best
         score in the alive sequences (i.e. the finished sequences are provably
         unchanging)

    Args:
      state: A dictionary with the current loop state.

    Returns:
      Bool tensor with value True if loop should continue, False if loop should
      terminate.
    """
        i = state[_StateKeys.CUR_INDEX]
        alive_log_probs = state[_StateKeys.ALIVE_LOG_PROBS]
        finished_scores = state[_StateKeys.FINISHED_SCORES]
        finished_flags = state[_StateKeys.FINISHED_FLAGS]
        not_at_max_decode_length = tf.less(i, self.max_decode_length)
        max_length_norm = _length_normalization((self.alpha), (self.max_decode_length), dtype=(self.dtype))
        best_alive_scores = alive_log_probs[:, 0] / max_length_norm
        finished_scores *= tf.cast(finished_flags, self.dtype)
        lowest_finished_scores = tf.reduce_min(finished_scores, axis=1)
        finished_batches = tf.reduce_any(finished_flags, 1)
        lowest_finished_scores += (1.0 - tf.cast(finished_batches, self.dtype)) * -inf(self.dtype)
        worst_finished_score_better_than_best_alive_score = tf.reduce_all(tf.greater(lowest_finished_scores, best_alive_scores))
        return tf.logical_and(not_at_max_decode_length, tf.logical_not(worst_finished_score_better_than_best_alive_score))

    def _search_step(self, state):
        """Beam search loop body.

    Grow alive sequences by a single ID. Sequences that have reached the EOS
    token are marked as finished. The alive and finished sequences with the
    highest log probabilities and scores are returned.

    A sequence's finished score is calculating by dividing the log probability
    by the length normalization factor. Without length normalization, the
    search is more likely to return shorter sequences.

    Args:
      state: A dictionary with the current loop state.

    Returns:
      new state dictionary.
    """
        new_seq, new_log_probs, topk_ids, new_cache = self._grow_alive_seq(state)
        new_finished_flags = tf.equal(topk_ids, self.eos_id)
        alive_state = self._get_new_alive_state(new_seq, new_log_probs, new_finished_flags, new_cache)
        finished_state = self._get_new_finished_state(state, new_seq, new_log_probs, new_finished_flags)
        new_state = {_StateKeys.CUR_INDEX: state[_StateKeys.CUR_INDEX] + 1}
        new_state.update(alive_state)
        new_state.update(finished_state)
        return [new_state]

    def _grow_alive_seq(self, state):
        """Grow alive sequences by one token, and collect top 2*beam_size sequences.

    2*beam_size sequences are collected because some sequences may have reached
    the EOS token. 2*beam_size ensures that at least beam_size sequences are
    still alive.

    Args:
      state: A dictionary with the current loop state.
    Returns:
      Tuple of
      (Top 2*beam_size sequences [batch_size, 2 * beam_size, cur_index + 1],
       Scores of returned sequences [batch_size, 2 * beam_size],
       New alive cache, for each of the 2 * beam_size sequences)
    """
        i = state[_StateKeys.CUR_INDEX]
        alive_seq = state[_StateKeys.ALIVE_SEQ]
        alive_log_probs = state[_StateKeys.ALIVE_LOG_PROBS]
        alive_cache = state[_StateKeys.ALIVE_CACHE]
        beams_to_keep = 2 * self.beam_size
        if self.padded_decode:
            flat_ids = tf.reshape(tf.slice(alive_seq, [0, 0, i], [self.batch_size, self.beam_size, 1]), [
             self.batch_size * self.beam_size, -1])
        else:
            flat_ids = _flatten_beam_dim(alive_seq)
        flat_cache = nest.map_structure(_flatten_beam_dim, alive_cache)
        flat_logits, flat_cache = self.symbols_to_logits_fn(flat_ids, i, flat_cache)
        logits = _unflatten_beam_dim(flat_logits, self.batch_size, self.beam_size)
        new_cache = nest.map_structure(lambda t: _unflatten_beam_dim(t, self.batch_size, self.beam_size), flat_cache)
        candidate_log_probs = _log_prob_from_logits(logits)
        log_probs = candidate_log_probs + tf.expand_dims(alive_log_probs, axis=2)
        flat_log_probs = tf.reshape(log_probs, [
         -1, self.beam_size * self.vocab_size])
        topk_log_probs, topk_indices = tf.nn.top_k(flat_log_probs, k=beams_to_keep)
        topk_beam_indices = topk_indices // self.vocab_size
        topk_seq, new_cache = _gather_beams([
         alive_seq, new_cache], topk_beam_indices, self.batch_size, beams_to_keep)
        topk_ids = topk_indices % self.vocab_size
        if self.padded_decode:
            topk_seq = tf.transpose(topk_seq, perm=[2, 0, 1])
            topk_seq = tf.tensor_scatter_nd_update(topk_seq, [[i + 1]], tf.expand_dims(topk_ids, axis=0))
            topk_seq = tf.transpose(topk_seq, perm=[1, 2, 0])
        else:
            topk_seq = tf.concat([topk_seq, tf.expand_dims(topk_ids, axis=2)], axis=2)
        return (
         topk_seq, topk_log_probs, topk_ids, new_cache)

    def _get_new_alive_state(self, new_seq, new_log_probs, new_finished_flags, new_cache):
        """Gather the top k sequences that are still alive.

    Args:
      new_seq: New sequences generated by growing the current alive sequences
        int32 tensor with shape [batch_size, 2 * beam_size, cur_index + 1]
      new_log_probs: Log probabilities of new sequences float32 tensor with
        shape [batch_size, beam_size]
      new_finished_flags: A boolean Tensor indicates which sequences are live
        inside the beam.
      new_cache: Dict of cached values for each sequence.

    Returns:
      Dictionary with alive keys from _StateKeys:
        {Top beam_size sequences that are still alive (don't end with eos_id)
         Log probabilities of top alive sequences
         Dict cache storing decoder states for top alive sequences}
    """
        new_log_probs += tf.cast(new_finished_flags, self.dtype) * -inf(self.dtype)
        top_alive_seq, top_alive_log_probs, top_alive_cache = _gather_topk_beams([
         new_seq, new_log_probs, new_cache], new_log_probs, self.batch_size, self.beam_size)
        return {_StateKeys.ALIVE_SEQ: top_alive_seq, 
         _StateKeys.ALIVE_LOG_PROBS: top_alive_log_probs, 
         _StateKeys.ALIVE_CACHE: top_alive_cache}

    def _get_new_finished_state(self, state, new_seq, new_log_probs, new_finished_flags):
        """Combine new and old finished sequences, and gather the top k sequences.

    Args:
      state: A dictionary with the current loop state.
      new_seq: New sequences generated by growing the current alive sequences
        int32 tensor with shape [batch_size, beam_size, i + 1]
      new_log_probs: Log probabilities of new sequences float32 tensor with
        shape [batch_size, beam_size]
      new_finished_flags: A boolean Tensor indicates which sequences are live
        inside the beam.

    Returns:
      Dictionary with finished keys from _StateKeys:
        {Top beam_size finished sequences based on score,
         Scores of finished sequences,
         Finished flags of finished sequences}
    """
        i = state[_StateKeys.CUR_INDEX]
        finished_seq = state[_StateKeys.FINISHED_SEQ]
        finished_scores = state[_StateKeys.FINISHED_SCORES]
        finished_flags = state[_StateKeys.FINISHED_FLAGS]
        if not self.padded_decode:
            finished_seq = tf.concat([
             finished_seq,
             tf.zeros([self.batch_size, self.beam_size, 1], tf.int32)],
              axis=2)
        length_norm = _length_normalization((self.alpha), (i + 1), dtype=(self.dtype))
        new_scores = new_log_probs / length_norm
        new_scores += (1.0 - tf.cast(new_finished_flags, self.dtype)) * -inf(self.dtype)
        finished_seq = tf.concat([finished_seq, new_seq], axis=1)
        finished_scores = tf.concat([finished_scores, new_scores], axis=1)
        finished_flags = tf.concat([finished_flags, new_finished_flags], axis=1)
        top_finished_seq, top_finished_scores, top_finished_flags = _gather_topk_beams([finished_seq, finished_scores, finished_flags], finished_scores, self.batch_size, self.beam_size)
        return {_StateKeys.FINISHED_SEQ: top_finished_seq, 
         _StateKeys.FINISHED_SCORES: top_finished_scores, 
         _StateKeys.FINISHED_FLAGS: top_finished_flags}


def sequence_beam_search(symbols_to_logits_fn, initial_ids, initial_cache, vocab_size, beam_size, alpha, max_decode_length, eos_id, padded_decode=False):
    """Search for sequence of subtoken ids with the largest probability.

  Args:
    symbols_to_logits_fn: A function that takes in ids, index, and cache as
      arguments. The passed in arguments will have shape:
        ids -> A tensor with shape [batch_size * beam_size, index].
        index -> A scalar.
        cache -> A nested dictionary of tensors [batch_size * beam_size, ...].
      The function must return a tuple of logits and new cache:
        logits -> A tensor with shape [batch * beam_size, vocab_size].
        new cache -> A nested dictionary with the same shape/structure as the
          inputted cache.
    initial_ids: An int32 tensor with shape [batch_size]. Starting ids for
      each batch item.
    initial_cache: A dictionary, containing starting decoder variables
      information.
    vocab_size: An integer, the size of the vocabulary, used for topk
      computation.
    beam_size: An integer, the number of beams.
    alpha: A float, defining the strength of length normalization.
    max_decode_length: An integer, the maximum length to decoded a sequence.
    eos_id: An integer, ID of eos token, used to determine when a sequence has
      finished.
    padded_decode: A bool, indicating if max_sequence_length padding is used
      for beam search.

  Returns:
    Top decoded sequences [batch_size, beam_size, max_decode_length]
    sequence scores [batch_size, beam_size]
  """
    batch_size = initial_ids.shape.as_list()[0] if padded_decode else tf.shape(initial_ids)[0]
    sbs = SequenceBeamSearch(symbols_to_logits_fn, vocab_size, batch_size, beam_size, alpha, max_decode_length, eos_id, padded_decode)
    return sbs.search(initial_ids, initial_cache)


def _log_prob_from_logits(logits):
    return logits - tf.reduce_logsumexp(logits, axis=2, keepdims=True)


def _length_normalization(alpha, length, dtype=tf.float32):
    """Return length normalization factor."""
    return tf.pow((5.0 + tf.cast(length, dtype)) / 6.0, alpha)


def _expand_to_beam_size(tensor, beam_size):
    """Tiles a given tensor by beam_size.

  Args:
    tensor: tensor to tile [batch_size, ...]
    beam_size: How much to tile the tensor by.

  Returns:
    Tiled tensor [batch_size, beam_size, ...]
  """
    tensor = tf.expand_dims(tensor, axis=1)
    tile_dims = [1] * tensor.shape.ndims
    tile_dims[1] = beam_size
    return tf.tile(tensor, tile_dims)


def _shape_list(tensor):
    """Return a list of the tensor's shape, and ensure no None values in list."""
    shape = tensor.get_shape().as_list()
    dynamic_shape = tf.shape(tensor)
    for i in range(len(shape)):
        if shape[i] is None:
            shape[i] = dynamic_shape[i]

    return shape


def _get_shape_keep_last_dim(tensor):
    shape_list = _shape_list(tensor)
    for i in range(len(shape_list) - 1):
        shape_list[i] = None

    if isinstance(shape_list[(-1)], tf.Tensor):
        shape_list[-1] = None
    return tf.TensorShape(shape_list)


def _get_shape(tensor):
    """Return the shape of the input tensor."""
    return tf.TensorShape(_shape_list(tensor))


def _flatten_beam_dim(tensor):
    """Reshapes first two dimensions in to single dimension.

  Args:
    tensor: Tensor to reshape of shape [A, B, ...]

  Returns:
    Reshaped tensor of shape [A*B, ...]
  """
    shape = _shape_list(tensor)
    shape[0] *= shape[1]
    shape.pop(1)
    return tf.reshape(tensor, shape)


def _unflatten_beam_dim(tensor, batch_size, beam_size):
    """Reshapes first dimension back to [batch_size, beam_size].

  Args:
    tensor: Tensor to reshape of shape [batch_size*beam_size, ...]
    batch_size: Tensor, original batch size.
    beam_size: int, original beam size.

  Returns:
    Reshaped tensor of shape [batch_size, beam_size, ...]
  """
    shape = _shape_list(tensor)
    new_shape = [batch_size, beam_size] + shape[1:]
    return tf.reshape(tensor, new_shape)


def _gather_beams(nested, beam_indices, batch_size, new_beam_size):
    """Gather beams from nested structure of tensors.

  Each tensor in nested represents a batch of beams, where beam refers to a
  single search state (beam search involves searching through multiple states
  in parallel).

  This function is used to gather the top beams, specified by
  beam_indices, from the nested tensors.

  Args:
    nested: Nested structure (tensor, list, tuple or dict) containing tensors
      with shape [batch_size, beam_size, ...].
    beam_indices: int32 tensor with shape [batch_size, new_beam_size]. Each
     value in beam_indices must be between [0, beam_size), and are not
     necessarily unique.
    batch_size: int size of batch
    new_beam_size: int number of beams to be pulled from the nested tensors.

  Returns:
    Nested structure containing tensors with shape
      [batch_size, new_beam_size, ...]
  """
    batch_pos = tf.range(batch_size * new_beam_size) // new_beam_size
    batch_pos = tf.reshape(batch_pos, [batch_size, new_beam_size])
    coordinates = tf.stack([batch_pos, beam_indices], axis=2)
    return nest.map_structure(lambda state: tf.gather_nd(state, coordinates), nested)


def _gather_topk_beams(nested, score_or_log_prob, batch_size, beam_size):
    """Gather top beams from nested structure."""
    _, topk_indexes = tf.nn.top_k(score_or_log_prob, k=beam_size)
    return _gather_beams(nested, topk_indexes, batch_size, beam_size)