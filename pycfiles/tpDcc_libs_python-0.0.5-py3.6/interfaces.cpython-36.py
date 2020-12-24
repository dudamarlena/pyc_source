# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/python/interfaces.py
# Compiled at: 2020-04-11 22:12:39
# Size of source mod 2**32: 772 bytes
"""
Module that contains interfaces class for different purposes
"""
from __future__ import print_function, division, absolute_import

class ISerializable(object):
    __doc__ = '\n    Interface class used to identify serializable/deserializable classes\n    '

    def __init__(self):
        super(ISerializable, self).__init__()

    def serialize(self, *args, **kwargs):
        """
        Serializes the current class
        """
        raise NotImplementedError('serialize method of ISerializable is not implemented!')

    def deserialize(self, *args, **kwargs):
        """
        Deserialize the current class
        """
        raise NotImplementedError('deseriailze method of ISerializable is not implemented!')