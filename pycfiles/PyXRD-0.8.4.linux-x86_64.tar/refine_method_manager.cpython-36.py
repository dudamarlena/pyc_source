# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refine_method_manager.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1756 bytes
from pyxrd.refinement.refine_method_meta import RefineMethodMeta
from .methods import *

class RefineMethodManager(object):

    @classmethod
    def initialize_methods(cls, refine_options):
        """
            Returns a dict of refine methods as values and their index as key
            with the passed refine_options dict applied.
        """
        refine_methods = {}
        for index, method in cls.get_all_methods().items():
            refine_methods[index] = method()

        default_options = {}
        for method in list(refine_methods.values()):
            default_options[method.index] = {name:getattr(type(method), name).default for name in method.options}

        if not refine_options == None:
            for index, options in zip(list(refine_options.keys()), list(refine_options.values())):
                index = int(index)
                if index in refine_methods:
                    method = refine_methods[index]
                    for arg, value in zip(list(options.keys()), list(options.values())):
                        if hasattr(method, arg):
                            setattr(method, arg, value)

        return refine_methods

    @classmethod
    def get_all_methods(cls):
        """ Returns all the registered refinement methods """
        return RefineMethodMeta.registered_methods

    @classmethod
    def get_method_from_index(cls, index):
        """ Returns the actual refinement method defined by the index """
        return cls.get_all_methods()[index]