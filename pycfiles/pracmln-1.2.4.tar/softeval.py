# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/learning/softeval.py
# Compiled at: 2018-04-24 04:48:32


def truthDegreeGivenSoftEvidence(gf, worldValues, mln):
    return mln.getTruthDegreeGivenSoftEvidence(gf, worldValues)


def noisyOr(worldValues, disj, mln):
    return mln._noisyOr(worldValues, disj)