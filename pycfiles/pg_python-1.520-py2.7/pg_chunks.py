# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/pg_python/pg_chunks.py
# Compiled at: 2019-06-07 02:37:00
"""
This file contains the code for making chunks out of a line or a phrase.
"""

def acceptable_word(word):
    from spacy.lang.en.stop_words import STOP_WORDS
    accepted = bool(2 <= len(word) <= 40 and word.lower() not in STOP_WORDS)
    return accepted


def get_chunks(text):
    import spacy
    nlp = spacy.load('en')
    doc = nlp(text)
    chunks = []
    for np in doc.noun_chunks:
        chunk = np.text
        chunk = (' ').join([ word for word in chunk.split() if acceptable_word(word) ])
        chunks.append(chunk)

    return chunks


if __name__ == '__main__':
    text = 'Ar and mo various roads under sub divn m 2112 dg 2016 17 sh provision of maintenance van with required labour and t and p'
    print get_chunks(text)
    text = 'Construction of police station, fire station and rajkishore vidyapitha at arisol, infovalley,khurda '
    print get_chunks(text)
    text = 'Timber treatment impregnation plant '
    print get_chunks(text)
    text = 'Timber treatment impregnation plant '
    print get_chunks(text)