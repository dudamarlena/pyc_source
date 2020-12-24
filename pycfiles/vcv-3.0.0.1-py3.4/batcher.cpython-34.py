# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/core/batcher.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 5617 bytes
"""Provides functions to batch a dictionary of input tensors."""
import collections, tensorflow as tf
from object_detection.core import prefetcher
rt_shape_str = '_runtime_shapes'

class BatchQueue(object):
    __doc__ = 'BatchQueue class.\n\n  This class creates a batch queue to asynchronously enqueue tensors_dict.\n  It also adds a FIFO prefetcher so that the batches are readily available\n  for the consumers.  Dequeue ops for a BatchQueue object can be created via\n  the Dequeue method which evaluates to a batch of tensor_dict.\n\n  Example input pipeline with batching:\n  ------------------------------------\n  key, string_tensor = slim.parallel_reader.parallel_read(...)\n  tensor_dict = decoder.decode(string_tensor)\n  tensor_dict = preprocessor.preprocess(tensor_dict, ...)\n  batch_queue = batcher.BatchQueue(tensor_dict,\n                                   batch_size=32,\n                                   batch_queue_capacity=2000,\n                                   num_batch_queue_threads=8,\n                                   prefetch_queue_capacity=20)\n  tensor_dict = batch_queue.dequeue()\n  outputs = Model(tensor_dict)\n  ...\n  -----------------------------------\n\n  Notes:\n  -----\n  This class batches tensors of unequal sizes by zero padding and unpadding\n  them after generating a batch. This can be computationally expensive when\n  batching tensors (such as images) that are of vastly different sizes. So it is\n  recommended that the shapes of such tensors be fully defined in tensor_dict\n  while other lightweight tensors such as bounding box corners and class labels\n  can be of varying sizes. Use either crop or resize operations to fully define\n  the shape of an image in tensor_dict.\n\n  It is also recommended to perform any preprocessing operations on tensors\n  before passing to BatchQueue and subsequently calling the Dequeue method.\n\n  Another caveat is that this class does not read the last batch if it is not\n  full. The current implementation makes it hard to support that use case. So,\n  for evaluation, when it is critical to run all the examples through your\n  network use the input pipeline example mentioned in core/prefetcher.py.\n  '

    def __init__(self, tensor_dict, batch_size, batch_queue_capacity, num_batch_queue_threads, prefetch_queue_capacity):
        """Constructs a batch queue holding tensor_dict.

    Args:
      tensor_dict: dictionary of tensors to batch.
      batch_size: batch size.
      batch_queue_capacity: max capacity of the queue from which the tensors are
        batched.
      num_batch_queue_threads: number of threads to use for batching.
      prefetch_queue_capacity: max capacity of the queue used to prefetch
        assembled batches.
    """
        static_shapes = collections.OrderedDict({key:tensor.get_shape() for key, tensor in tensor_dict.items()})
        runtime_shapes = collections.OrderedDict({key + rt_shape_str:tf.shape(tensor) for key, tensor in tensor_dict.items()})
        all_tensors = tensor_dict
        all_tensors.update(runtime_shapes)
        batched_tensors = tf.train.batch(all_tensors, capacity=batch_queue_capacity, batch_size=batch_size, dynamic_pad=True, num_threads=num_batch_queue_threads)
        self._queue = prefetcher.prefetch(batched_tensors, prefetch_queue_capacity)
        self._static_shapes = static_shapes
        self._batch_size = batch_size

    def dequeue(self):
        """Dequeues a batch of tensor_dict from the BatchQueue.

    TODO: use allow_smaller_final_batch to allow running over the whole eval set

    Returns:
      A list of tensor_dicts of the requested batch_size.
    """
        batched_tensors = self._queue.dequeue()
        tensors = {}
        shapes = {}
        for key, batched_tensor in batched_tensors.items():
            unbatched_tensor_list = tf.unstack(batched_tensor)
            for i, unbatched_tensor in enumerate(unbatched_tensor_list):
                if rt_shape_str in key:
                    shapes[(key[:-len(rt_shape_str)], i)] = unbatched_tensor
                else:
                    tensors[(key, i)] = unbatched_tensor

        tensor_dict_list = []
        batch_size = self._batch_size
        for batch_id in range(batch_size):
            tensor_dict = {}
            for key in self._static_shapes:
                tensor_dict[key] = tf.slice(tensors[(key, batch_id)], tf.zeros_like(shapes[(key, batch_id)]), shapes[(key, batch_id)])
                tensor_dict[key].set_shape(self._static_shapes[key])

            tensor_dict_list.append(tensor_dict)

        return tensor_dict_list