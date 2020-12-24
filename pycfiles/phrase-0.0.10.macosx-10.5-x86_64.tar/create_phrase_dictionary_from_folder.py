# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/brentpayne/anaconda/lib/python2.7/site-packages/phrase/create_phrase_dictionary_from_folder.py
# Compiled at: 2014-08-28 17:58:28
from collections import Counter
import pickle
from pprint import pprint
from phrase.corpus import FileCorpus
from phrase.phrase_generation import generate_phrase_dictionary
__author__ = 'brentpayne'

def main():
    import sys
    print sys.argv
    folder = sys.argv[1]
    pkl_filename = sys.argv[2]
    options = {}
    corpus = FileCorpus()
    corpus.add_folder(folder)
    phrase_dictionary = generate_phrase_dictionary(corpus.get_iterator)
    counts = Counter()
    with open(pkl_filename, 'w') as (fp):
        pickle.dump(phrase_dictionary, fp)
    for doc in corpus.get_iterator():
        for line in doc:
            run = phrase_dictionary.process(line)
            for token_id in run:
                if token_id < 0:
                    counts[token_id] += 1

    pprint([ phrase_dictionary.get_phrase(token_id) for token_id, _ in counts.most_common(25) ])


if __name__ == '__main__':
    main()