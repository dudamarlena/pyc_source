# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kieffer/workspace/fabio/build/lib.macosx-10.6-intel-3.5/fabio/third_party/six.py
# Compiled at: 2017-11-15 03:51:36
# Size of source mod 2**32: 2023 bytes
"""Wrapper module for the `six` library.

Feed this module using a local silx copy of `six` if it exists.
Else it expect to have an available `six` library installed in the Python path.

It should be used like that:

.. code-block::

    from fabio.third_party import six

"""
from __future__ import absolute_import
__authors__ = [
 'Valentin Valls']
__license__ = 'MIT'
__date__ = '28/07/2017'
try:
    from ._local.six import *
except ImportError:
    import six
    if tuple(int(i) for i in six.__version__.split('.')[:2]) < (1, 8):
        raise ImportError('Six version is too old')
    from six import *