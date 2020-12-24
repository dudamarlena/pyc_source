# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/fc/vector.py
# Compiled at: 2015-09-05 21:22:50
from __future__ import absolute_import, division, print_function
import abc

class SparseVector(object):
    """An abstract class for sparse vectors.

    Currently, there is no default implementation of a sparse vector.

    Other implementations of sparse vectors *must* inherit
    from this class. Otherwise they cannot be used inside a
    :class:`dossier.fc.FeatureCollection`.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass


class DenseVector(object):
    """An abstract class for dense vectors.

    Currently, there is no default implementation of a dense vector.

    Other implementations of dense vectors *must* inherit
    from this class. Otherwise they cannot be used inside a
    :class:`dossier.fc.FeatureCollection`.
    """
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        pass