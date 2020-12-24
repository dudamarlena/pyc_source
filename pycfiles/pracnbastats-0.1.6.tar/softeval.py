# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/nyga/work/code/pracmln/python2/pracmln/mln/learning/softeval.py
# Compiled at: 2018-04-24 04:48:32


def truthDegreeGivenSoftEvidence(gf, worldValues, mln):
    return mln.getTruthDegreeGivenSoftEvidence(gf, worldValues)


def noisyOr(worldValues, disj, mln):
    return mln._noisyOr(worldValues, disj)