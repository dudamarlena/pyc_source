# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/tagging/jos.py
# Compiled at: 2020-04-23 12:01:20
# Size of source mod 2**32: 1223 bytes
from .tagging import tag

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


def jos(text):
    """Extract postpositions (관계언/조사) from text.

    args:
        text (str): text to analyze.
        
    returns:
        list: list of morphemes tagged as postpositions.

    """
    return postpositions(text)


def jc(text):
    """Extract 격조사, 서술격조사 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 격조사/서술격조사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'jc']
    return filtered


def jx(text):
    """Extract 보조사 from text.

    args:
        text (str): Text to analyze.
        
    returns:
        list: List of morphemes tagged as 보조사.

    """
    tags = tag(text, zipped=True)
    filtered = [t[0] for t in tags if t[1] == 'jx']
    return filtered