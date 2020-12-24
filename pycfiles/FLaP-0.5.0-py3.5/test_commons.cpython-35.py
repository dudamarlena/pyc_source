# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tests\unit\latex\test_commons.py
# Compiled at: 2016-12-19 10:04:39
# Size of source mod 2**32: 3650 bytes
from unittest import TestCase, main
from unittest.mock import MagicMock
from flap.latex.commons import Stream, Position

class EmptyStreamTest(TestCase):

    def setUp(self):
        self._stream = Stream(iter([]))

    def test_reject_non_iterable_types(self):
        with self.assertRaises(AssertionError):
            Stream(34)

    def test_is_empty(self):
        self.assertTrue(self._stream.is_empty)

    def test_next_is_none(self):
        self.assertIsNone(self._stream.look_ahead())


class CharacterStreamTest(TestCase):

    def setUp(self):
        self._text = 'sample text'
        self._handler = MagicMock()
        self._stream = Stream(iter(self._text), self._handler)

    def test_returns_all_characters(self):
        self.assertEqual(self._text, ''.join(self._stream.take_all()))

    def test_triggers_handler(self):
        self._stream.take_all()
        self.assertEqual(len(self._text), self._handler.call_count)

    def test_look_ahead_does_not_trigger_handler(self):
        self._stream.look_ahead()
        self._handler.assert_not_called()


class ListStreamTest(TestCase):

    def setUp(self):
        self._text = 'sample text'
        self._handler = MagicMock()
        self._stream = Stream([c for c in self._text], self._handler)

    def test_returns_all_characters(self):
        self.assertEqual(self._text, ''.join(self._stream.take_all()))


class PositionTest(TestCase):

    def setUp(self):
        self._line = 1
        self._column = 4
        self._position = self._at(self._line, self._column)

    @staticmethod
    def _at(line, column):
        return Position(line, column)

    def test_next_line(self):
        self._verify(self._line + 1, 0, self._position.next_line())

    def _verify(self, line, column, position):
        self.assertEqual(line, position.line)
        self.assertEqual(column, position.column)

    def test_next_character(self):
        self._verify(self._line, self._column + 1, self._position.next_character())

    def test_equals_itself(self):
        self.assertEqual(self._position, self._position)

    def test_equals_an_equivalent_position(self):
        self.assertEqual(self._at(self._line, self._column), self._position)

    def test_differs_from_a_position_with_different_column(self):
        self.assertNotEqual(self._at(self._line, self._column + 1), self._position)

    def test_differs_from_a_position_with_different_line(self):
        self.assertNotEqual(self._at(self._line + 1, self._column), self._position)

    def test_differs_from_an_object_of_another_type(self):
        self.assertNotEqual(self._position, False)

    def test_representation(self):
        self.assertEqual(Position.REPRESENTATION.format(source=Position.UNKNOWN, line=self._line, column=self._column), str(self._position))


if __name__ == '__main__':
    main()