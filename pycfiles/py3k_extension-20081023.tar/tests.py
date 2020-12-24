# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/myint/projects/py3kwarn/py3kwarn/tests.py
# Compiled at: 2013-05-25 00:45:28
from __future__ import unicode_literals
import os, unittest
from py3kwarn import main
code_apply = b'apply(hello, args, kwargs)'
code_basestring = b'basestring'
code_buffer = b"buffer('hello', 1, 3)"
code_callable = b"callable('hello')"
code_dict = b'\nd.keys()\nd.iteritems()\nd.viewvalues()\n'
code_except = b'\ntry:\n    import asdf\nexcept E, T:\n    pass\n'
code_exec = b'exec code in ns1, ns2'
code_execfile = b"execfile('test.py')"
code_filter = b'filter(lambda x: x, [1, 2, 3])'
code_funcattrs = b'\ndef test():\n    pass\ntest.func_name\ntest.func_closure\ntest.func_dict\n'
code_has_key = b"d.has_key('foobar')"
code_unicode = b"ur'Hello World'"

class TestPy3kWarn(unittest.TestCase):

    def _test_code(self, name, casename=None):
        warnings = main.warnings_for_string(globals()[(b'code_' + name)], name)
        if not casename:
            casename = b'Fix' + name.title()
        self.assertTrue(len(warnings))
        self.assertTrue(casename in warnings[0][1])
        return warnings

    def test_apply(self):
        self._test_code(b'apply')

    def test_basestring(self):
        self._test_code(b'basestring')

    def test_buffer(self):
        self._test_code(b'basestring')

    def test_callable(self):
        self._test_code(b'callable')

    def test_dict(self):
        self._test_code(b'dict')

    def test_except(self):
        self._test_code(b'except')

    def test_exec(self):
        self._test_code(b'exec')

    def test_execfile(self):
        self._test_code(b'execfile')

    def test_filter(self):
        self._test_code(b'filter')

    def test_funcattrs(self):
        self._test_code(b'funcattrs')

    def test_has_key(self):
        self._test_code(b'has_key', b'HasKey')

    def test_unicode(self):
        self._test_code(b'unicode')

    def test_do_not_crash_on_unicode(self):
        main.warnings_for_string(b'u"å"')

    def test_main(self):
        main.main([
         os.path.join(os.path.dirname(__file__), b'__init__.py')])

    def test_with_nonexistent_file(self):
        main.main([b'nonexistent_file.py'])

    def test_ignore_compatible_unicode(self):
        self.assertFalse(main.warnings_for_string(b'unicode = str\nunicode("abc")\n'))

    def test_unichr(self):
        self.assertTrue(main.warnings_for_string(b'unichr(1)\n'))

    def test_ignore_compatible_unichr(self):
        self.assertFalse(main.warnings_for_string(b'unichr = chr\nunichr(1)\n'))

    def test_ignore_compatible_basestring(self):
        self.assertFalse(main.warnings_for_string(b'basestring = str\nbasestring\n'))

    def test_xrange(self):
        self.assertTrue(main.warnings_for_string(b'xrange(3)\n'))

    def test_print(self):
        self.assertTrue(main.warnings_for_string(b'print 3\n'))

    def test_print_with_parentheses(self):
        self.assertFalse(main.warnings_for_string(b'print("%d" % 3)\n'))

    def test_imports(self):
        self.assertTrue(main.warnings_for_string(b'from ConfigParser import RawConfigParser\n'))

    def test_imports_with_import_error_caught(self):
        self.assertFalse(main.warnings_for_string(b'try:\n    from ConfigParser import RawConfigParser\nexcept ImportError:\n    from configparser import RawConfigParser\n'))

    def test_imports_with_import_error_caught_the_other_way(self):
        self.assertFalse(main.warnings_for_string(b'try:\n    from configparser import RawConfigParser\nexcept ImportError:\n    from ConfigParser import RawConfigParser\n'))

    def test_long(self):
        self.assertTrue(main.warnings_for_string(b'long\n'))

    def test_ignore_compatible_long(self):
        self.assertFalse(main.warnings_for_string(b'long = int\nlong\n'))

    def test_zip(self):
        self.assertTrue(main.warnings_for_string(b'zip([1, 2], [3, 4])\n'))

    def test_ignore_compatible_zip(self):
        self.assertFalse(main.warnings_for_string(b'enumerate(zip([1, 2], [3, 4]))\n'))