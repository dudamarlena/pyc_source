# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/contrib/nginxparser.py
# Compiled at: 2019-05-16 13:41:33
"""  A class that parses nginx configuration with pyparsing """
import string, copy
from insights.contrib.pyparsing import Literal, White, Word, alphanums, CharsNotIn, Combine, Forward, Group, Optional, OneOrMore, ZeroOrMore, Regex, stringEnd, restOfLine

def create_parser():
    space = Optional(White())
    nonspace = Regex('\\S+')
    left_bracket = Literal('{').suppress()
    right_bracket = space.leaveWhitespace() + Literal('}').suppress()
    semicolon = Literal(';').suppress()
    key = Word(alphanums + '_/+-.')
    dollar_var = Combine(Literal('$') + Regex('[^\\{\\};,\\s]+'))
    condition = Regex('\\(.+\\)')
    dquoted = Regex('(\\".*\\")')
    squoted = Regex("(\\'.*\\')")
    nonspecial = Regex('[^\\{\\};,]')
    varsub = Regex('(\\$\\{\\w+\\})')
    value = Combine(ZeroOrMore(dquoted | squoted | varsub | nonspecial))
    location = CharsNotIn('{};,' + string.whitespace)
    modifier = Literal('=') | Literal('~*') | Literal('~') | Literal('^~')
    comment = space + Literal('#') + restOfLine
    assignment = space + key + Optional(space + value, default=None) + semicolon
    location_statement = space + Optional(modifier) + Optional(space + location + space)
    if_statement = space + Literal('if') + space + condition + space
    charset_map_statement = space + Literal('charset_map') + space + value + space + value
    map_statement = space + Literal('map') + space + nonspace + space + dollar_var + space
    map_pattern = Regex('".*"') | Regex("'.*'") | nonspace
    map_entry = space + map_pattern + space + value + space + semicolon
    map_block = Group(Group(map_statement).leaveWhitespace() + left_bracket + Group(ZeroOrMore(Group(comment | map_entry)) + space).leaveWhitespace() + right_bracket)
    block = Forward()
    block_begin = (Group(space + key + location_statement) ^ Group(if_statement) ^ Group(charset_map_statement)).leaveWhitespace()
    block_innards = Group(ZeroOrMore(Group(comment | assignment) | block | map_block) + space).leaveWhitespace()
    block << Group(block_begin + left_bracket + block_innards + right_bracket)
    script = OneOrMore(Group(comment | assignment) ^ block ^ map_block) + space + stringEnd
    return script.parseWithTabs().leaveWhitespace()


class UnspacedList(list):
    """After handling by create_parser(), there is white space existing in the list. Use this class to wrap a list
     [of lists], making any whitespace entries magically invisible"""

    def __init__(self, list_source):
        self.spaced = copy.deepcopy(list(list_source))
        self.dirty = False
        list.__init__(self, list_source)
        for i, entry in reversed(list(enumerate(self))):
            if isinstance(entry, list):
                sublist = UnspacedList(entry)
                list.__setitem__(self, i, sublist)
                self.spaced[i] = sublist.spaced
            elif self._spacey(entry):
                list.__delitem__(self, i)

    def _spacey(self, x):
        return isinstance(x, str) and x.isspace() or x == ''