# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/ansi.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1587 bytes
from dexy.filter import DexyFilter
from dexy.plugin import TemplatePlugin
try:
    from ansi2html import Ansi2HTMLConverter
    AVAILABLE = True
except ImportError:
    AVAILABLE = False

class Ansi2HTMLTemplatePlugin(TemplatePlugin):
    __doc__ = '\n    Expose ansi2html within templates.\n    '
    aliases = ['ansi2html']

    def is_active(self):
        return AVAILABLE

    def convert(self, doc, font_size='normal'):
        conv = Ansi2HTMLConverter(inline=True, font_size=font_size)
        return conv.convert((str(doc)), full=False)

    def run(self):
        return {'ansi2html': ('The convert method from ansi2html module.', self.convert)}


class Ansi2HTMLFilter(DexyFilter):
    __doc__ = '\n    Generates HTML from ANSI color codes using ansi2html.\n    '
    aliases = ['ansi2html']
    _settings = {'output-extensions':[
      '.html'], 
     'input-extensions':[
      '.txt', '.sh-session'], 
     'data-type':'sectioned', 
     'pre':('Whether to wrap in <pre> tags.', True), 
     'font-size':('CSS font size to be used.', 'normal')}

    def is_active(self):
        return AVAILABLE

    def process(self):
        conv = Ansi2HTMLConverter(inline=True, font_size=(self.setting('font-size')))
        if self.setting('pre'):
            s = '<pre>\n%s</pre>\n'
        else:
            s = '%s\n'
        for k, v in self.input_data.items():
            self.output_data[k] = s % conv.convert((str(v)), full=False)

        self.output_data.save()