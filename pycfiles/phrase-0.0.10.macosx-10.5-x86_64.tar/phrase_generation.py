# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brentpayne/anaconda/lib/python2.7/site-packages/phrase/phrase_generation.py
# Compiled at: 2014-08-28 17:58:28
from itertools import chain, imap
import math, pdb
from phrase.noun_phrase_dictionary import NounPhraseDictionary, exclude_ngram_filter
from phrase_dictionary import PhraseDictionary
__author__ = 'brentpayne'

def extend_phrase_dictionary(corpus, phrase_discovery_function, phrase_dictionary):
    """

    :param corpus: a corpus of document of sentences of tokens.
    So an iterable of iterables of iterables of tokens : corpus of files of sentences of tokens
     Or, restated, a list of sentences each split into tokens.
    :param phrase_function: a function that takes a corpus of tokens returns phrases.
     The return value is a list of lists with the interal lists being an ordered list of tokens.
     The ordered list represents a single phrase.
    :param phrase_dictionary: a PhraseDictionary or other type that implements both :func:`add` and :func:`process`
    :return: returns a phrase_dictionary
    """
    sentences = chain.from_iterable(corpus)
    tokens = chain.from_iterable(imap(phrase_dictionary.process, sentences))
    phrases = phrase_discovery_function(tokens)
    map(phrase_dictionary.add, (phrase_dictionary.decompose(ph) for ph in phrases))
    return phrase_dictionary


def generate_phrase_dictionary(corpus_func, min_word_count=1, max_phrase_count=20, colloc_rounds=4):
    """

    :param corpus_func: a function that returns an iterable to a corpus
    :param min_word_count: the minimum number of times a word needs to appear to be considered
    :param max_phrase_count: the maximum number of phrases to return
    :param colloc_rounds: number of rounds of collocation, the maximal phrase length is 2^(colloc_rounds).
         In practice most phrases are within 2-3 tokens.
    :return:
    """
    max_phrases_per_round = int(math.floor(max_phrase_count / colloc_rounds))
    phrase_dictionary = PhraseDictionary()
    for i in range(colloc_rounds):
        phrase_dictionary = extend_phrase_dictionary(corpus_func(), PhraseDictionary.generate_phrase_detection_function(min_token_count=min_word_count, max_phrases=max_phrases_per_round), phrase_dictionary)

    return phrase_dictionary


def generate_noun_phrase_dictionary(corpus_func, min_word_count=1, max_phrase_count=40, colloc_rounds=4):
    """

    :param corpus_func: a function that returns an iterable to a corpus
    :param min_word_count: the minimum number of times a word needs to appear to be considered
    :param max_phrase_count: the maximum number of phrases to return
    :param colloc_rounds: number of rounds of collocation, the maximal phrase length is 2^(colloc_rounds).
         In practice most phrases are within 2-3 tokens.
    :return:
    """
    max_phrases_per_round = int(max_phrase_count / colloc_rounds)
    phrase_dictionary = NounPhraseDictionary()
    for i in range(colloc_rounds):
        if i == colloc_rounds - 1:
            max_phrases_per_round = max_phrase_count - i * max_phrases_per_round
        phrase_dictionary = extend_phrase_dictionary(corpus_func(), NounPhraseDictionary.generate_phrase_detection_function(min_token_count=min_word_count, max_phrases=max_phrases_per_round, exclude_ngram_filter=exclude_ngram_filter), phrase_dictionary)

    return phrase_dictionary