# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zif/jsonserver/tests/test_json.py
# Compiled at: 2007-05-25 16:54:16
"""JSON Tests
jwashin 2005-08-18
altered imports to reflect zif namespace 2006-12-16 jmw
"""
import unittest
from zif.jsonserver import minjson as json
from zif.jsonserver.minjson import ReadException, WriteException

def spaceless(aString):
    return aString.replace(' ', '')


class JSONTests(unittest.TestCase):
    __module__ = __name__

    def testReadString(self):
        s = "'hello'"
        self.assertEqual(json.read(s), 'hello')

    def testWriteString(self):
        s = 'hello'
        self.assertEqual(json.write(s), '"hello"')

    def testReadInt(self):
        s = '1'
        self.assertEqual(json.read(s), 1)

    def testWriteInt(self):
        s = 1
        self.assertEqual(json.write(s), '1')

    def testReadLong(self):
        s = '999999999999999999999'
        self.assertEqual(json.read(s), 999999999999999999999)

    def testWriteShortLong(self):
        s = 1
        self.assertEqual(json.write(s), '1')

    def testWriteLongLong(self):
        s = 999999999999999999999
        self.assertEqual(json.write(s), '999999999999999999999')

    def testReadNegInt(self):
        s = '-1'
        assert json.read(s) == -1

    def testWriteNegInt(self):
        s = -1
        assert json.write(s) == '-1'

    def testReadFloat(self):
        s = '1.334'
        assert json.read(s) == 1.334

    def testReadEFloat1(self):
        s = '1.334E2'
        assert json.read(s) == 133.4

    def testReadEFloat2(self):
        s = '1.334E-02'
        assert json.read(s) == 0.01334

    def testReadeFloat1(self):
        s = '1.334e2'
        assert json.read(s) == 133.4

    def testReadeFloat2(self):
        s = '1.334e-02'
        assert json.read(s) == 0.01334

    def testWriteFloat(self):
        s = 1.334
        assert json.write(s) == '1.334'

    def testWriteDecimal(self):
        try:
            from decimal import Decimal
            s = Decimal('1.33')
            assert json.write(s) == '1.33'
        except ImportError:
            pass

    def testReadNegFloat(self):
        s = '-1.334'
        assert json.read(s) == -1.334

    def testWriteNegFloat(self):
        s = -1.334
        assert json.write(s) == '-1.334'

    def testReadEmptyDict(self):
        s = '{}'
        assert json.read(s) == {}

    def testWriteEmptyList(self):
        s = []
        assert json.write(s) == '[]'

    def testWriteEmptyTuple(self):
        s = ()
        assert json.write(s) == '[]'

    def testReadEmptyList(self):
        s = '[]'
        assert json.read(s) == []

    def testWriteEmptyDict(self):
        s = {}
        assert json.write(s) == '{}'

    def testReadTrue(self):
        s = 'true'
        assert json.read(s) == True

    def testWriteTrue(self):
        s = True
        assert json.write(s) == 'true'

    def testReadStringTrue(self):
        s = '"true"'
        assert json.read(s) == 'true'

    def testWriteStringTrue(self):
        s = 'True'
        assert json.write(s) == '"True"'

    def testReadStringNull(self):
        s = '"null"'
        assert json.read(s) == 'null'

    def testWriteStringNone(self):
        s = 'None'
        assert json.write(s) == '"None"'

    def testReadFalse(self):
        s = 'false'
        assert json.read(s) == False

    def testWriteFalse(self):
        s = False
        assert json.write(s) == 'false'

    def testReadNull(self):
        s = 'null'
        assert json.read(s) == None
        return

    def testWriteNone(self):
        s = None
        assert json.write(s) == 'null'
        return

    def testReadDictOfLists(self):
        s = "{'a':[],'b':[]}"
        assert json.read(s) == {'a': [], 'b': []}

    def testReadDictOfListsWithSpaces(self):
        s = "{  'a' :    [],  'b'  : []  }    "
        assert json.read(s) == {'a': [], 'b': []}

    def testWriteDictOfLists(self):
        s = {'a': [], 'b': []}
        assert spaceless(json.write(s)) == '{"a":[],"b":[]}'

    def testWriteDictOfTuples(self):
        s = {'a': (), 'b': ()}
        assert spaceless(json.write(s)) == '{"a":[],"b":[]}'

    def testWriteDictWithNonemptyTuples(self):
        s = {'a': ('fred', 7), 'b': ('mary', 1.234)}
        w = json.write(s)
        assert spaceless(w) == '{"a":["fred",7],"b":["mary",1.234]}'

    def testWriteVirtualTuple(self):
        s = (4, 4, 5, 6)
        w = json.write(s)
        assert spaceless(w) == '[4,4,5,6]'

    def testReadListOfDicts(self):
        s = '[{},{}]'
        assert json.read(s) == [{}, {}]

    def testReadListOfDictsWithSpaces(self):
        s = ' [ {    } ,{   \n} ]   '
        assert json.read(s) == [{}, {}]

    def testWriteListOfDicts(self):
        s = [{}, {}]
        assert spaceless(json.write(s)) == '[{},{}]'

    def testWriteTupleOfDicts(self):
        s = ({}, {})
        assert spaceless(json.write(s)) == '[{},{}]'

    def testReadListOfStrings(self):
        s = "['a','b','c']"
        assert json.read(s) == ['a', 'b', 'c']

    def testReadListOfStringsWithSpaces(self):
        s = " ['a'    ,'b'  ,\n  'c']  "
        assert json.read(s) == ['a', 'b', 'c']

    def testReadStringWithWhiteSpace(self):
        s = "'hello \\tworld'"
        assert json.read(s) == 'hello \tworld'

    def testWriteMixedList(self):
        o = [
         'OIL', 34, 199, 38.5]
        assert spaceless(json.write(o)) == '["OIL",34,199,38.5]'

    def testWriteMixedTuple(self):
        o = ('OIL', 34, 199, 38.5)
        assert spaceless(json.write(o)) == '["OIL",34,199,38.5]'

    def testWriteStringWithWhiteSpace(self):
        s = 'hello \tworld'
        assert json.write(s) == '"hello \\tworld"'

    def testWriteListofStringsWithApostrophes(self):
        s = [
         "hasn't", "don't", "isn't", True, "won't"]
        w = json.write(s)
        assert spaceless(w) == '["hasn\'t","don\'t","isn\'t",true,"won\'t"]'

    def testWriteTupleofStringsWithApostrophes(self):
        s = (
         "hasn't", "don't", "isn't", True, "won't")
        w = json.write(s)
        assert spaceless(w) == '["hasn\'t","don\'t","isn\'t",true,"won\'t"]'

    def testWriteListofStringsWithRandomQuoting(self):
        s = [
         "hasn't", 'do"n\'t', "isn't", True, 'wo"n\'t']
        w = json.write(s)
        assert 'true' in w

    def testWriteStringWithDoubleQuote(self):
        s = 'do"nt'
        w = json.write(s)
        assert w == '"do\\"nt"'

    def testReadDictWithSlashStarComments(self):
        s = "\n        {'a':false,  /*don't want b\n            b:true, */\n        'c':true\n        }\n        "
        assert json.read(s) == {'a': False, 'c': True}

    def testReadDictWithTwoSlashStarComments(self):
        s = "\n        {'a':false,  /*don't want b\n            b:true, */\n        'c':true,\n        'd':false,  /*don;t want e\n            e:true, */\n        'f':true\n        }\n        "
        assert json.read(s) == {'a': False, 'c': True, 'd': False, 'f': True}

    def testReadDictWithDoubleSlashComments(self):
        s = "\n        {'a':false,\n          //  b:true, don't want b\n        'c':true\n        }\n        "
        assert json.read(s) == {'a': False, 'c': True}

    def testReadStringWithEscapedSingleQuote(self):
        s = '"don\'t tread on me."'
        assert json.read(s) == "don't tread on me."

    def testWriteStringWithEscapedDoubleQuote(self):
        s = 'he said, "hi.'
        t = json.write(s)
        assert json.write(s) == '"he said, \\"hi."'

    def testReadStringWithEscapedDoubleQuote(self):
        s = '"She said, \\"Hi.\\""'
        assert json.read(s) == 'She said, "Hi."'

    def testReadStringWithNewLine(self):
        s = '"She said, \\"Hi,\\"\\n to which he did not reply."'
        assert json.read(s) == 'She said, "Hi,"\n to which he did not reply.'

    def testReadNewLine(self):
        s = '"\\n"'
        assert json.read(s) == '\n'

    def testWriteNewLine(self):
        s = '\n'
        assert json.write(s) == '"\\n"'

    def testWriteSimpleUnicode(self):
        s = 'hello'
        assert json.write(s) == '"hello"'

    def testReadBackSlashuUnicode(self):
        s = '"f"'
        assert json.read(s) == 'f'

    def testReadBackSlashuUnicodeInDictKey(self):
        s = '{"father":34}'
        assert json.read(s) == {'father': 34}

    def testReadDictKeyWithBackSlash(self):
        s = '{"mo\\use":22}'
        self.assertEqual(json.read(s), {'mo\\use': 22})

    def testWriteDictKeyWithBackSlash(self):
        s = {'mo\\use': 22}
        self.assertEqual(json.write(s), '{"mo\\\\use":22}')

    def testWriteListOfBackSlashuUnicodeStrings(self):
        s = [
         '€', '€', '€']
        self.assertEqual(spaceless(json.write(s)), '["€","€","€"]')

    def testWriteUnicodeCharacter(self):
        s = json.write('ခ', 'ascii')
        self.assertEqual('"ခ"', s)

    def testWriteUnicodeCharacter1(self):
        s = json.write('ခ', 'ascii', outputEncoding='ascii')
        self.assertEqual('"\\u1001"', s)

    def testWriteHexUnicode(self):
        s = unicode(b'\xff\xfe\xbf\x00Q\x00u\x00\xe9\x00 \x00p\x00a\x00s\x00a\x00?\x00', 'utf-16')
        p = json.write(s, 'latin-1', outputEncoding='latin-1')
        self.assertEqual(unicode(p, 'latin-1'), '"¿Qué pasa?"')

    def testWriteHexUnicode1(self):
        s = unicode(b'\xff\xfe\xbf\x00Q\x00u\x00\xe9\x00 \x00p\x00a\x00s\x00a\x00?\x00', 'utf-16')
        p = json.write(s, 'latin-1')
        self.assertEqual(p, '"¿Qué pasa?"')

    def testWriteDosPath(self):
        s = 'c:\\windows\\system'
        assert json.write(s) == '"c:\\\\windows\\\\system"'

    def testWriteDosPathInList(self):
        s = [
         'c:\\windows\\system', 'c:\\windows\\system', 'c:\\windows\\system']
        self.assertEqual(json.write(s), '["c:\\\\windows\\\\system","c:\\\\windows\\\\system","c:\\\\windows\\\\system"]')

    def readImportExploit(self):
        s = "\nimport('os').listdir('.')"
        json.read(s)

    def testImportExploit(self):
        self.assertRaises(ReadException, self.readImportExploit)

    def readClassExploit(self):
        s = '"__main__".__class__.__subclasses__()'
        json.read(s)

    def testReadClassExploit(self):
        self.assertRaises(ReadException, self.readClassExploit)

    def readBadJson(self):
        s = "'DOS'*30"
        json.read(s)

    def testReadBadJson(self):
        self.assertRaises(ReadException, self.readBadJson)

    def readUBadJson(self):
        s = "'DOS'*30"
        json.read(s)

    def testReadUBadJson(self):
        self.assertRaises(ReadException, self.readUBadJson)

    def testReadEncodedUnicode(self):
        obj = "'La Peña'"
        r = json.read(obj, 'utf-8')
        self.assertEqual(r, unicode('La Peña', 'utf-8'))

    def testUnicodeFromNonUnicode(self):
        obj = "'\\u20ac'"
        r = json.read(obj)
        self.assertEqual(r, '€')

    def testUnicodeInObjectFromNonUnicode(self):
        obj = "['\\u20ac', '\\u20acCESS', 'my\\u20ACCESS']"
        r = json.read(obj)
        self.assertEqual(r, ['€', '€CESS', 'my€CESS'])

    def testWriteWithEncoding(self):
        obj = 'La Peña'
        r = json.write(obj, 'latin-1', outputEncoding='latin-1')
        self.assertEqual(unicode(r, 'latin-1'), '"La Peña"')

    def testWriteWithEncodingBaseCases(self):
        input_uni = 'Árvíztűrő tükörfúrógép'
        good_result = '"Árvíztűrő tükörfúrógép"'
        obj = input_uni.encode('utf-8')
        r = json.write(obj, 'utf-8', outputEncoding='utf-8')
        self.assertEqual(unicode(r, 'utf-8'), good_result)
        obj = input_uni
        r = json.write(obj, outputEncoding='utf-8')
        self.assertEqual(unicode(r, 'utf-8'), good_result)
        obj = input_uni.encode('latin2')
        r = json.write(obj, 'latin2', outputEncoding='latin2')
        self.assertEqual(unicode(r, 'latin2'), good_result)
        obj = input_uni
        r = json.write(obj, 'latin2', outputEncoding='latin2')
        self.assertEqual(unicode(r, 'latin2'), good_result)
        good_composite_result = '["Árvíztűrő tükörfúrógép","Árvíztűrő tükörfúrógép"]'
        obj = [
         input_uni, input_uni]
        r = json.write(obj, outputEncoding='utf-8')
        self.assertEqual(unicode(r, 'utf-8'), good_composite_result)
        obj = [
         input_uni.encode('utf-8'), input_uni.encode('utf-8')]
        r = json.write(obj, 'utf-8')
        obj = [
         input_uni.encode('latin2'), input_uni.encode('latin2')]
        r = json.write(obj, 'latin2')
        obj = [
         input_uni, input_uni.encode('utf-8')]
        r = json.write(obj, 'utf-8')

    def testReadSpecialEscapedChars1(self):
        test = '"\\\\f"'
        self.assertEqual([ ord(x) for x in json.read(test) ], [92, 102])

    def testReadSpecialEscapedChars2(self):
        test = '"\\\\a"'
        self.assertEqual([ ord(x) for x in json.read(test) ], [92, 97])

    def testReadSpecialEscapedChars3(self):
        test = '"\\\\\\\\a"'
        self.assertEqual([ ord(x) for x in json.read(test) ], [92, 92, 97])

    def testReadSpecialEscapedChars4(self):
        test = '"\\\\\\\\b"'
        self.assertEqual([ ord(x) for x in json.read(test) ], [92, 92, 98])

    def testReadSpecialEscapedChars5(self):
        test = '"\\\\\\n"'
        self.assertEqual([ ord(x) for x in json.read(test) ], [92, 10])


def test_suite():
    loader = unittest.TestLoader()
    return loader.loadTestsFromTestCase(JSONTests)


if __name__ == '__main__':
    unittest.TextTestRunner().run(test_suite())