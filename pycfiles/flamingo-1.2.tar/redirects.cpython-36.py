# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/redirects.py
# Compiled at: 2020-02-26 05:03:46
# Size of source mod 2**32: 1563 bytes
import re
from flamingo.core.parser import ContentParser
HTML_TEMPLATE = '\n<!DOCTYPE html>\n<html>\n  <head>\n    <meta http-equiv="refresh" content="0; url={}">\n  </head>\n  <body></body>\n</html>\n'

class RedirectRulesParser(ContentParser):
    FILE_EXTENSIONS = [
     'rr']
    RULE_RE = re.compile('^(?P<code>[0-9]+)(\\s{1,})(?P<src>[^ ]+)(\\s{1,})(?P<dst>[^ \\n]+)$')

    def parse(self, file_content, content):
        content['output'] = '/dev/null'
        content['type'] = 'redirect-rules'
        content['rules'] = []
        for line in file_content.splitlines():
            if not not line:
                if line.startswith('#'):
                    pass
                else:
                    match = self.RULE_RE.search(line)
                    if not match:
                        pass
                    else:
                        match = match.groupdict()
                        content['rules'].append((
                         match['code'], match['src'], match['dst']))


class Redirects:

    def parser_setup(self, context):
        context.parser.add_parser(RedirectRulesParser(context))

    def contents_parsed(self, context):
        rules = sum(context.contents.filter(type='redirect-rules').values('rules'), [])
        for status_code, source, destination in rules:
            if source.startswith('/'):
                source = source[1:]
            content = {'type':'redirect-rule', 
             'output':source, 
             'content':HTML_TEMPLATE.format(destination), 
             'redirect':destination}
            (context.contents.add)(**content)