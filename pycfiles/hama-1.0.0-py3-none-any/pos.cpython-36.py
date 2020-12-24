# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/pos.py
# Compiled at: 2020-04-06 04:34:04
# Size of source mod 2**32: 2859 bytes
from .tagging import tag

def nouns(text):
    """Extract nouns (체언) from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as nouns.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] in ('nc', 'nq', 'nb', 'np', 'nn')]
    return filtered


def predicates(text):
    """Extract predicates (용언) from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as predicates.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] in ('pv', 'pa', 'px')]
    return filtered


def symbols(text):
    """Extract symbols from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as symbols.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 's']
    return filtered


def modifiers(text):
    """Extract modifiers (수식언) from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as modifiers.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] in ('mm', 'ma')]
    return filtered


def foreigns():
    """Extract foreign words from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as foreign words.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'f']
    return filtered


def postpositions(text):
    """Extract postpositions (관계언/조사) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as postpositions.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] in ('jc', 'jx', 'jp')]
    return filtered


def suffixes(text):
    """Extract suffixes (어미) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as suffixes.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] in ('ep', 'ec', 'et', 'ef')]
    return filtered


def affixes(text):
    """Extract affixes (접사) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as affixes.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] in ('xp', 'xs')]
    return filtered


def orthotones(text):
    """Extract orthotones (독립언) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as orthotones.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'ii']
    return filtered