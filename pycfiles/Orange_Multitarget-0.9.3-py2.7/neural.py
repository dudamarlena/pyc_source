# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/_multitarget/neural.py
# Compiled at: 2012-11-23 17:14:54
"""
.. index:: Multi-target Neural Network Learner

********************************************************
Multi-target Neural Network Learner (``neural``)
********************************************************

"""
from Orange.classification.neural import NeuralNetworkLearner, NeuralNetworkClassifier
if __name__ == '__main__':
    import Orange, time
    print 'STARTED'
    global_timer = time.time()
    l = Orange.multitarget.neural.NeuralNetworkLearner(n_mid=20, reg_fact=0.1, max_iter=100)
    data = Orange.data.Table('multitarget:emotions.tab')
    res = Orange.evaluation.testing.cross_validation([l], data, 3)
    scores = Orange.multitarget.scoring.mt_average_score(res, Orange.evaluation.scoring.RMSE)
    for i in range(len(scores)):
        print res.classifierNames[i], scores[i]

    data = Orange.data.Table('multitarget:flare.tab')
    res = Orange.evaluation.testing.cross_validation([l], data, 3)
    scores = Orange.multitarget.scoring.mt_average_score(res, Orange.evaluation.scoring.RMSE)
    for i in range(len(scores)):
        print res.classifierNames[i], scores[i]

    print '--DONE %.2f --' % (time.time() - global_timer)