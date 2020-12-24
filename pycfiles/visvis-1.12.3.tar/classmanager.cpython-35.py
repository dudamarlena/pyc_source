# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\dev\pylib\visvis\utils\ssdf\classmanager.py
# Compiled at: 2016-03-22 04:56:47
# Size of source mod 2**32: 3747 bytes
""" ssdf.classmaneger.py

Implements the code to register classes at ssdf for automatic 
conversion (kinda like pickling).

"""
import sys
from . import __version__

class _ClassManager:
    __doc__ = " _ClassManager\n    \n    This static class enables registering classes, which \n    can then be stored to ssdf and loaded from ssdf.\n    \n    On module loading, the sys module is given a reference to the \n    ClassManager called '_ssdf_class_manager'. Other classes can \n    thereby register themselves without knowing how to import \n    ssdf (provided that ssdf is already imported).\n    \n    "
    _registered_classes = {}

    @classmethod
    def _register_at_sys(manager):
        """ _register_at_sys()
        
        Register the manager at the sys module if there is not 
        already one of a higher version.
        
        """
        if hasattr(sys, '_ssdf_class_manager'):
            other = sys._ssdf_class_manager
            if manager.__version__() >= other.__version__():
                sys._ssdf_class_manager = manager
                manager._registered_classes.update(other._registered_classes)
                return manager
            else:
                return other
        else:
            sys._ssdf_class_manager = manager
            return manager

    @classmethod
    def __version__(manager):
        return __version__

    @classmethod
    def is_compatible_class(manager, cls):
        """ is_compatible_class(cls)
        
        Returns True if the given class is SSDF-compatible.
        
        """
        return not manager.is_incompatible_class(cls)

    @classmethod
    def is_incompatible_class(manager, cls):
        """ is_incompatible_class(cls)
        
        Returns a string giving the reason why the given class 
        if not SSDF-compatible. If the class is compatible, this 
        function returns None.
        
        """
        if not hasattr(cls, '__to_ssdf__'):
            return "class does not have '__to_ssdf__' method"
        if not hasattr(cls, '__from_ssdf__'):
            return "class does not have '__from_ssdf__' classmethod"
        if not isinstance(cls, type):
            return 'class is not a type (does not inherit object on Python 2.x)'

    @classmethod
    def register_class(manager, *args):
        """ register_class(class1, class2, class3, ...)
        
        Register one or more classes. Registered classes can be saved and 
        restored from ssdf. 
        
        A class needs to implement two methods to qualify for registration:
        * A method __to_ssdf__() that returns an ssdf.Struct
        * A classmethod __from_ssdf__(s) that accepts an ssdf.Struct and
          creates an instance of that class.
        
        """
        for cls in args:
            incomp = manager.is_incompatible_class(cls)
            if incomp:
                raise ValueError('Cannot register class %s: %s.' % (
                 cls.__name__, incomp))
            else:
                manager._registered_classes[cls.__name__] = cls

    @classmethod
    def is_registered_class(manager, cls):
        """ is_registered_class(cls)
        
        Returns True if the given class is registered.
        
        """
        return cls in manager._registered_classes.values()


ClassManager = _ClassManager._register_at_sys()