# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/pyagram/entity_relationship_diagram.py
# Compiled at: 2016-08-06 03:52:29
# Size of source mod 2**32: 4246 bytes
import pyparsing as pp, re, inflect, pprint as p
from pyagram.diagram import Diagram

class EntityRelationshipDiagram(Diagram):

    def lexical_analysis(self, src):
        delimited = re.sub('\\s+', ' ', ' '.join(src.strip().split('\n'))).split(';')
        result = []
        for stmt in delimited:
            if stmt == '':
                return result
            string = pp.Regex('[a-zA-Z0-9=_]+')
            nums = pp.Regex('[0-9]+')
            ws = pp.OneOrMore(pp.White()).suppress()
            lp = pp.Regex('[(]').suppress()
            rp = pp.Regex('[)]').suppress()
            c = pp.Regex('[,]').suppress()
            q = pp.Regex("[']").suppress()
            table_name = string.setResultsName('table_name')
            create_table = (pp.Keyword('CREATE', caseless=True) + ws + pp.Keyword('TABLE', caseless=True) + ws + pp.Optional(pp.Keyword('IF', caseless=True) + ws + pp.Keyword('NOT', caseless=True) + ws + pp.Keyword('EXISTS', caseless=True))).suppress() + table_name + lp
            column_name = string.setResultsName('column_name')
            data_type = string.setResultsName('data_type')
            length = lp + nums.setResultsName('length') + rp
            nullable = (pp.Optional(pp.Keyword('NOT', caseless=True) + ws) + pp.Keyword('NULL', caseless=True)).setResultsName('nullable')
            default_value = pp.Keyword('DEFAULT', caseless=True).suppress() + ws + string.setResultsName('default_value')
            auto_increment = pp.Keyword('AUTO_INCREMENT', caseless=True).setResultsName('auto_increment')
            column = pp.Optional(ws) + column_name + ws + data_type + pp.Optional(pp.MatchFirst([length, ws + nullable, ws + default_value, ws + auto_increment])) + pp.Optional(pp.MatchFirst([ws + nullable, ws + default_value, ws + auto_increment])) + pp.Optional(pp.MatchFirst([ws + default_value, ws + auto_increment])) + pp.Optional(ws + auto_increment) + pp.Optional(ws) + c
            primary_key = pp.Keyword('PRIMARY KEY', caseless=True).suppress() + lp + pp.OneOrMore(q + string.setResultsName('primary_key') + q + pp.Optional(c)) + rp + pp.Optional(c)
            key = pp.Keyword('KEY', caseless=True).suppress() + lp + q + string.setResultsName('key') + q + pp.Optional(c) + rp + pp.Optional(c)
            parser = create_table + pp.OneOrMore(pp.Group(column)) + pp.Optional(primary_key) + pp.Optional(key) + rp + pp.OneOrMore(ws + string).suppress()
            result.append(parser.parseString(stmt, parseAll=True))

        return result

    def syntactic_analysis(self, src):
        i = inflect.engine()
        relations = {}
        foreign_keys = {}
        for table in src:
            for k, v in table.items():
                if k == 'table_name':
                    foreign_keys[(i.singular_noun(v) if i.singular_noun(v) else v) + '_id'] = v

        for table in src:
            for k, v in table.items():
                if k == 'table_name':
                    table_name = v

            for e in table:
                if 'column_name' in e and e['column_name'] in foreign_keys.keys():
                    relations[table_name + ':' + e['column_name']] = foreign_keys[e['column_name']] + ':id'

        result = {}
        result['src'] = src
        result['relations'] = relations
        return result

    def generate_dot(self, src):
        dot = 'digraph erd{\n\tnode [shape=record];\n'
        fontsetting = 'fontname="' + self.fontname + '"' if self.fontname else ''
        node_prop = ', '.join(filter(None, [fontsetting, 'style="rounded"']))
        dot += '\tnode [' + node_prop + '];\n'
        dot += '\tedge [' + fontsetting + '];\n'
        for table in src['src']:
            for k, v in table.items():
                if k == 'table_name':
                    dot += '\t' + v + ' [label="{[' + v + ']|'

            for e in table:
                if 'column_name' in e:
                    dot += '\t<' + e['column_name'] + '>' + e['column_name'] + '|'

            dot = dot[0:-1]
            dot += '}"];\n'

        for k, v in src['relations'].items():
            dot += '\t' + k + ' -> ' + v + ' [dir=none];\n'

        dot += '}'
        return dot