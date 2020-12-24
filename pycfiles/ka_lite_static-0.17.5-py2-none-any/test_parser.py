# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/tests/test_parser.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import textwrap, unittest
from slimit import ast
from slimit.parser import Parser
from slimit.visitors import nodevisitor

class ParserTestCase(unittest.TestCase):

    def test_line_terminator_at_the_end_of_file(self):
        parser = Parser()
        parser.parse('var $_ = function(x){}(window);\n')

    def _test_function_expression(self):
        text = "\n        if (true) {\n          function() {\n            foo;\n            location = 'http://anywhere.com';\n          }\n        }\n        "
        parser = Parser()
        parser.parse(text)

    def test_modify_tree(self):
        text = '\n        for (var i = 0; i < 10; i++) {\n          var x = 5 + i;\n        }\n        '
        parser = Parser()
        tree = parser.parse(text)
        for node in nodevisitor.visit(tree):
            if isinstance(node, ast.Identifier) and node.value == 'i':
                node.value = 'hello'

        self.assertMultiLineEqual(tree.to_ecma(), textwrap.dedent('\n            for (var hello = 0; hello < 10; hello++) {\n              var x = 5 + hello;\n            }\n            ').strip())

    def test_bug_no_semicolon_at_the_end_of_block_plus_newline_at_eof(self):
        text = textwrap.dedent('\n        function add(x, y) {\n          return x + y;\n        }\n        ')
        parser = Parser()
        tree = parser.parse(text)
        self.assertTrue(bool(tree.children()))

    def test_function_expression_is_part_of_member_expr_nobf(self):
        text = 'window.done_already || function () { return "slimit!" ; }();'
        self.assertTrue(bool(Parser().parse(text).children()))

    def test_that_parsing_eventually_stops(self):
        text = 'var a;\n        , b;'
        parser = Parser()
        self.assertRaises(SyntaxError, parser.parse, text)


class ASITestCase(unittest.TestCase):
    TEST_CASES = [
     ("\n        switch (day) {\n          case 1:\n            result = 'Mon';\n            break\n          case 2:\n            break\n        }\n        ",
 "\n         switch (day) {\n           case 1:\n             result = 'Mon';\n             break;\n           case 2:\n             break;\n         }\n         "),
     ('\n        while (true)\n          continue\n        a = 1;\n        ', '\n         while (true) continue;\n         a = 1;\n         '),
     ('\n        return\n        a;\n        ', '\n         return;\n         a;\n        '),
     ('\n        x = 5\n        ', '\n         x = 5;\n         '),
     ('\n        var a, b\n        var x\n        ', '\n         var a, b;\n         var x;\n         '),
     ('\n        var a, b\n        var x\n        ', '\n         var a, b;\n         var x;\n         '),
     ('\n        return\n        a + b\n        ', '\n         return;\n         a + b;\n         '),
     ('while (true) ;', 'while (true) ;'),
     ('\n        if (x) {\n          y()\n        }\n        ', '\n         if (x) {\n           y();\n         }\n         '),
     ('\n        for ( ; i < length; i++) {\n        }\n        ', '\n         for ( ; i < length; i++) {\n\n         }\n         '),
     ('\n        var i;\n        for (i; i < length; i++) {\n        }\n        ', '\n         var i;\n         for (i; i < length; i++) {\n\n         }\n         ')]

    def test_throw_statement(self):
        input = textwrap.dedent("\n        throw\n          'exc';\n        ")
        parser = Parser()
        self.assertRaises(SyntaxError, parser.parse, input)


def make_test_function(input, expected):

    def test_func(self):
        parser = Parser()
        result = parser.parse(input).to_ecma()
        self.assertMultiLineEqual(result, expected)

    return test_func


for index, (input, expected) in enumerate(ASITestCase.TEST_CASES):
    input = textwrap.dedent(input).strip()
    expected = textwrap.dedent(expected).strip()
    func = make_test_function(input, expected)
    setattr(ASITestCase, 'test_case_%d' % index, func)