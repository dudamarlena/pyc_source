# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/tables.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: TODO
    
"""
from parser import XMLElement, ParagraphToken, WHITESPACE, STRUCTUREMOD, LINEBREAK, EncapsulateToken
ENCAPSULATE_TABLE = 'encapsulate table'
TABLE_START = 'table start tag'
TABLE_MID = 'table middle tag'
TABLE_END = 'table end tag'
TABLE_RESULT = 'table result'
TABLE_SEPARATOR = 'table separator'

def _lists_to_table(table_lists):
    col_num = max([ len(row) for row in table_lists ])
    xhtml_table = XMLElement('table')
    xhtml_table.attributes['class'] = 'wiki-table'
    for row in table_lists:
        xhtml_row = XMLElement('tr')
        xhtml_table.append(xhtml_row)
        for item in row:
            if item is None:
                if xhtml_row.is_empty():
                    xhtml_item = XMLElement('td')
                    xhtml_row.append(xhtml_item)
                else:
                    attributes = xhtml_row.content[(-1)].attributes
                    attributes['colspan'] = str(int(attributes.get('colspan', 1)) + 1)
            else:
                (content, modifiers) = item
                content.xhtml.tag = 'td'
                for (key, value) in modifiers.items():
                    if key in ('align', 'valign'):
                        content.xhtml.attributes[key] = value

                xhtml_row.append(content.xhtml)

        attributes = xhtml_row.content[(-1)].attributes
        colspan = int(attributes.get('colspan', 1)) + col_num - len(row)
        if colspan > 1:
            attributes['colspan'] = str(colspan)

    return xhtml_table


class TableResultToken(ParagraphToken):
    __module__ = __name__

    def __init__(self, table_rows, token):
        ParagraphToken.__init__(self, token)
        self.rows = table_rows
        self.table_xhtml = XMLElement('table')
        self.xhtml.append(self.table_xhtml)

    def evaluate(self, result, tokens, state, procs):
        if len(tokens) >= 2 and tokens[0].is_a(LINEBREAK) and tokens[1].is_a(TABLE_RESULT):
            next_token = tokens.pop(0)
            next_token = tokens.pop(0)
            self.token += next_token.token
            self.rows.extend(next_token.rows)
        else:
            xhtml = _lists_to_table(self.rows)
            self.table_xhtml.clone(xhtml)
        ParagraphToken.evaluate(self, result, tokens, state, procs)

    def do_extended_close(self, inserted_token):
        inserted_token.xhtml.append(*self.xhtml.content)

    def is_a(self, *capabilities):
        return TABLE_RESULT in capabilities or ParagraphToken.is_a(self, *capabilities)


class TableToken(EncapsulateToken):
    __module__ = __name__

    def __init__(self, token, *args, **kwargs):
        EncapsulateToken.__init__(self, token, *args, **kwargs)
        self.STATE = ENCAPSULATE_TABLE
        self.table_row = []
        self.table_rows = []
        self.modifiers = {}

    def evaluate(self, result, tokens, state, procs):
        while len(tokens) > 0 and tokens[0].is_a(WHITESPACE, STRUCTUREMOD):
            next_token = tokens.pop(0)
            try:
                next_token.modify(self.modifiers)
            except AttributeError:
                self.consumed_whitespace_right = True
                self.token = self.token + ' '

        if self.type == '_' and len(tokens) > 0 and tokens[0].is_a(LINEBREAK):
            self.type = ')'
        EncapsulateToken.evaluate(self, result, tokens, state, procs)

    def render(self, new_token):
        EncapsulateToken.render(self, new_token)
        if len(self.table_rows) > 0:
            self.result.append(TableResultToken(self.table_rows, ''))

    def insert_result(self, match, result_token):
        if match.type == '(':
            if len(self.tokens) >= 2 and self.tokens[0].is_a(LINEBREAK) and self.tokens[1].is_a(TABLE_SEPARATOR) and self.tokens[1].type == '(':
                self.tokens.pop(0)
                new_table = self.tokens[0]
                new_table.table_rows = self.table_rows
            else:
                self.tokens.insert(0, TableResultToken(self.table_rows, self.token))
        elif match.type == '_':
            self.tokens.insert(0, self)

    def close(self, match, new_token):
        if new_token.xhtml.is_not_empty() or self.consumed_whitespace_left or match.consumed_whitespace_right:
            self.table_row.insert(0, (new_token, match.modifiers))
        else:
            self.table_row.insert(0, None)
        if match.type == '(':
            self.table_rows = match.table_rows
            self.table_rows.append(self.table_row)
        EncapsulateToken.close(self, match, new_token)
        return

    def is_a(self, *capabilities):
        return TABLE_SEPARATOR in capabilities or EncapsulateToken.is_a(self, *capabilities)


def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[TABLE_START] = (
     10, '^\\|', TableToken, dict(type='(', preference=30))
    wiki_parser.regexes[TABLE_MID] = (11, '\\|', TableToken, dict(type='_', preference=30))
    wiki_parser.regexes[TABLE_END] = (10, '\\|$', TableToken, dict(type=')', preference=30))