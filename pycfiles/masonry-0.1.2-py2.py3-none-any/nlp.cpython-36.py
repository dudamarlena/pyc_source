# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cmusselle/Mango/Workspace/rss-miner/package/src/rss_miner/nlp.py
# Compiled at: 2017-05-14 13:30:20
# Size of source mod 2**32: 1125 bytes
import collections, re

def paragraphs_to_sentences(paragraph_list):
    """Convert a list of paragraphs into a list of sentences"""
    nested_list = [text_to_sentences(p) for p in paragraph_list]
    sentence_list = flatten_nested_list(nested_list)
    return list(sentence_list)


def text_to_sentences(text):
    """ Split input text into a list of sentences. """
    regex = '(?<!\\w\\.\\w.)(?<![A-Z][a-z]\\.)(?<=\\.|\\?|\\!)\\s'
    result = re.split(pattern=regex, string=text, flags=(re.MULTILINE))
    sentences = [s.strip() for s in result]
    sentences = [s for s in sentences if s]
    return sentences


def flatten_nested_list(nested_list):
    """Flattern a list by returning all the elements as a generator"""
    for el in nested_list:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten_nested_list(el)
        else:
            yield el