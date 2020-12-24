# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/drqascripts/retriever/prep_wikipedia.py
# Compiled at: 2019-08-29 06:03:42
# Size of source mod 2**32: 1135 bytes
"""Preprocess function to filter/prepare Wikipedia docs."""
import regex as re
from html.parser import HTMLParser
PARSER = HTMLParser()
BLACKLIST = set(['23443579', '52643645'])

def preprocess(article):
    for k, v in article.items():
        article[k] = PARSER.unescape(v)

    if article['id'] in BLACKLIST:
        return
    if '(disambiguation)' in article['title'].lower():
        return
    if '(disambiguation page)' in article['title'].lower():
        return
    else:
        if re.match('(List of .+)|(Index of .+)|(Outline of .+)', article['title']):
            return
        return {'id':article['title'],  'text':article['text']}