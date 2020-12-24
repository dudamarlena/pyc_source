# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/font2char2word2sent2doc/char2word2sent2doc.py
# Compiled at: 2017-04-14 04:25:54
# Size of source mod 2**32: 1765 bytes
import extenteten as ex, qnd, qndex, tensorflow as tf
from .word2sent2doc import add_flags as add_child_flags
from .ar2word2sent2doc import ar2word2sent2doc

@ex.func_scope()
def char2word2sent2doc(document, *, words, char_space_size, char_embedding_size, **ar2word2sent2doc_hyperparams):
    """
    The argument `document` is in the shape of
    (#examples, #sentences per document, #words per sentence).
    """
    if not ex.static_rank(document) == 3:
        raise AssertionError
    elif not ex.static_rank(words) == 2:
        raise AssertionError
    with tf.variable_scope('char_embeddings'):
        char_embeddings = ex.embeddings(id_space_size=char_space_size, embedding_size=char_embedding_size,
          name='char_embeddings')
    return ar2word2sent2doc(document, words=words, 
     char_embeddings=char_embeddings, **ar2word2sent2doc_hyperparams)


def add_flags():
    adder = add_child_flags()
    return adder


def def_char2word2sent2doc():
    adder = add_flags()
    adder.add_flag('char_embedding_size', type=int, default=100)
    classify = qndex.def_classify()
    word_array = qndex.nlp.def_word_array()

    def model(document, label=None, *, mode, key=None):
        return classify(char2word2sent2doc(
 document, words=word_array(), 
         char_space_size=len(qnd.FLAGS.chars), **adder.flags),
          label,
          key=key,
          mode=mode,
          regularization_scale=(qnd.FLAGS.regularization_scale))

    return model