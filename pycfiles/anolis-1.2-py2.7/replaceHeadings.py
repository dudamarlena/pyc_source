# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/replaceHeadings.py
# Compiled at: 2013-02-15 13:25:53
from __future__ import unicode_literals
from anolislib import utils
from anolislib.processes import outliner
numered_headings = frozenset([b'h1', b'h2', b'h3', b'h4', b'h5', b'h6'])

class replaceHeadings(object):
    """Replace numeric headings with the numeric headings appropriate for their
       depth."""

    def __init__(self, ElementTree, **kwargs):
        self.replaceHeadings(ElementTree, **kwargs)

    def replaceHeadings(self, ElementTree, **kwargs):
        outline_creator = outliner.Outliner(ElementTree, **kwargs)
        outline = outline_creator.build(**kwargs)
        sections = [ (section, 1) for section in reversed(outline) ]
        while sections:
            section, depth = sections.pop()
            if section.header is not None and section.header.tag in numered_headings:
                if depth <= 6:
                    section.header.tag = b'h%i' % depth
                else:
                    raise TooDeepException(b'Too deep for numbered headers')
            sections.extend([ (child_section, depth + 1) for child_section in reversed(section)
                            ])

        return


class TooDeepException(utils.AnolisException):
    """That's real deep. But we only have six levels of numbered headers."""
    pass