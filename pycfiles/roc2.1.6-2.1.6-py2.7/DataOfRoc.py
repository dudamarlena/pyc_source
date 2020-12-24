# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\ROC\DataOfRoc.py
# Compiled at: 2018-08-16 03:57:30
import matplotlib.pyplot as plt
from Analyze import Analyze
import os.path

def DataOfRoc(standard_path='truth', test_path='test'):
    db = []
    pos, db, temp = Analyze(standard_path, test_path)
    tp, fp = (0.0, 0.0)
    for i in range(len(db)):
        tp += db[i][0]
        fp += db[i][1]

    rate = fp / pos
    print ' checking wrong num=%f\n standard true num=%f\n recall rate=%f' % (tp, pos, rate)
    return (tp, pos, rate)


if __name__ == '__main__':
    DataOfRoc()