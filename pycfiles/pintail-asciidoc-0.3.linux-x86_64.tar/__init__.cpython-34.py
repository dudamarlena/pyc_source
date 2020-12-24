# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/pintail/asciidoc/__init__.py
# Compiled at: 2016-07-06 11:58:41
# Size of source mod 2**32: 1830 bytes
import os, subprocess
from lxml import etree
import pintail.site, pintail.mallard

class AsciiDocPage(pintail.mallard.MallardPage, pintail.site.ToolsProvider):

    def __init__(self, directory, source_file):
        pintail.mallard.MallardPage.__init__(self, directory, source_file)

    @property
    def stage_file(self):
        if self.source_file.endswith('.adoc'):
            return self.source_file[:-5] + '.page'
        else:
            return self.source_file

    def stage_page(self):
        pintail.site.Site._makedirs(self.directory.stage_path)
        subprocess.call(['asciidoctor-mallard',
         '-o', self.stage_path,
         self.source_path])

    @classmethod
    def get_pages(cls, directory, filename):
        if filename.endswith('.adoc'):
            return [AsciiDocPage(directory, filename)]
        return []

    @classmethod
    def build_tools(cls, site):
        pass