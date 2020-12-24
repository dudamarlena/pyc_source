# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/models/tests/test_soft_selectors.py
# Compiled at: 2015-07-08 07:34:06
from dossier.models.soft_selectors import make_ngram_corpus

def test_make_ngram_corpus():
    corpus_clean_visibles = [
     '\nEnlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture \n',
     '\nEnlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture \n',
     '\nEnlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture \n',
     '\nEnlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture \n',
     '\nEnlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture Enlarge Picture \n',
     '\nto decipher a hastily scribbled note\n',
     '\nto decipher a hastily scribbled note\n',
     '\nto decipher a hastily scribbled note\n',
     '\nto decipher a hastily scribbled note\n',
     '\nto decipher a hastily scribbled note\n']
    candidates = make_ngram_corpus(corpus_clean_visibles, 6, True)
    count = 0
    for c in candidates:
        if not c:
            continue
        assert c == ['to decipher a hastily scribbled note']
        count += 1

    assert count == 5