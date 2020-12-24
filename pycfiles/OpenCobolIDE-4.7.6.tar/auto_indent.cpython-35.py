# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/colin/Projects/pyqode.cobol/pyqode/cobol/modes/auto_indent.py
# Compiled at: 2016-12-29 05:32:02
# Size of source mod 2**32: 1621 bytes
"""
This module contains a cobol specific auto indenter mode.
"""
from pyqode.core.api import TextHelper
from pyqode.core.modes import AutoIndentMode
from pyqode.cobol.api import regex, keywords

class CobolAutoIndentMode(AutoIndentMode):
    __doc__ = '\n    Implements a smarter (regex based) automatic indentater.\n\n    Automatic indentation is triggered when the user press enter. The base\n    implementation is to use the previous line indentation. This works fine\n    in most situations but there are cases where the indenter could\n    automatically increase indentation (e.g. after an if statement or a\n    loop,...). This is what this mode do.\n\n    '

    def _get_indent(self, cursor):
        prev_line_text = TextHelper(self.editor).current_line_text()
        if not self.editor.free_format:
            prev_line_text = '       ' + prev_line_text[7:]
        diff = len(prev_line_text) - len(prev_line_text.lstrip())
        post_indent = ' ' * diff
        min_column = self.editor.indenter_mode.min_column
        if len(post_indent) < min_column:
            post_indent = min_column * ' '
        text = cursor.block().text().upper()
        patterns = [
         regex.PARAGRAPH_PATTERN,
         regex.STRUCT_PATTERN,
         regex.BRANCH_START,
         regex.LOOP_PATTERN]
        for ptrn in patterns:
            if ptrn.indexIn(text) != -1:
                post_indent += self.editor.tab_length * ' '
                return ('', post_indent)

        return (
         '', post_indent)