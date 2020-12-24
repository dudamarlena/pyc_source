# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/unitexlemmatizer/lemmatizer.py
# Compiled at: 2017-01-19 11:25:51
from __future__ import unicode_literals
import logging
unitex_dictionary = None
udtags2unitex = {b'verb': b'V', b'aux': b'V', 
   b'noun': b'N', 
   b'adj': b'A'}
lemmatizable_delaf_tags = set(udtags2unitex.values())
lemmatizable_ud_tags = set(udtags2unitex.keys())

def load_unitex_dictionary(path):
    """
    Load the Unitex dictionary with inflected word forms.

    This function must be called before using `get_lemma`.
    :param path: the path to the unitex dictionary file
    """
    global unitex_dictionary
    logging.debug(b'Reading Unitex dictionary')
    with open(path, b'rb') as (f):
        unitex_dictionary = {}
        for line in f:
            line = unicode(line, b'utf-8').strip()
            inflected, rest = line.split(b',')
            if b'-' in inflected:
                continue
            lemma, morph = rest.split(b'.')
            if b':' in morph:
                pos, _ = morph.split(b':')
            else:
                pos = morph
            if pos not in lemmatizable_delaf_tags:
                continue
            unitex_dictionary[(inflected, pos)] = lemma


def get_lemma(word, pos, check_other_pos=True):
    """
    Retrieve the lemma of a word given its POS tag.

    If the combination of word and POS is not known, return the
    word itself.
    :param word: the word string
    :param pos: part of speech in Universal Treebanks standard
        (the only ones used are AUX, NOUN, VERB, ADJ; any other
        results in the lemma being the word itself)
    :param check_other_pos: if True and the combination of word and
        POS is not found in the Unitex dictionary, other POS tags
        will be tried.
    """
    if unitex_dictionary is None:
        raise RuntimeError(b'Unitex dictionary was not loaded before calling get_lemma')
    word = word.lower()
    pos = pos.lower()
    if pos not in lemmatizable_ud_tags:
        return word
    unitex_pos = udtags2unitex[pos]
    if (
     word, unitex_pos) not in unitex_dictionary:
        if len(word) == 1:
            return word
        return check_other_pos or word
    else:
        if unitex_pos == b'N':
            try_these = [
             b'A', b'V']
        else:
            if unitex_pos == b'A':
                try_these = [
                 b'N', b'V']
            else:
                try_these = [
                 b'N', b'A']
            for other_pos in try_these:
                if (
                 word, other_pos) in unitex_dictionary:
                    logging.debug((b'Could not find lemma for word {} with POS {},but found for POS {}').format(word, unitex_pos, other_pos))
                    return unitex_dictionary[(word, other_pos)]

            return word
        return unitex_dictionary[(word, unitex_pos)]