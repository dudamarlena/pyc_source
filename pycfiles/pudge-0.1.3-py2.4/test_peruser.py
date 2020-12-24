# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.0-Power_Macintosh/egg/pudge/test/test_peruser.py
# Compiled at: 2006-03-14 16:35:23
import pudge.peruser as peruser, pudge.test.package as test_package

def test_fixfile():
    assert peruser.fix_file('bla/bla.pyc') == 'bla/bla.py'


def test_get_peruser_type():
    assert peruser.get_peruser_type(test_package) is peruser.ModulePeruser
    assert peruser.get_peruser_type(test_package.func) is peruser.CallablePeruser
    assert peruser.get_peruser_type(test_package.Class) is peruser.ClassPeruser
    assert peruser.get_peruser_type(test_package.name) is peruser.NamePeruser


def test_find_module():
    m = peruser.find('pudge.test.package')
    assert isinstance(m, peruser.ModulePeruser)
    assert m.obj is test_package
    assert m.name == 'package'
    assert m.parent is not None
    return


def test_member_func():
    m = peruser.find('pudge.test.package')
    func = m.member('func')
    assert func.obj is test_package.func
    assert func.name == 'func'


def test_get_qualified_name():
    m = peruser.find('pudge.test.package')
    func = m.member('func')
    assert func.get_qualified_name() == 'pudge.test.package.func'


def test_get_filename():
    expected = peruser.fix_file(test_package.__file__)
    m = peruser.find('pudge.test.package')
    assert m.get_file() == expected
    func = m.member('func')
    assert func.get_file() == expected
    cls = m.member('Class')
    assert cls.get_file() == expected
    name = m.member('name')
    assert name.get_file() == expected