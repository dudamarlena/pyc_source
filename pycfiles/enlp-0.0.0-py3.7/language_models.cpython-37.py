# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/enlp/language_models.py
# Compiled at: 2019-11-27 15:57:30
# Size of source mod 2**32: 1164 bytes
"""
Contains functions for generating & saving custom spacy language models
"""
import spacy

def add_vectors_to_langmod(wvs, mod_lang):
    """ Add word vectors to language model

    Parameters
    ----------
    wvs : :obj:`gensim model`
        Trained word vector model
    mod_lang  : :obj:`str`
        language of model to be created

    Returns
    -------
        nlp : :obj:`spacy.lang`
            SpaCy language model with new word vectors incorporated
    """
    nlp = spacy.blank(mod_lang)
    keys = []
    for idx in range(len(wvs.index2word)):
        keys.append(wvs.index2word[idx])

    nlp.vocab.vectors = spacy.vocab.Vectors(data=(wvs.syn0), keys=keys)
    return nlp


def save_spacy_model(model, path):
    """ Save spacy model to file

    Parameters
    ----------
    model : :obj:`spacy.lang`
        SpaCy language model
    path  : :obj:`str`
        file path to save model

    Returns
    -------
    """
    model.to_disk(path)