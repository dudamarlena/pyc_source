# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/h2o/decorators/abstract.py
# Compiled at: 2007-12-02 16:26:56
"""
"""

def abstract(func):
    """
    This decorator help quickly document abstract methods:

    example::

        >>> class A(object):
        ...   @abstract
        ...   def test(self):
        ...     "method docstring...."

        >>> A().test()
        Traceback (most recent call last): 
        ...
        NotImplementedError: should be overriden
      
    """

    def override(*args, **kwargs):
        raise NotImplementedError, 'should be overriden'

    override.__name__ = func.__name__
    return override


from salamoia.tests import *
runDocTests()