# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/third_party/gzip.py
# Compiled at: 2017-11-15 03:51:36
# Size of source mod 2**32: 2105 bytes
"""Wrapper module for the `gzip` library.

Feed this module using a local copy of `gzip` if it exists.
Else it expect to have an available `gzip` library installed in
the Python path.

It should be used like that:

.. code-block::

    from fabio.third_party import gzip

"""
from __future__ import absolute_import
__authors__ = [
 'Valentin Valls']
__license__ = 'MIT'
__date__ = '28/07/2017'
import sys as __sys
if __sys.version_info < (2, 7):
    from ._local.gzip import *
else:
    import gzip as __gzip
    for k, v in __gzip.__dict__.items():
        if k.startswith('_'):
            pass
        else:
            vars()[k] = v