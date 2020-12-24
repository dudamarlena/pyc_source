# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/classextension.py
# Compiled at: 2007-12-02 16:26:55
__all__ = [
 'ClassExtension']

def _func():
    pass


class ClassExtensionMetaclass(type):
    """
    This metaclass is the machinery that make ClassExtension work
    """
    __module__ = __name__

    def __init__(cls, name, bases, dict):
        if name == 'ClassExtension':
            return
        base = bases[1]
        for i in dict:
            if isinstance(dict[i], type(_func)) or isinstance(dict[i], classmethod) or isinstance(dict[i], staticmethod):
                setattr(base, i, dict[i])


class ClassExtension(object):
    """
    With this class we can add methods to an already defined class.

    Can be used to add backend specific methods to the searchparser and similar.

    It cannot be used if the class has already a metaclass.

    It is used like that:

    >>> class A(object):
    ...   def __init__(self):
    ...      pass
    ...
    ...   def base(self):
    ...      return "base method"

    >>> class B(ClassExtension, A):
    ...   def pippo(self):
    ...      return "pippo"

    >>> a = A()
    >>> a.pippo()
    'pippo'
    """
    __module__ = __name__
    __metaclass__ = ClassExtensionMetaclass


from salamoia.tests import *
runDocTests()