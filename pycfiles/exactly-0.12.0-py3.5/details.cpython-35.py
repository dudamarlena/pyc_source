# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/description_tree/details.py
# Compiled at: 2020-01-29 09:08:18
# Size of source mod 2**32: 2523 bytes
import itertools
from typing import Sequence, Any
from exactly_lib.util.description_tree import tree
from exactly_lib.util.description_tree.renderer import DetailsRenderer, NodeRenderer
from exactly_lib.util.description_tree.tree import Detail
from exactly_lib.util.simple_textstruct.structure import TextStyle, TEXT_STYLE__NEUTRAL
from exactly_lib.util.strings import ToStringObject

class DetailsRendererOfConstant(DetailsRenderer):

    def __init__(self, details: Sequence[Detail]):
        self._details = details

    def render(self) -> Sequence[Detail]:
        return self._details


def empty() -> DetailsRenderer:
    return DetailsRendererOfConstant(())


class SequenceRenderer(DetailsRenderer):

    def __init__(self, details: Sequence[DetailsRenderer]):
        self._details = details

    def render(self) -> Sequence[Detail]:
        return list(itertools.chain.from_iterable([detail.render() for detail in self._details]))


class String(DetailsRenderer):

    def __init__(self, to_string_object: ToStringObject):
        self._to_string_object = to_string_object

    def render(self) -> Sequence[Detail]:
        return [tree.StringDetail(self._to_string_object)]


class PreFormattedString(DetailsRenderer):

    def __init__(self, to_string_object: ToStringObject, string_is_line_ended: bool=False):
        self._to_string_object = to_string_object
        self._string_is_line_ended = string_is_line_ended

    def render(self) -> Sequence[Detail]:
        return [
         tree.PreFormattedStringDetail(self._to_string_object, self._string_is_line_ended)]


class HeaderAndValue(DetailsRenderer):

    def __init__(self, header: ToStringObject, value: DetailsRenderer, header_text_style: TextStyle=TEXT_STYLE__NEUTRAL):
        self._header = header
        self._value = value
        self._header_text_style = header_text_style

    def render(self) -> Sequence[Detail]:
        return [
         tree.HeaderAndValueDetail(self._header, self._value.render(), self._header_text_style)]


class Tree(DetailsRenderer):

    def __init__(self, tree_: NodeRenderer[Any]):
        self._tree = tree_

    def render(self) -> Sequence[Detail]:
        return [tree.TreeDetail(self._tree.render())]