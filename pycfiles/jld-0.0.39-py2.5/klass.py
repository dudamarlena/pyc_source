# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Documents and Settings\Jean-Lou Dupont\My Documents\workspace_gae\jldupont\trunk\libs\python\jld\jld\tools\klass.py
# Compiled at: 2009-01-14 16:14:48
"""
    @author: Jean-Lou Dupont
"""
__author__ = 'Jean-Lou Dupont'
__version__ = '$Id: klass.py 799 2009-01-14 20:16:50Z JeanLou.Dupont $'
import inspect
from types import *

def searchForMethods(obj, prefix, stripPrefix=True):
    """ Search for all methods with starting prefix. 
        Returns 2 lists:
        1) matching method names (stripped if required)
        2) tuples (method_name, doc_string)
    """
    all_methods = inspect.getmembers(obj, lambda X: type(X) is MethodType)
    methods = filter(lambda X: str(X[0]).startswith(prefix), all_methods)
    _liste = []
    _matches = []
    for method in methods:
        _name = str(method[0])
        _type = method[1]
        if stripPrefix:
            _name = _name[len(prefix):]
        _liste.append((_name, inspect.getdoc(method[1])))
        _matches.append(_name)

    return (_matches, _liste)


if __name__ == '__main__':

    class X(object):

        def __init__(self):
            pass

        def cmd_C1(self):
            """Command C1"""
            pass

        def cmd_C2(self):
            """Command C2"""
            pass

        def other(self):
            pass


    print searchForMethods(X, 'cmd_')
    x = X()
    print searchForMethods(x, 'cmd_')
    print searchForMethods(X, '')