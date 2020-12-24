# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/attribute_dict.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 819 bytes
from . import deprecated
if deprecated.allowed():

    class AttributeDict(object):
        __doc__ = '\n        A dict that exposes its values as attributes.\n\n        DEPRECATED: use argparse.Namespace, or just a dict.\n        '

        def __init__(self, *args, **kwds):
            deprecated.deprecated('util.AttributeDict')
            for k, v in dict(*args, **kwds).items():
                setattr(self, k, v)

        def __setattr__(self, k, v):
            if isinstance(v, dict):
                v = AttributeDict(**v)
            super().__setattr__(k, v)

        def __eq__(self, other):
            return self.__dict__ == other.__dict__

        def __ne__(self, other):
            return self.__dict__ != other.__dict__

        def __bool__(self):
            return bool(self.__dict__)