# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\test_parser.py
# Compiled at: 2008-11-19 12:15:17
import unittest, time, string, parser

class TestParsers(unittest.TestCase):

    def setUp(self):
        pass

    def test_character_set(self):
        """Test CharacterSet parser class."""
        self._test_multiple(parser.CharacterSet(string.letters), [
         (
          'abc', ['abc', 'ab', 'a'])], must_finish=False)
        self._test_multiple(parser.CharacterSet(string.letters, minimum=0), [
         (
          'abc', ['abc', 'ab', 'a', ''])], must_finish=False)
        self._test_multiple(parser.CharacterSet(string.letters, greedy=False), [
         (
          'abc', ['a', 'ab', 'abc'])], must_finish=False)
        self._test_multiple(parser.CharacterSet(string.letters, minimum=2, maximum=5), [
         (
          'abcdefg', ['abcd', 'abc', 'ab'])], must_finish=False)

    def test_repetition(self):
        """Test repetition parser class."""
        word = parser.CharacterSet(string.letters)
        whitespace = parser.CharacterSet(string.whitespace)
        p = parser.Repetition(parser.Alternative((word, whitespace)))
        input_output = (
         (
          'abc', ['abc']),
         (
          'abc abc', ['abc', ' ', 'abc']),
         (
          'abc abc\t\t\n   cba', ['abc', ' ', 'abc', '\t\t\n   ', 'cba']))
        self._test_single(p, input_output)

    def test_optional_greedy(self):
        """Test greedy setting of optional parser class."""
        input = 'abc'
        p = parser.Sequence([
         parser.Sequence([
          parser.String('a'),
          parser.Optional(parser.String('b'), greedy=False)]),
         parser.Sequence([
          parser.Optional(parser.String('b')),
          parser.String('c')])])
        expected_output_1 = [
         [
          'a', None], ['b', 'c']]
        expected_output_2 = [['a', 'b'], [None, 'c']]
        state = parser.State(input)
        print 'Parser:', p
        print 'State:', state
        generator = p.parse(state)
        generator.next()
        root = state.build_parse_tree()
        self.assertEqual(root.value(), expected_output_1)
        print 'Output 1:', expected_output_1
        generator.next()
        root = state.build_parse_tree()
        self.assertEqual(root.value(), expected_output_2)
        print 'Output 2:', expected_output_2
        return

    def _test_single(self, parser_element, input_output):
        p = parser.Parser(parser_element)
        print 'Parser:', parser_element
        for (input, output) in input_output:
            print 'Input:', input
            result = p.parse(input)
            print 'Expected: %r' % output
            print 'Result: %r' % result
            self.assertEqual(result, output)

    def _test_multiple(self, parser_element, input_outputs, must_finish=True):
        p = parser.Parser(parser_element)
        print 'Parser:', parser_element
        for (input, outputs) in input_outputs:
            print 'Input:', input
            results = p.parse_multiple(input, must_finish)
            self.assertEqual(len(results), len(outputs))
            for (index, result, output) in zip(xrange(len(results)), results, outputs):
                if isinstance(result, list):
                    result = tuple(result)
                if isinstance(output, list):
                    output = tuple(output)
                print 'Expected: %r' % output
                print 'Result %d: %r' % (index, result)
                self.assertEqual(result, output)


def main():
    try:
        unittest.main()
    except SystemExit, e:
        pass
    except Exception, e:
        import traceback
        traceback.print_exc()

    time.sleep(600)


if __name__ == '__main__':
    main()