# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/controllers/wikiparser/special_characters.py
# Compiled at: 2006-11-21 20:30:39
"""fellowiki wiki parser: TODO support

TODO
    
"""
from parser import TextToken
NM_NO_DASH = 'n/m-dash: no dash'
M_DASH = 'm-dash'
N_DASH = 'n-dash'

def extend_wiki_parser(wiki_parser):
    wiki_parser.regexes[NM_NO_DASH] = (
     20, '----+', TextToken, dict())
    wiki_parser.regexes[M_DASH] = (21, '---', TextToken, dict(new_text='—'))
    wiki_parser.regexes[N_DASH] = (22, '--', TextToken, dict(new_text='–'))