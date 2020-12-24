# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/kemlglearn/preprocessing/test.py
# Compiled at: 2016-03-30 05:35:00
"""
.. module:: test

test
*************

:Description: test

    

:Authors: bejar
    

:Version: 

:Created on: 13/03/2015 16:34 

"""
__author__ = 'bejar'
from kemlglearn.preprocessing import Discretizer
from sklearn.datasets import make_blobs, load_iris, make_circles
X = load_iris()['data']
print X.shape
disc = Discretizer(bins=3, method='frequency')
disc.fit(X)
print disc.intervals
disc = Discretizer(bins=3, method='equal')
disc.fit(X)
print disc.intervals