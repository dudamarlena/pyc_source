# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/electrum_chi/electrum/difficulty.py
# Compiled at: 2019-08-24 06:06:43
# Size of source mod 2**32: 3815 bytes
"""
The implementation of Xaya's difficulty retargeting with continuous changes
and two independent mining algorithms.
"""
from . import blockchain
from . import powdata
MAX_TARGET_NEOSCRYPT = 110427941548649020598956093796432407239217743554726184882600387580788735
NUM_BLOCKS = 24

def algo_log2_weight(algo: int) -> int:
    """
  Returns how much harder the given difficulty algorithm is (as an
  exponent of two) compared to SHA-256d.  This is used to compute chain
  work and also to adjust the minimum difficulty to the different
  algorithms.
  """
    if algo == powdata.ALGO_SHA256D:
        return 0
    if algo == powdata.ALGO_NEOSCRYPT:
        return 10
    raise AssertionError(f"Unknown algorithm: {algo}")


def max_target(algo: int) -> int:
    """
  Returns the maximum target for the given algorithm.
  """
    res = MAX_TARGET_NEOSCRYPT
    diff = algo_log2_weight(powdata.ALGO_NEOSCRYPT) - algo_log2_weight(algo)
    assert diff >= 0, diff
    res >>= diff
    return res


def get_target_spacing(algo: int, h: int) -> int:
    """
  Returns the targeted block time in seconds for the given algorithm at
  the given height.
  """
    if h < 440000:
        return 60
    if algo == powdata.ALGO_SHA256D:
        return 120
    if algo == powdata.ALGO_NEOSCRYPT:
        return 40
    raise AssertionError(f"Unknown algorithm: {algo}")


def get_target(getter, algo: int, h: int) -> int:
    """
  Returns the difficulty target that should be applied for the given algorithm
  at the given height.  getter must be a function that returns the block data
  needed (height, timestamp and bits) when called with (algo, height) tuples.
  """
    if h == 0:
        return blockchain.Blockchain.bits_to_target(504365040)
    limit = max_target(algo)
    last = getter(algo, h - 1)
    if last is None:
        return limit
    cur = last
    for n in range(1, NUM_BLOCKS + 1):
        target = blockchain.Blockchain.bits_to_target(cur['bits'])
        if n == 1:
            res = target
        else:
            res = (res * n + target) // (n + 1)
        if n < NUM_BLOCKS:
            cur = getter(algo, cur['height'] - 1)
            if cur is None:
                return limit

    actual_time = last['timestamp'] - cur['timestamp']
    next_height = last['height'] + 1
    target_time = NUM_BLOCKS * get_target_spacing(algo, next_height)
    if actual_time < target_time // 3:
        actual_time = target_time // 3
    if actual_time > target_time * 3:
        actual_time = target_time * 3
    res *= actual_time
    res //= target_time
    if res > limit:
        res = limit
    return res