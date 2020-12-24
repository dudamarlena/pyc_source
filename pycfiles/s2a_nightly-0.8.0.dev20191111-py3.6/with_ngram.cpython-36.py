# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/data_input/with_ngram.py
# Compiled at: 2019-07-30 09:27:42
# Size of source mod 2**32: 1740 bytes
import functools, tensorflow as tf
from seq2annotation.data_input.char_and_ngrams import generator_fn

def input_fn(input_file, params=None, shuffle_and_repeat=False):
    params = params if params is not None else {}
    shapes = (([None], (), [None, 6]), [None])
    types = ((tf.string, tf.int32, tf.float32), tf.string)
    defaults = (('<pad>', 0, 0.0), 'O')
    dataset = tf.data.Dataset.from_generator((functools.partial(generator_fn, input_file, params)),
      output_shapes=shapes,
      output_types=types)
    if shuffle_and_repeat:
        dataset = dataset.shuffle(params['buffer']).repeat(params['epochs'])
    dataset = dataset.padded_batch(params.get('batch_size', 20), shapes, defaults).prefetch(1)
    feature, label = dataset.make_one_shot_iterator().get_next()
    return (
     {'words':feature[0], 
      'words_len':feature[1],  'lookup':feature[2]}, label)


if __name__ == '__main__':
    print(tf.executing_eagerly())
    with tf.Session() as (sess):
        data, label = input_fn('/Users/howl/PyCharmProjects/seq2annotation_ngram_lookup_ner_on_people_daily/data/test.txt', {'trie_data_mapping': {'person': ['/Users/howl/PyCharmProjects/hanzi_char_lookup_feature/data/THUOCL_lishimingren.txt']}})
        for k, v in data.items():
            print(k)
            data = sess.run(v)
            print(data)