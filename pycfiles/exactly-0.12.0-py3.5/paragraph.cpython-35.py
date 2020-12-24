# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/structure/paragraph.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 530 bytes
from typing import List
from exactly_lib.util.textformat.structure.core import Text, ParagraphItem

class Paragraph(ParagraphItem):

    def __init__(self, start_on_new_line_blocks: List[Text]):
        """
        :param start_on_new_line_blocks: Each element is a text that should start
        on a new line.
        """
        self.start_on_new_line_blocks = start_on_new_line_blocks

    def __str__(self):
        return '{}({})'.format(str(type(self)), repr(self.start_on_new_line_blocks))