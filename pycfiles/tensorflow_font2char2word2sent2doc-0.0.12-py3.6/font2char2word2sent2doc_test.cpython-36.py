# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/font2char2word2sent2doc/font2char2word2sent2doc_test.py
# Compiled at: 2017-01-18 01:59:38
# Size of source mod 2**32: 714 bytes
import sys, tensorflow as tf
from .font2char2word2sent2doc import def_font2char2word2sent2doc

def test_def_font2char2word2sent2doc():
    sys.argv = [
     'command',
     '--num_classes', '7',
     '--font_file', 'data/font.ttf',
     '--char_file', 'data/chars.txt',
     '--word_file', 'data/words.txt']
    model = def_font2char2word2sent2doc()
    zeros = lambda *shape: tf.zeros(shape, tf.int32)
    document = zeros(12, 34, 56)
    with tf.variable_scope('model0'):
        model(document, (zeros(12)), mode=(tf.contrib.learn.ModeKeys.TRAIN))
    with tf.variable_scope('model1'):
        model(document, (zeros(12, 10)), mode=(tf.contrib.learn.ModeKeys.TRAIN))