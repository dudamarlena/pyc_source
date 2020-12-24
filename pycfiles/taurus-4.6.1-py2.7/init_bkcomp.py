# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/init_bkcomp.py
# Compiled at: 2019-08-19 15:09:29
"""This package consists of a collection of useful classes and functions. Most of
the elements are taurus independent and can be used generically.

This module contains a python implementation of :mod:`json`. This was done because
json only became part of python since version 2.6.
The json implementation follows the rule:

    #. if python >= 2.6 use standard json from python distribution
    #. otherwise use private implementation distributed with taurus
"""
from __future__ import absolute_import
from .containers import *
from .enumeration import *
from .event import *
from .log import *
from .object import *
from .singleton import *
from .codecs import *
from .colors import *
from .constant import *
from .timer import *
from .safeeval import *
from .prop import *
from .threadpool import *
from .user import *
from . import eventfilters
try:
    from lxml import etree
except:
    etree = None

__docformat__ = 'restructuredtext'

def dictFromSequence(seq):
    """Translates a sequence into a dictionary by converting each to elements of
    the sequence (k,v) into a k:v pair in the dictionary

    :param seq: (sequence) any sequence object
    :return: (dict) dictionary built from the given sequence"""

    def _pairwise(iterable):
        """Utility method used by dictFromSequence"""
        itnext = iter(iterable).__next__
        while True:
            yield (
             itnext(), itnext())

    return dict(_pairwise(seq))