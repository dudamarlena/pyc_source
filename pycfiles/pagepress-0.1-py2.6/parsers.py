# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/pagepress/parsers.py
# Compiled at: 2012-03-23 03:34:40
import logging
from markdown import Markdown as MarkdownParser
log = logging.getLogger(__name__)

class Markdown:

    def __init__(self):
        self.markdown = MarkdownParser(output_format='html5', extensions=[
         'tables'])

    def parse(self, fp):
        meta = {}

        def read_file():
            in_head = True
            for line in fp:
                if not in_head:
                    yield line
                elif len(line) < 2:
                    in_head = False
                    yield line
                else:
                    (name, value) = line.split(':')
                    meta[name.lower()] = value.strip()

        content = self.markdown.convert(('').join(read_file()))
        self.markdown.reset()
        pagetype = meta.pop('type', 'templated')
        return (pagetype, meta, content)