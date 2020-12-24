# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/tomohiko/.virtualenvs/pygments-dmdl_py36/lib/python3.6/site-packages/dmdl/lexer.py
# Compiled at: 2017-08-03 01:25:37
# Size of source mod 2**32: 20044 bytes
__doc__ = '\n Copyright 2016 cocoatomo\n\n Licensed under the Apache License, Version 2.0 (the "License");\n you may not use this file except in compliance with the License.\n You may obtain a copy of the License at\n\n     http://www.apache.org/licenses/LICENSE-2.0\n\n Unless required by applicable law or agreed to in writing, software\n distributed under the License is distributed on an "AS IS" BASIS,\n WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n See the License for the specific language governing permissions and\n limitations under the License.\n'
from pygments.lexer import RegexLexer, include, default
from pygments.token import Text, Whitespace, Keyword, Name, Literal, String, Number, Operator, Punctuation, Comment

def list_with_separator(rule_name, element_rule, element_type, separator_rule, separator_type):
    sub_rule = '_following-' + rule_name
    element_rule_name = '_element-of-' + rule_name
    return {rule_name: [
                 include('skip'),
                 (
                  element_rule, element_type, ('#pop', sub_rule))], 
     
     sub_rule: [
                include('skip'),
                (
                 separator_rule, separator_type, element_rule_name),
                default('#pop')], 
     
     element_rule_name: [
                         include('skip'),
                         (
                          element_rule, element_type, '#pop')]}


class DmdlLexer(RegexLexer):
    name = 'Dmdl'
    aliases = ['dmdl']
    filenames = ['*.dmdl']
    import re
    flags = re.MULTILINE | re.DOTALL
    NAME = '[a-z]([a-z0-9])*(_[a-z0-9]+)*'
    PSEUDO_ELEMENT = '<.+?>'
    tokens = {'skip':[
      (
       '[ \\t\\r\\n]', Whitespace),
      (
       '/\\*', Comment.Multiline, 'block-comment'),
      (
       '--.*?$', Comment.Singleline),
      (
       '//.*?$', Comment.Singleline),
      (
       '\\.\\.\\.', Punctuation)], 
     'block-comment':[
      (
       '\\*/', Comment.Multiline, '#pop'),
      (
       '.', Comment.Multiline)], 
     'string-literal':[
      (
       '[^"\\\\]', String.Double),
      (
       '\\\\[btnfr\\\\"]', String.Double),
      (
       '\\\\0[0-3]?[0-7]?[0-7]', String.Double),
      (
       '"', String.Double, '#pop')], 
     'type':[
      include('skip'),
      (
       PSEUDO_ELEMENT, Keyword.Type, '#pop'),
      include('basic-type'),
      include('reference-type'),
      include('collection-type')], 
     'basic-type':[
      (
       'INT', Keyword.Type, '#pop'),
      (
       'LONG', Keyword.Type, '#pop'),
      (
       'BYTE', Keyword.Type, '#pop'),
      (
       'SHORT', Keyword.Type, '#pop'),
      (
       'DECIMAL', Keyword.Type, '#pop'),
      (
       'FLOAT', Keyword.Type, '#pop'),
      (
       'DOUBLE', Keyword.Type, '#pop'),
      (
       'TEXT', Keyword.Type, '#pop'),
      (
       'BOOLEAN', Keyword.Type, '#pop'),
      (
       'DATETIME', Keyword.Type, '#pop'),
      (
       'DATE', Keyword.Type, '#pop')], 
     'reference-type':[
      include('skip'),
      (
       NAME, Keyword.Type, '#pop')], 
     'collection-type':[
      include('skip'),
      (
       '\\{', Punctuation, ('#pop', 'collection-type-array-or-map'))], 
     'collection-type-array-or-map':[
      include('skip'),
      (
       ':', Punctuation, ('#pop', 'closing-curly-brace', 'type')),
      default(('#pop', 'closing-curly-brace', 'type'))], 
     'name':[
      include('skip'),
      (
       NAME, Name, '#pop')], 
     'name-or-pseudo-element':[
      include('skip'),
      (
       NAME, Name, '#pop'),
      (
       PSEUDO_ELEMENT, Name, '#pop')], 
     'literal':[
      include('skip'),
      (
       '"', String.Double, ('#pop', 'string-literal')),
      include('decimal-literal'),
      include('integer-literal'),
      include('boolean-literal')], 
     'integer-literal':[
      (
       '0', Number.Integer, '#pop'),
      (
       '[1-9][0-9]*', Number.Integer, '#pop')], 
     'decimal-literal':[
      (
       '\\.[0-9]+', Number.Float, '#pop'),
      (
       '0\\.[0-9]*', Number.Float, '#pop'),
      (
       '[1-9][0-9]*\\.[0-9]*', Number.Float, '#pop')], 
     'boolean-literal':[
      (
       'TRUE', Literal, '#pop'),
      (
       'FALSE', Literal, '#pop')], 
     'root':[
      include('skip'),
      (
       '"', String.Double, ('model-name-bind', 'attribute-list', 'description')),
      default(('model-name-bind', 'attribute-list'))], 
     'description':[
      default(('#pop', 'string-literal'))], 
     'attribute-list':[
      include('skip'),
      (
       '@', Name.Attribute, 'attribute'),
      default('#pop')], 
     'attribute':[
      include('skip'),
      default(('#pop', 'attribute-option-tuple', 'attribute-name'))], 
     'attribute-option-tuple':[
      include('skip'),
      (
       '\\(', Punctuation, ('#pop', 'attribute-option')),
      default('#pop')], 
     'attribute-option':[
      include('skip'),
      (
       '\\)', Punctuation, '#pop'),
      default(('#pop', 'attribute-element-list'))], 
     'attribute-element-list':[
      include('skip'),
      default(('#pop', 'following-attribute-element', 'attribute-element'))], 
     'following-attribute-element':[
      include('skip'),
      (
       '\\)', Punctuation, '#pop'),
      (
       ',', Punctuation, 'attribute-element')], 
     'attribute-element':[
      include('skip'),
      (
       '\\)', Punctuation, '#pop:2'),
      default(('#pop', 'attribute-value', 'bind', 'name'))], 
     'bind':[
      include('skip'),
      (
       '=', Operator, '#pop')], 
     'attribute-value':[
      include('skip'),
      (
       '\\{', Punctuation, ('#pop', 'attribute-value-array-or-map-1')),
      include('literal'),
      default(('#pop', 'qualified-name'))], 
     'attribute-value-array-or-map-1':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop'),
      (
       ':', Punctuation, ('#pop', 'closing-curly-brace')),
      (
       '(?=[".0-9TF])', Literal, ('#pop', 'attribute-value-array-or-map-2', 'literal')),
      default(('#pop', 'attribute-value-array'))], 
     'attribute-value-array-or-map-2':[
      include('skip'),
      (
       ':', Punctuation, ('#pop', 'following-attribute-pair', 'attribute-value')),
      default(('#pop', 'following-attribute-value'))], 
     'closing-curly-brace':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop')], 
     'attribute-value-array':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop'),
      default(('#pop', 'attribute-value-list'))], 
     'attribute-value-list':[
      include('skip'),
      default(('#pop', 'following-attribute-value', 'attribute-value'))], 
     'following-attribute-value':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop'),
      (
       ',', Punctuation, 'attribute-value-ext')], 
     'attribute-value-ext':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop:2'),
      default(('#pop', 'attribute-value'))], 
     'following-attribute-pair':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop'),
      (
       ',', Punctuation, 'attribute-pair-ext')], 
     'attribute-pair-ext':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop:2'),
      default(('#pop', 'attribute-pair'))], 
     'attribute-pair':[
      include('skip'),
      default(('#pop', 'attribute-value', 'colon', 'literal'))], 
     'colon':[
      include('skip'),
      (
       ':', Punctuation, '#pop')], 
     'model-name-bind':[
      include('skip'),
      (
       'projective(?![a-z0-9_])', Keyword.Type, ('#pop', 'record-expression', 'bind', 'model-name')),
      (
       'joined(?![a-z0-9_])', Keyword.Type, ('#pop', 'join-expression', 'bind', 'model-name')),
      (
       'summarized(?![a-z0-9_])', Keyword.Type, ('#pop', 'summarize-expression', 'bind', 'model-name')),
      default(('#pop', 'record-expression', 'bind', 'model-name'))], 
     'model-name':[
      include('skip'),
      (
       NAME, Name.Class, '#pop'),
      (
       PSEUDO_ELEMENT, Name.Class, '#pop')], 
     'record-expression':[
      include('skip'),
      default(('#pop', 'following-record-term', 'record-term'))], 
     'record-term':[
      include('skip'),
      (
       PSEUDO_ELEMENT, Name.Variable.Instance, '#pop'),
      (
       '\\{', Punctuation, ('#pop', 'property-definition')),
      default(('#pop', 'model-reference'))], 
     'following-record-term':[
      include('skip'),
      (
       ';', Punctuation, '#pop'),
      (
       '\\+', Operator, 'record-term')], 
     'property-definition':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop'),
      (
       '"', String.Double, ('end-of-declaration', 'property-definition-latter-half', 'name-or-pseudo-element',
 'attribute-list', 'description')),
      default(('end-of-declaration', 'property-definition-latter-half', 'name-or-pseudo-element',
         'attribute-list'))], 
     'property-definition-latter-half':[
      include('skip'),
      (
       ':', Punctuation, ('#pop', 'property-definition-with-type', 'type')),
      (
       '=', Operator, ('#pop', 'property-expression'))], 
     'property-definition-with-type':[
      include('skip'),
      (
       '=', Operator, ('#pop', 'property-expression')),
      default('#pop')], 
     'property-expression':[
      include('skip'),
      (
       '\\{', Punctuation, ('#pop', 'attribute-value-array-or-map-1')),
      default(('#pop', 'qualified-name'))], 
     'model-reference':[
      include('skip'),
      (
       NAME, Name.Class, '#pop'),
      (
       PSEUDO_ELEMENT, Name.Class, '#pop')], 
     'join-expression':[
      include('skip'),
      default(('#pop', 'following-join-term', 'join-term'))], 
     'join-term':[
      include('skip'),
      default(('#pop', 'grouping', 'model-mapping', 'model-reference'))], 
     'model-mapping':[
      include('skip'),
      (
       '->', Operator, ('#pop', 'model-mapping-body')),
      default('#pop')], 
     'model-mapping-body':[
      include('skip'),
      (
       '\\{', Punctuation, ('#pop', 'property-mapping')),
      (
       PSEUDO_ELEMENT, Name.Variable.Instance, '#pop')], 
     'property-mapping':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop'),
      (
       '"', String.Double, ('end-of-declaration', 'name-or-pseudo-element', 'mapping-arrow', 'name-or-pseudo-element',
 'attribute-list', 'description')),
      default(('end-of-declaration', 'name-or-pseudo-element', 'mapping-arrow', 'name-or-pseudo-element',
         'attribute-list'))], 
     'mapping-arrow':[
      include('skip'),
      (
       '->', Operator, '#pop')], 
     'grouping':[
      include('skip'),
      (
       '%', Operator, ('#pop', 'property-list')),
      default('#pop')], 
     'following-join-term':[
      include('skip'),
      (
       ';', Punctuation, '#pop'),
      (
       '\\+', Operator, 'join-term')], 
     'summarize-expression':[
      include('skip'),
      default(('#pop', 'following-summarize-term', 'summarize-term'))], 
     'summarize-term':[
      include('skip'),
      default(('#pop', 'grouping', 'model-folding', 'model-name'))], 
     'model-folding':[
      include('skip'),
      (
       '=>', Operator, ('#pop', 'model-folding-body'))], 
     'model-folding-body':[
      include('skip'),
      (
       '\\{', Punctuation, ('#pop', 'property-folding'))], 
     'property-folding':[
      include('skip'),
      (
       '\\}', Punctuation, '#pop'),
      (
       '"', String.Double, ('end-of-declaration', 'name-or-pseudo-element', 'mapping-arrow', 'name-or-pseudo-element',
 'aggregator', 'attribute-list', 'description')),
      default(('end-of-declaration', 'name-or-pseudo-element', 'mapping-arrow', 'name-or-pseudo-element',
         'aggregator', 'attribute-list'))], 
     'aggregator':[
      include('skip'),
      (
       'any(?![a-z0-9_])', Name.Function, '#pop'),
      (
       'sum(?![a-z0-9_])', Name.Function, '#pop'),
      (
       'max(?![a-z0-9_])', Name.Function, '#pop'),
      (
       'min(?![a-z0-9_])', Name.Function, '#pop'),
      (
       'count(?![a-z0-9_])', Name.Function, '#pop'),
      (
       PSEUDO_ELEMENT, Name.Function, '#pop')], 
     'following-summarize-term':[
      include('skip'),
      (
       ';', Punctuation, '#pop'),
      (
       '\\+', Operator, 'summarize-term')], 
     'end-of-declaration':[
      include('skip'),
      (
       ';', Punctuation, '#pop')]}
    tokens.update(list_with_separator('attribute-name', NAME, Name.Attribute, '\\.', Name.Attribute))
    tokens.update(list_with_separator('qualified-name', NAME, Name, '\\.', Name))
    tokens.update(list_with_separator('property-list', '|'.join([NAME, PSEUDO_ELEMENT]), Name, ',', Punctuation))


def debug(code):
    dl = DmdlLexer()
    for t in dl.get_tokens_unprocessed(code):
        print(t)


if __name__ == '__main__':
    import sys
    sys.exit(debug(sys.argv[1]))