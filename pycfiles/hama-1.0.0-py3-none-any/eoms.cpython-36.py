# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tagging/eoms.py
# Compiled at: 2020-04-23 12:01:24
# Size of source mod 2**32: 1757 bytes
from .tagging import tag

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


def eoms(text):
    """Extract suffixes (어미) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as suffixes.

    """
    return suffixes(text)


def ep(text):
    """Extract 선어말어미 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 선어말어미.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'ep']
    return filtered


def ec(text):
    """Extract 연결어미 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 연결어미.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'ec']
    return filtered


def et(text):
    """Extract 전성어미 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 전성어미.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'et']
    return filtered


def ef(text):
    """Extract 종결어미 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 종결어미.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'ef']
    return filtered