# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/font2char2word2sent2doc/font2char_test.py
# Compiled at: 2017-04-12 22:56:41
# Size of source mod 2**32: 518 bytes
import extenteten as ex, tensorflow as tf
from . import font2char

@ex.func_scope()
def test_font2char():
    assert ex.static_rank(font2char.font2char((tf.zeros([64, 224, 224])),
      nums_of_channels=([
     32] * 4),
      nums_of_attention_channels=([
     32] * 3))) == 2


@ex.func_scope()
def test_attend_to_image():
    assert ex.static_rank(font2char._attend_to_image((tf.zeros([64, 224, 224, 1])),
      nums_of_channels=([
     32] * 3))) == 4