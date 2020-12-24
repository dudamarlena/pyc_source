# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\squeak\entropy.py
# Compiled at: 2015-01-23 10:06:10
import pandas as pd
rx = pd.read_csv('data/rx.csv')
ry = pd.read_csv('data/ry.csv')
x = rx.iloc[0]
y = ry.iloc[0]
nx = pd.read_csv('data/nx.csv')
ny = pd.read_csv('data/ny.csv')
x = nx.iloc[0]
y = ny.iloc[0]
dx = x.diff()

def sample_entropy(ts, edim=2, r=0.2 * np.std(ts), tau=1):
    N = len(ts)
    correl = []
    datamat = np.zeros((edim + 1, N - edim - 1))
    for i in range(1, edim + 1 + 1):
        datamat[i - 1] = ts[i - 1:N - edim + i - 2]

    for m in [edim, edim + 1]:
        count = np.zeros((1, N - edim - 1))
        tempmat = datamat[:m,]
        for i in range(N - m - 1):
            a = tempmat[..., i:N - edim - 1]
            b = np.transpose([tempmat[(..., i - 1)]] * (N - edim - i - 1))
            X = np.abs(a - b)
            dst = np.max(X, axis=0)
            d = dst < r
            count[(..., i)] = float(sum(d)) / (N - edim)

        correl.append(sum(count) / (N - edim))

    return np.log(correl[0] / correl[1])


def approx_entropy(ts, edim=2, r=0.2 * sd(ts), elag=1):
    N = len(ts)
    result = []
    for j in [1, 2]:
        m = edim + j - 1
        phi = []
        dataMat = np.zeros((m, N - m + 1))
        for i in range(m):
            dataMat[(i,)] = ts[i:N - m + i + 1]

        for i in range(N - m + 1):
            rep = np.transpose([dataMat[(..., i - 1)]] * (N - m + 1))
            tempMat = np.abs(dataMat - rep)
            boolMat = np.max(tmpMat > r, axis=0)
            phi.append(float(np.sum(~boolMat)) / (N - m + 1))