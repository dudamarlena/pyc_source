# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/Clumsy/misc/inherit_docstrings.py
# Compiled at: 2018-11-23 11:41:24
# Size of source mod 2**32: 4914 bytes
"""inherit_docstrings.py
author = nikratio

class Animal:
    def move_to(self, dest):
        '''Move to *dest*'''
        pass

def check_docstring(fn):
    assert fn.__doc__ == Animal.move_to.__doc__
    return fn

class Bird(Animal, metaclass=InheritableDocstrings):
    @check_docstring
    @copy_ancestor_docstring
    def move_to(self, dest):
        self._fly_to(dest)

assert Animal.move_to.__doc__ == Bird.move_to.__doc__

See Also
http://code.activestate.com/recipes/578587-inherit-method-docstrings-without-breaking-decorat/

"""
from functools import partial
__all__ = [
 'InheritableDocstrings']

def mro(*bases):
    return bases[0].__mro__


def copy_ancestor_docstring(fn):
    """Copy docstring for method from superclass

    For this decorator to work, the class has to use the `InheritableDocstrings`
    metaclass.
    """
    raise RuntimeError('Decorator can only be used in classes using the `InheritableDocstrings` metaclass')


def _copy_ancestor_docstring(mro, fn):
    """Decorator to set docstring for *fn* from *mro*"""
    if fn.__doc__ is not None:
        raise RuntimeError('Function already has docstring')
    for cls in mro:
        super_fn = getattr(cls, fn.__name__, None)
        if super_fn is None:
            continue
        fn.__doc__ = super_fn.__doc__
        break
    else:
        raise RuntimeError("Can't inherit docstring for %s: method does not exist in superclass" % fn.__name__)

    return fn


class InheritableDocstrings(type):
    __doc__ = "Object to allow inheriting of docstrings\n    class Animal:\n        def move_to(self, dest):\n            '''Move to *dest*'''\n            pass\n\n\n    class Bird(Animal, metaclass=InheritableDocstrings):\n        @copy_ancestor_docstring\n        def move_to(self, dest):\n            self._fly_to(dest) # Why is this fly to? I get it's a bird but isn't it unresolved?\n\n\n    assert Animal.move_to.__doc__ == Bird.move_to.__doc__\n\n    # ----> Use with other decorators\n    class Animal:\n        def move_to(self, dest):\n            '''Move to *dest*'''\n            pass\n\n\n    def check_docstring(fn):\n        assert fn.__doc__ == Animal.move_to.__doc__\n        return fn\n\n\n    class Bird(Animal, metaclass=InheritableDocstrings):\n        @check_docstring\n        @copy_ancestor_docstring\n        def move_to(self, dest):\n            self._fly_to(dest)\n\n\n    assert Animal.move_to.__doc__ == Bird.move_to.__doc__\n    print(Animal.move_to.__doc__, Bird.move_to.__doc__)\n    "

    @classmethod
    def __prepare__(cls, name, bases, **kwds):
        classdict = (super().__prepare__)(name, bases, *kwds)
        classdict['copy_ancestor_docstring'] = partial(_copy_ancestor_docstring, mro(*bases))
        return classdict

    def __new__(cls, name, bases, classdict):
        if 'copy_ancestor_docstring' in classdict:
            copy_impl = getattr(classdict['copy_ancestor_docstring'], 'func', None)
            if copy_impl is not _copy_ancestor_docstring:
                raise RuntimeError('No copy_ancestor_docstring attribute may be created in classes using the InheritableDocstrings metaclass')
            del classdict['copy_ancestor_docstring']
        return super().__new__(cls, name, bases, classdict)


if __name__ == '__main__':

    class Animal:

        def move_to(self, dest):
            """Move to *dest*"""
            pass


    class Bird(Animal, metaclass=InheritableDocstrings):

        @copy_ancestor_docstring
        def move_to(self, dest):
            self._fly_to(dest)


    assert Animal.move_to.__doc__ == Bird.move_to.__doc__

    class Animal:

        def move_to(self, dest):
            """Move to *dest*"""
            pass


    def check_docstring(fn):
        assert fn.__doc__ == Animal.move_to.__doc__
        return fn


    class Bird(Animal, metaclass=InheritableDocstrings):

        @check_docstring
        @copy_ancestor_docstring
        def move_to(self, dest):
            self._fly_to(dest)


    assert Animal.move_to.__doc__ == Bird.move_to.__doc__
    print(Animal.move_to.__doc__, Bird.move_to.__doc__)