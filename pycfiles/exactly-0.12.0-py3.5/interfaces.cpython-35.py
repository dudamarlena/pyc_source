# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/textformat/rendering/html/paragraph_item/interfaces.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 294 bytes
from xml.etree.ElementTree import Element
from exactly_lib.util.textformat.structure.core import ParagraphItem

class ParagraphItemRenderer:

    def apply(self, parent: Element, x: ParagraphItem, skip_surrounding_p_element=False) -> Element:
        raise NotImplementedError()