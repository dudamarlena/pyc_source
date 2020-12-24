# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: fdtool\modules\Apriori_Gen.py
# Compiled at: 2018-06-19 13:38:40


def powerset(s):
    x = len(s)
    Powerset = []
    for i in range(1 << x):
        Powerset.append([ s[j] for j in range(x) if i & 1 << j ])

    return Powerset


def oneUp(C_km1):
    flat_list = list(set([ item for sublist in C_km1 for item in sublist ]))
    AttributeSubsets = (Subset for Subset in powerset(flat_list))
    return [ Subset for Subset in AttributeSubsets if len(Subset) == len(next(iter(C_km1))) + 1 ]


def oneDown(C_k):
    flat_list = list(set([ item for sublist in C_k for item in sublist ]))
    AttributeSubsets = (Subset for Subset in powerset(flat_list))
    return [ Subset for Subset in AttributeSubsets if len(Subset) == len(next(iter(C_k))) - 1 ]