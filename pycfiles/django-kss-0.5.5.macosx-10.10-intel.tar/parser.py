# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tim/Projects/luyu/venv/lib/python2.7/site-packages/django_kss/pykss/parser.py
# Compiled at: 2015-02-08 05:35:41
import os
from .comment import CommentParser
from .exceptions import SectionDoesNotExist
from .section import Section

class Parser(object):

    def __init__(self, *paths):
        self.paths = paths

    def parse(self):
        sections = {}
        filenames = [ os.path.join(subpath, filename) for path in self.paths for subpath, dirs, files in os.walk(path) for filename in files
                    ]
        for filename in filenames:
            parser = CommentParser(filename)
            for block in parser.blocks:
                section = Section(block, os.path.basename(filename))
                if section.section:
                    sections[section.section] = section

        return sections

    @property
    def sections(self):
        if not hasattr(self, '_sections'):
            self._sections = self.parse()
        return self._sections

    def section(self, reference):
        try:
            return self.sections[reference]
        except KeyError:
            raise SectionDoesNotExist('Section "%s" does not exist.' % reference)