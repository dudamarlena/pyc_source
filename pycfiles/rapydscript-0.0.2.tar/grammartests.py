# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/host/inst/rapydscript/tests/grammartests.py
# Compiled at: 2013-02-27 23:07:45
import unittest
from rapydscript.grammar import compile
from textwrap import dedent

class PyvaTest(unittest.TestCase):

    def check(self, source, result):
        source = ('\n').join(line for line in dedent(compile(dedent(source))).strip().splitlines() if line)
        result = ('\n').join(line for line in dedent(result).strip().splitlines() if line)
        try:
            self.assertEqual(source, result)
        except:
            raise AssertionError('\n%s\n!=\n%s' % (repr(source), repr(result)))


class TestTuplePackingUnpacking(PyvaTest):

    def test_return_normal_not_packed(self):
        self.check('\n            def():\n                return [1, 2, 3]\n            ', '\n            function() {\n              return [1, 2, 3];\n            }\n            ')

    def test_return_pack_normal(self):
        self.check("\n            def():\n                return 'a', 2\n            ", '\n            function() {\n              return ["a", 2];\n            }\n            ')
        self.check('\n            def():\n                return a, b2\n            ', '\n            function() {\n              return [a, b2];\n            }\n            ')
        self.check('\n            def():\n                return a\n            ', '\n            function() {\n              return a;\n            }\n            ')
        self.check('\n            def():\n                return a,\n            ', '\n            function() {\n              return [a];\n            }\n            ')

    def test_return_pack_tuples(self):
        self.check('\n            def():\n                return 1, (2, 3), 4,(5,6)\n            ', '\n            function() {\n              return [1, [2, 3], 4, [5, 6]];\n            }\n            ')

    def test_return_pack_lists(self):
        self.check('\n            def():\n                return 1, [2, 3], 4,[5,6]\n            ', '\n            function() {\n              return [1, [2, 3], 4, [5, 6]];\n            }\n            ')

    def test_return_pack_strings_with_commas(self):
        self.check("\n            def():\n                return 'a', 'hello, test',\n            ", '\n            function() {\n              return ["a", "hello, test"];\n            }\n            ')

    def test_return_pack_function_call(self):
        self.check("\n            def():\n                return 'a',2,callme('b', 2,c),'last, one'\n            ", '\n            function() {\n              return ["a", 2, callme("b", 2, c), "last, one"];\n            }\n            ')

    def test_assigment_left_two(self):
        self.check("\n            vara, varb = callme('var', c)\n            ", '\n            _$rapyd_tuple$_ = callme("var", c);\n            vara = _$rapyd_tuple$_[0];\n            varb = _$rapyd_tuple$_[1];\n            ')

    def test_assigment_item_in_list(self):
        """
        Make sure this still works
        """
        self.check('\n        def f(self):\n            myself = [0, 1, 2]\n            myself[1] = 4\n        ', '\n        f = function() {\n          var myself;\n          myself = [0, 1, 2];\n          myself[1] = 4;\n        };\n        ')

    def test_assigment_left_three(self):
        self.check("\n            vara, varb,varc = callme('var', c)\n            ", '\n            _$rapyd_tuple$_ = callme("var", c);\n            vara = _$rapyd_tuple$_[0];\n            varb = _$rapyd_tuple$_[1];\n            varc = _$rapyd_tuple$_[2];\n            ')

    def test_assigment_right_three(self):
        self.check("\n            packed_tuple = vara,'testme', 2,callable(2,3)\n            ", '\n            packed_tuple = [vara, "testme", 2, callable(2, 3)];\n            ')

    def test_for_loop_unpacking(self):
        self.check('\n            for vara,varb in input_list:\n                pass\n            ', '\n            var _$tmp1_data = _$rapyd$_iter(input_list);\n            var _$tmp2_len = _$tmp1_data.length;\n            for (var _$tmp3_index = 0; _$tmp3_index < _$tmp2_len; _$tmp3_index++) {\n              _$rapyd$_tuple = _$tmp1_data[_$tmp3_index];\n              vara = _$rapyd$_tuple[0];\n              varb = _$rapyd$_tuple[1];\n            }\n            ')

    def test_for_loop_packing(self):
        self.check("\n            for input in 'inputa', obj.call2(), vara, 9.2:\n                pass\n            ", '\n            var _$tmp1_data = _$rapyd$_iter(["inputa", obj.call2(), vara, 9.2]);\n            var _$tmp2_len = _$tmp1_data.length;\n            for (var _$tmp3_index = 0; _$tmp3_index < _$tmp2_len; _$tmp3_index++) {\n              input = _$tmp1_data[_$tmp3_index];\n            }\n            ')


class TestListComprehensions(PyvaTest):

    def test_to_and_til(self):
        self.check('\n\t\t\ta = [1 to 5]\n\t\t', '\n\t\t\ta = range(1, 5+1);\n\t\t')
        self.check('\n\t\t\ta = [1 til 5]\n\t\t', '\n\t\t\ta = range(1, 5);\n\t\t')
        self.check('\n\t\t\ta = [1 + 2 to 5 * 6]\n\t\t', '\n\t\t\ta = range((1 + 2), (5 * 6)+1);\n\t\t')
        self.check('\n\t\tfor i in [4 til 10]:\n\t\t\tpass\n\t\t', '\n\t\tvar _$tmp1_data = _$rapyd$_iter(range(4, 10));\n\t\tvar _$tmp2_len = _$tmp1_data.length;\n\t\tfor (var _$tmp3_index = 0; _$tmp3_index < _$tmp2_len; _$tmp3_index++) {\n\t\t  i = _$tmp1_data[_$tmp3_index];\n\t\t}\n\t\t')


class TestNonlocalKeyword(PyvaTest):

    def test_return_normal_not_packed(self):
        self.check('\n        def():\n            x = 2\n            def ():\n                y = 5\n        ', '\n        function() {\n          var x;\n          x = 2;\n          function() {\n            var y;\n            y = 5;\n          }\n        }\n        ')
        self.check('\n        def():\n            x = 2\n            def ():\n                nonlocal y\n                y = 5\n        ', '\n        function() {\n          var x;\n          x = 2;\n          function() {\n            y = 5;\n          }\n        }\n        ')


class Test(PyvaTest):

    def test_in(self):
        self.check('x in y', '(x in y);')
        self.check('x not in y', '!(x in y);')

    def test_len(self):
        self.check('len(x)', 'x.length;')

    def test_dot(self):
        self.check('x.y.z', 'x.y.z;')

    def test_delete(self):
        self.check('del x[a]', 'delete x[a];')
        self.check("del x['a']", 'delete x["a"];')
        self.check('del x.a', 'delete x.a;')

    def test_getitem(self):
        self.check('x[0]', 'x[0];')
        self.check('x[0][bla]', 'x[0][bla];')

    def test_negative_getitem_special(self):
        self.check('x[-1]', 'x.slice(-1)[0];')
        self.check('x[-2]', 'x.slice(-2, -1)[0];')

    def test_slicing(self):
        self.check('x[:]', 'x.slice(0);')
        self.check('x[3+3:]', 'x.slice((3 + 3));')
        self.check('x[3+3:]', 'x.slice((3 + 3));')
        self.check('x[:10]', 'x.slice(0, 10);')
        self.check('x[5:10]', 'x.slice(5, 10);')

    def test_hasattr(self):
        self.check('hasattr(x, y)', '(typeof x[y] != "undefined");')
        self.check('not hasattr(x, y)', '(typeof x[y] == "undefined");')

    def test_getattr(self):
        self.check('getattr(x, y)', 'x[y];')

    def test_setattr(self):
        self.check('setattr(x, y, z)', 'x[y] = z;')

    def test_dot_getitem(self):
        self.check('x.y[0]', 'x.y[0];')
        self.check('x.y[0].z', 'x.y[0].z;')
        self.check('x.y[0].z[214]', 'x.y[0].z[214];')

    def test_call_dot_getitem(self):
        self.check('x.f().y[0]', 'x.f().y[0];')
        self.check('x.y[0].z()', 'x.y[0].z();')
        self.check('x.y[0].z[214].f().a', 'x.y[0].z[214].f().a;')

    def test_floats(self):
        self.check('2.3 * 1.4', '(2.3 * 1.4);')

    def test_assign_call_dot_getitem(self):
        self.check('a = x.f().y[0]', 'a = x.f().y[0];')
        self.check('a = x.y[0].z()', 'a = x.y[0].z();')
        self.check('a = x.y[0].z[214].f().a', 'a = x.y[0].z[214].f().a;')
        self.check('a += x.y[0].z[214].f().a', 'a += x.y[0].z[214].f().a;')

    def test_return(self):
        self.check('\n        def():\n            return\n        ', '\n        function() {\n          return;\n        }\n        ')
        self.check('\n        def():\n            return x\n        ', '\n        function() {\n          return x;\n        }\n        ')

    def test_return_expression(self):
        self.check('\n        def():\n            return a < 5 and 6 >= b or 2 <= 8\n        ', '\n        function() {\n          return (((a < 5) && (6 >= b)) || (2 <= 8));\n        }\n        ')

    def test_if(self):
        self.check('\n        if a == 3 or b is None and c == True or d != False:\n            f()\n        ', '\n        if ((((a == 3) || ((b === null) && (c == true))) || (d != false))) {\n          f();\n        }\n        ')
        self.check('\n        if a < 5 and 6 >= b or 2 <= 8:\n            f()\n        ', '\n        if ((((a < 5) && (6 >= b)) || (2 <= 8))) {\n          f();\n        }\n        ')
        self.check('\n        if(a < 5):\n            f()\n        ', '\n        if ((a < 5)) {\n          f();\n        }\n        ')

    def test_while(self):
        self.check('\n        while a == 3 or b is None and c == True or d != False:\n            f()\n            if x:\n                break\n            continue\n        ', '\n        while ((((a == 3) || ((b === null) && (c == true))) || (d != false))) {\n          f();\n          if (x) {\n            break;\n          }\n\n          continue;\n        }\n        ')
        self.check('\n        while(a == 3):\n            f()\n        ', '\n        while ((a == 3)) {\n          f();\n        }\n        ')

    def test_for_range_literal(self):
        self.check('\n        for i in range(10):\n            f()\n        ', '\n        for (i = 0; i < 10; i++) {\n          f();\n        }\n        ')
        self.check('\n        for i in range(2, 10):\n            f()\n        ', '\n        for (i = 2; i < 10; i++) {\n          f();\n        }\n        ')
        self.check('\n        for i in range(2, 10, 2):\n            f()\n        ', '\n        for (i = 2; i < 10; i += 2) {\n          f();\n        }\n        ')

    def test_for_range_nonliteral(self):
        self.check('\n        for i in range(x(10)):\n            f()\n        ', '\n        var _$tmp1_end = x(10);\n        for (i = 0; i < _$tmp1_end; i++) {\n          f();\n        }\n        ')
        self.check('\n        for i in range(x(2), x(10)):\n            f()\n        ', '\n        var _$tmp1_end = x(10);\n        for (i = x(2); i < _$tmp1_end; i++) {\n          f();\n        }\n        ')
        self.check('\n        for i in range(x(2), x(10), x(2)):\n            f()\n        ', '\n        var _$tmp1_end = x(10), _$tmp2_step = x(2);\n        for (i = x(2); i < _$tmp1_end; i += _$tmp2_step) {\n          f();\n        }\n        ')

    def test_for_reversed_range_literal(self):
        self.check('\n        for i in reversed(range(2, 10)):\n            f()\n        ', '\n        for (i = (10) - 1; i >= 2; i--) {\n          f();\n        }\n        ')
        self.check('\n        for i in reversed(range(2, 10, 2)):\n            f()\n        ', '\n        for (i = (10) - 1; i >= 2; i -= 2) {\n          f();\n        }\n        ')

    def test_for_reversed_range_nonliteral(self):
        self.check('\n        for i in reversed(range(x(10))):\n            f()\n        ', '\n        i = x(10);\n        while (i--) {\n          f();\n        }\n        ')
        self.check('\n        for i in reversed(range(x(2), x(10))):\n            f()\n        ', '\n        var _$tmp1_end = x(2);\n        for (i = (x(10)) - 1; i >= _$tmp1_end; i--) {\n          f();\n        }\n        ')
        self.check('\n        for i in reversed(range(x(2), x(10), x(2))):\n            f()\n        ', '\n        var _$tmp1_end = x(2), _$tmp2_step = x(2);\n        for (i = (x(10)) - 1; i >= _$tmp1_end; i -= _$tmp2_step) {\n          f();\n        }\n        ')

    def test_for_in(self):
        self.check('\n        for i in x.y[10].z():\n            f(i)\n        ', '\n        var _$tmp1_data = _$rapyd$_iter(x.y[10].z());\n        var _$tmp2_len = _$tmp1_data.length;\n        for (var _$tmp3_index = 0; _$tmp3_index < _$tmp2_len; _$tmp3_index++) {\n          i = _$tmp1_data[_$tmp3_index];\n\n          f(i);\n        }\n        ')

    def test_one_liners(self):
        self.check('\n        def f(): pass\n        while True: pass\n        for i in reversed(range(10)): pass\n        ', '\n        f = function() {\n        };\n        while (true) {\n        }\n        i = 10;\n        while (i--) {\n        }\n        ')

    def test_simple_prototype(self):
        self.check("\n        x.prototype = {\n            'add': def(self, a, b, c):\n                return 1 + 2\n            ,\n        }\n        ", '\n        x.prototype = {\n          "add": (function(a, b, c) {\n            return (1 + 2);\n          })\n        };\n        ')

    def test_multi_line_lambda(self):
        self.check("\n        x.prototype = {\n            '__init__': def(self):\n                def nested():\n                    return None\n                a = 3\n                x = a + 3\n                return x\n            ,\n            'add': def(self, a, b, c):\n                return 1 + 2\n            ,\n        }\n        ", '\n        x.prototype = {\n          "__init__": (function() {\n            var a, nested, x;\n\n            nested = function() {\n              return null;\n            };\n\n            a = 3;\n            x = (a + 3);\n            return x;\n          }),\n          "add": (function(a, b, c) {\n            return (1 + 2);\n          })\n        };\n        ')

    def test_lambda_call(self):
        self.check('\n        (def():\n            global x\n            x = 5\n        )()\n        ', '\n        (function() {\n          x = 5;\n        })();\n        ')

    def test_self(self):
        self.check('\n        self.f()\n        ', '\n        self.f();\n        ')
        self.check('\n        def f():\n            self.f()\n        ', '\n        f = function() {\n          self.f();\n        };\n        ')
        self.check('\n        def f(self):\n            self.f()\n        ', '\n        f = function() {\n          this.f();\n        };\n        ')
        self.check('\n        def f(self):\n            myself = self\n            def g():\n                myself.f()\n        ', '\n        f = function() {\n          var g, myself;\n          myself = this;\n          g = function() {\n            myself.f();\n          };\n        };\n        ')


if __name__ == '__main__':
    unittest.main()