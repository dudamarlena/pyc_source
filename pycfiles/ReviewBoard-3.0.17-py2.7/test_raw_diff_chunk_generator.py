# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_raw_diff_chunk_generator.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.diffviewer.chunk_generator import RawDiffChunkGenerator
from reviewboard.testing import TestCase

class RawDiffChunkGeneratorTests(TestCase):
    """Unit tests for RawDiffChunkGenerator."""

    @property
    def generator(self):
        """Create a dummy generator for tests that need it.

        This generator will be void of any content. It's intended for
        use in tests that need to operate on its utility functions.
        """
        return RawDiffChunkGenerator(b'', b'', b'', b'')

    def test_get_chunks(self):
        """Testing RawDiffChunkGenerator.get_chunks"""
        old = b'This is line 1\nAnother line\nLine 3.\nla de da.\n'
        new = b'This is line 1\nLine 3.\nla de doo.\n'
        generator = RawDiffChunkGenerator(old, new, b'file1', b'file2')
        chunks = list(generator.get_chunks())
        self.assertEqual(len(chunks), 4)
        self.assertEqual(chunks[0][b'change'], b'equal')
        self.assertEqual(chunks[1][b'change'], b'delete')
        self.assertEqual(chunks[2][b'change'], b'equal')
        self.assertEqual(chunks[3][b'change'], b'replace')

    def test_get_move_info_with_new_range_no_preceding(self):
        """Testing RawDiffChunkGenerator._get_move_info with new move range and
        no adjacent preceding move range
        """
        generator = RawDiffChunkGenerator([], [], b'file1', b'file2')
        self.assertEqual(generator._get_move_info(10, {8: 100, 
           10: 200, 
           11: 201}), (
         200, True))

    def test_get_move_info_with_new_range_preceding(self):
        """Testing RawDiffChunkGenerator._get_move_info with new move range and
        adjacent preceding move range
        """
        generator = RawDiffChunkGenerator([], [], b'file1', b'file2')
        self.assertEqual(generator._get_move_info(10, {8: 100, 
           9: 101, 
           10: 200, 
           11: 201}), (
         200, True))

    def test_get_move_info_with_existing_range(self):
        """Testing RawDiffChunkGenerator._get_move_info with existing move
        range
        """
        generator = RawDiffChunkGenerator([], [], b'file1', b'file2')
        self.assertEqual(generator._get_move_info(11, {8: 100, 
           9: 101, 
           10: 200, 
           11: 201}), (
         201, False))

    def test_get_move_info_with_no_move(self):
        """Testing RawDiffChunkGenerator._get_move_info with no move range"""
        generator = RawDiffChunkGenerator([], [], b'file1', b'file2')
        self.assertIsNone(generator._get_move_info(500, {8: 100, 
           9: 101, 
           10: 200, 
           11: 201}))

    def test_indent_spaces(self):
        """Testing RawDiffChunkGenerator._serialize_indentation with spaces"""
        self.assertEqual(self.generator._serialize_indentation(b'    ', 4), ('&gt;&gt;&gt;&gt;',
                                                                             ''))

    def test_indent_tabs(self):
        """Testing RawDiffChunkGenerator._serialize_indentation with tabs"""
        self.assertEqual(self.generator._serialize_indentation(b'\t', 8), ('&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&gt;|',
                                                                           ''))

    def test_indent_spaces_and_tabs(self):
        """Testing RawDiffChunkGenerator._serialize_indentation
        with spaces and tabs
        """
        self.assertEqual(self.generator._serialize_indentation(b'   \t', 8), ('&gt;&gt;&gt;&mdash;&mdash;&mdash;&gt;|',
                                                                              ''))

    def test_indent_tabs_and_spaces(self):
        """Testing RawDiffChunkGenerator._serialize_indentation
        with tabs and spaces
        """
        self.assertEqual(self.generator._serialize_indentation(b'\t   ', 11), ('&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&gt;|&gt;&gt;&gt;',
                                                                               ''))

    def test_indent_9_spaces_and_tab(self):
        """Testing RawDiffChunkGenerator._serialize_indentation
        with 9 spaces and tab
        """
        self.assertEqual(self.generator._serialize_indentation(b'       \t', 8), ('&gt;&gt;&gt;&gt;&gt;&gt;&gt;|',
                                                                                  ''))

    def test_indent_8_spaces_and_tab(self):
        """Testing RawDiffChunkGenerator._serialize_indentation
        with 8 spaces and tab
        """
        self.assertEqual(self.generator._serialize_indentation(b'      \t', 8), ('&gt;&gt;&gt;&gt;&gt;&gt;&gt;|',
                                                                                 ''))

    def test_indent_7_spaces_and_tab(self):
        """Testing RawDiffChunkGenerator._serialize_indentation
        with 7 spaces and tab
        """
        self.assertEqual(self.generator._serialize_indentation(b'     \t', 8), ('&gt;&gt;&gt;&gt;&gt;&mdash;&gt;|',
                                                                                ''))

    def test_unindent_spaces(self):
        """Testing RawDiffChunkGenerator._serialize_unindentation with spaces
        """
        self.assertEqual(self.generator._serialize_unindentation(b'    ', 4), ('&lt;&lt;&lt;&lt;',
                                                                               ''))

    def test_unindent_tabs(self):
        """Testing RawDiffChunkGenerator._serialize_unindentation with tabs"""
        self.assertEqual(self.generator._serialize_unindentation(b'\t', 8), ('|&lt;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;',
                                                                             ''))

    def test_unindent_spaces_and_tabs(self):
        """Testing RawDiffChunkGenerator._serialize_unindentation
        with spaces and tabs
        """
        self.assertEqual(self.generator._serialize_unindentation(b'   \t', 8), ('&lt;&lt;&lt;|&lt;&mdash;&mdash;&mdash;',
                                                                                ''))

    def test_unindent_tabs_and_spaces(self):
        """Testing RawDiffChunkGenerator._serialize_unindentation
        with tabs and spaces
        """
        self.assertEqual(self.generator._serialize_unindentation(b'\t   ', 11), ('|&lt;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;&lt;&lt;&lt;',
                                                                                 ''))

    def test_unindent_9_spaces_and_tab(self):
        """Testing RawDiffChunkGenerator._serialize_unindentation
        with 9 spaces and tab
        """
        self.assertEqual(self.generator._serialize_unindentation(b'       \t', 8), ('&lt;&lt;&lt;&lt;&lt;&lt;&lt;|',
                                                                                    ''))

    def test_unindent_8_spaces_and_tab(self):
        """Testing RawDiffChunkGenerator._serialize_unindentation
        with 8 spaces and tab
        """
        self.assertEqual(self.generator._serialize_unindentation(b'      \t', 8), ('&lt;&lt;&lt;&lt;&lt;&lt;|&lt;',
                                                                                   ''))

    def test_unindent_7_spaces_and_tab(self):
        """Testing RawDiffChunkGenerator._serialize_unindentation
        with 7 spaces and tab
        """
        self.assertEqual(self.generator._serialize_unindentation(b'     \t', 8), ('&lt;&lt;&lt;&lt;&lt;|&lt;&mdash;',
                                                                                  ''))

    def test_highlight_indent(self):
        """Testing RawDiffChunkGenerator._highlight_indentation
        with indentation
        """
        self.assertEqual(self.generator._highlight_indentation(b'', b'        foo', True, 4, 4), ('',
                                                                                                  '<span class="indent">&gt;&gt;&gt;&gt;</span>    foo'))

    def test_highlight_indent_with_adjacent_tag(self):
        """Testing RawDiffChunkGenerator._highlight_indentation
        with indentation and adjacent tag wrapping whitespace
        """
        self.assertEqual(self.generator._highlight_indentation(b'', b'<span class="s"> </span>foo', True, 1, 1), ('',
                                                                                                                  '<span class="s"><span class="indent">&gt;</span></span>foo'))

    def test_highlight_indent_with_unexpected_chars(self):
        """Testing RawDiffChunkGenerator._highlight_indentation
        with indentation and unexpected markup chars
        """
        self.assertEqual(self.generator._highlight_indentation(b'', b' <span>  </span> foo', True, 4, 2), ('',
                                                                                                           ' <span>  </span> foo'))

    def test_highlight_unindent(self):
        """Testing RawDiffChunkGenerator._highlight_indentation
        with unindentation
        """
        self.assertEqual(self.generator._highlight_indentation(b'        foo', b'', False, 4, 4), ('<span class="unindent">&lt;&lt;&lt;&lt;</span>    foo',
                                                                                                   ''))

    def test_highlight_unindent_with_adjacent_tag(self):
        """Testing RawDiffChunkGenerator._highlight_indentation
        with unindentation and adjacent tag wrapping whitespace
        """
        self.assertEqual(self.generator._highlight_indentation(b'<span class="s"> </span>foo', b'', False, 1, 1), ('<span class="s"><span class="unindent">&lt;</span></span>foo',
                                                                                                                   ''))

    def test_highlight_unindent_with_unexpected_chars(self):
        """Testing RawDiffChunkGenerator._highlight_indentation
        with unindentation and unexpected markup chars
        """
        self.assertEqual(self.generator._highlight_indentation(b' <span>  </span> foo', b'', False, 4, 2), (' <span>  </span> foo',
                                                                                                            ''))

    def test_highlight_unindent_with_replacing_last_tab_with_spaces(self):
        """Testing RawDiffChunkGenerator._highlight_indentation
        with unindentation and replacing last tab with spaces
        """
        self.assertEqual(self.generator._highlight_indentation(b'<span>\t\t        </span> foo', b'', False, 2, 16), ('<span><span class="unindent">|&lt;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;|&lt;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;</span>        </span> foo',
                                                                                                                      ''))

    def test_highlight_unindent_with_replacing_3_tabs_with_tab_spaces(self):
        """Testing RawDiffChunkGenerator._highlight_indentation
        with unindentation and replacing 3 tabs with 1 tab and 8 spaces
        """
        self.assertEqual(self.generator._highlight_indentation(b'<span>\t        </span> foo', b'', False, 1, 24), ('<span><span class="unindent">|&lt;&mdash;&mdash;&mdash;&mdash;&mdash;&mdash;</span>        </span> foo',
                                                                                                                    ''))