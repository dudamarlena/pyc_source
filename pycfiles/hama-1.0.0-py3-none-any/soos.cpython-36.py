# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tagging/soos.py
# Compiled at: 2020-04-23 12:01:12
# Size of source mod 2**32: 1141 bytes
from .tagging import tag

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


def soos(text):
    """Extract modifiers (수식언) from text.

    Args:
        text (str): Text to analyze.
        
    Returns:
        list: List of morphemes tagged as modifiers.

    """
    return modifiers(text)


def mm(text):
    """Extract 관형사 from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: List of morphemes tagged as 관형사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'mm']
    return filtered


def ma(text):
    """Extract 부사 from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: List of morphemes tagged as 부사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'ma']
    return filtered