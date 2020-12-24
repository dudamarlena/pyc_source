# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tgwebservices/tests/test_controllers.py
# Compiled at: 2010-01-29 07:00:58
try:
    from xml.etree import cElementTree as et
except ImportError:
    import cElementTree as et

from tgwebservices.iconv import _get_single_value, handle_json_params

class Person(object):
    name = str
    age = int
    married = False


def test_complex_conversion_simple_class():
    tree = et.fromstring('<p>\n    <name>Super Value Menu</name>\n    <age>17</age>\n    <married>no</married>\n</p>')
    val = _get_single_value(tree, Person)
    print val
    assert isinstance(val, Person)
    assert val.age == 17
    assert val.name == 'Super Value Menu'
    print val.married
    assert val.married == False


class Family1(object):
    lastname = str
    members = [str]


def test_complex_conversion_with_list():
    tree = et.fromstring('<family>\n    <lastname>Brady</lastname>\n    <members>\n        <item>Mike</item>\n        <item>Carol</item>\n        <item>Greg</item>\n        <item>Peter</item>\n        <item>Bobby</item>\n        <item>Marsha</item>\n        <item>Jan</item>\n        <item>Cindy</item>\n    </members>\n</family>\n')
    val = _get_single_value(tree, Family1)
    assert val.lastname == 'Brady'
    print val.members
    assert len(val.members) == 8
    assert val.members[2] == 'Greg'


class Family2(object):
    lastname = str
    members = [Person]


def test_complex_with_list_of_instances():
    tree = et.fromstring('<family>\n    <lastname>Brady</lastname>\n    <members>\n        <item>\n            <name>Mike</name>\n            <age>42</age>\n        </item>\n        <item>\n            <name>Carol</name>\n            <age>40</age>\n        </item>\n        <item>\n            <name>Greg</name>\n            <age>17</age>\n        </item>\n        <item>\n            <name>Peter</name>\n            <age>13</age>\n        </item>\n        <item>\n            <name>Bobby</name>\n            <age>8</age>\n        </item>\n        <item>\n            <name>Marsha</name>\n            <age>16</age>\n        </item>\n        <item>\n            <name>Jan</name>\n            <age>13</age>\n        </item>\n        <item>\n            <name>Cindy</name>\n            <age>7</age>\n        </item>\n    </members>\n</family>\n')
    val = _get_single_value(tree, Family2)
    assert val.lastname == 'Brady'
    print val.members
    assert len(val.members) == 8


def test_list_of_bools():
    tree = et.fromstring('<list>\n    <item>no</item>\n    <item>false</item>\n    <item>yes</item>\n    <item>False</item>\n    <item>true</item>\n</list>')
    val = _get_single_value(tree, [bool])
    print val
    assert len(val) == 5


def test_json_conversion_of_class():
    input_types = {'person': Person}
    data = {'person': {'name': 'Fred', 'age': 99}}
    kw = handle_json_params(data, input_types)
    assert isinstance(kw['person'], Person)
    print kw['person'].age
    assert kw['person'].age == 99
    assert kw['person'].name == 'Fred'


def test_json_conversion_of_nested_class():
    input_types = {'family': Family2}
    data = {'family': {'lastname': 'Brady', 'members': [{'name': 'Mike', 'age': 42}, {'name': 'Carol', 'age': 40}]}}
    kw = handle_json_params(data, input_types)
    assert isinstance(kw['family'], Family2)
    assert len(kw['family'].members) == 2
    assert kw['family'].members[0].name == 'Mike'
    assert kw['family'].members[0].age == 42