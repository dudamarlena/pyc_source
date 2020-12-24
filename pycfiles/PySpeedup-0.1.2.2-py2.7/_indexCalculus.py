# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyspeedup/algorithms/_indexCalculus.py
# Compiled at: 2017-02-25 12:54:13
from pyspeedup.algorithms import gcd
from pyspeedup.algorithms import divideMod
from pyspeedup.algorithms import invMod

def discreteLog(n, a, p, primes):
    """Uses index calculus to find n=a^m mod p using the list of primes provided."""
    nList = []
    temp = n
    for prime in primes:
        while temp % prime == 0:
            temp //= prime
            nList.append(prime)

    if temp != 1:
        nList.append(temp)
        primes.append(temp)
    primeEquations = []
    aPowM, m = (1, 0)
    while not (len(primeEquations) == len(primes) and sum([ sum(x[0:-1]) for x in primeEquations ]) == len(primes)) and m < p - 1:
        curList = []
        temp = 0
        while temp != 1 or m > p:
            aPowM, m = aPowM * a % p, m + 1
            if m >= p - 1:
                return None
            curList = []
            temp = aPowM
            for prime in primes:
                while temp % prime == 0:
                    temp //= prime
                    curList.append(prime)

        primeEquations.append([ curList.count(x) for x in primes ])
        primeEquations[(-1)].append(m)
        rowReduce(primeEquations, p - 1)

    out = 0
    for i in nList:
        out += primeEquations[primes.index(i)][(-1)]
        out %= p - 1

    return out


def rowReduce(lstList, p):
    """Takes a list of lists as a representation of rows of a matrix mod p, and reduces it."""
    length = min(len(lstList), len(lstList[0]) - 1)
    for i in range(0, length):
        if lstList[i][i] % p == 0 or gcd(lstList[i][i], p) != 1:
            for j in range(i, len(lstList)):
                if lstList[j][i] % p != 0 and gcd(lstList[j][i], p) == 1:
                    lstList.insert(i, lstList.pop(j))
                    break

            if lstList[i][i] % p == 0:
                continue
        for j in range(i + 1, len(lstList)):
            if lstList[j][i] % p == 0:
                continue
            try:
                scalingfactor = divideMod(lstList[j][i], lstList[i][i], p)
            except:
                scalingfactor = lstList[j][i] // lstList[i][i]

            for k in range(len(lstList[0])):
                lstList[j][k] -= scalingfactor * lstList[i][k]
                lstList[j][k] %= p

    for i in range(0, length):
        if lstList[i][i] % p == 0:
            continue
        if lstList[i][i] != 1:
            try:
                inv = invMod(lstList[i][i], p)
            except:
                inv = p // lstList[i][i] + 1

            lstList[i] = [ x * inv % p for x in lstList[i] ]
        for j in range(i):
            if lstList[j][i] % p == 0:
                continue
            try:
                inv = divideMod(lstList[j][i], lstList[i][i], p)
            except:
                continue

            for k in range(len(lstList[0])):
                lstList[j][k] -= inv * lstList[i][k]
                lstList[j][k] %= p

    for i in reversed(range(len(lstList))):
        if lstList[i] and not any(lstList[i][0:-1]):
            lstList.pop(i)

    return lstList