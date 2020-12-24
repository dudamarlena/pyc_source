# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/data_input/simple.py
# Compiled at: 2019-07-30 09:27:42
# Size of source mod 2**32: 3047 bytes
import functools, tensorflow as tf
from seq2annotation.data_input.char_level_conllz import generator_fn

def index_table_from_file(vocabulary_file=None):
    index_table = {}
    index_counter = 0
    with open(vocabulary_file) as (fd):
        for line in fd:
            key = line.strip()
            index_table[key] = index_counter
            index_counter += 1

    class Lookuper(object):

        def __init__(self, index_table):
            self.index_table = index_table

        def lookup(self, string):
            return self.index_table.get(string)

    return Lookuper(index_table)


def input_fn(params=None, input_file=None, config=None, shuffle_and_repeat=False):
    config = config if config is not None else {}
    shapes = (([None], ()), [None])
    types = ((tf.string, tf.int32), tf.string)
    defaults = (('<pad>', 0), 'O')
    dataset = tf.data.Dataset.from_generator((functools.partial(generator_fn, input_file)),
      output_shapes=shapes,
      output_types=types)
    if shuffle_and_repeat:
        dataset = dataset.shuffle(config['buffer']).repeat(config['epochs'])
    dataset = dataset.padded_batch((params['batch_size']),
      shapes, defaults, drop_remainder=(config['use_tpu'])).prefetch(1)
    words_index_table = index_table_from_file(config['words'])
    tags_index_table = index_table_from_file(config['words'])
    dataset = dataset.map(lambda x, y: ((words_index_table.lookup(x[0]), x[1]), tags_index_table.lookup(y)))
    feature, label = dataset.make_one_shot_iterator().get_next()
    return (
     {'words':feature[0], 
      'words_len':feature[1]}, label)