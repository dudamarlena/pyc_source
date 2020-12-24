# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tagging/jubs.py
# Compiled at: 2020-04-23 12:01:28
# Size of source mod 2**32: 1130 bytes
from .tagging import tag

def affixes(text):
    """Extract affixes (접사) from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as affixes.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] in ('xp', 'xs')]
    return filtered


def jubs(text):
    """Extract affixes (접사) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as affixes.

    """
    return affixes(text)


def xp(text):
    """Extract 접두사 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 접두사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'xp']
    return filtered


def xs(text):
    """Extract 접미사 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 접미사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'xs']
    return filtered