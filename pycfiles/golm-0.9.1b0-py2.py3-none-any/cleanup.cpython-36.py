# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/core/nlp/cleanup.py
# Compiled at: 2018-04-15 15:31:50
# Size of source mod 2**32: 1468 bytes
import re
from core.nlp.tools.czech_stemmer import cz_stem_all
from core.nlp.tools.porter2 import Stemmer
from core.nlp.tools.toktok import ToktokTokenizer
tokenizer = ToktokTokenizer()
stemmers = {'en':Stemmer('en').stemWords, 
 'cz':cz_stem_all}

def tokenize(text: str, stemming=False, language='en'):
    """
    Tokenizes text, optionally stemming the tokens.
    :param text:        Text to be tokenized.
    :param stemming:    Boolean, enables stemming.
                        Default is false.
    :param language:    Stemming language. Default is 'en'.
    :return:
    """
    tokens = tokenizer.tokenize(text)
    if stemming:
        stemmer = stemmers.get(language)
        if not stemmer:
            raise Exception('No known stemmer for language {}!'.format(language))
        tokens = [s.lower() for s in stemmer(tokens)]
    return [str(token).lower() for token in tokens]


def build_imputation_rules(imputation: dict):
    rules = []
    for item in imputation:
        stem, suffixes, nearest = item['stem'], item['suffixes'], item['nearest']
        regex = re.escape(stem) + '(?:' + '|'.join([re.escape(suffix) for suffix in suffixes]) + ')'
        rule = (regex, nearest)
        rules.append(rule)

    return rules


def imputer(tokens: list, rules: dict):
    for i, token in enumerate(tokens):
        for regex, nearest in rules:
            if re.match(regex, token):
                tokens[i] = nearest

    return tokens