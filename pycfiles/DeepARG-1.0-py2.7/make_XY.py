# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deeparg/argdb/make_XY.py
# Compiled at: 2018-12-06 14:22:32
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
import theano
from collections import Counter
floatX = theano.config.floatX

def make_xy2(alignments):
    print 'getting sample names and matrix X'
    samples = alignments.keys()
    X = alignments.values()
    print 'getting labels'
    Y = [ i.split('|')[2] for i in samples ]
    Y_dict = {i:ix for ix, i in enumerate(set(Y))}
    Y_rev = {y:x for x, y in Y_dict.iteritems()}
    Y = np.array([ Y_dict[i] for i in Y ], dtype='int32')
    print 'Formating X to matrix'
    h = DictVectorizer(sparse=False)
    X = h.fit_transform(X)
    X = X.astype(floatX)
    feature_names = h.get_feature_names()
    print 'Normalizing the matrix X'
    min_max_scaler = preprocessing.MinMaxScaler()
    NX = min_max_scaler.fit_transform(X)
    print 'Feature selection'
    return {'samples': samples, 'X': X, 
       'Y': Y, 
       'X_red': NX, 
       'features': feature_names, 
       'Y_dict': Y_dict, 
       'Y_rev': Y_rev}