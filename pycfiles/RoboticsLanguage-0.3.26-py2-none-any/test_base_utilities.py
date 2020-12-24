# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/glopes/Projects/RoboticsLanguage/RoboticsLanguage/Base/Tests/test_base_utilities.py
# Compiled at: 2019-09-09 15:48:16
import unittest, os
from lxml import etree
from RoboticsLanguage.Base import Utilities

class TestBaseUtilities(unittest.TestCase):

    def test_importModule(self):
        self.assertEqual(Utilities.importModule('RoboticsLanguage', 'Outputs', 'RosCpp', 'Manifesto').Manifesto.manifesto['packageShortName'], 'roscpp')

    def test_isKeyDefined(self):
        self.assertTrue(Utilities.isKeyDefined('test', {'test': 'ok'}))
        self.assertFalse(Utilities.isKeyDefined('ok', {'test': 'ok'}))

    def test_isDefined(self):
        self.assertTrue(Utilities.isDefined({'a': {'b': {'c': 'd'}}}, '/a'))
        self.assertTrue(Utilities.isDefined({'a': {'b': {'c': 'd'}}}, '/a/b'))
        self.assertTrue(Utilities.isDefined({'a': {'b': {'c': 'd'}}}, '/a/b/c'))
        self.assertFalse(Utilities.isDefined({'a': {'b': {'c': 'd'}}}, '/a/b/c/d'))
        self.assertFalse(Utilities.isDefined({'a': {'b': {'c': 'd'}}}, 'a/z/c'))

    def test_getDictValue(self):
        self.assertEqual(Utilities.getDictValue('a', {'a': {'b': {'c': 'd'}}}), {'b': {'c': 'd'}})
        self.assertEqual(Utilities.getDictValue('b', {'a': {'b': {'c': 'd'}}}), None)
        return

    def test_mergeDictionaries(self):
        self.assertEqual(Utilities.mergeDictionaries({'a': {'b': '1'}}, {'a': {'b': '1'}}), {'a': {'b': '1'}})
        self.assertEqual(Utilities.mergeDictionaries({'a': '1'}, {'b': '2'}), {'a': '1', 'b': '2'})
        self.assertEqual(Utilities.mergeDictionaries({'a': '1', 'b': '2'}, {'a': '2', 'c': '3'}), {'a': '1', 'b': '2', 'c': '3'})
        self.assertEqual(Utilities.mergeDictionaries({'a': {'b': '1', 'c': '3'}, 'b': '2'}, {'a': {'b': '2', 'f': '5'}, 'z': '9'}), {'a': {'b': '1', 'f': '5', 'c': '3'}, 'z': '9', 'b': '2'})
        self.assertEqual(Utilities.mergeDictionaries({'a': {'b': {'x': '1', 'w': '6'}, 'c': '3'}, 'b': '2'}, {'a': {'b': {'x': '2', 'y': '7'}, 'f': '5'}, 'z': '9'}), {'a': {'b': {'x': '1', 'w': '6', 'y': '7'}, 'f': '5', 'c': '3'}, 'z': '9', 'b': '2'})

    def test_flatDictionary(self):
        self.assertEqual(Utilities.flatDictionary({'a': {'b': 'c'}}), {'-a-b': 'c'})
        self.assertEqual(Utilities.flatDictionary({'a': {'b': 'c'}}, s='+'), {'+a+b': 'c'})
        self.assertEqual(Utilities.flatDictionary({'a': {'b': {'c': {'d': 'e'}}}}), {'-a-b-c-d': 'e'})
        self.assertEqual(Utilities.flatDictionary({'a': {'b': {'c': {'d': 'e', 'z': 'a'}}}}), {'-a-b-c-d': 'e', '-a-b-c-z': 'a'})
        self.assertEqual(Utilities.flatDictionary({'a': {'b': {'c': {'string': 'e', 'number': 1, 'array': [1, 2, 3]}}}, 'b': 'c'}), {'-a-b-c-array': [1, 2, 3], '-a-b-c-number': 1, '-a-b-c-string': 'e', '-b': 'c'})

    def test_unflatDictionary(self):
        self.assertEqual(Utilities.unflatDictionary({'-a-b': 'c'}), {'a': {'b': 'c'}})
        self.assertEqual(Utilities.unflatDictionary({'+a+b': 'c'}, s='+'), {'a': {'b': 'c'}})
        self.assertEqual(Utilities.unflatDictionary({'-a-b-c-d': 'e'}), {'a': {'b': {'c': {'d': 'e'}}}})

    def test_lowerNoSpace(self):
        self.assertEqual(Utilities.lowerNoSpace('Here Is A Phrase'), 'hereisaphrase')

    def test_lowerSpaceToDash(self):
        self.assertEqual(Utilities.lowerSpaceToDash('Here Is A Phrase'), 'here-is-a-phrase')

    def test_underscore(self):
        self.assertEqual(Utilities.underscore('/Here Is A.Phrase'), '_here_is_a_phrase')

    def test_underscoreFullCaps(self):
        self.assertEqual(Utilities.underscoreFullCaps('/Here Is A.Phrase'), '_HERE_IS_A_PHRASE')

    def test_fullCaps(self):
        self.assertEqual(Utilities.fullCaps('/Here Is_A.Phrase'), 'HEREISAPHRASE')

    def test_smartTitle(self):
        self.assertEqual(Utilities.smartTitle('this test is OK and RoL'), 'This Test Is OK And RoL')

    def test_camelCase(self):
        self.assertEqual(Utilities.camelCase('/this_test is.OK and RoL'), 'ThisTestIsOKAndRoL')

    def test_ensureList(self):
        self.assertEqual(Utilities.ensureList([1, 2, 3]), [1, 2, 3])
        self.assertEqual(Utilities.ensureList(1), [1])

    def test_findFileType(self):
        Utilities.createFolder('/tmp/RoL/1')
        with open('/tmp/RoL/1/test.py', 'w') as (template_file):
            template_file.write("print('hello')")
        self.assertEqual([ x for x in Utilities.findFileType(path='/tmp/RoL/1', followlinks=False) ], [
         '/tmp/RoL/1/test.py'])

    def test_findFileName(self):
        Utilities.createFolder('/tmp/RoL/2')
        with open('/tmp/RoL/2/test.py', 'w') as (template_file):
            template_file.write("print('hello')")
        self.assertEqual([ x for x in Utilities.findFileName('test.py', path='/tmp/RoL/2', followlinks=False) ], [
         '/tmp/RoL/2/test.py'])

    def test_createFolder(self):
        with self.assertRaises(Exception):
            try:
                Utilities.createFolder('/tmp/test')
            except:
                pass
            else:
                raise Exception

    def test_createFolderForFile(self):
        with self.assertRaises(Exception):
            try:
                Utilities.createFolderForFile('/tmp/test/test.txt')
            except:
                pass
            else:
                raise Exception

    def test_text(self):
        xml1 = etree.fromstring('<string>some text</string>')
        xml2 = etree.fromstring('<xml><string>some text</string></xml>')
        self.assertEqual(Utilities.text(xml1), 'some text')
        self.assertEqual(Utilities.text(xml2), '')

    def test_templateEngine(self):
        Utilities.createFolder('/tmp/RoL/templates/_foldername_')
        Utilities.createFolder('/tmp/RoL/deploy')
        with open('/tmp/RoL/templates/_foldername_/copy.txt', 'w') as (template_file):
            template_file.write('A file to copy')
        with open('/tmp/RoL/templates/_foldername_/_test_.txt.template', 'w') as (template_file):
            template_file.write('A template for a {{code|xpath("/node")|text}}')
        code = etree.fromstring('<node>hello</node>')
        parameters = {}
        filepatterns = {'foldername': 'testfolder', 'test': 'hello'}
        templates_path = '/tmp/RoL/templates'
        deploy_path = '/tmp/RoL/deploy'
        Utilities.templateEngine(code, parameters, filepatterns, templates_path, deploy_path)
        result1 = os.path.isfile('/tmp/RoL/deploy/testfolder/hello.txt')
        result2 = os.path.isfile('/tmp/RoL/deploy/testfolder/copy.txt')
        if result1:
            with open('/tmp/RoL/deploy/testfolder/hello.txt', 'r') as (template_file):
                text = template_file.read()
                result3 = text == 'A template for a hello'
        if result2:
            with open('/tmp/RoL/deploy/testfolder/copy.txt', 'r') as (template_file):
                text = template_file.read()
                result4 = text == 'A file to copy'
        self.assertTrue(result1)
        self.assertTrue(result2)
        self.assertTrue(result3)
        self.assertTrue(result4)


if __name__ == '__main__':
    unittest.main()