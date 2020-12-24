# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Yass/mambo/md_ext.py
# Compiled at: 2019-06-02 14:11:56
# Size of source mod 2**32: 2482 bytes
"""
A utils for Markdown

convert : render markdown to html
get_toc : Get the Table of Content
get_images: Return a list of images, can be used to extract the top image

"""
import os, markdown
from jinja2.nodes import CallBlock
from jinja2.ext import Extension

class MarkdownTagExtension(Extension):
    __doc__ = '\n    A simple extension for adding a {% markdown %}{% endmarkdown %} tag to Jinja\n\n    <div> \n    {% markdown %}\n        ## Hi\n    {% endmarkdown %}\n    </div>\n    '
    tags = set(['markdown'])

    def __init__(self, environment):
        super(MarkdownTagExtension, self).__init__(environment)
        environment.extend(markdowner=markdown.Markdown(extensions=['extra']))

    def parse(self, parser):
        lineno = next(parser.stream).lineno
        body = parser.parse_statements([
         'name:endmarkdown'],
          drop_needle=True)
        return CallBlock(self.call_method('_markdown_support'), [], [], body).set_lineno(lineno)

    def _markdown_support(self, caller):
        block = caller()
        block = self._strip_whitespace(block)
        return self._render_markdown(block)

    def _strip_whitespace(self, block):
        lines = block.split('\n')
        whitespace = ''
        output = ''
        if len(lines) > 1:
            for char in lines[1]:
                if char == ' ' or char == '\t':
                    whitespace += char
                else:
                    break

        for line in lines:
            output += line.replace(whitespace, '', 1) + '\r\n'

        return output.strip()

    def _render_markdown(self, block):
        block = self.environment.markdowner.convert(block)
        return block


class MarkdownExtension(Extension):
    options = {}
    file_extensions = '.md'

    def preprocess(self, source, name, filename=None):
        if not name or name and os.path.splitext(name)[1] not in self.file_extensions:
            return source
        else:
            return convert(source)


mkd = markdown.Markdown(extensions=[
 'markdown.extensions.extra',
 'markdown.extensions.nl2br',
 'markdown.extensions.sane_lists',
 'markdown.extensions.toc'])

def convert(text):
    """
    Convert MD text to HTML
    :param text:
    :return:
    """
    mkd.reset()
    return mkd.convert(text)