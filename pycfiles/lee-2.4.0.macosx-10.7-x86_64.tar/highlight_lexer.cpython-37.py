# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/zk/anaconda3/lib/python3.7/site-packages/lee/highlight_lexer.py
# Compiled at: 2020-02-11 23:16:56
# Size of source mod 2**32: 2084 bytes
from pygments import highlight
from pygments.lexers import PythonLexer, CppLexer, MarkdownLexer, JavascriptLexer, JavascriptSmartyLexer, JavaLexer
import pygments.formatters as tf
from termcolor import colored

def lexer(s):
    code = False
    bold = False
    code_block = False
    language = ''
    b = []
    l = len(s)
    i = 0
    while i < l:
        c = s[i]
        if c == '`':
            if s[(i + 1)] == '`' and s[(i + 2)] == '`':
                code_block = not code_block
                i += 2
                while s[i] != '\n':
                    language += s[i]
                    i += 1

                code_block or (yield ('break', ''))
                print('...', language.strip())
                yield (language.strip(), ''.join(b))
                language = ''
                b = []
            else:
                code = not code
                if not code:
                    yield (
                     'block', ''.join(b))
                    b = []
        else:
            if c == '*':
                if s[(i + 1)] == '*':
                    bold = not bold
                    i += 1
                    if not bold:
                        yield (
                         'bold', ''.join(b))
                        b = []
            elif code or code_block:
                b.append(c)
            else:
                yield (
                 'normal', c)
        i += 1


def terminal_print(ss):
    for t, st in lexer(ss):
        if t == 'cpp':
            print(highlight(st, CppLexer(), tf()))
        elif t == 'python':
            print(highlight(st, PythonLexer(), tf()))
        elif t == 'js':
            print(highlight(st, JavascriptSmartyLexer(), tf()))
        elif t == 'java':
            print(highlight(st, JavaLexer(), tf()))
        elif t == 'block':
            print((colored(st, 'yellow')), end='')
        elif t == 'break':
            print('\n')
        else:
            print(st, end='')


if __name__ == '__main__':
    s = '\n    this isi goodfosdf\n    ``` java \n    System.out.println("helo");\n\n    ```\n\n    '
    terminal_print(s)