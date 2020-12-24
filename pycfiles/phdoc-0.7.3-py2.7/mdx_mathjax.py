# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/phdoc/mdx_mathjax.py
# Compiled at: 2013-09-25 10:00:36
"""
This near trivial extension makes MathJax formulas AtomicStrings.
"""
import markdown

class MathJaxInlinePattern(markdown.inlinepatterns.Pattern):
    """
    Pattern for in-line math, recommended.
    """

    def __init__(self):
        markdown.inlinepatterns.Pattern.__init__(self, '(?<!\\\\)(\\\\\\()(.+?)(\\\\\\))')

    def handleMatch(self, m):
        node = markdown.util.etree.Element('span')
        node.text = markdown.util.AtomicString('\\(' + m.group(3) + '\\)')
        return node


class MathJaxInlinePattern2(markdown.inlinepatterns.Pattern):
    """
    Pattern for in-line math, single-dollars.
    """

    def __init__(self):
        markdown.inlinepatterns.Pattern.__init__(self, '(?<!\\\\)(\\$)(.+?)(\\$)')

    def handleMatch(self, m):
        node = markdown.util.etree.Element('span')
        node.text = markdown.util.AtomicString('$' + m.group(3) + '$')
        return node


class MathJaxBlockPattern(markdown.inlinepatterns.Pattern):
    """
    Pattern for block math. Note that block refers to mathjax behaviour, we
    allow this element in-line in the markup.
    """

    def __init__(self):
        markdown.inlinepatterns.Pattern.__init__(self, '(?<!\\\\)(\\\\\\[)(.+?)(\\\\\\])')

    def handleMatch(self, m):
        node = markdown.util.etree.Element('span')
        node.text = markdown.util.AtomicString('\\[' + m.group(3) + '\\]')
        return node


class MathJaxExtension(markdown.Extension):

    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('mathjaxi', MathJaxInlinePattern(), '<escape')
        md.inlinePatterns.add('mathjaxi2', MathJaxInlinePattern2(), '<escape')
        md.inlinePatterns.add('mathjaxb', MathJaxBlockPattern(), '<escape')


def makeExtension(configs=None):
    return MathJaxExtension(configs)