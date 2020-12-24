# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/font2char2word2sent2doc/word2sent2doc.py
# Compiled at: 2017-04-14 04:25:54
# Size of source mod 2**32: 1683 bytes
import extenteten as ex, tensorflow as tf, qnd, qndex
from .rd2sent2doc import rd2sent2doc

@ex.func_scope()
def word2sent2doc(document, *, word_space_size, word_embedding_size, **rd2sent2doc_hyperparams):
    assert ex.static_rank(document) == 3
    with tf.variable_scope('word_embeddings'):
        word_embeddings = tf.gather(ex.embeddings(id_space_size=word_space_size, embedding_size=word_embedding_size,
          name='word_embeddings'), ex.flatten(document))
    return rd2sent2doc(document,
 word_embeddings, save_memory=True, **rd2sent2doc_hyperparams)


def add_flags():
    qnd.add_flag('regularization_scale', type=float, default=1e-08)
    adder = qnd.FlagAdder()
    adder.add_flag('word_embedding_size', type=int, default=100)
    adder.add_flag('sentence_embedding_size', type=int, default=100)
    adder.add_flag('document_embedding_size', type=int, default=100)
    adder.add_flag('context_vector_size', type=int, default=100)
    return adder


def def_word2sent2doc():
    adder = add_flags()
    classify = qndex.def_classify()
    get_words = qndex.nlp.def_words()

    def model(document, label=None, *, mode, key=None):
        return classify(word2sent2doc(
 document, word_space_size=len(get_words()), **adder.flags),
          label,
          key=key,
          mode=mode,
          regularization_scale=(qnd.FLAGS.regularization_scale))

    return model