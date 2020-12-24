# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/tests/test_web.py
# Compiled at: 2015-07-08 07:34:06
from __future__ import absolute_import, division, print_function
try:
    from gensim import corpora, models
    TFIDF = True
except ImportError:
    TFIDF = False

import pytest
from dossier.models.features import sip
from dossier.models.tests import kvl, store

@pytest.fixture
def tfidf():
    if not TFIDF:
        return
    doc1 = 'Andrew likes Diet Pepsi.'
    doc2 = 'Andrew knows the muffin man.'
    doc3 = 'Andrew lives near the muffin man on Shirley Lane.'
    corpus = map(sip.noun_phrases, [doc1, doc2, doc3])
    dictionary = corpora.Dictionary(corpus)
    bows = [ dictionary.doc2bow(tokens) for tokens in corpus ]
    return models.TfidfModel(bows, id2word=dictionary)