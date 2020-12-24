# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tests/test_builders.py
# Compiled at: 2016-08-26 08:08:37
from unittest import TestCase
from pojen import builders

class BuildersTestCase(TestCase):

    def test_builds_method(self):
        name = 'add'
        acc = 'private'
        ret = 'int'
        params = {'a': 'int', 
           'b': 'int'}
        body = '\n    return a+b;'
        method = builders.method(name, acc, ret, params, body)
        pre = '    private int add(int a,int b){\n    return a+b;}'
        self.assertEqual(method.replace('\n', ''), pre.replace('\n', ''))

    def test_builds_getter(self):
        varname = 'name'
        vartype = 'String'
        method = builders.getter(varname, vartype)
        pre = '    public String getName(){\n        return this.name;\n    }'
        self.assertEqual(method.replace('\n', ''), pre.replace('\n', ''))

    def test_builds_setter(self):
        varname = 'name'
        vartype = 'String'
        method = builders.setter(varname, vartype)
        pre = '    public void setName(String name){\n        this.name = name;\n    }'
        self.assertEqual(method.replace('\n', ''), pre.replace('\n', ''))

    def test_builds_field(self):
        varname = 'name'
        vartype = 'String'
        acc_modifier = 'private'
        field = builders.field(varname, vartype, acc_modifier)
        pre = 'private String name;'
        self.assertEqual(field, pre)

    def test_builds_class(self):
        classname = 'Obj'
        fields = {'name': 'String'}
        _class = builders.generate_class(classname, fields)
        pre = 'public class Obj{\n    private String name;\n\n\n    public String getName(){\n        return this.name;\n    }\n\n    public void setName(String name){\n        this.name = name;\n    }\n\n}'
        self.assertEqual(_class, pre)