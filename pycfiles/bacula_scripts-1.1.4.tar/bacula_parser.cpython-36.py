# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/philipp/Dokumente/computer/devel/pro/bacula_scripts/bacula_scripts/bacula_parser.py
# Compiled at: 2018-07-29 12:28:54
# Size of source mod 2**32: 6140 bytes
""" bacula_parse
Parse the output of `bareos-dir -xc`, `bareos-sd -xc` or `bareos-fd -xc` and transform the data,
using lark-parser, into python's dictionary format.
"""
import pprint, re
from lark import Lark
from lark import Transformer
from collections import defaultdict
from subprocess import Popen, PIPE
from helputils.core import format_exception

def preprocess_config(daemon, hn=False):
    """Parse bareos-dir, bareos-sd or bareos-fd config and return as dictionary"""
    cmd = ('%s -xc' % daemon).split()
    if hn:
        cmd = [
         'ssh', '-tt', hn] + cmd
    p1 = Popen(cmd, stdout=PIPE)
    try:
        text2 = p1.communicate()[0].decode('UTF-8')
    except Exception as e:
        print(format_exception(e))
        print('\n---------\n\nFailed to decode config. Try `bareos-dir -xc`, `bareos-fd -xc`, `bareos-sd -xc`\nmanually. There could be an error in your bareos config.\n---------\n\n')
        return

    if p1.returncode != 0:
        print('Bareos config error')
        return
    else:
        text2 = '{'.join(list(filter(None, [x.strip(' ') for x in text2.split('{')])))
        text2 = '}'.join(list(filter(None, [x.strip(' ') for x in text2.split('}')])))
        text2 = '\n'.join(list(filter(None, [x.strip() for x in text2.split('\n')])))
        quote_open = False
        text3 = list()
        unescaped_quotes = '(?<!\\\\)(?:\\\\\\\\)*"'
        has_comma = '(,)(?=(?:[^"]|"[^"]*")*$)'
        for line in text2.split('\n'):
            if '=' in line or quote_open:
                directive = quote_open or line.split('=', 1)
                directive_name = directive[0]
                directive_value = directive[1]
            else:
                directive_value += ' %s' % line
            comma_count = len(re.findall(has_comma, line))
            if not quote_open:
                if comma_count != 0:
                    continue
            equal_count = line.count('=')
            if equal_count >= 2:
                if not quote_open:
                    continue
            quote_count = len(re.findall(unescaped_quotes, line))
            if quote_count >= 5:
                if not quote_open:
                    continue
            directive_name = directive_name.strip()
            directive_value = directive_value.strip()
            quote_count_value = len(re.findall(unescaped_quotes, directive_value))
            if quote_count_value >= 3:
                pass
            else:
                if quote_count == 2:
                    line = '"%s" = %s' % (directive_name, directive_value)
                else:
                    if quote_count == 0:
                        if not quote_open:
                            directive_value = directive_value.strip()
                            line = '"%s" = "%s"' % (directive_name, directive_value)
                if quote_count == 0:
                    if quote_open:
                        continue
                if quote_count == 1:
                    if quote_open:
                        quote_open = False
                        directive_value = directive_value.strip()
                        line = '"%s" = %s' % (directive_name, directive_value)
                if quote_count == 1:
                    if not quote_open:
                        quote_open = True
                        continue
                text3.append(line)

        text4 = list()
        for line in text3:
            if '{' in line:
                left, right = line.split('{')
                left = '"%s"' % left
                line = left + '{'
            text4.append(line)

        text4 = '\n'.join(text4)
        if text4[(-1)] != '\n':
            text4 += '\n'
        return text4


class MyTransformer(Transformer):

    def string(self, items):
        return ''.join(items)

    def resource(self, items):
        resource_type = items[0].strip('"')
        directives = items[1:]
        for directive in directives:
            if not directive:
                pass
            else:
                for name, value in directive.items():
                    if name.lower() == 'name':
                        resource_name = value

        try:
            resource_name
        except:
            return
        else:
            resource_dict = defaultdict(lambda : defaultdict(defaultdict))
            for directive in directives:
                if not directive:
                    pass
                else:
                    for directive, value in directive.items():
                        resource_dict[resource_name][directive] = value

            return {resource_type: resource_dict}

    def resources(self, items):
        _dict = defaultdict(list)
        _dict = defaultdict(lambda : defaultdict(defaultdict))
        for d in items:
            for k1, v1 in d.items():
                for k2, v2 in v1.items():
                    name = d[k1][k2]['Name']
                    _dict[k1][k2] = v2

        return _dict

    def directive(self, items):
        items2 = list()
        for x in items:
            items2.append(x.strip('"'))

        return {items2[0]: items2[1]}


def bacula_parse(daemon='bareos-dir', hn=False):
    parser = Lark('\n        ?value: resources\n              | resource\n              | directive\n              | string\n        string    : ESCAPED_STRING\n        resource  : (string "{" "\\n" (directive|resource)* "}" "\\n")\n        resources : resource*\n        directive : string " " "=" " " string "\\n"\n\n        %import common.ESCAPED_STRING\n        %import common.WORD\n        %import common.WS\n    ',
      start='value')
    config = preprocess_config(daemon, hn)
    if not config:
        return
    else:
        tree = parser.parse(config)
        trans = MyTransformer().transform(tree)
        return trans