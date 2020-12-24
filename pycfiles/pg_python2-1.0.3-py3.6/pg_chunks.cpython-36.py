# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_chunks.py
# Compiled at: 2018-08-03 07:58:28
# Size of source mod 2**32: 2245 bytes
"""
This file contains the code for making chunks out of a line or a phrase.
"""
import nltk
from nltk.corpus import stopwords
stopwords = stopwords.words('english')

def leaves(tree):
    """Finds NP (nounphrase) leaf nodes of a chunk tree."""
    for subtree in tree.subtrees(filter=(lambda t: t.label() == 'NP')):
        yield subtree.leaves()


def normalise(word):
    """Normalises words to lowercase and stems and lemmatizes it."""
    word = word.lower()
    word = lemmatizer.lemmatize(word)
    return word


def acceptable_word(word):
    """Checks conditions for acceptable word: length, stopword."""
    accepted = bool(2 <= len(word) <= 40 and word.lower() not in stopwords)
    return accepted


sentence_re = '(?x)      # set flag to allow verbose regexps\n      ([A-Z])(\\.[A-Z])+\\.?  # abbreviations, e.g. U.S.A.\n    | \\w+(-\\w+)*            # words with optional internal hyphens\n    | \\$?\\d+(\\.\\d+)?%?      # currency and percentages, e.g. $12.40, 82%\n    | \\.\\.\\.                # ellipsis\n    | [][.,;"\'?():-_`]      # these are separate tokens\n'
lemmatizer = nltk.WordNetLemmatizer()
stemmer = nltk.stem.porter.PorterStemmer()
grammar = '\n    NBAR:\n        {<NN.*|JJ>*<NN.*>}  # Nouns and Adjectives, terminated with Nouns\n\n    NP:\n        {<NBAR>}\n        {<NBAR><IN><NBAR>}  # Above, connected with in/of/etc...\n'

def get_chunks(text):
    terms = []
    chunker = nltk.RegexpParser(grammar)
    toks = nltk.regexp_tokenize(text, sentence_re)
    postoks = nltk.tag.pos_tag(toks)
    tree = chunker.parse(postoks)
    for leaf in leaves(tree):
        term = [normalise(w) for w, t in leaf if acceptable_word(w)]
        terms.append(' '.join(term))

    return terms


if __name__ == '__main__':
    txt = 'Ar and mo various roads under sub divn m 2112 dg 2016 17 sh provision of maintenance van with required \n    labour and t and p'
    print(get_chunks(txt))
    txt = 'Construction of police station, fire station and rajkishore vidyapitha at arisol, infovalley,khurda '
    print(get_chunks(txt))
    txt = 'Timber treatment impregnation plant '
    print(get_chunks(txt))