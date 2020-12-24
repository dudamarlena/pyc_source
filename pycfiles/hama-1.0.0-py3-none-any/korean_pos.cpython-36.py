# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/korean_pos.py
# Compiled at: 2020-04-06 04:38:27
# Size of source mod 2**32: 1590 bytes
from .pos import *

def ches(text):
    """Extract nouns (체언) from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as nouns.

    """
    return nouns(text)


def yongs(text):
    """Extract predicates (용언) from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as predicates.

    """
    return predicates(text)


def soos(text):
    """Extract modifiers (수식언) from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as modifiers.

    """
    return modifiers(text)


def doks(text):
    """Extract orthotones (독립언) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as orthotones.

    """
    return orthotones(text)


def jos(text):
    """Extract postpositions (관계언/조사) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as postpositions.

    """
    return postpositions(text)


def eoms(text):
    """Extract suffixes (어미) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as suffixes.

    """
    return suffixes(text)


def jubs(text):
    """Extract affixes (접사) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as affixes.

    """
    return affixes(text)