# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/phdoc/mdx_fold.py
# Compiled at: 2013-09-26 11:25:45
"""
An extension for blocks that start hidden,
but can be shown when the viewer wants it.
These are marked up as blockquote with ``fold`` class.
The motivation is adding abstracts to publication lists.
"""
import re, markdown

class FoldExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        """
        Add `FoldBlockProcessor` to the Markdown instance.
        """
        md.parser.blockprocessors.add('fold_block', FoldBlockProcessor(md.parser), '>quote')


class FoldBlockProcessor(markdown.blockprocessors.BlockProcessor):
    """
    Pretty much the original BlockQuoteProcessor with an additional class.
    """
    RE = re.compile('(^|\\n)[ ]{0,3}\\|[ ]?(.*)')

    def test(self, parent, block):
        return bool(self.RE.search(block))

    def run(self, parent, blocks):
        block = blocks.pop(0)
        m = self.RE.search(block)
        if m:
            before = block[:m.start()]
            self.parser.parseBlocks(parent, [before])
            block = ('\n').join([ self.clean(line) for line in block[m.start():].split('\n')
                                ])
        sibling = self.lastChild(parent)
        if sibling and sibling.tag == 'blockquote':
            quote = sibling
        else:
            quote = markdown.util.etree.SubElement(parent, 'blockquote', {'class': 'fold'})
        self.parser.state.set('fold_block')
        self.parser.parseChunk(quote, block)
        self.parser.state.reset()

    def clean(self, line):
        """ Remove ``|`` from beginning of a line. """
        m = self.RE.match(line)
        if line.strip() == '|':
            return ''
        else:
            if m:
                return m.group(2)
            return line