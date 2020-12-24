# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tagging/doks.py
# Compiled at: 2020-04-23 12:01:16
# Size of source mod 2**32: 856 bytes
from .tagging import tag

def orthotones(text):
    """Extract orthotones (독립언) from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as orthotones.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'ii']
    return filtered


def doks(text):
    """Extract orthotones (독립언) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as orthotones.

    """
    return orthotones(text)


def ii(text):
    """Extract 감탄사 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 감탄사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'ii']
    return filtered