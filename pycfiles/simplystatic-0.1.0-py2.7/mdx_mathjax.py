# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/simplystatic/mdx_mathjax.py
# Compiled at: 2014-01-31 13:49:30
import markdown

class MathJaxPattern(markdown.inlinepatterns.Pattern):

    def __init__(self):
        markdown.inlinepatterns.Pattern.__init__(self, '(?<!\\\\)(\\$\\$?)(.+?)\\2')

    def handleMatch(self, m):
        node = markdown.util.etree.Element('mathjax')
        node.text = markdown.util.AtomicString(m.group(2) + m.group(3) + m.group(2))
        return node


class MathJaxExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('mathjax', MathJaxPattern(), '<escape')


def makeExtension(configs=None):
    return MathJaxExtension(configs)