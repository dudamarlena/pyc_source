# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/font2char2word2sent2doc/rd2sent2doc.py
# Compiled at: 2017-01-13 02:21:00
# Size of source mod 2**32: 2034 bytes
import functools, extenteten as ex, tensorflow as tf

def rd2sent2doc(document, word_embeddings, *, sentence_embedding_size, document_embedding_size, context_vector_size, save_memory=False):
    """
    word2sent2doc model lacking word embeddings as parameters
    """
    if not ex.static_rank(document) == 3:
        raise AssertionError
    elif not ex.static_rank(word_embeddings) == 2:
        raise AssertionError
    embeddings_to_embedding = functools.partial((ex.bidirectional_embeddings_to_embedding),
      context_vector_size=context_vector_size)
    with tf.variable_scope('word2sent'):
        sentences = _flatten_document_into_sentences(document)
        sentence_embeddings = _restore_document_shape(embeddings_to_embedding((_restore_sentence_shape(word_embeddings, sentences) if save_memory else tf.gather(word_embeddings, sentences)),
          sequence_length=(ex.id_vector_to_length(sentences)),
          output_size=sentence_embedding_size), document)
    with tf.variable_scope('sent2doc'):
        return embeddings_to_embedding(sentence_embeddings,
          sequence_length=(ex.id_tensor_to_length(document)),
          output_size=document_embedding_size)


@ex.func_scope()
def _flatten_document_into_sentences(document):
    return tf.reshape(document, [-1] + ex.static_shape(document)[2:])


@ex.func_scope()
def _restore_document_shape(sentences, document):
    return tf.reshape(sentences, [
     -1, ex.static_shape(document)[1]] + ex.static_shape(sentences)[1:])


@ex.func_scope()
def _restore_sentence_shape(words, sentences):
    return tf.reshape(words, [
     -1, ex.static_shape(sentences)[1]] + ex.static_shape(words)[1:])