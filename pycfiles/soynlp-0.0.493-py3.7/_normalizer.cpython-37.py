# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soynlp/tokenizer/_normalizer.py
# Compiled at: 2018-10-01 05:46:57
# Size of source mod 2**32: 1452 bytes
import re
from soynlp.hangle import decompose, compose
repeatchars_patterns = [
 re.compile('(\\w\\w\\w\\w)\\1{3,}'),
 re.compile('(\\w\\w\\w)\\1{3,}'),
 re.compile('(\\w\\w)\\1{3,}'),
 re.compile('(\\w)\\1{3,}')]

def normalize(sentence, num_repeat=2):
    tokens = sentence.split()
    return ' '.join((_normalize_korean_token(token, num_repeat) for token in tokens))


def _normalize_korean_token(token, num_repeat=2):
    token = _normalize_emoji(token)
    token = _remove_repeat(token, num_repeat)
    return token


def _remove_repeat(token, num_repeat=2):
    if num_repeat > 0:
        for pattern in repeatchars_patterns:
            token = pattern.sub('\\1' * num_repeat, token)

    return token


def _normalize_emoji(token):
    if len(token) <= 1:
        return token
    token_ = []
    decomposeds = [decompose(c) for c in token]
    for char, cd, nd in zip(token, decomposeds, decomposeds[1:]):
        if not cd == None:
            if nd == None:
                token_.append(char)
                continue
            if nd[1] == ' ':
                if cd[2] == nd[0]:
                    token_.append(compose(cd[0], cd[1], ' ') + nd[0])
            if cd[2] == ' ':
                if nd[0] == ' ':
                    if cd[1] == nd[1]:
                        token_.append(cd[0] + cd[1] if cd[0] != ' ' else cd[1])
            token_.append(char)

    return ''.join(token_) + token[(-1)]