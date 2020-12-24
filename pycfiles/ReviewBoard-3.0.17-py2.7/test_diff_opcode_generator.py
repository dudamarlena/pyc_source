# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_diff_opcode_generator.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import print_function, unicode_literals
import os
from reviewboard.diffviewer.myersdiff import MyersDiffer
from reviewboard.diffviewer.opcode_generator import get_diff_opcode_generator
from reviewboard.testing import TestCase

class IndentationTests(TestCase):
    """Unit tests for DiffOpcodeGenerator indentation highlighting."""

    def setUp(self):
        super(IndentationTests, self).setUp()
        self.generator = get_diff_opcode_generator(MyersDiffer(b'', b''))

    def test_indentation_with_spaces(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with indenting spaces
        """
        self.assertEqual(self.generator._compute_line_indentation(b'    foo', b'        foo'), (
         True, 4, 4))

    def test_indentation_with_tabs(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with indenting tabs
        """
        self.assertEqual(self.generator._compute_line_indentation(b'    foo', b'\t    foo'), (
         True, 1, 8))

    def test_indentation_with_spaces_and_tabs(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with indenting spaces and tabs
        """
        self.assertEqual(self.generator._compute_line_indentation(b'    foo', b'  \t    foo'), (
         True, 3, 8))

    def test_indentation_with_tabs_and_spaces(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with indenting tabs and spaces
        """
        self.assertEqual(self.generator._compute_line_indentation(b'    foo', b'\t      foo'), (
         True, 3, 10))

    def test_indentation_with_replacing_tabs_with_spaces(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with replacing tabs with spaces
        """
        self.assertEqual(self.generator._compute_line_indentation(b'\tfoo', b'        foo'), None)
        return

    def test_indentation_with_replacing_spaces_with_tabs(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with spaces with tabs
        """
        self.assertEqual(self.generator._compute_line_indentation(b'        foo', b'\tfoo'), None)
        return

    def test_indentation_with_no_changes(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        without changes
        """
        self.assertEqual(self.generator._compute_line_indentation(b'    foo', b'    foo'), None)
        return

    def test_unindentation_with_spaces(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with unindenting spaces
        """
        self.assertEqual(self.generator._compute_line_indentation(b'        foo', b'    foo'), (
         False, 4, 4))

    def test_unindentation_with_tabs(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with unindenting tabs
        """
        self.assertEqual(self.generator._compute_line_indentation(b'\t    foo', b'    foo'), (
         False, 1, 8))

    def test_unindentation_with_spaces_and_tabs(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with unindenting spaces and tabs
        """
        self.assertEqual(self.generator._compute_line_indentation(b'  \t    foo', b'    foo'), (
         False, 3, 8))

    def test_unindentation_with_tabs_and_spaces(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with unindenting tabs and spaces
        """
        self.assertEqual(self.generator._compute_line_indentation(b'\t      foo', b'    foo'), (
         False, 3, 10))

    def test_unindentation_with_replacing_tabs_with_spaces(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with replacing tabs with spaces
        """
        self.assertEqual(self.generator._compute_line_indentation(b'\tfoo', b'    foo'), (
         False, 1, 4))

    def test_unindentation_with_replacing_some_tabs_with_spaces(self):
        """Testing DiffOpcodeGenerator._calculate_indentation
        with replacing some tabs with spaces
        """
        self.assertEqual(self.generator._compute_line_indentation(b'\t\t\tfoo', b'\t        foo'), (
         False, 3, 8))


class MoveDetectionTests(TestCase):
    """Unit tests for DiffOpcodeGenerator move detection."""

    def test_move_detection(self):
        """Testing DiffOpcodeGenerator move detection"""
        old = b'/*\n *\n */\n// ----\n\n\n/*\n * Says hello\n */\nvoid\nsay_hello()\n{\n\tprintf("Hello world!\\n");\n}\n\n\nint\ndummy()\n{\n\tif (1) {\n\t\t// whatever\n\t}\n}\n\n\nvoid\nsay_goodbye()\n{\n\tprintf("Goodbye!\\n");\n}\n'
        new = b'// ----\n\n\nint\ndummy()\n{\n\tif (1) {\n\t\t// whatever\n\t}\n}\n\n\n/*\n * Says goodbye\n */\nvoid\nsay_goodbye()\n{\n\tprintf("Goodbye!\\n");\n}\n\n\nvoid\nsay_hello()\n{\n\tprintf("Hello world!\\n");\n}\n\n\n/*\n *\n */\n'
        self._test_move_detection(old.splitlines(), new.splitlines(), [
         {23: 10, 
            24: 11, 
            25: 12, 
            26: 13}], [
         {10: 23, 
            11: 24, 
            12: 25, 
            13: 26}])

    def test_move_detection_with_replace_lines(self):
        """Testing DiffOpcodeGenerator move detection with replace lines"""
        self._test_move_detection([
         b'this is line 1, and it is sufficiently long',
         b'-------------------------------------------',
         b'-------------------------------------------',
         b'this is line 2, and it is sufficiently long'], [
         b'this is line 2, and it is sufficiently long',
         b'-------------------------------------------',
         b'-------------------------------------------',
         b'this is line 1, and it is sufficiently long'], [{1: 4}, {4: 1}], [{1: 4}, {4: 1}])

    def test_move_detection_with_whitespace_replace_lines(self):
        """Testing DiffOpcodeGenerator move detection with whitespace-only
        changes on replace lines
        """
        self._test_move_detection([
         b'this is line 1, and it is sufficiently long',
         b'-------------------------------------------',
         b'-------------------------------------------',
         b'this is line 2, and it is sufficiently long  '], [
         b'  this is line 1, and it is sufficiently long',
         b'-------------------------------------------',
         b'-------------------------------------------',
         b'this is line 2, and it is sufficiently long'], [], [])

    def test_move_detection_with_last_line_in_range(self):
        """Testing DiffOpcodeGenerator move detection with last line in a
        range
        """
        self._test_move_detection([
         b'this line will be replaced',
         b'',
         b'foo bar blah blah',
         b'this is line 1, and it is sufficiently long',
         b''], [
         b'this is line 1, and it is sufficiently long',
         b'',
         b'foo bar blah blah',
         b''], [{1: 4}], [{4: 1}])

    def test_move_detection_with_adjacent_regions(self):
        """Testing DiffOpcodeGenerator move detection with adjacent regions"""
        self._test_move_detection([
         b'1. Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         b'2. Phasellus et lectus vulputate, dictum mi id, auctor ante.',
         b'3. Nulla accumsan tellus ut felis ultrices euismod.',
         b'4. Donec quis augue sed arcu tristique pellentesque.',
         b'5. Fusce rutrum diam vel viverra sagittis.',
         b'6. Nam tincidunt sapien vitae lorem vestibulum tempor.',
         b'7. Donec fermentum tortor ut egestas convallis.'], [
         b'6. Nam tincidunt sapien vitae lorem vestibulum tempor.',
         b'7. Donec fermentum tortor ut egestas convallis.',
         b'4. Donec quis augue sed arcu tristique pellentesque.',
         b'5. Fusce rutrum diam vel viverra sagittis.',
         b'1. Lorem ipsum dolor sit amet, consectetur adipiscing elit.',
         b'2. Phasellus et lectus vulputate, dictum mi id, auctor ante.',
         b'3. Nulla accumsan tellus ut felis ultrices euismod.'], [
         {1: 6, 
            2: 7, 
            3: 4, 
            4: 5}], [
         {4: 3, 
            5: 4, 
            6: 1, 
            7: 2}])

    def test_move_detection_spanning_chunks(self):
        """Testing DiffOpcodeGenerator move detection spanning left-hand-side
        chunks
        """
        self._test_move_detection([
         b'Unchanged line 1',
         b'Unchanged line 2',
         b'Unchanged line 3',
         b'Unchanged line 4',
         b'====',
         b'this is line 1, and it is sufficiently long',
         b'',
         b'this is line 2, and it is sufficiently long',
         b'this is line 3, and it is sufficiently long',
         b''], [
         b'this is line 1, and it is sufficiently long',
         b'',
         b'this is line 2, and it is sufficiently long',
         b'this is line 3, and it is sufficiently long',
         b'Unchanged line 1',
         b'Unchanged line 2',
         b'Unchanged line 3',
         b'Unchanged line 4',
         b'====',
         b'this is line X, and it is sufficiently long',
         b'',
         b''], [
         {1: 6, 
            2: 7, 
            3: 8, 
            4: 9}], [
         {6: 1, 
            7: 2, 
            8: 3, 
            9: 4},
         {6: 1, 
            7: 2, 
            8: 3, 
            9: 4},
         {6: 1, 
            7: 2, 
            8: 3, 
            9: 4}])

    def test_move_detection_single_line_thresholds(self):
        """Testing DiffOpcodeGenerator move detection with a single line and
        line length threshold
        """
        self._test_move_detection([
         b'0123456789012345678',
         b'----',
         b'----',
         b'abcdefghijklmnopqrst'], [
         b'abcdefghijklmnopqrst',
         b'----',
         b'----',
         b'0123456789012345678'], [{1: 4}], [{4: 1}])

    def test_move_detection_multi_line_thresholds(self):
        """Testing DiffOpcodeGenerator move detection with a multiple lines and
        line count threshold
        """
        self._test_move_detection([
         b'123',
         b'456',
         b'789',
         b'ten',
         b'abcdefghijk',
         b'lmno',
         b'pqr'], [
         b'abcdefghijk',
         b'lmno',
         b'pqr',
         b'123',
         b'456',
         b'789',
         b'ten'], [
         {1: 5, 
            2: 6}], [
         {5: 1, 
            6: 2}])

    def test_move_detection_similar_blocks(self):
        """Testing DiffOpcodeGenerator move detection with multiple blocks of
        similar moved lines
        """
        testdata_path = os.path.abspath(os.path.join(__file__, b'..', b'..', b'testdata', b'move_detection'))
        with open(os.path.join(testdata_path, b'bug-4371-old.js'), b'r') as (fp):
            old = fp.readlines()
        with open(os.path.join(testdata_path, b'bug-4371-new.js'), b'r') as (fp):
            new = fp.readlines()
        self._test_move_detection(old, new, [
         {2633: 16, 
            2634: 17, 
            2635: 18, 
            2636: 19, 
            2637: 20, 
            2638: 21, 
            2639: 22, 
            2640: 23, 
            2642: 24, 
            2643: 25, 
            2644: 26, 
            2645: 27, 
            2646: 28, 
            2649: 31, 
            2650: 32, 
            2651: 33, 
            2652: 34, 
            2653: 35, 
            2654: 36, 
            2655: 37, 
            2656: 38, 
            2657: 39, 
            2658: 40, 
            2659: 41, 
            2660: 42, 
            2661: 43, 
            2662: 44, 
            2663: 45, 
            2664: 46, 
            2665: 47}], [
         {16: 2633, 
            17: 2634, 
            18: 2635, 
            19: 2636, 
            20: 2637, 
            21: 2638, 
            22: 2639, 
            23: 2640, 
            24: 2642, 
            25: 2643, 
            26: 2644, 
            27: 2645, 
            28: 2646, 
            31: 2649, 
            32: 2650, 
            33: 2651, 
            34: 2652, 
            35: 2653, 
            36: 2654, 
            37: 2655, 
            38: 2656, 
            39: 2657, 
            40: 2658, 
            41: 2659, 
            42: 2660, 
            43: 2661, 
            44: 2662, 
            45: 2663, 
            46: 2664, 
            47: 2665}])

    def test_move_detection_with_multiple_replace_candidates(self):
        """Testing DiffOpcodeGenerator move detection with multiple candidates
        for a replace line
        """
        self._test_move_detection([
         b'if 1:',
         b'    print "hi"',
         b'else:',
         b'    print "bye"',
         b'#',
         b'#',
         b'else:',
         b'    print "?"',
         b'#',
         b'#'], [
         b'if 0:',
         b'    print False',
         b'#',
         b'#',
         b'#',
         b'#',
         b'if 1:',
         b'    print "hi"',
         b'else:',
         b'    print "bye"'], [
         {7: 1, 
            8: 2, 
            9: 3, 
            10: 4}], [
         {1: 7, 
            2: 8, 
            3: 9, 
            4: 10},
         {1: 7, 
            2: 8, 
            3: 9, 
            4: 10}])

    def test_move_detection_with_multiple_replace_candidates_2(self):
        """Testing DiffOpcodeGenerator move detection with multiple candidates
        for a replace line
        """
        self._test_move_detection([
         b'if 1:',
         b'    print "hi"',
         b'else:',
         b'    print "bye"',
         b'= equal',
         b'for a in b:',
         b'    continue',
         b'else:',
         b'    assert False',
         b'=',
         b'= abc',
         b'= defg',
         b'= hijkl',
         b'= mnop',
         b'= qrs',
         b'= tuvw',
         b'= xyz',
         b'===='], [
         b'= equal',
         b'=',
         b'= abc',
         b'= defg',
         b'= hijkl',
         b'= mnop',
         b'= qrs',
         b'= tuvw',
         b'= xyz',
         b'if 1:',
         b'    print "hi"',
         b'else:',
         b'    print "bye"',
         b'====',
         b'for a in b:',
         b'    continue',
         b'else:',
         b'    assert False'], [
         {10: 1, 
            11: 2, 
            12: 3, 
            13: 4},
         {15: 6, 
            16: 7, 
            17: 8, 
            18: 9}], [
         {1: 10, 
            2: 11, 
            3: 12, 
            4: 13},
         {6: 15, 
            7: 16, 
            8: 17, 
            9: 18}])

    def _test_move_detection(self, a, b, expected_i_moves, expected_r_moves):
        differ = MyersDiffer(a, b)
        opcode_generator = get_diff_opcode_generator(differ)
        r_moves = []
        i_moves = []
        for opcodes in opcode_generator:
            print(opcodes)
            meta = opcodes[(-1)]
            try:
                r_moves.append(meta[b'moved-to'])
            except KeyError:
                pass

            try:
                i_moves.append(meta[b'moved-from'])
            except KeyError:
                pass

        self.assertEqual(i_moves, expected_i_moves)
        self.assertEqual(r_moves, expected_r_moves)