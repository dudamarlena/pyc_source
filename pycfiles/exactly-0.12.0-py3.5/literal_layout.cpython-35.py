# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/structure/literal_layout.py
# Compiled at: 2016-10-05 11:03:11
# Size of source mod 2**32: 293 bytes
from exactly_lib.util.textformat.structure.core import ParagraphItem

class LiteralLayout(ParagraphItem):

    def __init__(self, literal_text: str):
        self._literal_text = literal_text

    @property
    def literal_text(self) -> str:
        return self._literal_text