# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/font2char2word2sent2doc/ar2word2sent2doc.py
# Compiled at: 2017-01-13 02:21:00
# Size of source mod 2**32: 1175 bytes
import extenteten as ex, tensorflow as tf
from .rd2sent2doc import rd2sent2doc

def ar2word2sent2doc(document, *, words, char_embeddings, word_embedding_size, context_vector_size, save_memory=True, **rd2sent2doc_hyperparams):
    """char2word2sent2doc model without character embeddings as parameters
    """
    if not ex.static_rank(document) == 3:
        raise AssertionError
    else:
        assert ex.static_rank(words) == 2
        assert ex.static_rank(char_embeddings) == 2
    with tf.variable_scope('char2word'):
        word_embeddings = ex.bidirectional_id_vector_to_embedding((tf.gather(words, ex.flatten(document)) if save_memory else words),
          char_embeddings,
          output_size=word_embedding_size,
          context_vector_size=context_vector_size,
          dynamic_length=True)
    return rd2sent2doc(document,
 word_embeddings, context_vector_size=context_vector_size, 
     save_memory=save_memory, **rd2sent2doc_hyperparams)