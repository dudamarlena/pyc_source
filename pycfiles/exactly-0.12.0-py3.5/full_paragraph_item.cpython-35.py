# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/rendering/html/paragraph_item/full_paragraph_item.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 2364 bytes
from xml.etree.ElementTree import Element
from exactly_lib.util.textformat.rendering.html import text
from exactly_lib.util.textformat.rendering.html.paragraph_item import lists as list_rendering
from exactly_lib.util.textformat.rendering.html.paragraph_item import literal_layout
from exactly_lib.util.textformat.rendering.html.paragraph_item import paragraph
from exactly_lib.util.textformat.rendering.html.paragraph_item import table as table_rendering
from exactly_lib.util.textformat.rendering.html.paragraph_item.interfaces import ParagraphItemRenderer
from exactly_lib.util.textformat.structure import lists
from exactly_lib.util.textformat.structure.core import ParagraphItem
from exactly_lib.util.textformat.structure.literal_layout import LiteralLayout
from exactly_lib.util.textformat.structure.paragraph import Paragraph
from exactly_lib.util.textformat.structure.table import Table

class FullParagraphItemRenderer(ParagraphItemRenderer):

    def __init__(self, text_renderer: text.TextRenderer):
        self.text_renderer = text_renderer

    def apply(self, parent: Element, x: ParagraphItem, skip_surrounding_p_element=False) -> Element:
        if isinstance(x, Paragraph):
            return self.render_paragraph(parent, x, skip_surrounding_p_element)
        if isinstance(x, lists.HeaderContentList):
            return self.render_header_value_list(parent, x)
        if isinstance(x, LiteralLayout):
            return self.render_literal_layout(parent, x)
        if isinstance(x, Table):
            return self.render_table(parent, x)
        raise TypeError('Unknown {}: {}'.format(str(ParagraphItem), str(type(x))))

    def render_literal_layout(self, parent: Element, x: LiteralLayout):
        return literal_layout.render(parent, x)

    def render_paragraph(self, parent: Element, x: Paragraph, skip_surrounding_p_element: bool):
        return paragraph.render(self.text_renderer, parent, x, skip_surrounding_p_element)

    def render_header_value_list(self, parent: Element, x: lists.HeaderContentList):
        return list_rendering.render(self.text_renderer, self, parent, x)

    def render_table(self, parent: Element, x: Table):
        return table_rendering.render(self, parent, x)