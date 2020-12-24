# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/TAMO/util/WMWtest.py
# Compiled at: 2019-04-23 02:08:32
__doc__ = '\nRoutines and interface for computing Mann-Whitney (Wilcoxon two-sample test)\n\nCopyright (2005) Whitehead Institute for Biomedical Research (except as noted below)\nAll Rights Reserved\n\nAuthor: David Benjamin Gordon\n\n##\n## Ported from perl code obtained from:\n## http://www.fon.hum.uva.nl/Service/Statistics/Wilcoxon_Test.html\n\n## COMMENTS are from original PERL code, which had the following\n## information included in it:\n##\n##     Copyright (C) 1996, 2001  Rob van Son\n##     \n##     This program is free software; you can redistribute it and/or\n##     modify it under the terms of the GNU General Public License\n##     as published by the Free Software Foundation; either version 2\n##     of the License, or (at your option) any later version.\n##     \n##     This program is distributed in the hope that it will be useful,\n##     but WITHOUT ANY WARRANTY; without even the implied warranty of\n##     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n##     GNU General Public License for more details.\n##     \n##     You should have received a copy of the GNU General Public License\n##     along with this program(*); if not, write to the Free Software\n##     Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.\n\n#############################################################################\n## (*) Note: TAMO does not redistribute any source code from Rob van Son ####\n#############################################################################\n\n'
from TAMO.util import Arith
from math import *
import sys

def k_out_n(k, n):
    kn = 1.0
    while k > 0:
        kn *= float(n) / float(k)
        n = n - 1
        k = k - 1

    return kn


def CountSmallerRanks(W, Sum, m, Start, RankList):
    i, Temp, Smaller, End, mminus1 = (0, 0, 0, 0, 0)
    if Sum > W:
        return 0
    End = len(RankList)
    if m > 0:
        mminus1 = m - 1
        for i in range(Start, End - m):
            Temp = Sum + Ranklist[i]
            if Temp > W:
                return Smaller
            Smaller += CountSmallerRanks(W, Temp, mminus1, i + 1, Ranklist)

    else:
        if Sum + End + 1 <= W:
            return End - Start + 1
        for i in range(Start, End):
            Temp = Sum + RankList[i]
            if Temp <= W:
                Smaller += 1
            else:
                return Smaller

    return Smaller


def main():
    A = [ float(x.strip()) for x in open(sys.argv[1]).readlines() ]
    B = [ float(x.strip()) for x in open(sys.argv[2]).readlines() ]
    p, W = wlcxtest(A, B)
    print '%5.4g  ( %f )' % (p, W)


def WMWtest(A, B):
    """
    WMWtest(A,B) -- Computes the Wilcoxon-Mann-Whitney nonparametric W statistic for two distributions

    input:  list of numbers, list of numbers
    output: p-value, W-statistic
    """
    A.sort()
    B.sort()
    TotalList = A + B
    TotalList.sort()
    nA = len(A)
    nB = len(B)
    N = nA + nB
    MaxSum = N * (N + 1) / 2.0
    H0 = MaxSum / 2.0
    previous = []
    start = 0
    Total_rank = TotalList[:]
    for i in range(len(TotalList)):
        if TotalList[i] == previous:
            mean_rank = (start + i + 2) / 2.0
            for j in range(start, i + 1):
                Total_rank[j] = mean_rank

        else:
            Total_rank[i] = i + 1
            previous = TotalList[i]
            start = i

    if nA < nB:
        shortest = A
    else:
        shortest = B
    nShortest = len(shortest)
    W = 0
    for Value in shortest:
        i = 0
        while i < len(TotalList) and Value != TotalList[i]:
            i += 1

        W += Total_rank[i]

    if W > H0:
        W = MaxSum - W
    p = 0
    Permutations = k_out_n(nA, N)
    if Permutations >= 25000 or nShortest > 10:
        if W >= H0:
            Continuity = -0.5
        else:
            Continuity = 0.5
        Z = (W + Continuity - nShortest * (N + 1.0) / 2.0) / sqrt(nA * nB * (N + 1) / 12.0)
        Z = fabs(Z)
        p = 2 * (1 - Arith.lzprob(Z))
    if nShortest + 1 < 10 and p < 0.25 and Permutations < 60000:
        Less = CountSmallerRanks(W, 0, len(shortest) - 1, 0, Total_rank)
        if 2 * Less > Permutations:
            Less = CountSmallerRanks(W - 1, 0, len(shortest) - 1, 0, Total_rank)
            Less = Permutations - Less
        SumFrequencies = Permutations
        p = 2.0 * Less / SumFrequencies
    return (
     p, W)


if __name__ == '__main__':
    main()