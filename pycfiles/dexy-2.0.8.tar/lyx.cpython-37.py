# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/filters/lyx.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 968 bytes
from dexy.filter import DexyFilter

class LyxJinjaFilter(DexyFilter):
    __doc__ = "\n    Converts dexy:foo.txt|bar into << d['foo.txt|bar'] >>\n    \n    Makes it easier to compose documents with lyx and process them in dexy.\n    This expects you to do doc.lyx|lyx|lyxjinja|jinja|latex\n    "
    aliases = ['lyxjinja']
    _settings = {'input-extensions':[
      '.tex'], 
     'output-extensions':[
      '.tex']}

    def process_text(self, input_text):
        lines = []
        for line in input_text.splitlines():
            if line.startswith('dexy:'):
                _, clean_line = line.split('dexy:')
                if ':' in clean_line:
                    doc, section = clean_line.split(':')
                    lines.append("<< d['%s']['%s'] >>" % (doc, section))
                else:
                    lines.append("<< d['%s'] >>" % clean_line)
            else:
                lines.append(line)

        return '\n'.join(lines)