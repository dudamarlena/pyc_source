# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/rendering/text/text.py
# Compiled at: 2017-12-07 08:04:08
# Size of source mod 2**32: 778 bytes
from exactly_lib.util.textformat.structure import core

class CrossReferenceFormatter:

    def apply(self, cross_reference: core.CrossReferenceText) -> str:
        raise NotImplementedError()


class TextFormatter(core.TextVisitor):

    def __init__(self, cross_reference_formatter: CrossReferenceFormatter):
        self._cross_reference_formatter = cross_reference_formatter

    def apply(self, text: core.Text) -> str:
        return self.visit(text)

    def visit_cross_reference(self, text: core.CrossReferenceText):
        return self._cross_reference_formatter.apply(text)

    def visit_anchor(self, text: core.AnchorText):
        return self.apply(text.anchored_text)

    def visit_string(self, text: core.StringText):
        return text.value