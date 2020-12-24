# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/bashlex/heredoc.py
# Compiled at: 2019-03-01 15:42:24
from bashlex import ast, errors

def gatherheredocuments(tokenizer):
    while tokenizer.redirstack:
        if tokenizer._peekc() is None and not tokenizer._strictmode:
            tokenizer._shell_input_line_index += 1
            return
        redirnode, killleading = tokenizer.redirstack.pop(0)
        makeheredoc(tokenizer, redirnode, 0, killleading)

    return


def makeheredoc(tokenizer, redirnode, lineno, killleading):
    redirword = redirnode.output.word
    document = []
    startpos = tokenizer._shell_input_line_index
    fullline = tokenizer.readline(False)
    while fullline:
        if killleading:
            while fullline[0] == '\t':
                fullline = fullline[1:]

        if not fullline:
            continue
        if fullline[:-1] == redirword and fullline[len(redirword)] == '\n':
            document.append(fullline[:-1])
            break
        document.append(fullline)
        fullline = tokenizer.readline(False)

    if not fullline:
        raise errors.ParsingError('here-document at line %d delimited by end-of-file (wanted %r)' % (lineno, redirword), tokenizer._shell_input_line, tokenizer._shell_input_line_index)
    document = ('').join(document)
    endpos = tokenizer._shell_input_line_index - 1
    assert hasattr(redirnode, 'heredoc')
    redirnode.heredoc = ast.node(kind='heredoc', value=document, pos=(
     startpos, endpos))
    if redirnode.pos[1] + 1 == startpos:
        redirnode.pos = (
         redirnode.pos[0], endpos)
    return document