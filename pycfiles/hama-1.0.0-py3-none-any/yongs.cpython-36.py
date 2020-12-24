# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tagging/yongs.py
# Compiled at: 2020-04-23 12:01:01
# Size of source mod 2**32: 1149 bytes
from .tagging import tag

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


def yongs(text):
    """Extract predicates (용언) from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as predicates.

    """
    return predicates(text)


def pv(text):
    """Extract 동사 from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as 동사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'pv']
    return filtered


def pa(text):
    """Extract 형용사 from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as 형용사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'pa']
    return filtered