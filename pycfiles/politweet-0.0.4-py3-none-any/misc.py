# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/bhugo/workspace/politsiyakat/politsiyakat/data/misc.py
# Compiled at: 2018-04-12 08:03:22
import numpy as np

def baseline_index(a1, a2, no_antennae):
    """
   Computes unique index of a baseline given antenna 1 and antenna 2
   (zero indexed) as input. The arrays may or may not contain
   auto-correlations.

   There is a quadratic series expression relating a1 and a2
   to a unique baseline index(can be found by the double difference
   method)

   Let slow_varying_index be S = min(a1, a2). The goal is to find
   the number of fast varying terms. As the slow
   varying terms increase these get fewer and fewer, because
   we only consider unique baselines and not the conjugate
   baselines)
   B = (-S ^ 2 + 2 * S *  # Ant + S) / 2 + diff between the
   slowest and fastest varying antenna

  :param a1: array of ANTENNA_1 ids
  :param a2: array of ANTENNA_2 ids
  :param no_antennae: number of antennae in the array
  :return: array of baseline ids
  """
    if a1.shape != a2.shape:
        raise ValueError('a1 and a2 must have the same shape!')
    slow_index = np.min(np.array([a1, a2]), axis=0)
    return slow_index * (-slow_index + (2 * no_antennae + 1)) // 2 + np.abs(a1 - a2)


def uv_dist_per_baseline(no_baselines, nant, antenna_positions):
    """
  Given antenna positions in an earth centric earth fixed frame
  compute the unscaled uv distance per baseline
  :param no_baselines: Number of baselines
  :param nant: Number of antennae
  :param antenna_positions: array of [X,Y,Z] ITRS antenna positions
                            as found in a MS ANTENNA table
  return array of uv distances per unique baseline index
  """
    uv_dist_sq = np.zeros([no_baselines])
    relative_position_a0 = antenna_positions - antenna_positions[0]
    lbound = 0
    bi = 0
    for a0 in xrange(lbound, nant):
        for a1 in xrange(a0, nant):
            uv_dist_sq[bi] = np.sum((relative_position_a0[a0] - relative_position_a0[a1]) ** 2)
            bi += 1

        lbound += 1

    return np.sqrt(uv_dist_sq)


def ants_from_baseline(bl, nant):
    """
  Given unique baseline index and number of antennae lookup the corresponding
  antenna indicies (zero-indexed).
  :param bl: unique baseline index
  :param nant: number of antennae
  :return: pair of antenna indicies corresponding to unique index
  """
    lmat = np.triu((np.cumsum(np.arange(nant)[None, :] >= np.arange(nant)[:, None]) - 1).reshape([nant, nant]))
    v = np.argwhere(lmat == bl)
    return (
     v[(0, 0)], v[(0, 1)])