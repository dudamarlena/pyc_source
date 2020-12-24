# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/slimit/slimit/tests/test_lexer.py
# Compiled at: 2018-07-11 18:15:31
__author__ = 'Ruslan Spivak <ruslan.spivak@gmail.com>'
import doctest, unittest, difflib, pprint
from slimit.lexer import Lexer

class LexerTestCase(unittest.TestCase):

    def _get_lexer(self):
        lexer = Lexer()
        return lexer

    def assertListEqual(self, first, second):
        """Assert that two lists are equal.

        Prints differences on error.
        This method is similar to that of Python 2.7 'assertListEqual'
        """
        if first != second:
            message = ('\n').join(difflib.ndiff(pprint.pformat(first).splitlines(), pprint.pformat(second).splitlines()))
            self.fail('Lists differ:\n' + message)

    def test_illegal_unicode_char_in_identifier(self):
        lexer = self._get_lexer()
        lexer.input('6_tail')
        token = lexer.token()
        self.assertEqual(token.type, 'NUMBER')
        self.assertEqual(token.value, '6')

    TEST_CASES = [
     (
      'i my_variable_name c17 _dummy $str $ _ CamelCase class2type',
      [
       'ID i', 'ID my_variable_name', 'ID c17', 'ID _dummy',
       'ID $str', 'ID $', 'ID _', 'ID CamelCase', 'ID class2type']),
     (
      'π π_tail var꙼',
      [
       'ID π', 'ID π_tail', 'ID var꙼']),
     (
      'nullify truelie falsepositive',
      [
       'ID nullify', 'ID truelie', 'ID falsepositive']),
     (
      (' ').join(kw.lower() for kw in Lexer.keywords), [ '%s %s' % (kw, kw.lower()) for kw in Lexer.keywords ]),
     (
      'break Break BREAK', ['BREAK break', 'ID Break', 'ID BREAK']),
     (
      'null true false Null True False',
      [
       'NULL null', 'TRUE true', 'FALSE false',
       'ID Null', 'ID True', 'ID False']),
     (
      'a /= b', ['ID a', 'DIVEQUAL /=', 'ID b']),
     (
      '= == != === !== < > <= >= || && ++ -- << >> >>> += -= *= <<= >>= >>>= &= %= ^= |=',
      [
       'EQ =', 'EQEQ ==', 'NE !=', 'STREQ ===', 'STRNEQ !==', 'LT <',
       'GT >', 'LE <=', 'GE >=', 'OR ||', 'AND &&', 'PLUSPLUS ++',
       'MINUSMINUS --', 'LSHIFT <<', 'RSHIFT >>', 'URSHIFT >>>',
       'PLUSEQUAL +=', 'MINUSEQUAL -=', 'MULTEQUAL *=', 'LSHIFTEQUAL <<=',
       'RSHIFTEQUAL >>=', 'URSHIFTEQUAL >>>=', 'ANDEQUAL &=', 'MODEQUAL %=',
       'XOREQUAL ^=', 'OREQUAL |=']),
     (
      '. , ; : + - * % & | ^ ~ ? ! ( ) { } [ ]',
      [
       'PERIOD .', 'COMMA ,', 'SEMI ;', 'COLON :', 'PLUS +', 'MINUS -',
       'MULT *', 'MOD %', 'BAND &', 'BOR |', 'BXOR ^', 'BNOT ~',
       'CONDOP ?', 'NOT !', 'LPAREN (', 'RPAREN )', 'LBRACE {', 'RBRACE }',
       'LBRACKET [', 'RBRACKET ]']),
     (
      'a / b', ['ID a', 'DIV /', 'ID b']),
     (
      '3 3.3 0 0. 0.0 0.001 010 3.e2 3.e-2 3.e+2 3E2 3E+2 3E-2 0.5e2 0.5e+2 0.5e-2 33 128.15 0x001 0X12ABCDEF 0xabcdef',
      [
       'NUMBER 3', 'NUMBER 3.3', 'NUMBER 0', 'NUMBER 0.', 'NUMBER 0.0',
       'NUMBER 0.001', 'NUMBER 010', 'NUMBER 3.e2', 'NUMBER 3.e-2',
       'NUMBER 3.e+2', 'NUMBER 3E2', 'NUMBER 3E+2', 'NUMBER 3E-2',
       'NUMBER 0.5e2', 'NUMBER 0.5e+2', 'NUMBER 0.5e-2', 'NUMBER 33',
       'NUMBER 128.15', 'NUMBER 0x001', 'NUMBER 0X12ABCDEF',
       'NUMBER 0xabcdef']),
     (
      ' \'"\' ', ['STRING \'"\'']),
     (
      '"foo" \'foo\' "x\\";" \'x\\\';\' "foo\\tbar"',
      [
       'STRING "foo"', "STRING 'foo'", 'STRING "x\\";"',
       "STRING 'x\\';'", 'STRING "foo\\tbar"']),
     (
      '\'\\x55\' "\\x12ABCDEF" \'!@#$%^&*()_+{}[]\\";?\'',
      [
       "STRING '\\x55'", 'STRING "\\x12ABCDEF"',
       'STRING \'!@#$%^&*()_+{}[]\\";?\'']),
     (
      '\'\\u0001\' "\\uFCEF" \'a\\\\\\b\\n\'',
      [
       "STRING '\\u0001'", 'STRING "\\uFCEF"', "STRING 'a\\\\\\b\\n'"]),
     (
      '"тест строки\\""', ['STRING "тест строки\\""']),
     (
      "var tagRegExp = new RegExp('<(\\/*)(FooBar)', 'gi');",
      [
       'VAR var', 'ID tagRegExp', 'EQ =',
       'NEW new', 'ID RegExp', 'LPAREN (',
       "STRING '<(\\/*)(FooBar)'", 'COMMA ,', "STRING 'gi'",
       'RPAREN )', 'SEMI ;']),
     (
      '"<(\\/*)(FooBar)"', ['STRING "<(\\/*)(FooBar)"']),
     (
      "var a = 'hello \\\nworld'",
      [
       'VAR var', 'ID a', 'EQ =', "STRING 'hello world'"]),
     (
      'var a = "hello \\\nworld"',
      [
       'VAR var', 'ID a', 'EQ =', 'STRING "hello world"']),
     (
      'a=/a*/,1', ['ID a', 'EQ =', 'REGEX /a*/', 'COMMA ,', 'NUMBER 1']),
     (
      'a=/a*[^/]+/,1',
      [
       'ID a', 'EQ =', 'REGEX /a*[^/]+/', 'COMMA ,', 'NUMBER 1']),
     (
      'a=/a*\\[^/,1',
      [
       'ID a', 'EQ =', 'REGEX /a*\\[^/', 'COMMA ,', 'NUMBER 1']),
     (
      'a=/\\//,1', ['ID a', 'EQ =', 'REGEX /\\//', 'COMMA ,', 'NUMBER 1']),
     (
      'x = this / y;',
      [
       'ID x', 'EQ =', 'THIS this', 'DIV /', 'ID y', 'SEMI ;']),
     (
      'for (var x = a in foo && "</x>" || mot ? z:/x:3;x<5;y</g/i) {xyz(x++);}',
      [
       'FOR for', 'LPAREN (', 'VAR var', 'ID x', 'EQ =', 'ID a', 'IN in',
       'ID foo', 'AND &&', 'STRING "</x>"', 'OR ||', 'ID mot', 'CONDOP ?',
       'ID z', 'COLON :', 'REGEX /x:3;x<5;y</g', 'DIV /', 'ID i', 'RPAREN )',
       'LBRACE {', 'ID xyz', 'LPAREN (', 'ID x', 'PLUSPLUS ++', 'RPAREN )',
       'SEMI ;', 'RBRACE }']),
     (
      'for (var x = a in foo && "</x>" || mot ? z/x:3;x<5;y</g/i) {xyz(x++);}',
      [
       'FOR for', 'LPAREN (', 'VAR var', 'ID x', 'EQ =', 'ID a', 'IN in',
       'ID foo', 'AND &&', 'STRING "</x>"', 'OR ||', 'ID mot', 'CONDOP ?',
       'ID z', 'DIV /', 'ID x', 'COLON :', 'NUMBER 3', 'SEMI ;', 'ID x',
       'LT <', 'NUMBER 5', 'SEMI ;', 'ID y', 'LT <', 'REGEX /g/i',
       'RPAREN )', 'LBRACE {', 'ID xyz', 'LPAREN (', 'ID x', 'PLUSPLUS ++',
       'RPAREN )', 'SEMI ;', 'RBRACE }']),
     (
      '/????/, /++++/, /[----]/ ',
      [
       'REGEX /????/', 'COMMA ,',
       'REGEX /++++/', 'COMMA ,', 'REGEX /[----]/']),
     (
      '/\\[/', ['REGEX /\\[/']),
     (
      '/[i]/', ['REGEX /[i]/']),
     (
      '/[\\]]/', ['REGEX /[\\]]/']),
     (
      '/a[\\]]/', ['REGEX /a[\\]]/']),
     (
      '/a[\\]]b/', ['REGEX /a[\\]]b/']),
     (
      '/[\\]/]/gi', ['REGEX /[\\]/]/gi']),
     (
      '/\\[[^\\]]+\\]/gi', ['REGEX /\\[[^\\]]+\\]/gi']),
     (
      '\n            rexl.re = {\n            NAME: /^(?!\\d)(?:\\w)+|^"(?:[^"]|"")+"/,\n            UNQUOTED_LITERAL: /^@(?:(?!\\d)(?:\\w|\\:)+|^"(?:[^"]|"")+")\\[[^\\]]+\\]/,\n            QUOTED_LITERAL: /^\'(?:[^\']|\'\')*\'/,\n            NUMERIC_LITERAL: /^[0-9]+(?:\\.[0-9]*(?:[eE][-+][0-9]+)?)?/,\n            SYMBOL: /^(?:==|=|<>|<=|<|>=|>|!~~|!~|~~|~|!==|!=|!~=|!~|!|&|\\||\\.|\\:|,|\\(|\\)|\\[|\\]|\\{|\\}|\\?|\\:|;|@|\\^|\\/\\+|\\/|\\*|\\+|-)/\n            };\n            ',
      [
       'ID rexl', 'PERIOD .', 'ID re', 'EQ =', 'LBRACE {',
       'ID NAME', 'COLON :',
       'REGEX /^(?!\\d)(?:\\w)+|^"(?:[^"]|"")+"/', 'COMMA ,',
       'ID UNQUOTED_LITERAL', 'COLON :',
       'REGEX /^@(?:(?!\\d)(?:\\w|\\:)+|^"(?:[^"]|"")+")\\[[^\\]]+\\]/',
       'COMMA ,', 'ID QUOTED_LITERAL', 'COLON :',
       "REGEX /^'(?:[^']|'')*'/", 'COMMA ,', 'ID NUMERIC_LITERAL',
       'COLON :',
       'REGEX /^[0-9]+(?:\\.[0-9]*(?:[eE][-+][0-9]+)?)?/', 'COMMA ,',
       'ID SYMBOL', 'COLON :',
       'REGEX /^(?:==|=|<>|<=|<|>=|>|!~~|!~|~~|~|!==|!=|!~=|!~|!|&|\\||\\.|\\:|,|\\(|\\)|\\[|\\]|\\{|\\}|\\?|\\:|;|@|\\^|\\/\\+|\\/|\\*|\\+|-)/',
       'RBRACE }', 'SEMI ;']),
     (
      '\n            rexl.re = {\n            NAME: /^(?!\\d)(?:\\w)+|^"(?:[^"]|"")+"/,\n            UNQUOTED_LITERAL: /^@(?:(?!\\d)(?:\\w|\\:)+|^"(?:[^"]|"")+")\\[[^\\]]+\\]/,\n            QUOTED_LITERAL: /^\'(?:[^\']|\'\')*\'/,\n            NUMERIC_LITERAL: /^[0-9]+(?:\\.[0-9]*(?:[eE][-+][0-9]+)?)?/,\n            SYMBOL: /^(?:==|=|<>|<=|<|>=|>|!~~|!~|~~|~|!==|!=|!~=|!~|!|&|\\||\\.|\\:|,|\\(|\\)|\\[|\\]|\\{|\\}|\\?|\\:|;|@|\\^|\\/\\+|\\/|\\*|\\+|-)/\n            };\n            str = \'"\';\n        ',
      [
       'ID rexl', 'PERIOD .', 'ID re', 'EQ =', 'LBRACE {',
       'ID NAME', 'COLON :', 'REGEX /^(?!\\d)(?:\\w)+|^"(?:[^"]|"")+"/',
       'COMMA ,', 'ID UNQUOTED_LITERAL', 'COLON :',
       'REGEX /^@(?:(?!\\d)(?:\\w|\\:)+|^"(?:[^"]|"")+")\\[[^\\]]+\\]/',
       'COMMA ,', 'ID QUOTED_LITERAL', 'COLON :',
       "REGEX /^'(?:[^']|'')*'/", 'COMMA ,',
       'ID NUMERIC_LITERAL', 'COLON :',
       'REGEX /^[0-9]+(?:\\.[0-9]*(?:[eE][-+][0-9]+)?)?/', 'COMMA ,',
       'ID SYMBOL', 'COLON :',
       'REGEX /^(?:==|=|<>|<=|<|>=|>|!~~|!~|~~|~|!==|!=|!~=|!~|!|&|\\||\\.|\\:|,|\\(|\\)|\\[|\\]|\\{|\\}|\\?|\\:|;|@|\\^|\\/\\+|\\/|\\*|\\+|-)/',
       'RBRACE }', 'SEMI ;',
       'ID str', 'EQ =', 'STRING \'"\'', 'SEMI ;']),
     (
      ' this._js = "e.str(\\"" + this.value.replace(/\\\\/g, "\\\\\\\\").replace(/"/g, "\\\\\\"") + "\\")"; ',
      [
       'THIS this', 'PERIOD .', 'ID _js', 'EQ =',
       'STRING "e.str(\\""', 'PLUS +', 'THIS this', 'PERIOD .',
       'ID value', 'PERIOD .', 'ID replace', 'LPAREN (', 'REGEX /\\\\/g',
       'COMMA ,', 'STRING "\\\\\\\\"', 'RPAREN )', 'PERIOD .', 'ID replace',
       'LPAREN (', 'REGEX /"/g', 'COMMA ,', 'STRING "\\\\\\""', 'RPAREN )',
       'PLUS +', 'STRING "\\")"', 'SEMI ;'])]


def make_test_function(input, expected):

    def test_func(self):
        lexer = self._get_lexer()
        lexer.input(input)
        result = [ '%s %s' % (token.type, token.value) for token in lexer ]
        self.assertListEqual(result, expected)

    return test_func


for index, (input, expected) in enumerate(LexerTestCase.TEST_CASES):
    func = make_test_function(input, expected)
    setattr(LexerTestCase, 'test_case_%d' % index, func)

def test_suite():
    return unittest.TestSuite((
     unittest.makeSuite(LexerTestCase),
     doctest.DocFileSuite('../lexer.py', optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS)))