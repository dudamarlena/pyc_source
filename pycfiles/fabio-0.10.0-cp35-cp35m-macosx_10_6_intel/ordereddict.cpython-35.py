# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/third_party/ordereddict.py
# Compiled at: 2017-11-15 03:51:36
# Size of source mod 2**32: 1942 bytes
"""Wrapper module for the `ordereddict` library.

Feed this module using a local copy of `ordereddict` if it exists.
Else it expect to have an available `ordereddict` library installed in
the Python path.

It should be used like that:

.. code-block::

    from fabio.third_party.ordereddict import OrderedDict

"""
from __future__ import absolute_import
__authors__ = [
 'Valentin Valls']
__license__ = 'MIT'
__date__ = '28/07/2017'
try:
    from ._local.ordereddict import *
except ImportError:
    from collections import OrderedDict