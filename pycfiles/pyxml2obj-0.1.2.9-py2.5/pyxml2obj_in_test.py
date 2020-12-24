# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyxml2obj/pyxml2obj_in_test.py
# Compiled at: 2010-02-04 03:40:01
import unittest
from pyxml2obj import XMLin

class Xml2objInTest(unittest.TestCase):

    def testSimpleXML(self):
        expected = {'name1': 'value1', 'name2': 'value2'}
        opt = XMLin('<opt name1="value1" name2="value2"></opt>')
        self.assertEqual(opt, expected)
        self.assertEqual(isinstance(opt, dict), True)
        opt = XMLin('<opt name1="value1" name2="value2" />')
        self.assertEqual(opt, expected)
        opt = XMLin('\n    <opt> \n      <name1>value1</name1>\n      <name2>value2</name2>\n    </opt>\n    ')
        self.assertEqual(opt, expected)

    def testTwoLists(self):
        opt = XMLin('\n    <opt> \n      <name1>value1.1</name1>\n      <name1>value1.2</name1>\n      <name1>value1.3</name1>\n      <name2>value2.1</name2>\n      <name2>value2.2</name2>\n      <name2>value2.3</name2>\n    </opt>')
        self.assertEqual(opt, {'name1': [
                   'value1.1', 'value1.2', 'value1.3'], 
           'name2': [
                   'value2.1', 'value2.2', 'value2.3']})

    def testSimpleNestedHash(self):
        opt = XMLin('<opt><item name1="value1" name2="value2" /></opt>')
        self.assertEqual(opt, {'item': {'name1': 'value1', 'name2': 'value2'}})
        opt = XMLin('\n    <opt> \n      <item name1="value1" name2="value2" />\n      <item name1="value3" name2="value4" />\n    </opt>\n    ')
        self.assertEqual(opt, {'item': [{'name1': 'value1', 'name2': 'value2'}, {'name1': 'value3', 'name2': 'value4'}]})
        xml = '\n    <opt> \n      <item name="item1" attr1="value1" attr2="value2" />\n      <item name="item2" attr1="value3" attr2="value4" />\n    </opt>\n    '
        opt = XMLin(xml)
        self.assertEqual(opt, {'item': {'item1': {'attr1': 'value1', 'attr2': 'value2'}, 'item2': {'attr1': 'value3', 'attr2': 'value4'}}})
        opt = XMLin(xml, {'keyattr': [], 'contentkey': '-content'})
        self.assertEqual(opt, {'item': [{'name': 'item1', 'attr1': 'value1', 'attr2': 'value2'}, {'name': 'item2', 'attr1': 'value3', 'attr2': 'value4'}]})
        opt = XMLin(xml, {'keyattr': {}, 'contentkey': '-content'})
        self.assertEqual(opt, {'item': [{'name': 'item1', 'attr1': 'value1', 'attr2': 'value2'}, {'name': 'item2', 'attr1': 'value3', 'attr2': 'value4'}]})
        opt = XMLin('\n    <opt> \n      <item key="item1" attr1="value1" attr2="value2" />\n      <item key="item2" attr1="value3" attr2="value4" />\n    </opt>\n    ', {'contentkey': '-content'})
        self.assertEqual(opt, {'item': {'item1': {'attr1': 'value1', 'attr2': 'value2'}, 'item2': {'attr1': 'value3', 'attr2': 'value4'}}})
        opt = XMLin('\n    <opt> \n      <item id="item1" attr1="value1" attr2="value2" />\n      <item id="item2" attr1="value3" attr2="value4" />\n    </opt>\n    ', {'contentkey': '-content'})
        self.assertEqual(opt, {'item': {'item1': {'attr1': 'value1', 'attr2': 'value2'}, 'item2': {'attr1': 'value3', 'attr2': 'value4'}}})

    def testUserKey(self):
        xml = '\n    <opt> \n      <item xname="item1" attr1="value1" attr2="value2" />\n      <item xname="item2" attr1="value3" attr2="value4" />\n    </opt>\n    '
        target = {'item': {'item1': {'attr1': 'value1', 'attr2': 'value2'}, 'item2': {'attr1': 'value3', 'attr2': 'value4'}}}
        opt = XMLin(xml, {'keyattr': ['xname'], 'contentkey': '-content'})
        self.assertEqual(opt, target)
        opt = XMLin(xml, {'keyattr': ['wibble', 'xname'], 'contentkey': '-content'})
        self.assertEqual(opt, target)
        opt = XMLin(xml, {'keyattr': {'item': 'xname'}, 'contentkey': '-content'})
        self.assertEqual(opt, target)
        opt = XMLin(xml, {'keyattr': 'xname', 'contentkey': '-content'})
        self.assertEqual(opt, target)
        opt = XMLin(xml, {'KeyAttr': 'xname', 'contentkey': '-content'})
        self.assertEqual(opt, target)
        opt = XMLin(xml, {'key_attr': 'xname', 'contentkey': '-content'})
        self.assertEqual(opt, target)

    def testOverlapKey(self):
        xml = '\n    <opt>\n      <item id="one" value="1" name="a" />\n      <item id="two" value="2" />\n      <item id="three" value="3" />\n    </opt>\n    '
        target = {'item': {'three': {'value': '3'}, 'a': {'value': '1', 'id': 'one'}, 'two': {'value': '2'}}}
        opt = XMLin(xml, {'contentkey': '-content'})
        self.assertEqual(opt, target)
        target = {'item': {'one': {'value': '1', 'name': 'a'}, 'two': {'value': '2'}, 'three': {'value': '3'}}}
        opt = XMLin(xml, {'keyattr': {'item': 'id'}, 'contentkey': '-content'})
        self.assertEqual(opt, target)

    def testMoreComplex(self):
        xml = '\n    <opt>\n      <car license="SH6673" make="Ford" id="1">\n        <option key="1" pn="6389733317-12" desc="Electric Windows"/>\n        <option key="2" pn="3735498158-01" desc="Leather Seats"/>\n        <option key="3" pn="5776155953-25" desc="Sun Roof"/>\n      </car>\n      <car license="LW1804" make="GM"   id="2">\n        <option key="1" pn="9926543-1167" desc="Steering Wheel"/>\n      </car>\n    </opt>\n    '
        target = {'car': {'LW1804': {'id': '2', 
                              'make': 'GM', 
                              'option': {'9926543-1167': {'key': '1', 'desc': 'Steering Wheel'}}}, 
                   'SH6673': {'id': '1', 
                              'make': 'Ford', 
                              'option': {'6389733317-12': {'key': '1', 'desc': 'Electric Windows'}, '3735498158-01': {'key': '2', 'desc': 'Leather Seats'}, '5776155953-25': {'key': '3', 'desc': 'Sun Roof'}}}}}
        opt = XMLin(xml, {'forcearray': 1, 'keyattr': {'car': 'license', 'option': 'pn'}, 'contentkey': '-content'})
        self.assertEqual(opt, target)
        xml = '\n    <opt>\n      <item>\n        <name><firstname>Bob</firstname></name>\n        <age>21</age>\n      </item>\n      <item>\n        <name><firstname>Kate</firstname></name>\n        <age>22</age>\n      </item>\n    </opt>    \n    '
        target = {'item': [{'age': '21', 'name': {'firstname': 'Bob'}}, {'age': '22', 'name': {'firstname': 'Kate'}}]}
        opt = XMLin(xml, {'contentkey': '-content'})
        self.assertEqual(opt, target)

    def testAnounymousArray(self):
        xml = '\n      <opt>\n        <row>\n          <anon>0.0</anon><anon>0.1</anon><anon>0.2</anon>\n        </row>\n        <row>\n          <anon>1.0</anon><anon>1.1</anon><anon>1.2</anon>\n        </row>\n        <row>\n          <anon>2.0</anon><anon>2.1</anon><anon>2.2</anon>\n        </row>\n      </opt>\n      '
        expected = {'row': [
                 [
                  '0.0', '0.1', '0.2'],
                 [
                  '1.0', '1.1', '1.2'],
                 [
                  '2.0', '2.1', '2.2']]}
        opt = XMLin(xml, {'contentkey': '-content'})
        self.assertEqual(opt, expected)
        xml = '\n    <opt>\n      <anon>one</anon>\n      <anon>two</anon>\n      <anon>three</anon>\n    </opt>\n    '
        opt = XMLin(xml)
        target = ['one', 'two', 'three']
        self.assertEqual(opt, target)
        xml = '\n    <opt>\n      <anon>1</anon>\n      <anon>\n        <anon>2.1</anon>\n        <anon>\n          <anon>2.2.1</anon>\n          <anon>2.2.2</anon>\n        </anon>\n      </anon>\n    </opt>\n    '
        opt = XMLin(xml)
        target = [
         '1', ['2.1', ['2.2.1', '2.2.2']]]
        self.assertEqual(opt, target)

    def testContentAttribute(self):
        xml = '\n    <opt>\n      <item attr="value">text</item>\n    </opt>\n    '
        target = {'item': {'content': 'text', 
                    'attr': 'value'}}
        opt = XMLin(xml)
        self.assertEqual(opt, target)
        opt = XMLin(xml, {'contentkey': 'text_content'})
        self.assertEqual(opt, {'item': {'text_content': 'text', 
                    'attr': 'value'}})
        xml = '<opt attr="value">text content</opt>'
        opt = XMLin(xml, {'forcearray': 1})
        self.assertEqual(opt, {'attr': 'value', 
           'content': 'text content'})

    def test_forcearray(self):
        xml = '\n    <opt zero="0">\n      <one>i</one>\n      <two>ii</two>\n      <three>iii</three>\n      <three>3</three>\n      <three>c</three>\n    </opt>    \n    '
        opt = XMLin(xml, {'forcearray': ['two']})
        self.assertEqual(opt, {'zero': '0', 
           'one': 'i', 
           'two': [
                 'ii'], 
           'three': [
                   'iii', '3', 'c']})

    def testJapaneseNode(self):
        xml = '\n    <opt> \n      <name1>バリュー１</name1>\n      <name2>バリュー２</name2>\n    </opt>\n    '
        target = {'name1': 'バリュー１', 
           'name2': 'バリュー２'}
        opt = XMLin(xml)
        self.assertEqual(opt, target)


if __name__ == '__main__':
    unittest.main()