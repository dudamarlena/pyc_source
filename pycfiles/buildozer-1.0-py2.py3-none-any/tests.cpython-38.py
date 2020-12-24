# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/tests.py
# Compiled at: 2020-03-06 06:00:15
# Size of source mod 2**32: 44495 bytes
__doc__ = 'Tests for Buildout version checker'
import json, os, sys
from collections import OrderedDict
from io import BytesIO
from io import StringIO
from logging import Handler
from tempfile import NamedTemporaryFile
from unittest import TestCase
from unittest import TestLoader
from unittest import TestSuite
from urllib.error import URLError
from bvc import checker
from bvc.checker import UnusedVersionsChecker
from bvc.checker import VersionsChecker
from bvc.configparser import VersionsConfigParser
import bvc.logger as logger
from bvc.scripts import check_buildout_updates
from bvc.scripts import find_unused_versions
from bvc.scripts import indent_buildout

class LazyVersionsChecker(VersionsChecker):
    """LazyVersionsChecker"""

    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)


class LazyUnusedVersionsChecker(UnusedVersionsChecker):
    """LazyUnusedVersionsChecker"""

    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)


class URLOpener(object):
    """URLOpener"""
    results = {'egg':{'releases': ['0.3', '0.2']}, 
     'egg-dev':{'releases': ['1.0', '1.1b1']}, 
     'error-egg':[]}

    def __call__(self, url):
        package = url.split('/')[(-2)]
        try:
            json_payload = json.dumps(self.results[package])
        except KeyError:
            raise URLError('404')
        else:
            return BytesIO(bytes(json_payload, 'utf-8'))


class StubbedURLOpenTestCase(TestCase):
    """StubbedURLOpenTestCase"""

    def setUp(self):
        self.stub_url_open()
        super(StubbedURLOpenTestCase, self).setUp()

    def tearDown(self):
        self.unstub_url_open()
        super(StubbedURLOpenTestCase, self).tearDown()

    def stub_url_open(self):
        """
        Replace the urlopen used in bvc.
        """
        self.original_url_open = checker.urlopen
        checker.urlopen = URLOpener()

    def unstub_url_open(self):
        """
        Restaure the original urlopen function.
        """
        checker.urlopen = self.original_url_open


class StubbedListDirTestCase(TestCase):
    """StubbedListDirTestCase"""
    listdir_content = []

    def setUp(self):
        self.stub_listdir()
        super(StubbedListDirTestCase, self).setUp()

    def tearDown(self):
        self.unstub_listdir()
        super(StubbedListDirTestCase, self).tearDown()

    def stub_listdir(self):
        """
        Replace the os.listdir function.
        """
        self.original_listdir = os.listdir
        os.listdir = lambda x: self.listdir_content

    def unstub_listdir(self):
        """
        Restaure the original os.listdir function.
        """
        os.listdir = self.original_listdir


class DictHandler(Handler):
    """DictHandler"""

    def __init__(self, *ka, **kw):
        self.messages = {'debug':[],  'info':[],  'warning':[],  'error':[],  'critical':[]}
        (super(DictHandler, self).__init__)(*ka, **kw)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())


class LogsTestCase(TestCase):
    """LogsTestCase"""

    def setUp(self):
        self.logs = DictHandler()
        logger.addHandler(self.logs)
        super(LogsTestCase, self).setUp()

    def tearDown(self):
        logger.removeHandler(self.logs)
        super(LogsTestCase, self).tearDown()

    def assertLogs(self, debug=[], info=[], warning=[], error=[], critical=[]):
        expected = {'debug':debug, 
         'info':info,  'warning':warning, 
         'error':error,  'critical':critical}
        for key, item in expected.items():
            self.assertEquals(self.logs.messages[key], item)


class StdOutTestCase(TestCase):
    """StdOutTestCase"""

    def setUp(self):
        self.output = StringIO()
        self.saved_stdout = sys.stdout
        self.saved_stderr = sys.stderr
        sys.stdout = self.output
        sys.stderr = self.output
        super(StdOutTestCase, self).setUp()

    def tearDown(self):
        sys.stdout = self.saved_stdout
        sys.stderr = self.saved_stderr
        super(StdOutTestCase, self).tearDown()

    def assertStdOut(self, output):
        self.assertEquals(self.output.getvalue(), output)

    def assertInStdOut(self, output):
        self.assertTrue(output in self.output.getvalue())


class VersionsCheckerTestCase(StubbedURLOpenTestCase):

    def setUp(self):
        self.checker = LazyVersionsChecker(service_url='http://custom.pypi.org/pypi')
        super(VersionsCheckerTestCase, self).setUp()

    def test_parse_versions(self):
        config_file = NamedTemporaryFile()
        config_file.write('[sections]\nKey=Value\n'.encode('utf-8'))
        config_file.seek(0)
        self.assertEquals(self.checker.parse_versions(config_file.name), [])
        config_file.seek(0)
        config_file.write('[VERSIONS]\negg=0.1\nEgg = 0.2'.encode('utf-8'))
        config_file.seek(0)
        self.assertEquals(self.checker.parse_versions(config_file.name), [])
        config_file.seek(0)
        config_file.write('[versions]\negg=0.1\nEgg = 0.2'.encode('utf-8'))
        config_file.seek(0)
        self.assertEquals(self.checker.parse_versions(config_file.name), [
         ('egg', '0.1'), ('Egg', '0.2')])
        config_file.close()

    def test_include_exclude_versions(self):
        source_versions = OrderedDict([('egg', '0.1'), ('Egg', '0.2')])
        self.assertEquals(self.checker.include_exclude_versions(source_versions), source_versions)
        results = source_versions.copy()
        results['Django'] = '0.0.0'
        self.assertEquals(self.checker.include_exclude_versions(source_versions,
          includes=['Django', 'egg']), results)
        source_versions['Django'] = '1.5.1'
        source_versions['pytz'] = '2013b'
        results = OrderedDict([('pytz', '2013b')])
        self.assertEquals(self.checker.include_exclude_versions(source_versions,
          excludes=['Django', 'egg']), results)
        self.assertEquals(self.checker.include_exclude_versions(source_versions,
          includes=[
         'Django', 'egg'],
          excludes=[
         'Django', 'egg']), results)
        results['zc.buildout'] = '0.0.0'
        self.assertEquals(self.checker.include_exclude_versions(source_versions,
          includes=[
         'zc.buildout'],
          excludes=[
         'Django', 'egg']), results)

    def test_build_specifiers(self):
        self.assertEquals(self.checker.build_specifiers(('Django', 'zc.buildout'), {'django':'<=1.8', 
         'extra':'!=1.2'}), [
         ('Django', '<=1.8'), ('zc.buildout', '')])

    def test_fetch_last_versions(self):
        self.assertEquals(self.checker.fetch_last_versions([
         ('egg', ''), ('UnknowEgg', '')], False, 'service_url', 1, 1), [
         ('egg', '0.3'), ('UnknowEgg', '0.0.0')])
        self.assertEquals(self.checker.fetch_last_versions([
         ('egg', '<=0.2'), ('UnknowEgg', '>1.0')], False, 'service_url', 1, 1), [
         ('egg', '0.2'), ('UnknowEgg', '0.0.0')])
        results = self.checker.fetch_last_versions([
         ('egg', ''), ('UnknowEgg', '')], False, 'service_url', 1, 2)
        self.assertEquals(dict(results), dict([('egg', '0.3'), ('UnknowEgg', '0.0.0')]))

    def test_fetch_last_version(self):
        self.assertEquals(self.checker.fetch_last_version(('UnknowEgg', ''), False, 'service_url', 1), ('UnknowEgg',
                                                                                                        '0.0.0'))
        self.assertEquals(self.checker.fetch_last_version(('egg', ''), False, 'service_url', 1), ('egg',
                                                                                                  '0.3'))
        self.assertEquals(self.checker.fetch_last_version(('egg', '<0.3'), False, 'service_url', 1), ('egg',
                                                                                                      '0.2'))

    def test_fetch_last_version_with_prereleases(self):
        self.assertEquals(self.checker.fetch_last_version(('egg-dev', ''), False, 'service_url', 1), ('egg-dev',
                                                                                                      '1.0'))
        self.assertEquals(self.checker.fetch_last_version(('egg-dev', ''), True, 'service_url', 1), ('egg-dev',
                                                                                                     '1.1b1'))
        self.assertEquals(self.checker.fetch_last_version(('egg-dev', '<1.1'), True, 'service_url', 1), ('egg-dev',
                                                                                                         '1.0'))
        self.assertEquals(self.checker.fetch_last_version(('egg-dev', '<=1.1'), True, 'service_url', 1), ('egg-dev',
                                                                                                          '1.1b1'))

    def test_find_updates(self):
        versions = OrderedDict([('egg', '1.5.1'), ('Egg', '0.0.0')])
        last_versions = OrderedDict([('egg', '1.5.1'), ('Egg', '1.0')])
        self.assertEquals(self.checker.find_updates(versions, last_versions), [('Egg', '1.0')])


class UnusedVersionsCheckerTestCase(StubbedListDirTestCase):

    def setUp(self):
        self.checker = LazyUnusedVersionsChecker()
        super(UnusedVersionsCheckerTestCase, self).setUp()

    def test_get_used_versions(self):
        self.listdir_content = [
         'file',
         'package-1.0.egg',
         'composed_egg-1.0.egg']
        self.assertEquals(self.checker.get_used_versions('.'), [
         'package', 'composed_egg'])

    def test_get_find_unused_versions(self):
        self.assertEquals(self.checker.find_unused_versions([
         'egg', 'CAPegg', 'composed-egg', 'unused'], [
         'Egg', 'capegg', 'composed_egg']), [
         'unused'])


class VersionsConfigParserTestCase(TestCase):

    def test_parse_case_insensitive(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section]\nKEY=VALUE\nKey=Value\n'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser()
        config_parser.read(config_file.name)
        self.assertEquals(config_parser.sections(), ['Section'])
        self.assertEquals(config_parser.options('Section'), ['KEY', 'Key'])
        config_file.close()

    def test_perfect_indentation(self):
        config_parser = VersionsConfigParser()
        config_parser.add_section('Section')
        config_parser.set('Section', 'Option', 'Value')
        self.assertEquals(config_parser.perfect_indentation, 8)
        config_parser.set('Section', 'Option-long', None)
        self.assertEquals(config_parser.perfect_indentation, 12)
        config_parser.add_section('Section long')
        config_parser.set('Section long', 'Option-super-long', None)
        self.assertEquals(config_parser.perfect_indentation, 20)

    def test_write_section(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser()
        config_parser.add_section('Section')
        config_parser.set('Section', 'Option', 'Value')
        config_parser.set('Section', 'Option-void', None)
        config_parser.set('Section', 'Option-multiline', 'Value1\nValue2')
        config_parser.write_section(config_file, 'Section', 24, '')
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\nOption                  = Value\nOption-void             = \nOption-multiline        = Value1\n                          Value2\n')
        config_file.close()

    def test_write_section_ascii_sorting(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser()
        config_parser.add_section('Section')
        config_parser.set('Section', 'Option-multiline', 'Value1\nValue2')
        config_parser.set('Section', 'Option-void', None)
        config_parser.set('Section', 'Option', 'Value')
        config_parser.write_section(config_file, 'Section', 24, 'ascii')
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\nOption                  = Value\nOption-multiline        = Value1\n                          Value2\nOption-void             = \n')
        config_file.close()

    def test_write_section_alpha_sorting(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser()
        config_parser.add_section('Section')
        config_parser.set('Section', 'Option-multiline', 'Value1\nValue2')
        config_parser.set('Section', 'option-void', None)
        config_parser.set('Section', 'option', 'Value')
        config_parser.write_section(config_file, 'Section', 24, 'alpha')
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\noption                  = Value\nOption-multiline        = Value1\n                          Value2\noption-void             = \n')
        config_file.close()

    def test_write_section_length_sorting(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser()
        config_parser.add_section('Section')
        config_parser.set('Section', 'Option-multiline', 'Value1\nValue2')
        config_parser.set('Section', 'Option-void', None)
        config_parser.set('Section', 'Option-size', None)
        config_parser.set('Section', 'Option', 'Value')
        config_parser.write_section(config_file, 'Section', 24, 'length')
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\nOption                  = Value\nOption-size             = \nOption-void             = \nOption-multiline        = Value1\n                          Value2\n')
        config_file.close()

    def test_write_section_low_indentation(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser()
        config_parser.add_section('Section')
        config_parser.set('Section', 'Option', 'Value')
        config_parser.set('Section', 'Option-void', None)
        config_parser.set('Section', 'Option-multiline', 'Value1\nValue2')
        config_parser.write_section(config_file, 'Section', 12, '')
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\nOption      = Value\nOption-void = \nOption-multiline= Value1\n              Value2\n')
        config_file.close()

    def test_write(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser()
        config_parser.add_section('Section 1')
        config_parser.add_section('Section 2')
        config_parser.set('Section 1', 'Option', 'Value')
        config_parser.set('Section 1', 'Option-void', None)
        config_parser.set('Section 1', 'Option-add+', 'Value added')
        config_parser.set('Section 2', 'Option-multiline', 'Value1\nValue2')
        config_parser.set('Section 2', '<', 'Value1\nValue2')
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section 1]\nOption              = Value\nOption-void         = \nOption-add         += Value added\n\n[Section 2]\nOption-multiline    = Value1\n                      Value2\n<=                    Value1\n                      Value2\n')
        config_file.close()

    def test_write_ascii_sorting(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser(indentation=32, sorting='ascii')
        config_parser.add_section('Section 1')
        config_parser.add_section('Section 2')
        config_parser.set('Section 1', 'Option', 'Value')
        config_parser.set('Section 1', 'Option-void', None)
        config_parser.set('Section 1', 'Option-add+', 'Value added')
        config_parser.set('Section 2', 'Option-multiline', 'Value1\nValue2')
        config_parser.set('Section 2', '<', 'Value1\nValue2')
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section 1]\nOption                          = Value\nOption-add                     += Value added\nOption-void                     = \n\n[Section 2]\n<=                                Value1\n                                  Value2\nOption-multiline                = Value1\n                                  Value2\n')
        config_file.close()

    def test_write_alpha_sorting(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser(indentation=32, sorting='alpha')
        config_parser.add_section('Section 1')
        config_parser.add_section('Section 2')
        config_parser.set('Section 1', 'Option', 'Value')
        config_parser.set('Section 1', 'option-void', None)
        config_parser.set('Section 1', 'option-add+', 'Value added')
        config_parser.set('Section 2', 'option-multiline', 'Value1\nValue2')
        config_parser.set('Section 2', '<', 'Value1\nValue2')
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section 1]\nOption                          = Value\noption-add                     += Value added\noption-void                     = \n\n[Section 2]\n<=                                Value1\n                                  Value2\noption-multiline                = Value1\n                                  Value2\n')
        config_file.close()

    def test_write_indentation_zero(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser(indentation=0)
        config_parser.add_section('Section 1')
        config_parser.add_section('Section 2')
        config_parser.set('Section 1', 'Option', 'Value')
        config_parser.set('Section 1', 'Option-void', None)
        config_parser.set('Section 1', 'Option-add+', 'Value added')
        config_parser.set('Section 2', 'Option-multiline', 'Value1\nValue2')
        config_parser.set('Section 2', '<', 'Value1\nValue2')
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section 1]\nOption=Value\nOption-void=\nOption-add+=Value added\n\n[Section 2]\nOption-multiline=Value1\n  Value2\n<=Value1\n  Value2\n')
        config_file.close()

    def test_write_low_indentation(self):
        config_file = NamedTemporaryFile()
        config_parser = VersionsConfigParser(indentation=12)
        config_parser.add_section('Section 1')
        config_parser.add_section('Section 2')
        config_parser.set('Section 1', 'Option', 'Value')
        config_parser.set('Section 1', 'Option-void', None)
        config_parser.set('Section 2', 'Option-multiline', 'Value1\nValue2')
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section 1]\nOption      = Value\nOption-void = \n\n[Section 2]\nOption-multiline= Value1\n              Value2\n')
        config_file.close()

    def test_parse_and_write_buildout_operators(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section]\nAd+=dition\nSub-=straction'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser()
        config_parser.read(config_file.name)
        config_file.seek(0)
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\nAd     += dition\nSub    -= straction\n')
        config_file.close()

    def test_parse_and_write_buildout_operators_offset(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section]\nAd  +=dition\nSub - = straction'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser()
        config_parser.read(config_file.name)
        config_file.seek(0)
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\nAd     += dition\nSub    -= straction\n')
        config_file.close()

    def test_parse_and_write_buildout_operators_offset_with_indentation(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section]\nAd  +=dition\nSub - = straction'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser(indentation=24)
        config_parser.read(config_file.name)
        config_file.seek(0)
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\nAd                     += dition\nSub                    -= straction\n')
        config_file.close()

    def test_parse_and_write_buildout_operators_multilines(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section]\nAdd+=Multi\n  Lines'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser()
        config_parser.read(config_file.name)
        config_file.seek(0)
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\nAdd    += Multi\n          Lines\n')
        config_file.close()

    def test_parse_and_write_buildout_macros(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section]\n<=Macro\n Template'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser()
        config_parser.read(config_file.name)
        config_file.seek(0)
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\n<=    Macro\n      Template\n')
        config_file.close()

    def test_parse_and_write_buildout_macros_offset(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section]\n<  = Macro\n  Template'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser()
        config_parser.read(config_file.name)
        config_file.seek(0)
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\n<=    Macro\n      Template\n')
        config_file.close()

    def test_parse_and_write_buildout_macros_offset_with_indentation(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section]\n<  = Macro\n  Template'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser(indentation=24)
        config_parser.read(config_file.name)
        config_file.seek(0)
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section]\n<=                        Macro\n                          Template\n')
        config_file.close()

    def test_parse_and_write_buildout_conditional_sections(self):
        config_file = NamedTemporaryFile()
        config_file.write('[Section:Condition]\nKey=Value\n'.encode('utf-8'))
        config_file.seek(0)
        config_parser = VersionsConfigParser()
        config_parser.read(config_file.name)
        config_file.seek(0)
        config_parser.write(config_file.name)
        config_file.seek(0)
        self.assertEquals(config_file.read().decode('utf-8'), '[Section:Condition]\nKey = Value\n')
        config_file.close()


class FindUnusedVersionsTestCase(LogsTestCase, StdOutTestCase, StubbedListDirTestCase):
    listdir_content = [
     'egg-1.0.egg',
     'composed_egg-1.0.egg']

    def test_simple--- This code section failed: ---

 L. 729         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 730         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[versions]\nEgg=1.0\nUnused-egg=1.0\n'
               12  LOAD_METHOD              encode

 L. 731        14  LOAD_STR                 'utf-8'

 L. 730        16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 732        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 733        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           60  'to 60'
               42  STORE_FAST               'context'

 L. 734        44  LOAD_GLOBAL              find_unused_versions
               46  LOAD_METHOD              cmdline
               48  LOAD_FAST                'config_file'
               50  LOAD_ATTR                name
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          
               56  POP_BLOCK        
               58  BEGIN_FINALLY    
             60_0  COME_FROM_WITH       40  '40'
               60  WITH_CLEANUP_START
               62  WITH_CLEANUP_FINISH
               64  END_FINALLY      

 L. 735        66  LOAD_FAST                'self'
               68  LOAD_METHOD              assertEqual
               70  LOAD_FAST                'context'
               72  LOAD_ATTR                exception
               74  LOAD_ATTR                code
               76  LOAD_CONST               0
               78  CALL_METHOD_2         2  ''
               80  POP_TOP          

 L. 736        82  LOAD_FAST                'self'
               84  LOAD_ATTR                assertLogs

 L. 737        86  LOAD_STR                 '- 2 versions found in %s.'
               88  LOAD_FAST                'config_file'
               90  LOAD_ATTR                name
               92  BINARY_MODULO    

 L. 738        94  LOAD_STR                 '- 2 packages need to be checked for updates.'

 L. 737        96  BUILD_LIST_2          2 

 L. 739        98  LOAD_STR                 '- Unused-egg is unused.'
              100  BUILD_LIST_1          1 

 L. 736       102  LOAD_CONST               ('info', 'warning')
              104  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              106  POP_TOP          

 L. 740       108  LOAD_FAST                'self'
              110  LOAD_METHOD              assertStdOut
              112  LOAD_STR                 '- Unused-egg is unused.\n'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 741       118  LOAD_FAST                'config_file'
              120  LOAD_METHOD              close
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 58

    def test_write--- This code section failed: ---

 L. 744         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 745         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[versions]\nEgg=1.0\nUnused-egg=1.0\n'
               12  LOAD_METHOD              encode

 L. 746        14  LOAD_STR                 'utf-8'

 L. 745        16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 747        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 748        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L. 749        44  LOAD_GLOBAL              find_unused_versions
               46  LOAD_METHOD              cmdline
               48  LOAD_STR                 '%s -w'
               50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name
               54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L. 750        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 751        86  LOAD_FAST                'self'
               88  LOAD_ATTR                assertLogs

 L. 752        90  LOAD_STR                 '- 2 versions found in %s.'
               92  LOAD_FAST                'config_file'
               94  LOAD_ATTR                name
               96  BINARY_MODULO    

 L. 753        98  LOAD_STR                 '- 2 packages need to be checked for updates.'

 L. 754       100  LOAD_STR                 '- %s updated.'
              102  LOAD_FAST                'config_file'
              104  LOAD_ATTR                name
              106  BINARY_MODULO    

 L. 752       108  BUILD_LIST_3          3 

 L. 755       110  LOAD_STR                 '- Unused-egg is unused.'
              112  BUILD_LIST_1          1 

 L. 751       114  LOAD_CONST               ('info', 'warning')
              116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              118  POP_TOP          

 L. 756       120  LOAD_FAST                'self'
              122  LOAD_METHOD              assertStdOut
              124  LOAD_STR                 '- Unused-egg is unused.\n'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          

 L. 757       130  LOAD_FAST                'self'
              132  LOAD_METHOD              assertEquals

 L. 758       134  LOAD_FAST                'config_file'
              136  LOAD_METHOD              read
              138  CALL_METHOD_0         0  ''
              140  LOAD_METHOD              decode
              142  LOAD_STR                 'utf-8'
              144  CALL_METHOD_1         1  ''

 L. 759       146  LOAD_STR                 '[versions]\nEgg = 1.0\n'

 L. 757       148  CALL_METHOD_2         2  ''
              150  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_write_indentation--- This code section failed: ---

 L. 762         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 763         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[versions]\nEgg=1.0\nUnused-egg=1.0\n'
               12  LOAD_METHOD              encode

 L. 764        14  LOAD_STR                 'utf-8'

 L. 763        16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 765        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 766        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L. 767        44  LOAD_GLOBAL              find_unused_versions
               46  LOAD_METHOD              cmdline
               48  LOAD_STR                 '%s -w --indent 8'
               50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name
               54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L. 768        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 769        86  LOAD_FAST                'self'
               88  LOAD_ATTR                assertLogs

 L. 770        90  LOAD_STR                 '- 2 versions found in %s.'
               92  LOAD_FAST                'config_file'
               94  LOAD_ATTR                name
               96  BINARY_MODULO    

 L. 771        98  LOAD_STR                 '- 2 packages need to be checked for updates.'

 L. 772       100  LOAD_STR                 '- %s updated.'
              102  LOAD_FAST                'config_file'
              104  LOAD_ATTR                name
              106  BINARY_MODULO    

 L. 770       108  BUILD_LIST_3          3 

 L. 773       110  LOAD_STR                 '- Unused-egg is unused.'
              112  BUILD_LIST_1          1 

 L. 769       114  LOAD_CONST               ('info', 'warning')
              116  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              118  POP_TOP          

 L. 774       120  LOAD_FAST                'self'
              122  LOAD_METHOD              assertStdOut
              124  LOAD_STR                 '- Unused-egg is unused.\n'
              126  CALL_METHOD_1         1  ''
              128  POP_TOP          

 L. 775       130  LOAD_FAST                'self'
              132  LOAD_METHOD              assertEquals

 L. 776       134  LOAD_FAST                'config_file'
              136  LOAD_METHOD              read
              138  CALL_METHOD_0         0  ''
              140  LOAD_METHOD              decode
              142  LOAD_STR                 'utf-8'
              144  CALL_METHOD_1         1  ''

 L. 777       146  LOAD_STR                 '[versions]\nEgg     = 1.0\n'

 L. 775       148  CALL_METHOD_2         2  ''
              150  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_no_source--- This code section failed: ---

 L. 780         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L. 781        12  LOAD_GLOBAL              find_unused_versions
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L. 782        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 783        48  LOAD_FAST                'self'
               50  LOAD_ATTR                assertLogs

 L. 784        52  LOAD_STR                 "'versions.cfg' cannot be read."
               54  BUILD_LIST_1          1 

 L. 785        56  LOAD_STR                 '- 0 packages need to be checked for updates.'
               58  BUILD_LIST_1          1 

 L. 783        60  LOAD_CONST               ('warning', 'info')
               62  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               64  POP_TOP          

 L. 786        66  LOAD_FAST                'self'
               68  LOAD_METHOD              assertStdOut
               70  LOAD_STR                 "'versions.cfg' cannot be read.\n"
               72  CALL_METHOD_1         1  ''
               74  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_exclude--- This code section failed: ---

 L. 789         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 790         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[versions]\nEgg=1.0\nUnused-egg=1.0\n'
               12  LOAD_METHOD              encode

 L. 791        14  LOAD_STR                 'utf-8'

 L. 790        16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 792        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 793        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L. 794        44  LOAD_GLOBAL              find_unused_versions
               46  LOAD_METHOD              cmdline
               48  LOAD_STR                 '%s -e unused-egg'

 L. 795        50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name

 L. 794        54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L. 796        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 797        86  LOAD_FAST                'self'
               88  LOAD_ATTR                assertLogs

 L. 798        90  LOAD_STR                 '- 2 versions found in %s.'
               92  LOAD_FAST                'config_file'
               94  LOAD_ATTR                name
               96  BINARY_MODULO    

 L. 799        98  LOAD_STR                 '- 1 packages need to be checked for updates.'

 L. 798       100  BUILD_LIST_2          2 

 L. 797       102  LOAD_CONST               ('info',)
              104  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              106  POP_TOP          

 L. 800       108  LOAD_FAST                'self'
              110  LOAD_METHOD              assertStdOut
              112  LOAD_STR                 ''
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          

 L. 801       118  LOAD_FAST                'config_file'
              120  LOAD_METHOD              close
              122  CALL_METHOD_0         0  ''
              124  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_output_max--- This code section failed: ---

 L. 804         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 805         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[versions]\nEgg=1.0\nUnused-egg=1.0\n'
               12  LOAD_METHOD              encode

 L. 806        14  LOAD_STR                 'utf-8'

 L. 805        16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 807        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 808        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L. 809        44  LOAD_GLOBAL              find_unused_versions
               46  LOAD_METHOD              cmdline
               48  LOAD_STR                 '%s -vvv'
               50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name
               54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L. 810        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 811        86  LOAD_FAST                'self'
               88  LOAD_ATTR                assertLogs

 L. 812        90  LOAD_STR                 '- 2 versions found in %s.'
               92  LOAD_FAST                'config_file'
               94  LOAD_ATTR                name
               96  BINARY_MODULO    

 L. 813        98  LOAD_STR                 '- 2 packages need to be checked for updates.'

 L. 812       100  BUILD_LIST_2          2 

 L. 814       102  LOAD_STR                 '- Unused-egg is unused.'
              104  BUILD_LIST_1          1 

 L. 811       106  LOAD_CONST               ('info', 'warning')
              108  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              110  POP_TOP          

 L. 815       112  LOAD_FAST                'self'
              114  LOAD_METHOD              assertStdOut

 L. 816       116  LOAD_STR                 '- 2 versions found in %s.\n- 2 packages need to be checked for updates.\n- Unused-egg is unused.\n'

 L. 818       118  LOAD_FAST                'config_file'
              120  LOAD_ATTR                name

 L. 816       122  BINARY_MODULO    

 L. 815       124  CALL_METHOD_1         1  ''
              126  POP_TOP          

 L. 819       128  LOAD_FAST                'config_file'
              130  LOAD_METHOD              close
              132  CALL_METHOD_0         0  ''
              134  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_output_none--- This code section failed: ---

 L. 822         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 823         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[versions]\nEgg=1.0\nUnused-egg=1.0\n'
               12  LOAD_METHOD              encode

 L. 824        14  LOAD_STR                 'utf-8'

 L. 823        16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 825        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 826        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L. 827        44  LOAD_GLOBAL              find_unused_versions
               46  LOAD_METHOD              cmdline
               48  LOAD_STR                 '%s -q'
               50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name
               54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L. 828        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 829        86  LOAD_FAST                'self'
               88  LOAD_METHOD              assertStdOut
               90  LOAD_STR                 ''
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          

 L. 830        96  LOAD_FAST                'self'
               98  LOAD_METHOD              assertRaises
              100  LOAD_GLOBAL              SystemExit
              102  CALL_METHOD_1         1  ''
              104  SETUP_WITH          122  'to 122'
              106  STORE_FAST               'context'

 L. 831       108  LOAD_GLOBAL              find_unused_versions
              110  LOAD_METHOD              cmdline
              112  LOAD_STR                 'invalid -qqqq'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  POP_BLOCK        
              120  BEGIN_FINALLY    
            122_0  COME_FROM_WITH      104  '104'
              122  WITH_CLEANUP_START
              124  WITH_CLEANUP_FINISH
              126  END_FINALLY      

 L. 832       128  LOAD_FAST                'self'
              130  LOAD_METHOD              assertEqual
              132  LOAD_FAST                'context'
              134  LOAD_ATTR                exception
              136  LOAD_ATTR                code
              138  LOAD_CONST               0
              140  CALL_METHOD_2         2  ''
              142  POP_TOP          

 L. 833       144  LOAD_FAST                'self'
              146  LOAD_METHOD              assertStdOut
              148  LOAD_STR                 ''
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          

 L. 834       154  LOAD_FAST                'config_file'
              156  LOAD_METHOD              close
              158  CALL_METHOD_0         0  ''
              160  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_handle_error--- This code section failed: ---

 L. 837         0  LOAD_FAST                'self'
                2  LOAD_ATTR                listdir_content
                4  STORE_FAST               'original_listdir_content'

 L. 838         6  LOAD_CONST               42
                8  LOAD_FAST                'self'
               10  STORE_ATTR               listdir_content

 L. 839        12  LOAD_GLOBAL              NamedTemporaryFile
               14  CALL_FUNCTION_0       0  ''
               16  STORE_FAST               'config_file'

 L. 840        18  LOAD_FAST                'config_file'
               20  LOAD_METHOD              write
               22  LOAD_STR                 '[versions]\n'
               24  LOAD_METHOD              encode
               26  LOAD_STR                 'utf-8'
               28  CALL_METHOD_1         1  ''
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 841        34  LOAD_FAST                'self'
               36  LOAD_METHOD              assertRaises
               38  LOAD_GLOBAL              SystemExit
               40  CALL_METHOD_1         1  ''
               42  SETUP_WITH           66  'to 66'
               44  STORE_FAST               'context'

 L. 842        46  LOAD_GLOBAL              find_unused_versions
               48  LOAD_METHOD              cmdline
               50  LOAD_STR                 '%s'
               52  LOAD_FAST                'config_file'
               54  LOAD_ATTR                name
               56  BINARY_MODULO    
               58  CALL_METHOD_1         1  ''
               60  POP_TOP          
               62  POP_BLOCK        
               64  BEGIN_FINALLY    
             66_0  COME_FROM_WITH       42  '42'
               66  WITH_CLEANUP_START
               68  WITH_CLEANUP_FINISH
               70  END_FINALLY      

 L. 843        72  LOAD_FAST                'self'
               74  LOAD_METHOD              assertEqual
               76  LOAD_FAST                'context'
               78  LOAD_ATTR                exception
               80  LOAD_ATTR                code

 L. 844        82  LOAD_STR                 "'int' object is not iterable"

 L. 843        84  CALL_METHOD_2         2  ''
               86  POP_TOP          

 L. 845        88  LOAD_FAST                'original_listdir_content'
               90  LOAD_FAST                'self'
               92  STORE_ATTR               listdir_content

Parse error at or near `BEGIN_FINALLY' instruction at offset 64


class IndentCommandLineTestCase(LogsTestCase, StdOutTestCase):

    def test_simple--- This code section failed: ---

 L. 852         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 853         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[sections]\nKey=Value\n'
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'utf-8'
               16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 854        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 855        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L. 856        44  LOAD_GLOBAL              indent_buildout
               46  LOAD_METHOD              cmdline
               48  LOAD_STR                 '%s'
               50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name
               54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L. 857        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 858        86  LOAD_FAST                'self'
               88  LOAD_ATTR                assertLogs

 L. 859        90  LOAD_STR                 '- %s (re)indented at 4 spaces.'
               92  LOAD_FAST                'config_file'
               94  LOAD_ATTR                name
               96  BINARY_MODULO    
               98  BUILD_LIST_1          1 

 L. 858       100  LOAD_CONST               ('warning',)
              102  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              104  POP_TOP          

 L. 860       106  LOAD_FAST                'self'
              108  LOAD_METHOD              assertStdOut

 L. 861       110  LOAD_STR                 '- %s (re)indented at 4 spaces.\n'
              112  LOAD_FAST                'config_file'
              114  LOAD_ATTR                name
              116  BINARY_MODULO    

 L. 860       118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 862       122  LOAD_FAST                'self'
              124  LOAD_METHOD              assertEquals

 L. 863       126  LOAD_FAST                'config_file'
              128  LOAD_METHOD              read
              130  CALL_METHOD_0         0  ''
              132  LOAD_METHOD              decode
              134  LOAD_STR                 'utf-8'
              136  CALL_METHOD_1         1  ''

 L. 864       138  LOAD_STR                 '[sections]\nKey = Value\n'

 L. 862       140  CALL_METHOD_2         2  ''
              142  POP_TOP          

 L. 866       144  LOAD_FAST                'config_file'
              146  LOAD_METHOD              close
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_indentation--- This code section failed: ---

 L. 869         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 870         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[sections]\nKey=Value\n'
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'utf-8'
               16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 871        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 872        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L. 873        44  LOAD_GLOBAL              indent_buildout
               46  LOAD_METHOD              cmdline
               48  LOAD_STR                 '%s --indent 8'
               50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name
               54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L. 874        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 875        86  LOAD_FAST                'self'
               88  LOAD_ATTR                assertLogs

 L. 876        90  LOAD_STR                 '- %s (re)indented at 8 spaces.'
               92  LOAD_FAST                'config_file'
               94  LOAD_ATTR                name
               96  BINARY_MODULO    
               98  BUILD_LIST_1          1 

 L. 875       100  LOAD_CONST               ('warning',)
              102  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              104  POP_TOP          

 L. 877       106  LOAD_FAST                'self'
              108  LOAD_METHOD              assertStdOut

 L. 878       110  LOAD_STR                 '- %s (re)indented at 8 spaces.\n'
              112  LOAD_FAST                'config_file'
              114  LOAD_ATTR                name
              116  BINARY_MODULO    

 L. 877       118  CALL_METHOD_1         1  ''
              120  POP_TOP          

 L. 879       122  LOAD_FAST                'self'
              124  LOAD_METHOD              assertEquals

 L. 880       126  LOAD_FAST                'config_file'
              128  LOAD_METHOD              read
              130  CALL_METHOD_0         0  ''
              132  LOAD_METHOD              decode
              134  LOAD_STR                 'utf-8'
              136  CALL_METHOD_1         1  ''

 L. 881       138  LOAD_STR                 '[sections]\nKey     = Value\n'

 L. 879       140  CALL_METHOD_2         2  ''
              142  POP_TOP          

 L. 883       144  LOAD_FAST                'config_file'
              146  LOAD_METHOD              close
              148  CALL_METHOD_0         0  ''
              150  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_invalid_source--- This code section failed: ---

 L. 886         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L. 887        12  LOAD_GLOBAL              indent_buildout
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 'invalid.cfg'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L. 888        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 889        48  LOAD_FAST                'self'
               50  LOAD_ATTR                assertLogs
               52  LOAD_STR                 '- invalid.cfg cannot be read.'
               54  BUILD_LIST_1          1 
               56  LOAD_CONST               ('warning',)
               58  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               60  POP_TOP          

 L. 890        62  LOAD_FAST                'self'
               64  LOAD_METHOD              assertStdOut
               66  LOAD_STR                 '- invalid.cfg cannot be read.\n'
               68  CALL_METHOD_1         1  ''
               70  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_multiple_sources--- This code section failed: ---

 L. 893         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 894         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write
               10  LOAD_STR                 '[sections]\nKey=Value\n'
               12  LOAD_METHOD              encode
               14  LOAD_STR                 'utf-8'
               16  CALL_METHOD_1         1  ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L. 895        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 896        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L. 897        44  LOAD_GLOBAL              indent_buildout
               46  LOAD_METHOD              cmdline
               48  LOAD_STR                 '%s invalid.cfg'
               50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name
               54  BINARY_MODULO    
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L. 898        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L. 899        86  LOAD_FAST                'self'
               88  LOAD_ATTR                assertLogs

 L. 900        90  LOAD_STR                 '- %s (re)indented at 4 spaces.'
               92  LOAD_FAST                'config_file'
               94  LOAD_ATTR                name
               96  BINARY_MODULO    

 L. 901        98  LOAD_STR                 '- invalid.cfg cannot be read.'

 L. 900       100  BUILD_LIST_2          2 

 L. 899       102  LOAD_CONST               ('warning',)
              104  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              106  POP_TOP          

 L. 902       108  LOAD_FAST                'self'
              110  LOAD_METHOD              assertStdOut

 L. 903       112  LOAD_STR                 '- %s (re)indented at 4 spaces.\n- invalid.cfg cannot be read.\n'

 L. 904       114  LOAD_FAST                'config_file'
              116  LOAD_ATTR                name

 L. 903       118  BINARY_MODULO    

 L. 902       120  CALL_METHOD_1         1  ''
              122  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_no_source--- This code section failed: ---

 L. 907         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L. 908        12  LOAD_GLOBAL              indent_buildout
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L. 909        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 910        48  LOAD_FAST                'self'
               50  LOAD_ATTR                assertLogs

 L. 911        52  LOAD_STR                 'No files to (re)indent'
               54  BUILD_LIST_1          1 

 L. 910        56  LOAD_CONST               ('warning',)
               58  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               60  POP_TOP          

 L. 912        62  LOAD_FAST                'self'
               64  LOAD_METHOD              assertStdOut

 L. 913        66  LOAD_STR                 'No files to (re)indent\n'

 L. 912        68  CALL_METHOD_1         1  ''
               70  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_output_none--- This code section failed: ---

 L. 916         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L. 917        12  LOAD_GLOBAL              indent_buildout
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 'invalid.cfg -q'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L. 918        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 919        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertStdOut
               52  LOAD_STR                 ''
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L. 920        58  LOAD_FAST                'self'
               60  LOAD_METHOD              assertRaises
               62  LOAD_GLOBAL              SystemExit
               64  CALL_METHOD_1         1  ''
               66  SETUP_WITH           84  'to 84'
               68  STORE_FAST               'context'

 L. 921        70  LOAD_GLOBAL              indent_buildout
               72  LOAD_METHOD              cmdline
               74  LOAD_STR                 'source.cfg -qqqqqqq'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       66  '66'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      

 L. 922        90  LOAD_FAST                'self'
               92  LOAD_METHOD              assertEqual
               94  LOAD_FAST                'context'
               96  LOAD_ATTR                exception
               98  LOAD_ATTR                code
              100  LOAD_CONST               0
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          

 L. 923       106  LOAD_FAST                'self'
              108  LOAD_METHOD              assertStdOut
              110  LOAD_STR                 ''
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24


class CheckUpdatesCommandLineTestCase(LogsTestCase, StdOutTestCase, StubbedURLOpenTestCase):

    def test_no_args_no_source--- This code section failed: ---

 L. 931         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L. 932        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 ''
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L. 933        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 934        48  LOAD_FAST                'self'
               50  LOAD_ATTR                assertLogs

 L. 935        52  LOAD_STR                 "'versions.cfg' cannot be read."
               54  BUILD_LIST_1          1 

 L. 936        56  LOAD_STR                 '- 0 packages need to be checked for updates.'

 L. 937        58  LOAD_STR                 '- 0 package updates found.'

 L. 936        60  BUILD_LIST_2          2 

 L. 934        62  LOAD_CONST               ('warning', 'info')
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  POP_TOP          

 L. 939        68  LOAD_FAST                'self'
               70  LOAD_METHOD              assertStdOut
               72  LOAD_STR                 "'versions.cfg' cannot be read.\n"
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_include_no_source--- This code section failed: ---

 L. 942         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L. 943        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i egg'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L. 944        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 945        48  LOAD_FAST                'self'
               50  LOAD_ATTR                assertLogs

 L. 946        52  LOAD_STR                 '-> Last version of egg is 0.3.'

 L. 947        54  LOAD_STR                 '=> egg current version (0.0.0) and last version (0.3) are different.'

 L. 946        56  BUILD_LIST_2          2 

 L. 949        58  LOAD_STR                 '- 1 packages need to be checked for updates.'

 L. 950        60  LOAD_STR                 '> Fetching latest datas for egg...'

 L. 951        62  LOAD_STR                 '- 1 package updates found.'

 L. 949        64  BUILD_LIST_3          3 

 L. 952        66  LOAD_STR                 "'versions.cfg' cannot be read."

 L. 953        68  LOAD_STR                 '[versions]'

 L. 954        70  LOAD_STR                 'egg = 0.3        #  0.0.0'

 L. 952        72  BUILD_LIST_3          3 

 L. 945        74  LOAD_CONST               ('debug', 'info', 'warning')
               76  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               78  POP_TOP          

 L. 956        80  LOAD_FAST                'self'
               82  LOAD_METHOD              assertStdOut

 L. 957        84  LOAD_STR                 "'versions.cfg' cannot be read.\n[versions]\negg = 0.3        #  0.0.0\n"

 L. 956        86  CALL_METHOD_1         1  ''
               88  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_include_unavailable--- This code section failed: ---

 L. 963         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L. 964        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i unavailable'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L. 965        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 966        48  LOAD_FAST                'self'
               50  LOAD_ATTR                assertLogs

 L. 967        52  LOAD_STR                 "'versions.cfg' cannot be read."
               54  BUILD_LIST_1          1 

 L. 968        56  LOAD_STR                 '!> https://pypi.python.org/pypi/unavailable/json 404'

 L. 969        58  LOAD_STR                 '-> Last version of unavailable is 0.0.0.'

 L. 968        60  BUILD_LIST_2          2 

 L. 970        62  LOAD_STR                 '- 1 packages need to be checked for updates.'

 L. 971        64  LOAD_STR                 '> Fetching latest datas for unavailable...'

 L. 972        66  LOAD_STR                 '- 0 package updates found.'

 L. 970        68  BUILD_LIST_3          3 

 L. 966        70  LOAD_CONST               ('warning', 'debug', 'info')
               72  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               74  POP_TOP          

 L. 974        76  LOAD_FAST                'self'
               78  LOAD_METHOD              assertStdOut
               80  LOAD_STR                 "'versions.cfg' cannot be read.\n"
               82  CALL_METHOD_1         1  ''
               84  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_include_exclude--- This code section failed: ---

 L. 977         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L. 978        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i unavailable -e unavailable'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L. 979        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L. 980        48  LOAD_FAST                'self'
               50  LOAD_ATTR                assertLogs

 L. 981        52  LOAD_STR                 "'versions.cfg' cannot be read."
               54  BUILD_LIST_1          1 

 L. 982        56  LOAD_STR                 '- 0 packages need to be checked for updates.'

 L. 983        58  LOAD_STR                 '- 0 package updates found.'

 L. 982        60  BUILD_LIST_2          2 

 L. 980        62  LOAD_CONST               ('warning', 'info')
               64  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               66  POP_TOP          

 L. 985        68  LOAD_FAST                'self'
               70  LOAD_METHOD              assertStdOut
               72  LOAD_STR                 "'versions.cfg' cannot be read.\n"
               74  CALL_METHOD_1         1  ''
               76  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_write_include_in_blank--- This code section failed: ---

 L. 988         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L. 989         6  LOAD_FAST                'self'
                8  LOAD_METHOD              assertRaises
               10  LOAD_GLOBAL              SystemExit
               12  CALL_METHOD_1         1  ''
               14  SETUP_WITH           38  'to 38'
               16  STORE_FAST               'context'

 L. 990        18  LOAD_GLOBAL              check_buildout_updates
               20  LOAD_METHOD              cmdline

 L. 991        22  LOAD_STR                 '-i egg -w %s'
               24  LOAD_FAST                'config_file'
               26  LOAD_ATTR                name
               28  BINARY_MODULO    

 L. 990        30  CALL_METHOD_1         1  ''
               32  POP_TOP          
               34  POP_BLOCK        
               36  BEGIN_FINALLY    
             38_0  COME_FROM_WITH       14  '14'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

 L. 992        44  LOAD_FAST                'self'
               46  LOAD_METHOD              assertEqual
               48  LOAD_FAST                'context'
               50  LOAD_ATTR                exception
               52  LOAD_ATTR                code
               54  LOAD_CONST               0
               56  CALL_METHOD_2         2  ''
               58  POP_TOP          

 L. 993        60  LOAD_FAST                'config_file'
               62  LOAD_METHOD              seek
               64  LOAD_CONST               0
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L. 994        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEquals

 L. 995        74  LOAD_FAST                'config_file'
               76  LOAD_METHOD              read
               78  CALL_METHOD_0         0  ''
               80  LOAD_METHOD              decode
               82  LOAD_STR                 'utf-8'
               84  CALL_METHOD_1         1  ''

 L. 996        86  LOAD_STR                 '[versions]\negg = 0.3\n'

 L. 994        88  CALL_METHOD_2         2  ''
               90  POP_TOP          

 L. 998        92  LOAD_FAST                'self'
               94  LOAD_METHOD              assertStdOut

 L. 999        96  LOAD_STR                 '[versions]\negg = 0.3        #  0.0.0\n'

 L. 998        98  CALL_METHOD_1         1  ''
              100  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 36

    def test_write_include_in_blank_with_indentation--- This code section failed: ---

 L.1003         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L.1004         6  LOAD_FAST                'self'
                8  LOAD_METHOD              assertRaises
               10  LOAD_GLOBAL              SystemExit
               12  CALL_METHOD_1         1  ''
               14  SETUP_WITH           38  'to 38'
               16  STORE_FAST               'context'

 L.1005        18  LOAD_GLOBAL              check_buildout_updates
               20  LOAD_METHOD              cmdline

 L.1006        22  LOAD_STR                 '-i egg --indent 8 -w %s'
               24  LOAD_FAST                'config_file'
               26  LOAD_ATTR                name
               28  BINARY_MODULO    

 L.1005        30  CALL_METHOD_1         1  ''
               32  POP_TOP          
               34  POP_BLOCK        
               36  BEGIN_FINALLY    
             38_0  COME_FROM_WITH       14  '14'
               38  WITH_CLEANUP_START
               40  WITH_CLEANUP_FINISH
               42  END_FINALLY      

 L.1007        44  LOAD_FAST                'self'
               46  LOAD_METHOD              assertEqual
               48  LOAD_FAST                'context'
               50  LOAD_ATTR                exception
               52  LOAD_ATTR                code
               54  LOAD_CONST               0
               56  CALL_METHOD_2         2  ''
               58  POP_TOP          

 L.1008        60  LOAD_FAST                'config_file'
               62  LOAD_METHOD              seek
               64  LOAD_CONST               0
               66  CALL_METHOD_1         1  ''
               68  POP_TOP          

 L.1009        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEquals

 L.1010        74  LOAD_FAST                'config_file'
               76  LOAD_METHOD              read
               78  CALL_METHOD_0         0  ''
               80  LOAD_METHOD              decode
               82  LOAD_STR                 'utf-8'
               84  CALL_METHOD_1         1  ''

 L.1011        86  LOAD_STR                 '[versions]\negg     = 0.3\n'

 L.1009        88  CALL_METHOD_2         2  ''
               90  POP_TOP          

 L.1013        92  LOAD_FAST                'self'
               94  LOAD_METHOD              assertStdOut

 L.1014        96  LOAD_STR                 '[versions]\negg     = 0.3        #  0.0.0\n'

 L.1013        98  CALL_METHOD_1         1  ''
              100  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 36

    def test_write_in_existing_file_with_exclude--- This code section failed: ---

 L.1018         0  LOAD_GLOBAL              NamedTemporaryFile
                2  CALL_FUNCTION_0       0  ''
                4  STORE_FAST               'config_file'

 L.1019         6  LOAD_FAST                'config_file'
                8  LOAD_METHOD              write

 L.1020        10  LOAD_STR                 '[buildout]\ndevelop=.\n[versions]\nexcluded=1.0\negg=0.1'
               12  LOAD_METHOD              encode

 L.1021        14  LOAD_STR                 'utf-8'

 L.1020        16  CALL_METHOD_1         1  ''

 L.1019        18  CALL_METHOD_1         1  ''
               20  POP_TOP          

 L.1022        22  LOAD_FAST                'config_file'
               24  LOAD_METHOD              seek
               26  LOAD_CONST               0
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L.1023        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertRaises
               36  LOAD_GLOBAL              SystemExit
               38  CALL_METHOD_1         1  ''
               40  SETUP_WITH           64  'to 64'
               42  STORE_FAST               'context'

 L.1024        44  LOAD_GLOBAL              check_buildout_updates
               46  LOAD_METHOD              cmdline

 L.1025        48  LOAD_STR                 '-e excluded -w %s'
               50  LOAD_FAST                'config_file'
               52  LOAD_ATTR                name
               54  BINARY_MODULO    

 L.1024        56  CALL_METHOD_1         1  ''
               58  POP_TOP          
               60  POP_BLOCK        
               62  BEGIN_FINALLY    
             64_0  COME_FROM_WITH       40  '40'
               64  WITH_CLEANUP_START
               66  WITH_CLEANUP_FINISH
               68  END_FINALLY      

 L.1026        70  LOAD_FAST                'self'
               72  LOAD_METHOD              assertEqual
               74  LOAD_FAST                'context'
               76  LOAD_ATTR                exception
               78  LOAD_ATTR                code
               80  LOAD_CONST               0
               82  CALL_METHOD_2         2  ''
               84  POP_TOP          

 L.1027        86  LOAD_FAST                'self'
               88  LOAD_ATTR                assertLogs

 L.1028        90  LOAD_STR                 '-> Last version of egg is 0.3.'

 L.1029        92  LOAD_STR                 '=> egg current version (0.1) and last version (0.3) are different.'

 L.1028        94  BUILD_LIST_2          2 

 L.1031        96  LOAD_STR                 '- 2 versions found in %s.'
               98  LOAD_FAST                'config_file'
              100  LOAD_ATTR                name
              102  BINARY_MODULO    

 L.1032       104  LOAD_STR                 '- 1 packages need to be checked for updates.'

 L.1033       106  LOAD_STR                 '> Fetching latest datas for egg...'

 L.1034       108  LOAD_STR                 '- 1 package updates found.'

 L.1035       110  LOAD_STR                 '- %s updated.'
              112  LOAD_FAST                'config_file'
              114  LOAD_ATTR                name
              116  BINARY_MODULO    

 L.1031       118  BUILD_LIST_5          5 

 L.1036       120  LOAD_STR                 '[versions]'

 L.1037       122  LOAD_STR                 'egg = 0.3          #  0.1'

 L.1036       124  BUILD_LIST_2          2 

 L.1027       126  LOAD_CONST               ('debug', 'info', 'warning')
              128  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              130  POP_TOP          

 L.1038       132  LOAD_FAST                'config_file'
              134  LOAD_METHOD              seek
              136  LOAD_CONST               0
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          

 L.1039       142  LOAD_FAST                'self'
              144  LOAD_METHOD              assertEquals

 L.1040       146  LOAD_FAST                'config_file'
              148  LOAD_METHOD              read
              150  CALL_METHOD_0         0  ''
              152  LOAD_METHOD              decode
              154  LOAD_STR                 'utf-8'
              156  CALL_METHOD_1         1  ''

 L.1041       158  LOAD_STR                 '[buildout]\ndevelop     = .\n\n[versions]\nexcluded    = 1.0\negg         = 0.3\n'

 L.1039       160  CALL_METHOD_2         2  ''
              162  POP_TOP          

 L.1046       164  LOAD_FAST                'self'
              166  LOAD_METHOD              assertStdOut

 L.1047       168  LOAD_STR                 '[versions]\negg = 0.3          #  0.1\n'

 L.1046       170  CALL_METHOD_1         1  ''
              172  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 62

    def test_output_default--- This code section failed: ---

 L.1052         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L.1053        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i egg'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.1054        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.1055        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertStdOut

 L.1056        52  LOAD_STR                 "'versions.cfg' cannot be read.\n[versions]\negg = 0.3        #  0.0.0\n"

 L.1055        54  CALL_METHOD_1         1  ''
               56  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_output_with_plus_and_minus--- This code section failed: ---

 L.1062         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L.1063        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i egg -vvv -qqq'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.1064        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.1065        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertStdOut

 L.1066        52  LOAD_STR                 "'versions.cfg' cannot be read.\n[versions]\negg = 0.3        #  0.0.0\n"

 L.1065        54  CALL_METHOD_1         1  ''
               56  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_output_none--- This code section failed: ---

 L.1072         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L.1073        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i egg -q'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.1074        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.1075        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertStdOut
               52  LOAD_STR                 ''
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.1076        58  LOAD_FAST                'self'
               60  LOAD_METHOD              assertRaises
               62  LOAD_GLOBAL              SystemExit
               64  CALL_METHOD_1         1  ''
               66  SETUP_WITH           84  'to 84'
               68  STORE_FAST               'context'

 L.1077        70  LOAD_GLOBAL              check_buildout_updates
               72  LOAD_METHOD              cmdline
               74  LOAD_STR                 '-i egg -qqqqqqqq'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       66  '66'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      

 L.1078        90  LOAD_FAST                'self'
               92  LOAD_METHOD              assertEqual
               94  LOAD_FAST                'context'
               96  LOAD_ATTR                exception
               98  LOAD_ATTR                code
              100  LOAD_CONST               0
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          

 L.1079       106  LOAD_FAST                'self'
              108  LOAD_METHOD              assertStdOut
              110  LOAD_STR                 ''
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_output_increased--- This code section failed: ---

 L.1082         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L.1083        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i egg -v'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.1084        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.1085        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertStdOut

 L.1086        52  LOAD_STR                 "'versions.cfg' cannot be read.\n- 1 packages need to be checked for updates.\n> Fetching latest datas for egg...\n- 1 package updates found.\n[versions]\negg = 0.3        #  0.0.0\n"

 L.1085        54  CALL_METHOD_1         1  ''
               56  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_output_max--- This code section failed: ---

 L.1095         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L.1096        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i egg -vvvvvvvvvv'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.1097        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.1098        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertStdOut

 L.1099        52  LOAD_STR                 "'versions.cfg' cannot be read.\n- 1 packages need to be checked for updates.\n> Fetching latest datas for egg...\n-> Last version of egg is 0.3.\n=> egg current version (0.0.0) and last version (0.3) are different.\n- 1 package updates found.\n[versions]\negg = 0.3        #  0.0.0\n"

 L.1098        54  CALL_METHOD_1         1  ''
               56  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_output_max_specifiers--- This code section failed: ---

 L.1111         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L.1112        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i egg -s egg:<0.3 -vvv'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.1113        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               0
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.1114        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertStdOut

 L.1115        52  LOAD_STR                 "'versions.cfg' cannot be read.\n- 1 packages need to be checked for updates.\n> Fetching latest datas for egg...\n-> Last version of egg<0.3 is 0.2.\n=> egg current version (0.0.0) and last version (0.2) are different.\n- 1 package updates found.\n[versions]\negg = 0.2        #  0.0.0\n"

 L.1114        54  CALL_METHOD_1         1  ''
               56  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_specifiers_errors--- This code section failed: ---

 L.1127         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L.1128        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i egg -s egg<0.3'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.1129        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertEqual
               36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_CONST               2
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.1130        48  LOAD_FAST                'self'
               50  LOAD_METHOD              assertInStdOut
               52  LOAD_STR                 'error: argument -s/--specifier: key:value syntax not followed'
               54  CALL_METHOD_1         1  ''
               56  POP_TOP          

 L.1133        58  LOAD_FAST                'self'
               60  LOAD_METHOD              assertRaises
               62  LOAD_GLOBAL              SystemExit
               64  CALL_METHOD_1         1  ''
               66  SETUP_WITH           84  'to 84'
               68  STORE_FAST               'context'

 L.1134        70  LOAD_GLOBAL              check_buildout_updates
               72  LOAD_METHOD              cmdline
               74  LOAD_STR                 '-i egg -s egg:'
               76  CALL_METHOD_1         1  ''
               78  POP_TOP          
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM_WITH       66  '66'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      

 L.1135        90  LOAD_FAST                'self'
               92  LOAD_METHOD              assertEqual
               94  LOAD_FAST                'context'
               96  LOAD_ATTR                exception
               98  LOAD_ATTR                code
              100  LOAD_CONST               2
              102  CALL_METHOD_2         2  ''
              104  POP_TOP          

 L.1136       106  LOAD_FAST                'self'
              108  LOAD_METHOD              assertInStdOut
              110  LOAD_STR                 'error: argument -s/--specifier: key or value are empty'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24

    def test_handle_error--- This code section failed: ---

 L.1140         0  LOAD_FAST                'self'
                2  LOAD_METHOD              assertRaises
                4  LOAD_GLOBAL              SystemExit
                6  CALL_METHOD_1         1  ''
                8  SETUP_WITH           26  'to 26'
               10  STORE_FAST               'context'

 L.1141        12  LOAD_GLOBAL              check_buildout_updates
               14  LOAD_METHOD              cmdline
               16  LOAD_STR                 '-i error-egg'
               18  CALL_METHOD_1         1  ''
               20  POP_TOP          
               22  POP_BLOCK        
               24  BEGIN_FINALLY    
             26_0  COME_FROM_WITH        8  '8'
               26  WITH_CLEANUP_START
               28  WITH_CLEANUP_FINISH
               30  END_FINALLY      

 L.1142        32  LOAD_FAST                'self'
               34  LOAD_METHOD              assertTrue

 L.1143        36  LOAD_FAST                'context'
               38  LOAD_ATTR                exception
               40  LOAD_ATTR                code
               42  LOAD_METHOD              startswith

 L.1144        44  LOAD_STR                 'list indices must be integers'

 L.1143        46  CALL_METHOD_1         1  ''

 L.1142        48  CALL_METHOD_1         1  ''
               50  POP_TOP          

Parse error at or near `BEGIN_FINALLY' instruction at offset 24


loader = TestLoader()
test_suite = TestSuite([
 loader.loadTestsFromTestCase(VersionsCheckerTestCase),
 loader.loadTestsFromTestCase(UnusedVersionsCheckerTestCase),
 loader.loadTestsFromTestCase(VersionsConfigParserTestCase),
 loader.loadTestsFromTestCase(IndentCommandLineTestCase),
 loader.loadTestsFromTestCase(FindUnusedVersionsTestCase),
 loader.loadTestsFromTestCase(CheckUpdatesCommandLineTestCase)])