# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/max/code/oss/hyperopt/hyperopt/mix.py
# Compiled at: 2019-10-17 07:38:06
# Size of source mod 2**32: 1145 bytes
from builtins import zip
import numpy as np

def suggest(new_ids, domain, trials, seed, p_suggest):
    """Return the result of a randomly-chosen suggest function

    For example to search by sometimes using random search, sometimes anneal,
    and sometimes tpe, type:

        fmin(...,
            algo=partial(mix.suggest,
                p_suggest=[
                    (.1, rand.suggest),
                    (.2, anneal.suggest),
                    (.7, tpe.suggest),]),
            )

    Parameters
    ----------

    p_suggest: list of (probability, suggest) pairs
        Make a suggestion from one of the suggest functions,
        in proportion to its corresponding probability.
        sum(probabilities) must be [close to] 1.0

    """
    rng = np.random.RandomState(seed)
    ps, suggests = list(zip(*p_suggest))
    assert len(ps) == len(suggests) == len(p_suggest)
    if not np.isclose(sum(ps), 1.0):
        raise ValueError('Probabilities should sum to 1', ps)
    idx = rng.multinomial(n=1, pvals=ps).argmax()
    return suggests[idx](new_ids, domain, trials, seed=int(rng.randint(2147483648)))