# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tim/Projects/luyu/venv/lib/python2.7/site-packages/django_kss/pykss/comment.py
# Compiled at: 2014-11-20 06:52:44
import re
single_line_re = re.compile('^\\s*\\/\\/')
single_line_strip_re = re.compile('\\s*\\/\\/')
multi_line_start_re = re.compile('^\\s*\\/\\*')
multi_line_end_re = re.compile('.*\\*\\/')
multi_line_start_strip_re = re.compile('\\s*\\/\\*')
multi_line_end_strip_re = re.compile('\\*\\/')
multi_line_middle_strip_re = re.compile('^(\\s*\\*+)')
preceding_white_space_re = re.compile('^\\s*')

def is_single_line_comment(line):
    return single_line_re.match(line) is not None


def is_multi_line_comment_start(line):
    return multi_line_start_re.match(line) is not None


def is_multi_line_comment_end(line):
    if is_single_line_comment(line):
        return False
    else:
        return multi_line_end_re.match(line) is not None


def parse_single_line(line):
    return single_line_strip_re.sub('', line).rstrip()


def parse_multi_line(line):
    cleaned = multi_line_start_strip_re.sub('', line)
    return multi_line_end_strip_re.sub('', cleaned).rstrip()


def normalize(lines):
    cleaned = []
    indents = []
    for line in lines:
        line = multi_line_middle_strip_re.sub('', line)
        cleaned.append(line)
        match = preceding_white_space_re.match(line)
        if line:
            indents.append(len(match.group()))

    indent = min(indents) if indents else 0
    return ('\n').join([ line[indent:] for line in cleaned ]).strip()


class CommentParser(object):

    def __init__(self, filename):
        self.filename = filename

    def parse(self):
        blocks = []
        current_block = []
        inside_single_line_block = False
        inside_multi_line_block = False
        with open(self.filename) as (fileobj):
            for line in fileobj:
                if is_single_line_comment(line):
                    parsed = parse_single_line(line)
                    if inside_single_line_block:
                        current_block.append(parsed)
                    else:
                        current_block = [
                         parsed]
                        inside_single_line_block = True
                if is_multi_line_comment_start(line) or inside_multi_line_block:
                    parsed = parse_multi_line(line)
                    if inside_multi_line_block:
                        current_block.append(parsed)
                    else:
                        current_block = [
                         parsed]
                        inside_multi_line_block = True
                if is_multi_line_comment_end(line):
                    inside_multi_line_block = False
                if is_single_line_comment(line) is False and inside_multi_line_block is False:
                    if current_block:
                        blocks.append(normalize(current_block))
                    inside_single_line_block = False
                    current_block = []

        return blocks

    @property
    def blocks(self):
        if not hasattr(self, '_blocks'):
            self._blocks = self.parse()
        return self._blocks