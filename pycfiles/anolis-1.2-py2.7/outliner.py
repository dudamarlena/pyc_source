# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/outliner.py
# Compiled at: 2013-02-15 13:25:53
from __future__ import unicode_literals
from lxml import etree
from anolislib import utils
fixedRank = {b'h1': -1, b'h2': -2, b'h3': -3, b'h4': -4, b'h5': -5, b'h6': -6}

class section(list):
    """Represents the section of a document."""
    header = None

    def __repr__(self):
        return b'<section %s>' % repr(self.header)

    def append(self, child):
        list.append(self, child)
        child.parent = self

    def extend(self, children):
        list.extend(self, children)
        for child in children:
            child.parent = self


class Outliner:
    """Build the outline of an HTML document."""

    def __init__(self, ElementTree, **kwargs):
        self.ElementTree = ElementTree
        self.stack = []
        self.outlines = {}
        self.current_outlinee = None
        self.current_section = None
        return

    def _rank(self, element):
        if element.tag in fixedRank:
            return fixedRank[element.tag]
        else:
            if element.tag == b'hgroup':
                for i in range(1, 6):
                    if element.find(b'.//h%i' % i) is not None:
                        return -i
                else:
                    return -1

            else:
                raise ValueError(b'Only h1–h6 and hgroup elements have a rank')
            return

    def build(self, **kwargs):
        for action, element in etree.iterwalk(self.ElementTree, events=('start', 'end')):
            if action == b'end' and self.stack and self.stack[(-1)] == element:
                assert element.tag in utils.heading_content
                self.stack.pop()
            elif self.stack and self.stack[(-1)].tag in utils.heading_content:
                pass
            elif action == b'start' and (element.tag in utils.sectioning_content or element.tag in utils.sectioning_root):
                if self.current_outlinee is not None:
                    self.stack.append(self.current_outlinee)
                self.current_outlinee = element
                self.current_section = section()
                self.outlines[self.current_outlinee] = [
                 self.current_section]
            elif action == b'end' and element.tag in utils.sectioning_content and self.stack:
                self.current_outlinee = self.stack.pop()
                self.current_section = self.outlines[self.current_outlinee][(-1)]
                self.current_section += self.outlines[element]
            elif action == b'end' and element.tag in utils.sectioning_root and self.stack:
                self.current_outlinee = self.stack.pop()
                self.current_section = self.outlines[self.current_outlinee][(-1)]
                while self.current_section:
                    assert self.current_section != self.current_section[(-1)]
                    self.current_section = self.current_section[(-1)]

            elif action == b'end' and (element.tag in utils.sectioning_content or element.tag in utils.sectioning_root):
                assert self.current_outlinee == element
                self.current_section = self.outlines[self.current_outlinee][0]
                break
            elif self.current_outlinee is None:
                pass
            elif action == b'start' and element.tag in utils.heading_content:
                if self.current_section.header is None:
                    self.current_section.header = element
                elif self._rank(element) >= self._rank(self.outlines[self.current_outlinee][(-1)].header):
                    self.current_section = section()
                    self.outlines[self.current_outlinee].append(self.current_section)
                    self.current_section.header = element
                else:
                    candidate_section = self.current_section
                    while True:
                        if self._rank(element) < self._rank(candidate_section.header):
                            self.current_section = section()
                            candidate_section.append(self.current_section)
                            self.current_section.header = element
                            break
                        candidate_section = candidate_section.parent

                self.stack.append(element)

        try:
            return self.outlines[self.current_outlinee]
        except KeyError:
            return

        return