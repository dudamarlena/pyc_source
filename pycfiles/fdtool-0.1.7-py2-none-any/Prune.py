# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\mburanos\Desktop\Python27\Scripts\GitHub\FDTool\fdtool\modules\Prune.py
# Compiled at: 2018-06-20 09:24:43
import binaryRepr, Apriori_Gen

def f(C_k, E, Closure, df, U):
    SetsToRemove = []
    for S in C_k:
        for X in [ x for x in Apriori_Gen.oneDown(C_k) if len(Closure[binaryRepr.toBin(x, U)]) > 1 ]:
            if set(X).issubset(set(S)):
                Closure[binaryRepr.toBin(S, U)] = Closure[binaryRepr.toBin(S, U)].union(Closure[binaryRepr.toBin(X, U)].difference(set(X)))
                if any(set(X) == set(E[EQ][1]) for EQ in range(len(E))):
                    SetsToRemove.append(S)
                    if len(X) == 1:
                        try:
                            df = df.drop(X, 1)
                        except (KeyError, ValueError, TypeError) as e:
                            pass

                    continue
                if set(S).issubset(Closure[binaryRepr.toBin(X, U)]):
                    SetsToRemove.append(S)
                    continue
                if set(U) == Closure[binaryRepr.toBin(S, U)]:
                    SetsToRemove.append(S)
                    continue

    return ([ Candidate for Candidate in C_k if Candidate not in SetsToRemove ], Closure, df)