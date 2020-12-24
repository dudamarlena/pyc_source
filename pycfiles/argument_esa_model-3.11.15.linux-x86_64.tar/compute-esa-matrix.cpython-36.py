# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/argument_esa_model/compute-esa-matrix.py
# Compiled at: 2020-05-12 09:02:27
# Size of source mod 2**32: 796 bytes
import pickle
from matrix import ESAMatrix
from preprocessor import Preprocessor

def main():
    for corpus in ('strategic-intelligence', 'debatepedia', 'wikipedia'):
        corpus_path = '../../../../resources/corpora/' + corpus + '.csv'
        matrix_path = '../../../../resources/esa-w2v/' + corpus + '.mat'
        p = Preprocessor()
        preprocessed = p.preprocess(corpus_path, lemma=True)
        concepts = tuple(preprocessed.keys())
        bows = tuple([preprocessed[bow] for bow in preprocessed])
        terms = tuple(set([word for bow in bows for word in bow]))
        print(len(concepts))
        print(len(bows))
        print(len(terms))
        mat = ESAMatrix(terms, concepts, bows)
        pickle.dump(mat, open(matrix_path, 'wb'))


if __name__ == '__main__':
    main()