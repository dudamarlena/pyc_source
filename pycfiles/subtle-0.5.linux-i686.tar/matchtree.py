# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/guessit/matchtree.py
# Compiled at: 2013-03-18 16:30:48
from __future__ import unicode_literals
from guessit import UnicodeMixin, base_text_type, Guess
from guessit.textutils import clean_string, str_fill
from guessit.patterns import group_delimiters
from guessit.guess import merge_similar_guesses, merge_all, choose_int, choose_string
import copy, logging
log = logging.getLogger(__name__)

class BaseMatchTree(UnicodeMixin):
    """A MatchTree represents the hierarchical split of a string into its
    constituent semantic groups."""

    def __init__(self, string=b'', span=None, parent=None):
        self.string = string
        self.span = span or (0, len(string))
        self.parent = parent
        self.children = []
        self.guess = Guess()

    @property
    def value(self):
        return self.string[self.span[0]:self.span[1]]

    @property
    def clean_value(self):
        return clean_string(self.value)

    @property
    def offset(self):
        return self.span[0]

    @property
    def info(self):
        result = dict(self.guess)
        for c in self.children:
            result.update(c.info)

        return result

    @property
    def root(self):
        if not self.parent:
            return self
        return self.parent.root

    @property
    def depth(self):
        if self.is_leaf():
            return 0
        return 1 + max(c.depth for c in self.children)

    def is_leaf(self):
        return self.children == []

    def add_child(self, span):
        child = MatchTree(self.string, span=span, parent=self)
        self.children.append(child)

    def partition(self, indices):
        indices = sorted(indices)
        if indices[0] != 0:
            indices.insert(0, 0)
        if indices[(-1)] != len(self.value):
            indices.append(len(self.value))
        for start, end in zip(indices[:-1], indices[1:]):
            self.add_child(span=(self.offset + start,
             self.offset + end))

    def split_on_components(self, components):
        offset = 0
        for c in components:
            start = self.value.find(c, offset)
            end = start + len(c)
            self.add_child(span=(self.offset + start,
             self.offset + end))
            offset = end

    def nodes_at_depth(self, depth):
        if depth == 0:
            yield self
        for child in self.children:
            for node in child.nodes_at_depth(depth - 1):
                yield node

    @property
    def node_idx(self):
        if self.parent is None:
            return ()
        else:
            return self.parent.node_idx + (self.parent.children.index(self),)

    def node_at(self, idx):
        if not idx:
            return self
        try:
            return self.children[idx[0]].node_at(idx[1:])
        except:
            raise ValueError(b'Non-existent node index: %s' % (idx,))

    def nodes(self):
        yield self
        for child in self.children:
            for node in child.nodes():
                yield node

    def _leaves(self):
        if self.is_leaf():
            yield self
        else:
            for child in self.children:
                for leaf in child._leaves():
                    yield leaf

    def leaves(self):
        return list(self._leaves())

    def to_string(self):
        empty_line = b' ' * len(self.string)

        def to_hex(x):
            if isinstance(x, int):
                if x < 10:
                    return str(x)
                return chr(55 + x)
            return x

        def meaning(result):
            mmap = {b'episodeNumber': b'E', b'season': b'S', 
               b'extension': b'e', 
               b'format': b'f', 
               b'language': b'l', 
               b'country': b'C', 
               b'videoCodec': b'v', 
               b'audioCodec': b'a', 
               b'website': b'w', 
               b'container': b'c', 
               b'series': b'T', 
               b'title': b't', 
               b'date': b'd', 
               b'year': b'y', 
               b'releaseGroup': b'r', 
               b'screenSize': b's'}
            if result is None:
                return b' '
            else:
                for prop, l in mmap.items():
                    if prop in result:
                        return l

                return b'x'

        lines = [empty_line] * (self.depth + 2)
        lines[-2] = self.string
        for node in self.nodes():
            if node == self:
                continue
            idx = node.node_idx
            depth = len(idx) - 1
            if idx:
                lines[depth] = str_fill(lines[depth], node.span, to_hex(idx[(-1)]))
            if node.guess:
                lines[-2] = str_fill(lines[(-2)], node.span, b'_')
                lines[-1] = str_fill(lines[(-1)], node.span, meaning(node.guess))

        lines.append(self.string)
        return (b'\n').join(lines)

    def __unicode__(self):
        return self.to_string()


class MatchTree(BaseMatchTree):
    """The MatchTree contains a few "utility" methods which are not necessary
    for the BaseMatchTree, but add a lot of convenience for writing
    higher-level rules."""

    def _unidentified_leaves(self, valid=lambda leaf: len(leaf.clean_value) >= 2):
        for leaf in self._leaves():
            if not leaf.guess and valid(leaf):
                yield leaf

    def unidentified_leaves(self, valid=lambda leaf: len(leaf.clean_value) >= 2):
        return list(self._unidentified_leaves(valid))

    def _leaves_containing(self, property_name):
        if isinstance(property_name, base_text_type):
            property_name = [
             property_name]
        for leaf in self._leaves():
            for prop in property_name:
                if prop in leaf.guess:
                    yield leaf
                    break

    def leaves_containing(self, property_name):
        return list(self._leaves_containing(property_name))

    def first_leaf_containing(self, property_name):
        try:
            return next(self._leaves_containing(property_name))
        except StopIteration:
            return

        return

    def _previous_unidentified_leaves(self, node):
        node_idx = node.node_idx
        for leaf in self._unidentified_leaves():
            if leaf.node_idx < node_idx:
                yield leaf

    def previous_unidentified_leaves(self, node):
        return list(self._previous_unidentified_leaves(node))

    def _previous_leaves_containing(self, node, property_name):
        node_idx = node.node_idx
        for leaf in self._leaves_containing(property_name):
            if leaf.node_idx < node_idx:
                yield leaf

    def previous_leaves_containing(self, node, property_name):
        return list(self._previous_leaves_containing(node, property_name))

    def is_explicit(self):
        """Return whether the group was explicitly enclosed by
        parentheses/square brackets/etc."""
        return self.value[0] + self.value[(-1)] in group_delimiters

    def matched(self):
        parts = [ node.guess for node in self.nodes() if node.guess ]
        parts = copy.deepcopy(parts)
        for int_part in ('year', 'season', 'episodeNumber'):
            merge_similar_guesses(parts, int_part, choose_int)

        for string_part in ('title', 'series', 'container', 'format', 'releaseGroup',
                            'website', 'audioCodec', 'videoCodec', 'screenSize',
                            'episodeFormat', 'audioChannels'):
            merge_similar_guesses(parts, string_part, choose_string)

        result = merge_all(parts, append=[
         b'language', b'subtitleLanguage', b'other'])
        log.debug(b'Final result: ' + result.nice_string())
        return result