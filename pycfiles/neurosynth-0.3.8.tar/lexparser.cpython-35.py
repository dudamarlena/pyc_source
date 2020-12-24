# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tal/Dropbox/Code/neurosynth/neurosynth/base/lexparser.py
# Compiled at: 2015-08-25 12:25:05
# Size of source mod 2**32: 2717 bytes
""" Parsing expression grammar for feature-based study selection. """
from ply import lex
from ply import yacc
import pandas as pd, logging
logger = logging.getLogger('neurosynth.lexparser')

class Lexer(object):
    tokens = ('WORD', 'FLOAT', 'ANDNOT', 'OR', 'AND', 'LPAR', 'RPAR', 'LT', 'RT')
    t_ANDNOT = '\\&\\~'
    t_AND = '\\&'
    t_OR = '\\|'
    t_LPAR = '\\('
    t_RPAR = '\\)'
    t_LT = '\\<'
    t_RT = '\\>'
    t_ignore = ' \t'

    def __init__(self, dataset=None):
        self.dataset = dataset

    def t_WORD(self, t):
        r"""[a-zA-Z\_\-\*]+"""
        return t

    def t_FLOAT(self, t):
        r"""[0-9\.]+"""
        t.value = float(t.value)
        return t

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, optimize=1, **kwargs)

    def t_error(self, t):
        logger.error('Illegal character %s!' % t.value[0])
        t.lexer.skip(1)

    def test(self, data):
        self.lexer.input(data)
        while True:
            tok = self.lexer.token()
            if not tok:
                break
            print(tok)


class Parser(object):

    def __init__(self, lexer, dataset, threshold=0.001, func=sum):
        self.lexer = lexer
        self.dataset = dataset
        self.threshold = threshold
        self.func = func
        self.tokens = lexer.tokens

    def p_list_andnot(self, p):
        """list : list ANDNOT list"""
        p[0] = p[1][(set(p[1].index) - set(p[3].index))]

    def p_list_and(self, p):
        """list : list AND list"""
        p[0] = pd.concat([
         p[1], p[3]], axis=1).dropna().apply(self.func, axis=1)

    def p_list_or(self, p):
        """list : list OR list"""
        p[0] = pd.concat([
         p[1], p[3]], axis=1).fillna(0.0).apply(self.func, axis=1)

    def p_list_lt(self, p):
        """list : list LT freq"""
        p[0] = p[1][(p[1] < p[3])]

    def p_list_rt(self, p):
        """list : list RT freq"""
        p[0] = p[1][(p[1] >= p[3])]

    def p_feature_words(self, p):
        """feature : WORD WORD
                | feature WORD"""
        p[0] = ' '.join([p[1], p[2]])

    def p_list_feature(self, p):
        """list : feature
            | WORD """
        p[0] = self.dataset.get_studies(features=p[1], frequency_threshold=self.threshold, func=self.func, return_type='weights')

    def p_list_expr(self, p):
        """list : LPAR list RPAR"""
        p[0] = p[2]

    def p_freq_float(self, p):
        """freq : FLOAT"""
        p[0] = p[1]

    def build(self, **kwargs):
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_error(self, p):
        print(p)

    def parse(self, input):
        return self.parser.parse(input)