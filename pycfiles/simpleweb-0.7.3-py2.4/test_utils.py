# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/test/test_utils.py
# Compiled at: 2007-01-10 11:06:17
import utils
__all__ = ['Bogus']

class Bogus:
    __module__ = __name__

    def foo(self):
        pass


def test_get_functions():
    funcs = utils.get_functions('test_utils')
    assert test_get_functions in funcs
    assert Bogus not in funcs
    funcs2 = utils.get_functions('test_utils.Bogus')
    assert Bogus.foo.im_func in funcs2


def test_get_methods_dict():
    methods_dict = utils.get_methods_dict('test_utils', ['test_get_functions', 'test_get_methods_dict'])
    assert test_get_methods_dict is methods_dict['test_get_methods_dict']
    assert test_get_functions is methods_dict['test_get_functions']


def test_from_import():
    from plugins import dblayer
    from test_utils import Bogus
    dbl = utils.from_import('plugins.dblayer')
    assert dbl is dblayer
    bg = utils.from_import('test_utils.Bogus')
    assert bg is Bogus