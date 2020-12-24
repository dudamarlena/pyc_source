# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/extensions/test_check_raise_docs.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 23316 bytes
"""Unit tests for the raised exception documentation checking in the
`DocstringChecker` in :mod:`pylint.extensions.check_docs`
"""
from __future__ import absolute_import, division, print_function
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, astroid
from pylint.extensions.docparams import DocstringParameterChecker
from pylint.testutils import CheckerTestCase, Message, set_config

class TestDocstringCheckerRaise(CheckerTestCase):
    __doc__ = 'Tests for pylint_plugin.RaiseDocChecker'
    CHECKER_CLASS = DocstringParameterChecker

    def test_ignores_no_docstring(self):
        raise_node = astroid.extract_node("\n        def my_func(self):\n            raise RuntimeError('hi') #@\n        ")
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_unknown_style(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring."""\n            raise RuntimeError(\'hi\')\n        ')
        raise_node = node.body[0]
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    @set_config(accept_no_raise_doc=False)
    def test_warns_unknown_style(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring."""\n            raise RuntimeError(\'hi\')\n        ')
        raise_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_missing_sphinx_raises(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises NameError: Never\n            """\n            raise RuntimeError(\'hi\')\n            raise NameError(\'hi\')\n        ')
        raise_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_missing_google_raises(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises:\n                NameError: Never\n            """\n            raise RuntimeError(\'hi\')\n            raise NameError(\'hi\')\n        ')
        raise_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_google_attr_raises_exact_exc(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a google docstring.\n\n            Raises:\n                re.error: Sometimes\n            """\n            import re\n            raise re.error(\'hi\')  #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_google_attr_raises_substr_exc(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a google docstring.\n\n            Raises:\n                re.error: Sometimes\n            """\n            from re import error\n            raise error(\'hi\')  #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_valid_missing_google_attr_raises(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a google docstring.\n\n            Raises:\n                re.anothererror: Sometimes\n            """\n            from re import error\n            raise error(\'hi\')\n        ')
        raise_node = node.body[1]
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('error', ))):
            self.checker.visit_raise(raise_node)

    def test_find_invalid_missing_google_attr_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a google docstring.\n\n            Raises:\n                bogusmodule.error: Sometimes\n            """\n            from re import error\n            raise error(\'hi\') #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    @set_config(accept_no_raise_doc=False)
    def test_google_raises_with_prefix(self):
        code_snippet = '\n        def my_func(self):\n            """This is a google docstring.\n\n            Raises:\n                {prefix}re.error: Sometimes\n            """\n            import re\n            raise re.error(\'hi\') #@\n        '
        for prefix in ('~', '!'):
            raise_node = astroid.extract_node(code_snippet.format(prefix=prefix))
            with self.assertNoMessages():
                self.checker.visit_raise(raise_node)

    def test_find_missing_numpy_raises(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises\n            ------\n            NameError\n                Never\n            """\n            raise RuntimeError(\'hi\')\n            raise NameError(\'hi\')\n        ')
        raise_node = node.body[0]
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_ignore_spurious_sphinx_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises RuntimeError: Always\n            :except NameError: Never\n            :raise OSError: Never\n            :exception ValueError: Never\n            """\n            raise RuntimeError(\'Blah\') #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_all_sphinx_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises RuntimeError: Always\n            :except NameError: Never\n            :raise OSError: Never\n            :exception ValueError: Never\n            """\n            raise RuntimeError(\'hi\') #@\n            raise NameError(\'hi\')\n            raise OSError(2, \'abort!\')\n            raise ValueError(\'foo\')\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_all_google_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises:\n                RuntimeError: Always\n                NameError: Never\n            """\n            raise RuntimeError(\'hi\') #@\n            raise NameError(\'hi\')\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_all_numpy_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises\n            ------\n            RuntimeError\n                Always\n            NameError\n                Never\n            """\n            raise RuntimeError(\'hi\') #@\n            raise NameError(\'hi\')\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_finds_rethrown_sphinx_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises NameError: Sometimes\n            """\n            try:\n                fake_func()\n            except RuntimeError:\n                raise #@\n\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_rethrown_google_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises:\n                NameError: Sometimes\n            """\n            try:\n                fake_func()\n            except RuntimeError:\n                raise #@\n\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_rethrown_numpy_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises\n            ------\n            NameError\n                Sometimes\n            """\n            try:\n                fake_func()\n            except RuntimeError:\n                raise #@\n\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_finds_rethrown_sphinx_multiple_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises NameError: Sometimes\n            """\n            try:\n                fake_func()\n            except (RuntimeError, ValueError):\n                raise #@\n\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError, ValueError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_rethrown_google_multiple_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises:\n                NameError: Sometimes\n            """\n            try:\n                fake_func()\n            except (RuntimeError, ValueError):\n                raise #@\n\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError, ValueError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_rethrown_numpy_multiple_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises\n            ------\n            NameError\n                Sometimes\n            """\n            try:\n                fake_func()\n            except (RuntimeError, ValueError):\n                raise #@\n\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError, ValueError', ))):
            self.checker.visit_raise(raise_node)

    def test_ignores_caught_sphinx_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises NameError: Sometimes\n            """\n            try:\n                raise RuntimeError(\'hi\') #@\n            except RuntimeError:\n                pass\n\n            raise NameError(\'hi\')\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_caught_google_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            Raises:\n                NameError: Sometimes\n            """\n            try:\n                raise RuntimeError(\'hi\') #@\n            except RuntimeError:\n                pass\n\n            raise NameError(\'hi\')\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_caught_numpy_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a numpy docstring.\n\n            Raises\n            ------\n            NameError\n                Sometimes\n            """\n            try:\n                raise RuntimeError(\'hi\') #@\n            except RuntimeError:\n                pass\n\n            raise NameError(\'hi\')\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_numpy_attr_raises_exact_exc(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a numpy docstring.\n\n            Raises\n            ------\n            re.error\n                Sometimes\n            """\n            import re\n            raise re.error(\'hi\')  #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_numpy_attr_raises_substr_exc(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a numpy docstring.\n\n            Raises\n            ------\n            re.error\n                Sometimes\n            """\n            from re import error\n            raise error(\'hi\')  #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_valid_missing_numpy_attr_raises(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a numpy docstring.\n\n            Raises\n            ------\n            re.anothererror\n                Sometimes\n            """\n            from re import error\n            raise error(\'hi\')\n        ')
        raise_node = node.body[1]
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('error', ))):
            self.checker.visit_raise(raise_node)

    def test_find_invalid_missing_numpy_attr_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a numpy docstring.\n\n            Raises\n            ------\n            bogusmodule.error\n                Sometimes\n            """\n            from re import error\n            raise error(\'hi\') #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    @set_config(accept_no_raise_doc=False)
    def test_numpy_raises_with_prefix(self):
        code_snippet = '\n        def my_func(self):\n            """This is a numpy docstring.\n\n            Raises\n            ------\n            {prefix}re.error\n                Sometimes\n            """\n            import re\n            raise re.error(\'hi\') #@\n        '
        for prefix in ('~', '!'):
            raise_node = astroid.extract_node(code_snippet.format(prefix=prefix))
            with self.assertNoMessages():
                self.checker.visit_raise(raise_node)

    def test_find_missing_sphinx_raises_infer_from_instance(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises NameError: Never\n            """\n            my_exception = RuntimeError(\'hi\')\n            raise my_exception #@\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_missing_sphinx_raises_infer_from_function(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises NameError: Never\n            """\n            def ex_func(val):\n                return RuntimeError(val)\n            raise ex_func(\'hi\') #@\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_find_sphinx_attr_raises_exact_exc(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a sphinx docstring.\n\n            :raises re.error: Sometimes\n            """\n            import re\n            raise re.error(\'hi\')  #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_sphinx_attr_raises_substr_exc(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a sphinx docstring.\n\n            :raises re.error: Sometimes\n            """\n            from re import error\n            raise error(\'hi\')  #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_find_valid_missing_sphinx_attr_raises(self):
        node = astroid.extract_node('\n        def my_func(self):\n            """This is a sphinx docstring.\n\n            :raises re.anothererror: Sometimes\n            """\n            from re import error\n            raise error(\'hi\')\n        ')
        raise_node = node.body[1]
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('error', ))):
            self.checker.visit_raise(raise_node)

    def test_find_invalid_missing_sphinx_attr_raises(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a sphinx docstring.\n\n            :raises bogusmodule.error: Sometimes\n            """\n            from re import error\n            raise error(\'hi\') #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    @set_config(accept_no_raise_doc=False)
    def test_sphinx_raises_with_prefix(self):
        code_snippet = '\n        def my_func(self):\n            """This is a sphinx docstring.\n\n            :raises {prefix}re.error: Sometimes\n            """\n            import re\n            raise re.error(\'hi\') #@\n        '
        for prefix in ('~', '!'):
            raise_node = astroid.extract_node(code_snippet.format(prefix=prefix))
            with self.assertNoMessages():
                self.checker.visit_raise(raise_node)

        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_raise_uninferable(self):
        raise_node = astroid.extract_node('\n        from unknown import Unknown\n\n        def my_func(self):\n            """This is a docstring.\n\n            :raises NameError: Never\n            """\n            raise Unknown(\'hi\') #@\n            raise NameError(\'hi\')\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_returns_from_inner_functions(self):
        raise_node = astroid.extract_node('\n        def my_func(self):\n            """This is a docstring.\n\n            :raises NameError: Never\n            """\n            def ex_func(val):\n                def inner_func(value):\n                    return OSError(value)\n                return RuntimeError(val)\n            raise ex_func(\'hi\') #@\n            raise NameError(\'hi\')\n        ')
        node = raise_node.frame()
        with self.assertAddsMessages(Message(msg_id='missing-raises-doc',
          node=node,
          args=('RuntimeError', ))):
            self.checker.visit_raise(raise_node)

    def test_ignores_returns_use_only_names(self):
        raise_node = astroid.extract_node('\n        def myfunc():\n            """This is a docstring\n\n            :raises NameError: Never\n            """\n            def inner_func():\n                return 42\n\n            raise inner_func() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_ignores_returns_use_only_exception_instances(self):
        raise_node = astroid.extract_node('\n        def myfunc():\n            """This is a docstring\n\n            :raises MyException: Never\n            """\n            class MyException(Exception):\n                pass\n            def inner_func():\n                return MyException\n\n            raise inner_func() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_no_crash_when_inferring_handlers(self):
        raise_node = astroid.extract_node('\n        import collections\n\n        def test():\n           """raises\n\n           :raise U: pass\n           """\n           try:\n              pass\n           except collections.U as exc:\n              raise #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_no_crash_when_cant_find_exception(self):
        raise_node = astroid.extract_node('\n        import collections\n\n        def test():\n           """raises\n\n           :raise U: pass\n           """\n           try:\n              pass\n           except U as exc:\n              raise #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)

    def test_no_error_notimplemented_documented(self):
        raise_node = astroid.extract_node('\n        def my_func():\n            """\n            Raises:\n                NotImplementedError: When called.\n            """\n            raise NotImplementedError #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_raise(raise_node)