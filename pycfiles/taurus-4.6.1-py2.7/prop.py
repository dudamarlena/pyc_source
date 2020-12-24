# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/prop.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains a decorator to simplify the use of property."""
from __future__ import print_function
from __future__ import absolute_import
__all__ = [
 'propertx']
__docformat__ = 'restructuredtext'

def propertx(fct):
    """
        Decorator to simplify the use of property.
        Like @property for attrs who need more than a getter.
        For getter only property use @property.

        adapted from http://code.activestate.com/recipes/502243/
    """
    arg = [
     None, None, None, None]
    for i, f in enumerate(fct()):
        arg[i] = f

    if not arg[3]:
        arg[3] = fct.__doc__
    return property(*arg)


if __name__ == '__main__':
    from .log import Logger

    class example(object, Logger):

        def __init__(self):
            Logger.__init__(self, 'example')
            self._a = 100
            self.bar = 'why'

        @propertx
        def bar():

            def get(self):
                print('\tgetting', self._a)
                return self._a

            def set(self, val):
                print('\tsetting', val)
                self._a = val

            return (get, set)


    foo = example()
    print(foo.bar)