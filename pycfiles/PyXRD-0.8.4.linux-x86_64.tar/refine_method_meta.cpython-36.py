# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refine_method_meta.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1140 bytes
import logging
logger = logging.getLogger(__name__)
from .refine_method_option import RefineMethodOption

class RefineMethodMeta(type):
    __doc__ = "\n        The metaclass for creating a RefineMethod (sub)class\n        Will register the class type so we can build a list of RefineMethod \n        classes dynamically.\n        If the (sub)class does not want to be registered, it should set\n        the 'disabled' class attribute to True.\n    "
    registered_methods = {}

    def __new__(meta, name, bases, class_dict):
        options = []
        for name, value in class_dict.items():
            if isinstance(value, RefineMethodOption):
                options.append(name)
                setattr(value, 'label', name)

        class_dict['options'] = options
        cls = type.__new__(meta, name, bases, class_dict)
        if not getattr(cls, 'disabled', False):
            meta.registered_methods[getattr(cls, 'index')] = cls
        return cls