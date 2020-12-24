# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/easy.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1983 bytes
from dexy.filter import DexyFilter
from pygments.formatters import LatexFormatter

class EasyLatex(DexyFilter):
    __doc__ = '\n    Wraps your text in LaTeX article header/footer.\n    Easy way to generate a document which can be compiled using LaTeX (includes\n    Pygments syntax highlighting).\n    '
    aliases = ['easylatex']
    _settings = {'input-extensions':[
      '.tex'], 
     'output-extensions':[
      '.tex'], 
     'documentclass':('The document class to generate.', 'article'), 
     'style':('The pygments style to use.', 'default'), 
     'title':('Title of article.', ''), 
     'author':('Author of article.', ''), 
     'date':('Date of article.', ''), 
     'font':('The font size to use.', '11pt'), 
     'papersize':('The document class to generate.', 'a4paper'), 
     'preamble':('Additional custom LaTeX content to include in header.', '')}

    def pygments_sty(self):
        formatter = LatexFormatter(style=(self.setting('style')))
        return formatter.get_style_defs()

    def process_text(self, input_text):
        args = self.setting_values()
        args['input'] = input_text
        args['pygments'] = self.pygments_sty()
        if self.setting('title'):
            args['title'] = '\\title{%(title)s}' % args
            args['maketitle'] = '\\maketitle'
        else:
            args['title'] = ''
            args['maketitle'] = ''
        if self.setting('date'):
            args['date'] = '\\date{%(date)s}' % args
        if self.setting('author'):
            args['author'] = '\\author{%(author)s}' % args
        return self.template % args

    template = '\\documentclass[%(font)s,%(papersize)s]{%(documentclass)s}\n\\usepackage{color}\n\\usepackage{fancyvrb}\n%(pygments)s\n\n%(preamble)s\n\n%(title)s\n%(author)s\n%(date)s\n\n\\begin{document}\n\n%(maketitle)s\n\n\n%(input)s\n\n\\end{document}\n'