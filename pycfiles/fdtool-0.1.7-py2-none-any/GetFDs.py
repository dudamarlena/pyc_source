# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fdtool\modules\GetFDs.py
# Compiled at: 2018-06-19 13:38:40
import binaryRepr

def call_counter(func):

    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)

    helper.calls = 0
    helper.__name__ = func.__name__
    return helper


@call_counter
def CardOfPartition(Candidate, df):
    if len(Candidate) == 1:
        return df[Candidate[0]].nunique()
    else:
        return df.drop_duplicates(Candidate).count()[0]


def f(C_km1, df, Closure, U, Cardinality):
    F = []
    U_c = list(df.head(0))
    SubsetsToCheck = [ list(Subset) for Subset in set([ frozenset(Candidate + [v_i]) for Candidate in C_km1 for v_i in list(set(U_c).difference(Closure[binaryRepr.toBin(Candidate, U)])) ]) ]
    if len(C_km1[0]) == 1:
        SubsetsToCheck += C_km1
    for Cand, Card in zip(SubsetsToCheck, map(CardOfPartition, SubsetsToCheck, [df] * len(SubsetsToCheck))):
        Cardinality[binaryRepr.toBin(Cand, U)] = Card

    for Candidate in C_km1:
        for v_i in list(set(U_c).difference(Closure[binaryRepr.toBin(Candidate, U)])):
            if Cardinality[binaryRepr.toBin(Candidate, U)] == Cardinality[binaryRepr.toBin(Candidate + [v_i], U)]:
                Closure[binaryRepr.toBin(Candidate, U)].add(v_i)
                F.append([tuple(Candidate), v_i])

    return (
     Closure, F, Cardinality)