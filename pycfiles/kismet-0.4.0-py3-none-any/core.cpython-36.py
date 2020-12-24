# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mara_kim/Documents/code/autochthe/kismet-py/kismet/core.py
# Compiled at: 2019-02-02 16:22:44
# Size of source mod 2**32: 2240 bytes
import regex
from kismet.parser import KismetParser
from kismet.personality.core import analyze
parser = KismetParser()

def process(string: str):
    parsed, emoted = process_parts(string)
    if parsed:
        if emoted:
            return parsed + '\n' + emoted
    if parsed:
        return parsed
    else:
        if emoted:
            return emoted
        return ''


def process_parts(string: str):
    return (parser.parse(string), analyze(string))


def process_markdown(string: str):
    blocks = code_blocks(string)
    answers = [answer for answer in [parser.parse(block) for block in blocks] if answer is not None]
    result = '```\n' + '\n'.join(answers) + '\n```' if answers else None
    return (result, analyze(string))


def code_blocks(string: str, syntax_type: str='kismet'):
    blocks = []
    fence = None
    ignore = False
    for line in string.splitlines(keepends=True):
        while line:
            if fence:
                match = regex.search(fence, line)
                if match:
                    if not ignore:
                        blocks[(-1)] += line[:match.start()]
                    fence = None
                    line = line[match.end():]
                else:
                    if not ignore:
                        blocks[(-1)] += line
                        line = None
                    else:
                        line = None
            else:
                match = regex.search('^`{3,}', line)
                if match:
                    fence = '^' + match.group()
                    syntax = line[match.end():]
                    if syntax != '\n':
                        if syntax != syntax_type + '\n':
                            ignore = True
                    else:
                        blocks.append('')
                    line = None
                else:
                    match = regex.search('`+', line)
                    if match:
                        fence = match.group()
                        line = line[match.end():]
                        blocks.append('')
                    else:
                        line = None

    if fence:
        del blocks[-1]
    return blocks