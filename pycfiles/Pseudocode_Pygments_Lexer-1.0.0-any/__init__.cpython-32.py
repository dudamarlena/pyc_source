# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pseudocode_lexer/__init__.py
# Compiled at: 2012-09-25 14:12:22
import re
from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.token import Error, Punctuation, Text, Comment, Operator, Keyword, Name, String, Number

class PseudocodeLexer(RegexLexer):
    """
    A Pseudo code (fr) lexer
    """
    name = 'Pseudocode'
    aliases = ['pseudocode', 'pseudo', 'algorithm', 'algo']
    filenames = ['*.algo', '*.pseudocode']
    mimetypes = []
    flags = re.IGNORECASE
    tokens = {'root': [
              (
               '\\/\\*.*\\*\\/', Comment),
              include('strings'),
              include('core'),
              (
               '[a-z][a-z0-9_]*', Name.Variable),
              include('nums'),
              (
               '[\\s]+', Text)], 
     'core': [
              (
               '\\b(debut|début|fin|si|alors|sinon|fin_si|tant_que|tantque|fin_tantque|faire|répéterrepeter|type|structure|fin_structure|fonction|procédure|procedure|retourner|renvoyer)\\s*\\b',
               Keyword),
              (
               '\\b(entier|chaine|chaîne|réel|reel|caractère|caractere|booléen|booleen)\\s*\\b',
               Keyword.Type),
              (
               '(\\*|\\+|-|\\/|<|>|<=|>=|=|<>|\\\\\\\\|mod|<-|←|≤|≥|≠|÷|×|:)',
               Operator),
              (
               '(\\(|\\)|\\,|\\;)',
               Punctuation),
              (
               '(:)',
               Keyword.Declaration),
              (
               '\\b(sqrt|pow|cos|sin|tan|arccos|arcsin|arctan|arctan2|lire|ecrire|écrire|exp|ln|log)\\s*\\b',
               Name.Builtin)], 
     'strings': [
                 (
                  '"([^"])*"', String.Double),
                 (
                  "'([^'])*'", String.Single)], 
     'nums': [
              (
               '\\d+(?![.Ee])', Number.Integer),
              (
               '[+-]?\\d*\\.\\d+([eE][-+]?\\d+)?', Number.Float),
              (
               '[+-]?\\d+\\.\\d*([eE][-+]?\\d+)?', Number.Float)]}