# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_python3.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 41347 bytes
"""Tests for the python3 checkers."""
from __future__ import absolute_import
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, sys, textwrap, astroid, pytest
from pylint import testutils
from pylint.checkers import python3 as checker
from pylint.interfaces import INFERENCE, INFERENCE_FAILURE
python2_only = pytest.mark.skipif((sys.version_info[0] > 2), reason='Python 2 only')

class TestPython3Checker(testutils.CheckerTestCase):
    CHECKER_CLASS = checker.Python3Checker

    def check_bad_builtin(self, builtin_name):
        node = astroid.extract_node(builtin_name + '  #@')
        message = builtin_name.lower() + '-builtin'
        with self.assertAddsMessages(testutils.Message(message, node=node)):
            self.checker.visit_name(node)

    @python2_only
    def test_bad_builtins(self):
        builtins = [
         'apply',
         'buffer',
         'cmp',
         'coerce',
         'execfile',
         'file',
         'input',
         'intern',
         'long',
         'raw_input',
         'round',
         'reduce',
         'StandardError',
         'unichr',
         'unicode',
         'xrange',
         'reload']
        for builtin in builtins:
            self.check_bad_builtin(builtin)

    def as_iterable_in_for_loop_test(self, fxn):
        code = 'for x in {}(): pass'.format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_used_by_iterable_in_for_loop_test(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = astroid.extract_node('\n        for x in (whatever(\n            {}() #@\n        )):\n            pass\n        '.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_iterable_in_genexp_test(self, fxn):
        code = 'x = (x for x in {}())'.format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_starred_context(self, fxn):
        code = 'x = test(*{}())'.format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_listcomp_test(self, fxn):
        code = 'x = [x for x in {}(None, [1])]'.format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_yield_from(self, fxn):
        code = 'yield from {}()'.format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_used_in_variant_in_genexp_test(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = astroid.extract_node('\n        list(\n            __({}(x))\n            for x in [1]\n        )\n        '.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_used_in_variant_in_listcomp_test(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = astroid.extract_node('\n        [\n            __({}(None, x))\n        for x in [[1]]]\n        '.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_argument_to_callable_constructor_test(self, fxn, callable_fn):
        module = astroid.parse('x = {}({}())'.format(callable_fn, fxn))
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_materialized_filter(self, callable_fn):
        module = astroid.parse('list(filter(None, {}()))'.format(callable_fn))
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_random_fxn_test(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = astroid.extract_node('\n        y(\n            {}() #@\n        )\n        '.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def as_argument_to_str_join_test(self, fxn):
        code = "x = ''.join({}())".format(fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_argument_to_itertools_functions(self, fxn):
        code = '\n        from __future__ import absolute_import\n        import itertools\n        from itertools import product\n        for i,j in product({fxn}(), repeat=2):\n            pass\n        for i,j in itertools.product({fxn}(), repeat=2):\n            pass\n        '.format(fxn=fxn)
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def as_iterable_in_unpacking(self, fxn):
        node = astroid.extract_node('\n        a, b = __({}())\n        '.format(fxn))
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def as_assignment(self, fxn):
        checker = '{}-builtin-not-iterating'.format(fxn)
        node = astroid.extract_node('\n        a = __({}())\n        '.format(fxn))
        message = testutils.Message(checker, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def iterating_context_tests(self, fxn):
        """Helper for verifying a function isn't used as an iterator."""
        self.as_iterable_in_for_loop_test(fxn)
        self.as_used_by_iterable_in_for_loop_test(fxn)
        self.as_iterable_in_genexp_test(fxn)
        self.as_iterable_in_listcomp_test(fxn)
        self.as_used_in_variant_in_genexp_test(fxn)
        self.as_used_in_variant_in_listcomp_test(fxn)
        self.as_argument_to_random_fxn_test(fxn)
        self.as_argument_to_str_join_test(fxn)
        self.as_iterable_in_unpacking(fxn)
        self.as_assignment(fxn)
        self.as_argument_to_materialized_filter(fxn)
        self.as_iterable_in_yield_from(fxn)
        self.as_iterable_in_starred_context(fxn)
        self.as_argument_to_itertools_functions(fxn)
        for func in ('iter', 'list', 'tuple', 'sorted', 'set', 'sum', 'any', 'all',
                     'enumerate', 'dict', 'OrderedDict'):
            self.as_argument_to_callable_constructor_test(fxn, func)

    def test_dict_subclasses_methods_in_iterating_context(self):
        iterating, not_iterating = astroid.extract_node('\n        from __future__ import absolute_import\n        from collections import defaultdict\n        d = defaultdict(list)\n        a, b = d.keys() #@\n        x = d.keys() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(iterating.value)
        message = testutils.Message('dict-keys-not-iterating', node=(not_iterating.value))
        with self.assertAddsMessages(message):
            self.checker.visit_call(not_iterating.value)

    def test_dict_methods_in_iterating_context(self):
        iterating_code = [
         'for x in {}(): pass',
         '(x for x in {}())',
         '[x for x in {}()]',
         'iter({}())',
         'a, b = {}()',
         'max({}())',
         'min({}())',
         '3 in {}()',
         'set().update({}())',
         '[].extend({}())',
         '{{}}.update({}())',
         '\n            from __future__ import absolute_import\n            from itertools import chain\n            chain.from_iterable({}())\n            ']
        non_iterating_code = [
         'x = __({}())', '__({}())[0]']
        for method in ('keys', 'items', 'values'):
            dict_method = '{{}}.{}'.format(method)
            for code in iterating_code:
                with_value = code.format(dict_method)
                module = astroid.parse(with_value)
                with self.assertNoMessages():
                    self.walk(module)

            for code in non_iterating_code:
                with_value = code.format(dict_method)
                node = astroid.extract_node(with_value)
                checker = 'dict-{}-not-iterating'.format(method)
                message = testutils.Message(checker, node=node)
                with self.assertAddsMessages(message):
                    self.checker.visit_call(node)

    def test_map_in_iterating_context(self):
        self.iterating_context_tests('map')

    def test_zip_in_iterating_context(self):
        self.iterating_context_tests('zip')

    def test_range_in_iterating_context(self):
        self.iterating_context_tests('range')

    def test_filter_in_iterating_context(self):
        self.iterating_context_tests('filter')

    def defined_method_test(self, method, warning):
        """Helper for verifying that a certain method is not defined."""
        node = astroid.extract_node('\n            class Foo(object):\n                def __{}__(self, other):  #@\n                    pass'.format(method))
        message = testutils.Message(warning, node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)

    def test_delslice_method(self):
        self.defined_method_test('delslice', 'delslice-method')

    def test_getslice_method(self):
        self.defined_method_test('getslice', 'getslice-method')

    def test_setslice_method(self):
        self.defined_method_test('setslice', 'setslice-method')

    def test_coerce_method(self):
        self.defined_method_test('coerce', 'coerce-method')

    def test_oct_method(self):
        self.defined_method_test('oct', 'oct-method')

    def test_hex_method(self):
        self.defined_method_test('hex', 'hex-method')

    def test_nonzero_method(self):
        self.defined_method_test('nonzero', 'nonzero-method')

    def test_cmp_method(self):
        self.defined_method_test('cmp', 'cmp-method')

    def test_div_method(self):
        self.defined_method_test('div', 'div-method')

    def test_idiv_method(self):
        self.defined_method_test('idiv', 'idiv-method')

    def test_rdiv_method(self):
        self.defined_method_test('rdiv', 'rdiv-method')

    def test_eq_and_hash_method(self):
        """Helper for verifying that a certain method is not defined."""
        node = astroid.extract_node('\n            class Foo(object):  #@\n                def __eq__(self, other):\n                    pass\n                def __hash__(self):\n                    pass')
        with self.assertNoMessages():
            self.checker.visit_classdef(node)

    def test_eq_and_hash_is_none(self):
        """Helper for verifying that a certain method is not defined."""
        node = astroid.extract_node('\n            class Foo(object):  #@\n                def __eq__(self, other):\n                    pass\n                __hash__ = None')
        with self.assertNoMessages():
            self.checker.visit_classdef(node)

    def test_eq_without_hash_method(self):
        """Helper for verifying that a certain method is not defined."""
        node = astroid.extract_node('\n            class Foo(object):  #@\n                def __eq__(self, other):\n                    pass')
        message = testutils.Message('eq-without-hash', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_classdef(node)

    @python2_only
    def test_print_statement(self):
        node = astroid.extract_node('print "Hello, World!" #@')
        message = testutils.Message('print-statement', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_print(node)

    @python2_only
    def test_backtick(self):
        node = astroid.extract_node('`test`')
        message = testutils.Message('backtick', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_repr(node)

    def test_relative_import(self):
        node = astroid.extract_node('import string  #@')
        message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_import(node)
        with self.assertNoMessages():
            self.checker.visit_import(node)

    def test_relative_from_import(self):
        node = astroid.extract_node('from os import path  #@')
        message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_importfrom(node)
        with self.assertNoMessages():
            self.checker.visit_importfrom(node)

    def test_absolute_import(self):
        module_import = astroid.parse('from __future__ import absolute_import; import os')
        module_from = astroid.parse('from __future__ import absolute_import; from os import path')
        with self.assertNoMessages():
            for module in (module_import, module_from):
                self.walk(module)

    def test_import_star_module_level(self):
        node = astroid.extract_node('\n        def test():\n            from lala import * #@\n        ')
        absolute = testutils.Message('no-absolute-import', node=node)
        star = testutils.Message('import-star-module-level', node=node)
        with self.assertAddsMessages(absolute, star):
            self.checker.visit_importfrom(node)

    def test_division(self):
        nodes = astroid.extract_node('            from _unknown import a, b\n            3 / 2  #@\n            3 / int(a) #@\n            int(a) / 3 #@\n            a / b #@\n            ')
        for node in nodes:
            message = testutils.Message('old-division', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_binop(node)

    def test_division_with_future_statement(self):
        module = astroid.parse('from __future__ import division; 3 / 2')
        with self.assertNoMessages():
            self.walk(module)

    def test_floor_division(self):
        node = astroid.extract_node(' 3 // 2  #@')
        with self.assertNoMessages():
            self.checker.visit_binop(node)

    def test_division_by_float(self):
        nodes = astroid.extract_node('            3.0 / 2  #@\n            3 / 2.0  #@\n            3 / float(a)  #@\n            float(a) / 3  #@\n            ')
        with self.assertNoMessages():
            for node in nodes:
                self.checker.visit_binop(node)

    def test_division_different_types(self):
        nodes = astroid.extract_node('\n        class A:\n            pass\n        A / 2 #@\n        A() / 2 #@\n        "a" / "a" #@\n        class Path:\n            def __div__(self, other):\n                return 42\n        Path() / 24 #@\n        ')
        for node in nodes:
            with self.assertNoMessages():
                self.checker.visit_binop(node)

    def test_dict_iter_method(self):
        for meth in ('keys', 'values', 'items'):
            node = astroid.extract_node('x.iter%s()  #@' % meth)
            message = testutils.Message('dict-iter-method', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_dict_iter_method_on_dict(self):
        nodes = astroid.extract_node('\n        from collections import defaultdict\n        {}.iterkeys() #@\n        defaultdict(list).iterkeys() #@\n        class Someclass(dict):\n            pass\n        Someclass().iterkeys() #@\n\n        # Emits even though we are not sure they are dicts\n        x.iterkeys() #@\n\n        def func(x):\n            x.iterkeys() #@\n        ')
        for node in nodes:
            message = testutils.Message('dict-iter-method', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_dict_not_iter_method(self):
        arg_node = astroid.extract_node('x.iterkeys(x)  #@')
        stararg_node = astroid.extract_node('x.iterkeys(*x)  #@')
        kwarg_node = astroid.extract_node('x.iterkeys(y=x)  #@')
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node):
                self.checker.visit_call(node)

    def test_dict_view_method(self):
        for meth in ('keys', 'values', 'items'):
            node = astroid.extract_node('x.view%s()  #@' % meth)
            message = testutils.Message('dict-view-method', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_dict_viewkeys(self):
        nodes = astroid.extract_node('\n        from collections import defaultdict\n        {}.viewkeys() #@\n        defaultdict(list).viewkeys() #@\n        class Someclass(dict):\n            pass\n        Someclass().viewkeys() #@\n\n        # Emits even though they might not be dicts\n        x.viewkeys() #@\n\n        def func(x):\n            x.viewkeys() #@\n        ')
        for node in nodes:
            message = testutils.Message('dict-view-method', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_next_method(self):
        node = astroid.extract_node('x.next()  #@')
        message = testutils.Message('next-method-called', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_not_next_method(self):
        arg_node = astroid.extract_node('x.next(x)  #@')
        stararg_node = astroid.extract_node('x.next(*x)  #@')
        kwarg_node = astroid.extract_node('x.next(y=x)  #@')
        with self.assertNoMessages():
            for node in (arg_node, stararg_node, kwarg_node):
                self.checker.visit_call(node)

    def test_metaclass_assignment(self):
        node = astroid.extract_node('\n            class Foo(object):  #@\n                __metaclass__ = type')
        message = testutils.Message('metaclass-assignment', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_classdef(node)

    def test_metaclass_global_assignment(self):
        module = astroid.parse('__metaclass__ = type')
        with self.assertNoMessages():
            self.walk(module)

    @python2_only
    def test_parameter_unpacking(self):
        node = astroid.extract_node('def func((a, b)):#@\n pass')
        arg = node.args.args[0]
        with self.assertAddsMessages(testutils.Message('parameter-unpacking', node=arg)):
            self.checker.visit_arguments(node.args)

    @python2_only
    def test_old_raise_syntax(self):
        node = astroid.extract_node('raise Exception, "test"')
        message = testutils.Message('old-raise-syntax', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    def test_xreadlines_attribute(self):
        node = astroid.extract_node('\n        f.xreadlines #@\n        ')
        message = testutils.Message('xreadlines-attribute', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_exception_message_attribute(self):
        node = astroid.extract_node('\n        try:\n            raise Exception("test")\n        except Exception as e:\n            e.message #@\n        ')
        message = testutils.Message('exception-message-attribute', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_normal_message_attribute(self):
        node = astroid.extract_node('\n        e.message #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    def test_invalid_codec(self):
        node = astroid.extract_node('foobar.encode("hex") #@')
        message = testutils.Message('invalid-str-codec', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_valid_codec(self):
        node = astroid.extract_node('foobar.encode("ascii", "ignore")  #@')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_visit_call_with_kwarg(self):
        node = astroid.extract_node('foobar.raz(encoding="hex")  #@')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_invalid_open_codec(self):
        node = astroid.extract_node('open(foobar, encoding="hex") #@')
        message = testutils.Message('invalid-str-codec', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_valid_open_codec(self):
        node = astroid.extract_node('open(foobar, encoding="palmos") #@')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    @python2_only
    def test_raising_string(self):
        node = astroid.extract_node('raise "Test"')
        message = testutils.Message('raising-string', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_raise(node)

    @python2_only
    def test_checker_disabled_by_default(self):
        node = astroid.parse(textwrap.dedent('\n        abc = 1l\n        raise Exception, "test"\n        raise "test"\n        `abc`\n        '))
        with self.assertNoMessages():
            self.walk(node)

    def test_using_cmp_argument(self):
        nodes = astroid.extract_node('\n        [].sort(cmp=lambda x: x) #@\n        a = list(range(x))\n        a.sort(cmp=lambda x: x) #@\n\n        sorted([], cmp=lambda x: x) #@\n        ')
        for node in nodes:
            message = testutils.Message('using-cmp-argument', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_call(node)

    def test_sys_maxint(self):
        node = astroid.extract_node('\n        import sys\n        sys.maxint #@\n        ')
        message = testutils.Message('sys-max-int', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_itertools_izip(self):
        node = astroid.extract_node('\n        from itertools import izip #@\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        message = testutils.Message('deprecated-itertools-function', node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_deprecated_types_fields(self):
        node = astroid.extract_node('\n        from types import StringType #@\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        message = testutils.Message('deprecated-types-field', node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_sys_maxint_imort_from(self):
        node = astroid.extract_node('\n        from sys import maxint #@\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        message = testutils.Message('sys-max-int', node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_object_maxint(self):
        node = astroid.extract_node('\n        sys = object()\n        sys.maxint #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    def test_bad_import(self):
        node = astroid.extract_node('\n        import urllib2, sys #@\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        message = testutils.Message('bad-python3-import', node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_import(node)

    def test_bad_import_turtle(self):
        node = astroid.extract_node('\n        import turtle #@\n        turtle.Turtle()\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_import(node)

    def test_bad_import_dbm(self):
        node = astroid.extract_node('\n        from dbm import open as open_ #@\n        open_("dummy.db")\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_importfrom(node)

    @python2_only
    def test_bad_import_not_on_relative(self):
        samples = ['from .commands import titi', 'from . import commands']
        for code in samples:
            node = astroid.extract_node(code)
            absolute_import_message = testutils.Message('no-absolute-import', node=node)
            with self.assertAddsMessages(absolute_import_message):
                self.checker.visit_importfrom(node)
            self.checker._future_absolute_import = False

    def test_bad_import_conditional(self):
        node = astroid.extract_node('\n        import six\n        if six.PY2:\n            import urllib2 #@\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_import(node)

    def test_bad_import_try_except_handler(self):
        node = astroid.extract_node('\n        try:\n            from hashlib import sha\n        except:\n            import sha #@\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_import(node)

    def test_bad_import_try(self):
        node = astroid.extract_node('\n        try:\n            import md5  #@\n        except:\n            from hashlib import md5\n        finally:\n            pass\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_import(node)

    def test_bad_import_try_finally(self):
        node = astroid.extract_node('\n        try:\n            import Queue  #@\n        finally:\n            import queue\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        message = testutils.Message('bad-python3-import', node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_import(node)

    def test_bad_import_from(self):
        node = astroid.extract_node('\n        from cStringIO import StringIO #@\n        ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        message = testutils.Message('bad-python3-import', node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_bad_string_attribute(self):
        node = astroid.extract_node('\n        import string\n        string.maketrans #@\n        ')
        message = testutils.Message('deprecated-string-function', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_bad_operator_attribute(self):
        node = astroid.extract_node('\n        import operator\n        operator.div #@\n        ')
        message = testutils.Message('deprecated-operator-function', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_comprehension_escape(self):
        assign, escaped_node = astroid.extract_node('\n        a = [i for i in range(10)] #@\n        i #@\n        ')
        good_module = astroid.parse('\n        {c for c in range(10)} #@\n        {j:j for j in range(10)} #@\n        [image_child] = [x for x in range(10)]\n        thumbnail = func(__(image_child))\n        ')
        message = testutils.Message('comprehension-escape', node=escaped_node)
        with self.assertAddsMessages(message):
            self.checker.visit_listcomp(assign.value)
        with self.assertNoMessages():
            self.walk(good_module)

    def test_comprehension_escape_newly_introduced(self):
        node = astroid.extract_node('\n        [i for i in range(3)]\n        for i in range(3):\n            i\n        ')
        with self.assertNoMessages():
            self.walk(node)

    def test_exception_escape(self):
        module = astroid.parse('\n        try: 1/0\n        except ValueError as exc:\n            pass\n        exc #@\n        try:\n           2/0\n        except (ValueError, TypeError) as exc:\n           exc = 2\n        exc #@\n        try:\n           2/0\n        except (ValueError, TypeError): #@\n           exc = 2\n        ')
        message = testutils.Message('exception-escape', node=(module.body[1].value))
        with self.assertAddsMessages(message):
            self.checker.visit_excepthandler(module.body[0].handlers[0])
        with self.assertNoMessages():
            self.checker.visit_excepthandler(module.body[2].handlers[0])
            self.checker.visit_excepthandler(module.body[4].handlers[0])

    def test_bad_sys_attribute(self):
        node = astroid.extract_node('\n        import sys\n        sys.exc_clear #@\n        ')
        message = testutils.Message('deprecated-sys-function', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_attribute(node)

    def test_bad_urllib_attribute(self):
        nodes = astroid.extract_node('\n        import urllib\n        urllib.addbase #@\n        urllib.splithost #@\n        urllib.urlretrieve #@\n        urllib.urlopen #@\n        urllib.urlencode #@\n        ')
        for node in nodes:
            message = testutils.Message('deprecated-urllib-function', node=node)
            with self.assertAddsMessages(message):
                self.checker.visit_attribute(node)

    def test_ok_string_attribute(self):
        node = astroid.extract_node('\n        import string\n        string.ascii_letters #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_attribute(node)

    def test_bad_string_call(self):
        node = astroid.extract_node('\n        import string\n        string.upper("hello world") #@\n        ')
        message = testutils.Message('deprecated-string-function', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_ok_shadowed_call(self):
        node = astroid.extract_node('\n        import six.moves.configparser\n        six.moves.configparser.ConfigParser() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_ok_string_call(self):
        node = astroid.extract_node('\n        import string\n        string.Foramtter() #@\n        ')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_bad_string_import_from(self):
        node = astroid.extract_node('\n         from string import atoi #@\n         ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        message = testutils.Message('deprecated-string-function', node=node)
        with self.assertAddsMessages(absolute_import_message, message):
            self.checker.visit_importfrom(node)

    def test_ok_string_import_from(self):
        node = astroid.extract_node('\n         from string import digits #@\n         ')
        absolute_import_message = testutils.Message('no-absolute-import', node=node)
        with self.assertAddsMessages(absolute_import_message):
            self.checker.visit_importfrom(node)

    def test_bad_str_translate_call_string_literal(self):
        node = astroid.extract_node("\n         foobar.translate(None, 'abc123') #@\n         ")
        message = testutils.Message('deprecated-str-translate-call',
          node=node, confidence=INFERENCE_FAILURE)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_bad_str_translate_call_variable(self):
        node = astroid.extract_node("\n         def raz(foobar):\n           foobar.translate(None, 'hello') #@\n         ")
        message = testutils.Message('deprecated-str-translate-call',
          node=node, confidence=INFERENCE_FAILURE)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_bad_str_translate_call_infer_str(self):
        node = astroid.extract_node('\n         foobar = "hello world"\n         foobar.translate(None, foobar) #@\n         ')
        message = testutils.Message('deprecated-str-translate-call',
          node=node, confidence=INFERENCE)
        with self.assertAddsMessages(message):
            self.checker.visit_call(node)

    def test_ok_str_translate_call_integer(self):
        node = astroid.extract_node('\n         foobar.translate(None, 33) #@\n         ')
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_ok_str_translate_call_keyword(self):
        node = astroid.extract_node("\n         foobar.translate(None, 'foobar', raz=33) #@\n         ")
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_ok_str_translate_call_not_str(self):
        node = astroid.extract_node("\n         foobar = {}\n         foobar.translate(None, 'foobar') #@\n         ")
        with self.assertNoMessages():
            self.checker.visit_call(node)

    def test_non_py2_conditional(self):
        code = '\n        from __future__ import absolute_import\n        import sys\n        x = {}\n        if sys.maxsize:\n            x.iterkeys()  #@\n        '
        node = astroid.extract_node(code)
        module = node.parent.parent
        message = testutils.Message('dict-iter-method', node=node)
        with self.assertAddsMessages(message):
            self.walk(module)

    def test_six_conditional(self):
        code = '\n        from __future__ import absolute_import\n        import six\n        x = {}\n        if six.PY2:\n            x.iterkeys()\n        '
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def test_versioninfo_conditional(self):
        code = '\n        from __future__ import absolute_import\n        import sys\n        x = {}\n        if sys.version_info[0] == 2:\n            x.iterkeys()\n        '
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def test_versioninfo_tuple_conditional(self):
        code = '\n        from __future__ import absolute_import\n        import sys\n        x = {}\n        if sys.version_info == (2, 7):\n            x.iterkeys()\n        '
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def test_six_ifexp_conditional(self):
        code = '\n        from __future__ import absolute_import\n        import six\n        import string\n        string.translate if six.PY2 else None\n        '
        module = astroid.parse(code)
        with self.assertNoMessages():
            self.walk(module)

    def test_next_defined(self):
        node = astroid.extract_node('\n            class Foo(object):\n                def next(self):  #@\n                    pass')
        message = testutils.Message('next-method-defined', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)

    def test_next_defined_too_many_args(self):
        node = astroid.extract_node('\n            class Foo(object):\n                def next(self, foo=None):  #@\n                    pass')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_next_defined_static_method_too_many_args(self):
        node = astroid.extract_node('\n            class Foo(object):\n                @staticmethod\n                def next(self):  #@\n                    pass')
        with self.assertNoMessages():
            self.checker.visit_functiondef(node)

    def test_next_defined_static_method(self):
        node = astroid.extract_node('\n            class Foo(object):\n                @staticmethod\n                def next():  #@\n                    pass')
        message = testutils.Message('next-method-defined', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)

    def test_next_defined_class_method(self):
        node = astroid.extract_node('\n            class Foo(object):\n                @classmethod\n                def next(cls):  #@\n                    pass')
        message = testutils.Message('next-method-defined', node=node)
        with self.assertAddsMessages(message):
            self.checker.visit_functiondef(node)


@python2_only
class TestPython3TokenChecker(testutils.CheckerTestCase):
    CHECKER_CLASS = checker.Python3TokenChecker

    def _test_token_message(self, code, symbolic_message):
        tokens = testutils._tokenize_str(code)
        message = testutils.Message(symbolic_message, line=1)
        with self.assertAddsMessages(message):
            self.checker.process_tokens(tokens)

    def test_long_suffix(self):
        for code in ('1l', '1L'):
            self._test_token_message(code, 'long-suffix')

    def test_old_ne_operator(self):
        self._test_token_message('1 <> 2', 'old-ne-operator')

    def test_old_octal_literal(self):
        for octal in ('045', '055', '075', '077', '076543'):
            self._test_token_message(octal, 'old-octal-literal')

        for non_octal in ('45', '00', '085', '08', '1'):
            tokens = testutils._tokenize_str(non_octal)
            with self.assertNoMessages():
                self.checker.process_tokens(tokens)

    def test_non_ascii_bytes_literal(self):
        code = 'b"测试"'
        self._test_token_message(code, 'non-ascii-bytes-literal')
        for code in ('测试', '测试', 'abcdef', b'\x80'):
            tokens = testutils._tokenize_str(code)
            with self.assertNoMessages():
                self.checker.process_tokens(tokens)