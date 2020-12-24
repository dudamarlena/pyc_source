# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/tests/test_mangler.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import textwrap, unittest
from slimit.parser import Parser
from slimit.mangler import mangle

class ManglerTestCase(unittest.TestCase):
    TEST_CASES = [
     ('\n        function test() {\n          function is_false() {\n            var xpos = 5;\n            var point = {\n              xpos: 17,\n              ypos: 10\n            };\n            return true;\n          }\n        }\n        ',
 '\n         function a() {\n           function a() {\n             var a = 5;\n             var b = {\n               xpos: 17,\n               ypos: 10\n             };\n             return true;\n           }\n         }\n         '),
     ("\n        var result = function() {\n          var long_name = 'long name';\n          var not_so_long = 'indeed', log = 5;\n          global_x = 56;\n          console.log(long_name + not_so_long);\n          new_result = function(arg1, arg2) {\n            var arg2 = 'qwerty';\n            console.log(long_name + not_so_long + arg1 + arg2 + global_x);\n          };\n        };\n        ",
 "\n         var a = function() {\n           var a = 'long name';\n           var b = 'indeed', c = 5;\n           global_x = 56;\n           console.log(a + b);\n           new_result = function(c, d) {\n             var d = 'qwerty';\n             console.log(a + b + c + d + global_x);\n           };\n         };\n         "),
     ("\n        function a() {\n          var $exc1 = null;\n          try {\n            lala();\n          } catch($exc) {\n            if ($exc.__name__ == 'hi') {\n              return 'bam';\n            }\n          }\n          return 'bum';\n        }\n        ",
 "\n         function a() {\n           var a = null;\n           try {\n             lala();\n           } catch (b) {\n             if (b.__name__ == 'hi') {\n               return 'bam';\n             }\n           }\n           return 'bum';\n         }\n         "),
     ('\n        function a(arg) {\n          arg = 9;\n          var arg = 0;\n          return arg;\n        }\n        ',
 '\n         function a(a) {\n           a = 9;\n           var a = 0;\n           return a;\n         }\n         ')]


def make_test_function(input, expected):

    def test_func(self):
        parser = Parser()
        tree = parser.parse(input)
        mangle(tree, toplevel=True)
        self.assertMultiLineEqual(textwrap.dedent(tree.to_ecma()).strip(), textwrap.dedent(expected).strip())

    return test_func


for index, (input, expected) in enumerate(ManglerTestCase.TEST_CASES):
    func = make_test_function(input, expected)
    setattr(ManglerTestCase, 'test_case_%d' % index, func)