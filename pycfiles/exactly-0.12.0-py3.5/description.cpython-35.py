# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/description.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 1822 bytes
from typing import List
from exactly_lib.util.textformat.structure.core import Text, StringText, ParagraphItem
from exactly_lib.util.textformat.structure.document import SectionContents

class Description(tuple):

    def __new__(cls, single_line_description: Text, rest_paragraphs: List[ParagraphItem]):
        """
        :param single_line_description: Mandatory short description.
        """
        return tuple.__new__(cls, (single_line_description,
         rest_paragraphs))

    @property
    def single_line_description(self) -> Text:
        return self[0]

    @property
    def rest(self) -> List[ParagraphItem]:
        return self[1]


class DescriptionWithSubSections(tuple):

    def __new__(cls, single_line_description: Text, rest: SectionContents):
        """
        :param single_line_description: Mandatory short description.
        """
        return tuple.__new__(cls, (single_line_description,
         rest))

    @property
    def single_line_description(self) -> Text:
        return self[0]

    @property
    def rest(self) -> SectionContents:
        return self[1]


def single_line_description(line: str) -> Description:
    return Description(StringText(line), [])


def single_line_description_with_sub_sections(line: str) -> DescriptionWithSubSections:
    return DescriptionWithSubSections(StringText(line), SectionContents([], []))


def from_simple_description(description: Description) -> DescriptionWithSubSections:
    return DescriptionWithSubSections(description.single_line_description, SectionContents(description.rest, []))