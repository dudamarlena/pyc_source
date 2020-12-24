# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/pyxml2obj/pyxml2obj_out_test.py
# Compiled at: 2010-02-03 10:43:26
import re, unittest
from pyxml2obj import XMLin, XMLout

class XML2objOutTest(unittest.TestCase):

    def testScalar(self):
        xml = XMLout('scalar')
        self.assertEqual(XMLin(xml), 'scalar')

    def testHash(self):
        hash1 = {'one': '1', 'two': 'II', 'three': '...'}
        xml = XMLout(hash1)
        self.assertEqual(XMLin(xml), hash1)

    def testSimmpleArray(self):
        tree = {'array': ['one', 'two', 'three']}
        expect = '<root>\n  <array>one</array>\n  <array>two</array>\n  <array>three</array>\n</root>\n'
        xml = XMLout(tree)
        self.assertEqual(xml, expect)

    def testNestedHash(self):
        tree = {'value': '555 1234', 'hash1': {'one': 1}, 'hash2': {'two': 2}}
        expected = '<root value="555 1234">\n  <hash1 one="1" />\n  <hash2 two="2" />\n</root>\n'
        xml = XMLout(tree)
        self.assertEqual(xml, expected)

    def testAnonymousArray(self):
        tree = [
         '1', 'two', 'Ⅲ']
        expected = '<root>\n  <anon>1</anon>\n  <anon>two</anon>\n  <anon>Ⅲ</anon>\n</root>\n'
        xml = XMLout(tree)
        self.assertEqual(xml, expected)

    def testNestedAnonymousArray(self):
        tree = [
         [
          1.1, 1.2], [2.1, 2.2]]
        expected = '<root>\n  <anon>\n    <anon>1.1</anon>\n    <anon>1.2</anon>\n  </anon>\n  <anon>\n    <anon>2.1</anon>\n    <anon>2.2</anon>\n  </anon>\n</root>\n'
        xml = XMLout(tree)
        self.assertEqual(xml, expected)

    def testHashOfHash(self):
        tree = {'country': {'England': {'capital': 'London'}, 'France': {'capital': 'Paris'}, 'Turkey': {'capital': 'Istanbul'}}}
        expected = '<root>\n  <country>\n    <England capital="London" />\n    <France capital="Paris" />\n    <Turkey capital="Istanbul" />\n  </country>\n</root>\n'
        xml = XMLout(tree, {'keyattr': []})
        self.assertEqual(xml, expected)
        expected = '\n^\\s*<(\\w+)\\s*>\\s*\n(\n   <country(\\s*fullname="Turkey"  |\\s*capital="Istanbul" ){2}\\s*/>\\s*\n  |<country(\\s*fullname="France"  |\\s*capital="Paris"    ){2}\\s*/>\\s*\n  |<country(\\s*fullname="England" |\\s*capital="London"   ){2}\\s*/>\\s*\n){3}\n</\\1>\\s*$\n'
        xml = XMLout(tree, {'keyattr': ['fullname']})
        self.assert_(re.match(expected, xml, re.VERBOSE))
        xml = XMLout(tree, {'keyattr': 'fullname'})
        self.assert_(re.match(expected, xml, re.VERBOSE))
        xml = XMLout(tree, {'keyattr': {'country': 'fullname'}})
        self.assert_(re.match(expected, xml, re.VERBOSE))
        xml = XMLout(tree, {'keyattr': {'country': '+fullname'}})
        self.assert_(re.match(expected, xml, re.VERBOSE))
        xml = XMLout(tree, {'keyattr': {'country': '-fullname'}})
        self.assert_(re.match(expected, xml, re.VERBOSE))
        expected = '\n  ^\\s*<(\\w+)\\s*>\\s*\n    (\n      <country(\\s*name="Turkey"|\\s*capital="Istanbul"){2}\\s*/>\\s*\n     |<country(\\s*name="France"|\\s*capital="Paris"){2}\\s*/>\\s*\n     |<country(\\s*name="England"|\\s*capital="London"){2}\\s*/>\\s*\n    ){3}\n  </\\1>$\n  '
        xml = XMLout(tree)
        self.assert_(re.match(expected, xml, re.VERBOSE))

    def test_forld_a_nested_hash(self):
        tree = {'country': {'England': {'capital': 'London'}}}
        xml = XMLout(tree)
        expected = '\n  ^\\s*<(\\w+)\\s*>\\s*\n    (\n     <country(\\s*name="England"|\\s*capital="London"){2}\\s*/>\\s*\n    )\n  </\\1>$\n  '
        self.assert_(re.match(expected, xml, re.VERBOSE))

    def test_xml_decl(self):
        tree = {'one': 1}
        xml = XMLout(tree, {'xmldecl': 1})
        no_header = xml.replace("<?xml version='1.0' standalone='yes'?>", '')
        self.assertTrue(xml != no_header)
        self.assert_(re.match('^\\s*<root\\s+one="1"\\s*/>', no_header, re.VERBOSE))
        custom_header = '<?xml custom header ?>'
        xml = XMLout(tree, {'xmldecl': custom_header})
        no_header = xml.replace(custom_header, '')
        self.assertTrue(xml != no_header)
        self.assert_(re.match('^\\s*<root\\s+one="1"\\s*/>', no_header, re.VERBOSE))

    def test_escape(self):
        tree = {'a': '<A>', 'b': '"B"', 'c': '&C&'}
        xml = XMLout(tree)
        self.assert_(re.search('a="&lt;A&gt;"', xml))
        self.assert_(re.search('b="&quot;B&quot;"', xml))
        self.assert_(re.search('c="&amp;C&amp;"', xml))
        tree = {'a': '<A>', 'b': '"B"', 'c': ['&C&']}
        xml = XMLout(tree, {'noescape': 1})
        self.assert_(re.search('a="<A>"', xml))
        self.assert_(re.search('b=""B""', xml))
        self.assert_(re.search('<c>&C&</c>', xml))

    def test_circular_data(self):
        tree = {'a': '1'}
        tree['b'] = tree
        try:
            xml = XMLout(tree)
            self.fail('circular data is not detected')
        except:
            pass

    def test_complex_hash(self):
        tree = {'car': {'LW1804': {'option': {'9926543-1167': {'key': 1, 'desc': 'Steering Wheel'}}, 'id': 2, 
                              'make': 'GM'}, 
                   'SH6673': {'option': {'6389733317-12': {'key': 2, 'desc': 'Electric Windows'}, '3735498158-01': {'key': 3, 'desc': 'Leather Seats'}, '5776155953-25': {'key': 4, 'desc': 'Sun Roof'}}, 'id': 1, 
                              'make': 'Ford'}}}
        xml = XMLout(tree, {'keyattr': {'car': 'license', 'option': 'pn'}})
        self.assert_(re.search('\\s*make="GM"', xml))
        self.assert_(re.search('\\s*id="2"', xml))
        self.assert_(re.search('\\s*license="LW1804"', xml))
        self.assert_(re.search('\\s*desc="Steering Wheel"', xml))
        self.assert_(re.search('\\s*pn="9926543-1167"', xml))
        self.assert_(re.search('\\s*key="1"', xml))
        self.assert_(re.search('\\s*make="Ford"', xml))
        self.assert_(re.search('\\s*id="1"', xml))
        self.assert_(re.search('\\s*license="SH6673"', xml))
        self.assert_(re.search('\\s*desc="Electric Windows"', xml))
        self.assert_(re.search('\\s*pn="6389733317-12"', xml))
        self.assert_(re.search('\\s*key="2"', xml))
        self.assert_(re.search('\\s*desc="Leather Seats"', xml))
        self.assert_(re.search('\\s*pn="3735498158-01"', xml))
        self.assert_(re.search('\\s*key="3"', xml))
        self.assert_(re.search('\\s*desc="Sun Roof"', xml))
        self.assert_(re.search('\\s*pn="5776155953-25"', xml))
        self.assert_(re.search('\\s*key="4"', xml))

    def test_grouptag(self):
        tree = {'prefix': 'before', 
           'dirs': [
                  '/usr/bin', '/usr/local/bin'], 
           'suffix': 'after'}
        expected = '<root>\n  <dirs>\n    <dir>/usr/bin</dir>\n    <dir>/usr/local/bin</dir>\n  </dirs>\n  <prefix>before</prefix>\n  <suffix>after</suffix>\n</root>\n'
        xml = XMLout(tree, {'grouptags': {'dirs': 'dir'}, 'noattr': 1})
        self.assertEqual(xml, expected)
        try:
            xml = XMLout(tree, {'grouptags': {'dirs': 'dirs'}, 'noattr': 1})
            fail('cant detect invalid group tag')
        except:
            self.assertTrue(True)

    def test_keeproot(self):
        tree = {'seq': {'name': 'alpha', 
                   'alpha': [
                           1, 2, 3]}}
        xml1 = XMLout(tree, {'rootname': 'sequence'})
        xml2 = XMLout({'sequence': tree}, {'keeproot': 1})
        self.assertEqual(xml1, xml2)
        xml = XMLout(tree, {'keeproot': 1})
        match = re.search('root', xml)
        self.assertTrue(match == None)
        return

    def test_contentkey(self):
        tree = {'one': 1, 'content': 'text'}
        xml = XMLout(tree)
        expected = '^\\s*<root\\s+one="1">text</root>\\s*$'
        self.assert_(re.match(expected, xml, re.VERBOSE))

    def test_noattr(self):
        tree = {'attr1': 'value1', 
           'attr2': 'value2', 
           'nest': [
                  'one', 'two', 'three']}
        expected = '<root>\n  <attr1>value1</attr1>\n  <attr2>value2</attr2>\n  <nest>one</nest>\n  <nest>two</nest>\n  <nest>three</nest>\n</root>\n'
        xml = XMLout(tree, {'noattr': 1})
        self.assertEqual(xml, expected)
        tree = {'number': {'twenty one': {'dec': 21, 'hex': '0x15'}, 'thirty two': {'dec': 32, 'hex': '0x20'}}}
        xml = XMLout(tree, {'noattr': 1, 'keyattr': ['word']})
        xml = re.sub('\\s*<(dec)>21</\\1>\\s*', '21', xml)
        xml = re.sub('\\s*<(hex)>0x15</\\1>\\s*', '21', xml)
        xml = re.sub('\\s*<(word)>twenty one</\\1>\\s*', '21', xml)
        xml = re.sub('\\s*<(number)>212121</\\1>\\s*', 'NUM', xml)
        xml = re.sub('\\s*<(dec)>32</\\1>\\s*', '32', xml)
        xml = re.sub('\\s*<(hex)>0x20</\\1>\\s*', '32', xml)
        xml = re.sub('\\s*<(word)>thirty two</\\1>\\s*', '32', xml)
        xml = re.sub('\\s*<(number)>323232</\\1>\\s*', 'NUM', xml)
        self.assert_(re.match('^<(\\w+)\\s*>NUMNUM</\\1>$', xml))

    def test_rootname(self):
        xml = XMLout('scalar', {'rootname': 'TOM'})
        self.assert_(re.match('^\\s*<TOM>scalar<\\/TOM>\\s*$', xml))
        tree = {'array': ['one', 'two', 'three']}
        xml = XMLout(tree, {'rootname': 'LARRY'})
        xml = re.sub('<array>one</array>\\s*', '', xml)
        xml = re.sub('<array>two</array>\\s*', '', xml)
        xml = re.sub('<array>three</array>\\s*', '', xml)
        self.assert_(re.match('^<(LARRY)\\s*>\\s*<\\/\\1>\\s*$', xml))

    def test_valueattr(self):
        tree = {'one': 1, 'two': 2, 'six': 6}
        expected = '^<root\\s+two="2"\\s*>\n      (\n        \\s*<one\\s+value="1"\\s*/>\n      | \\s*<six\\s+num="6"\\s*/>\n      ){2}\n    \\s*</root>$\n'
        xml = XMLout(tree, {'ValueAttr': {'one': 'value', 'six': 'num'}})
        self.assert_(re.match(expected, xml, re.VERBOSE))

    def test_grouptags(self):
        tree = {'dirs': {'first': '/usr/bin', 
                    'second': '/usr/local/bin'}}
        expected = '^<(\\w+)>\\s*\n    <dirs>\\s*\n      <dir\n        (?:\n          \\s+first="/usr/bin"\n         |\\s+second="/usr/local/bin"\n        ){2}\\s*\n      />\\s*\n    </dirs>\\s*\n  </\\1>$\n'
        xml = XMLout(tree, {'grouptags': {'dirs': 'dir'}, 'keyattr': {'dir': 'name'}, 'contentkey': '-content'})
        self.assert_(re.match(expected, xml, re.VERBOSE))


if __name__ == '__main__':
    unittest.main()