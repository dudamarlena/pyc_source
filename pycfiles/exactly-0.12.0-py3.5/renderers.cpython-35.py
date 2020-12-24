# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/description_tree/renderers.py
# Compiled at: 2019-12-27 10:07:33
# Size of source mod 2**32: 2209 bytes
import itertools
from typing import Generic, Sequence, Callable
from exactly_lib.util.description_tree.renderer import NODE_DATA, NodeRenderer, DetailsRenderer
from exactly_lib.util.description_tree.tree import Node

class Constant(Generic[NODE_DATA], NodeRenderer[NODE_DATA]):

    def __init__(self, constant: Node[NODE_DATA]):
        self._constant = constant

    def render(self) -> Node[NODE_DATA]:
        return self._constant


def header_only(header: str) -> NodeRenderer[None]:
    return NodeRendererFromParts(header, None, (), ())


def header_and_detail(header: str, detail: DetailsRenderer) -> NodeRenderer[None]:
    return NodeRendererFromParts(header, None, (detail,), ())


class NodeRendererFromParts(Generic[NODE_DATA], NodeRenderer[NODE_DATA]):

    def __init__(self, header: str, data: NODE_DATA, details: Sequence[DetailsRenderer], children: Sequence[NodeRenderer[NODE_DATA]]):
        self._header = header
        self._data = data
        self._details = details
        self._children = children

    def render(self) -> Node[NODE_DATA]:
        return Node(self._header, self._data, list(itertools.chain.from_iterable(d.render() for d in self._details)), [c.render() for c in self._children])


class CachedSingleInvokation(Generic[NODE_DATA], NodeRenderer[NODE_DATA]):
    __doc__ = 'Result is that of the given renderer, which is invoked at most once.'

    def __init__(self, renderer: NodeRenderer[NODE_DATA]):
        self._renderer = renderer
        self._cache = None

    def render(self) -> Node[NODE_DATA]:
        if self._cache is None:
            self._cache = self._renderer.render()
        return self._cache


class FromFunction(Generic[NODE_DATA], NodeRenderer[NODE_DATA]):

    def __init__(self, renderer: Callable[([], NodeRenderer[NODE_DATA])]):
        self._renderer = renderer

    def render(self) -> Node[NODE_DATA]:
        return self._renderer().render()