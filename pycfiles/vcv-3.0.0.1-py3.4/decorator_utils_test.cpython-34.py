# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/util/decorator_utils_test.py
# Compiled at: 2018-06-15 01:22:48
# Size of source mod 2**32: 4197 bytes
"""decorator_utils tests."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import functools
from tensorflow.python.platform import test
from tensorflow.python.platform import tf_logging as logging
from tensorflow.python.util import decorator_utils

def _test_function(unused_arg=0):
    pass


class GetQualifiedNameTest(test.TestCase):

    def test_method(self):
        self.assertEqual('GetQualifiedNameTest.test_method', decorator_utils.get_qualified_name(GetQualifiedNameTest.test_method))

    def test_function(self):
        self.assertEqual('_test_function', decorator_utils.get_qualified_name(_test_function))


class AddNoticeToDocstringTest(test.TestCase):

    def _check(self, doc, expected):
        self.assertEqual(decorator_utils.add_notice_to_docstring(doc=doc, instructions='Instructions', no_doc_str='Nothing here', suffix_str='(suffix)', notice=[
         'Go away']), expected)

    def test_regular(self):
        expected = 'Brief (suffix)\n\nGo away\nInstructions\n\nDocstring\n\nArgs:\n  arg1: desc'
        self._check('Brief\n\nDocstring\n\nArgs:\n  arg1: desc', expected)
        self._check('Brief\n\n  Docstring\n\n  Args:\n    arg1: desc', expected)
        self._check('Brief\n  \n  Docstring\n  \n  Args:\n    arg1: desc', expected)
        self._check('\n  Brief\n  \n  Docstring\n  \n  Args:\n    arg1: desc', expected)
        self._check('\n  Brief\n  \n  Docstring\n  \n  Args:\n    arg1: desc', expected)

    def test_brief_only(self):
        expected = 'Brief (suffix)\n\nGo away\nInstructions'
        self._check('Brief', expected)
        self._check('Brief\n', expected)
        self._check('Brief\n  ', expected)
        self._check('\nBrief\n  ', expected)
        self._check('\n  Brief\n  ', expected)

    def test_no_docstring(self):
        expected = 'Nothing here\n\nGo away\nInstructions'
        self._check(None, expected)
        self._check('', expected)

    def test_no_empty_line(self):
        expected = 'Brief (suffix)\n\nGo away\nInstructions\n\nDocstring'
        self._check('Brief\nDocstring', expected)
        self._check('Brief\n  Docstring', expected)
        self._check('\nBrief\nDocstring', expected)
        self._check('\n  Brief\n  Docstring', expected)


class ValidateCallableTest(test.TestCase):

    def test_function(self):
        decorator_utils.validate_callable(_test_function, 'test')

    def test_method(self):
        decorator_utils.validate_callable(self.test_method, 'test')

    def test_callable(self):

        class TestClass(object):

            def __call__(self):
                pass

        decorator_utils.validate_callable(TestClass(), 'test')

    def test_partial(self):
        partial = functools.partial(_test_function, unused_arg=7)
        decorator_utils.validate_callable(partial, 'test')

    def test_fail_non_callable(self):
        x = 0
        self.assertRaises(ValueError, decorator_utils.validate_callable, x, 'test')


if __name__ == '__main__':
    test.main()