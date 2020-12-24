# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/beehive/formatter/filters.py
# Compiled at: 2014-10-30 06:03:53
# Size of source mod 2**32: 1178 bytes
__status__ = 'DEAD, BROKEN'
from gherkin.tag_expression import TagExpression

class LineFilter(object):

    def __init__(self, lines):
        self.lines = lines

    def eval(self, tags, names, ranges):
        for r in ranges:
            for line in self.lines:
                if r[0] <= line <= r[1]:
                    return True

        return False

    def filter_table_body_rows(self, rows):
        body = [r for r in rows[1:] if r.line in self.lines]
        return [rows[0]] + body


class RegexpFilter(object):

    def __init__(self, regexen):
        self.regexen = regexen

    def eval(self, tags, names, ranges):
        for regex in self.regexen:
            for name in names:
                if regex.search(name):
                    return True

        return False

    def filter_table_body_rows(self, rows):
        return rows


class TagFilter(object):

    def __init__(self, tags):
        self.tag_expression = TagExpression(tags)

    def eval(self, tags, names, ranges):
        return self.tag_expression.eval([tag.name for tag in set(tags)])

    def filter_table_body_rows(self, rows):
        return rows