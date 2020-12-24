# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/tests/test_ecmavisitor.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import textwrap, unittest
from slimit.parser import Parser

class ECMAVisitorTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = 2000

    TEST_CASES = [
     '\n        {\n          var a = 5;\n        }\n        ',
     '\n        var a;\n        var b;\n        var a, b = 3;\n        var a = 1, b;\n        var a = 5, b = 7;\n        ',
     '\n        ;\n        ;\n        ;\n        ',
     'if (true) var x = 100;',
     '\n        if (true) {\n          var x = 100;\n          var y = 200;\n        }\n        ',
     'if (true) if (true) var x = 100; else var y = 200;',
     '\n        if (true) {\n          var x = 100;\n        } else {\n          var y = 200;\n        }\n        ',
     '\n        for (i = 0; i < 10; i++) {\n          x = 10 * i;\n        }\n        ',
     '\n        for (var i = 0; i < 10; i++) {\n          x = 10 * i;\n        }\n        ',
     '\n        for (i = 0, j = 10; i < j && j < 15; i++, j++) {\n          x = i * j;\n        }\n        ',
     '\n        for (var i = 0, j = 10; i < j && j < 15; i++, j++) {\n          x = i * j;\n        }\n        ',
     '\n        for (p in obj) {\n\n        }\n        ',
     '\n        for (Q || (Q = []); d < b; ) {\n          d = 1;\n        }\n        ',
     '\n        for (new Foo(); d < b; ) {\n          d = 1;\n        }\n        ',
     '\n        for (2 >> (foo ? 32 : 43) && 54; 21; ) {\n          a = c;\n        }\n        ',
     '\n        for (/^.+/g; cond(); ++z) {\n          ev();\n        }\n        ',
     '\n        for (var p in obj) {\n          p = 1;\n        }\n        ',
     '\n        do {\n          x += 1;\n        } while (true);\n        ',
     '\n        while (false) {\n          x = null;\n        }\n        ',
     "\n        while (true) {\n          continue;\n          s = 'I am not reachable';\n        }\n        ",
     "\n        while (true) {\n          continue label1;\n          s = 'I am not reachable';\n        }\n        ",
     "\n        while (true) {\n          break;\n          s = 'I am not reachable';\n        }\n        ",
     "\n        while (true) {\n          break label1;\n          s = 'I am not reachable';\n        }\n        ",
     '\n        {\n          return;\n        }\n        ',
     '\n        {\n          return 1;\n        }\n        ',
     '\n        with (x) {\n          var y = x * 2;\n        }\n        ',
     '\n        label: while (true) {\n          x *= 3;\n        }\n        ',
     "\n        switch (day_of_week) {\n          case 6:\n          case 7:\n            x = 'Weekend';\n            break;\n          case 1:\n            x = 'Monday';\n            break;\n          default:\n            break;\n        }\n        ",
     "\n        throw 'exc';\n        ",
     'debugger;',
     '\n        5 + 7 - 20 * 10;\n        ++x;\n        --x;\n        x++;\n        x--;\n        x = 17 /= 3;\n        s = mot ? z : /x:3;x<5;y</g / i;\n        ',
     '\n        try {\n          x = 3;\n        } catch (exc) {\n          x = exc;\n        }\n        ',
     '\n        try {\n          x = 3;\n        } finally {\n          x = null;\n        }\n        ',
     '\n        try {\n          x = 5;\n        } catch (exc) {\n          x = exc;\n        } finally {\n          y = null;\n        }\n        ',
     '\n        function foo(x, y) {\n          z = 10;\n          return x + y + z;\n        }\n        ',
     '\n        function foo() {\n          return 10;\n        }\n        ',
     '\n        var a = function() {\n          return 10;\n        };\n        ',
     '\n        var a = function foo(x, y) {\n          return x + y;\n        };\n        ',
     '\n        function foo() {\n          function bar() {\n\n          }\n        }\n        ',
     '\n        var mult = function(x) {\n          return x * 10;\n        }();\n        ',
     'foo();',
     'foo(x, 7);',
     'foo()[10];',
     'foo().foo;',
     'var foo = new Foo();',
     'var bar = new Foo.Bar();',
     'var bar = new Foo.Bar()[7];',
     '\n        var obj = {\n          foo: 10,\n          bar: 20\n        };\n        ',
     "\n        var obj = {\n          1: 'a',\n          2: 'b'\n        };\n        ",
     "\n        var obj = {\n          'a': 100,\n          'b': 200\n        };\n        ",
     '\n        var obj = {\n        };\n        ',
     '\n        var a = [1,2,3,4,5];\n        var res = a[3];\n        ',
     'var a = [,,,];',
     'var a = [1,,,4];',
     'var a = [1,,3,,5];',
     "\n        String.prototype.foo = function(data) {\n          var tmpl = this.toString();\n          return tmpl.replace(/{{\\s*(.*?)\\s*}}/g, function(a, b) {\n            var node = data;\n            if (true) {\n              var value = true;\n            } else {\n              var value = false;\n            }\n            $.each(n.split('.'), function(i, sym) {\n              node = node[sym];\n            });\n            return node;\n          });\n        };\n        ",
     'Expr.match[type].source + (/(?![^\\[]*\\])(?![^\\(]*\\))/.source);',
     '(options = arguments[i]) != null;',
     'return (/h\\d/i).test(elem.nodeName);',
     '\n        e.b(d) ? (a = [c.f(j[1])], e.fn.attr.call(a, d, !0)) : a = [k.f(j[1])];\n        ',
     '\n        (function() {\n          x = 5;\n        }());\n        ',
     '\n        (function() {\n          x = 5;\n        })();\n        ',
     'return !(match === true || elem.getAttribute("classid") !== match);',
     'var el = (elem ? elem.ownerDocument || elem : 0).documentElement;',
     'typeof second.length === "number";',
     '\n        for (o(); i < 3; i++) {\n\n        }\n        ',
     '\n        Name.prototype = {\n          get fullName() {\n            return this.first + " " + this.last;\n          },\n          set fullName(name) {\n            var names = name.split(" ");\n            this.first = names[0];\n            this.last = names[1];\n          }\n        };\n        ']


def make_test_function(input, expected):

    def test_func(self):
        parser = Parser()
        result = parser.parse(input).to_ecma()
        self.assertMultiLineEqual(result, expected)

    return test_func


for index, input in enumerate(ECMAVisitorTestCase.TEST_CASES):
    input = textwrap.dedent(input).strip()
    func = make_test_function(input, input)
    setattr(ECMAVisitorTestCase, 'test_case_%d' % index, func)