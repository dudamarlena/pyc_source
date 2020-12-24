# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/operations/random.py
# Compiled at: 2019-06-14 18:22:47
# Size of source mod 2**32: 520 bytes
import numpy as np

def random_factor(max_card=3, max_scope=3, max_factor=10, min_factor=1, ftype=lambda x: x):
    n = np.random.randint(1, max_scope + 1)
    scope = apogee.legacy.random.urandint(min_factor, max_factor, size=(n,))
    card = np.random.randint(2, max_card + 1, n)
    return ftype(scope, card, np.ones(np.product(card)))


def random_factor_graph(n, gtype=lambda x: x, **kwargs):
    factors = []
    for i in range(n):
        factors.append(random_factor(**kwargs))

    return gtype(*factors)