# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pedersen/pedersen.py
# Compiled at: 2018-09-19 04:57:57
from Crypto import Random
from Crypto.Random import random
from Crypto.Util import number

def generate(param):
    q = param[1]
    g = param[2]
    h = param[3]
    return (q, g, h)


class verifier:

    def setup(self, security):
        p = number.getPrime(2 * security, Random.new().read)
        q = 2 * p + 1
        g = number.getRandomRange(1, q - 1)
        s = number.getRandomRange(1, q - 1)
        h = pow(g, s, q)
        param = (
         p, q, g, h)
        return p

    def open(self, param, c, x, *r):
        result = 'False'
        q, g, h = generate(param)
        sum = 0
        for i in r:
            sum += i

        res = pow(g, x, q) * pow(h, sum, q) % q
        if c == res:
            result = 'True'
        return result

    def add(self, param, *cm):
        addCM = 1
        for x in cm:
            addCM *= x

        addCM = addCM % param[1]
        return addCM


class prover:

    def commit(self, param, x):
        q, g, h = generate(param)
        r = number.getRandomRange(1, q - 1)
        c = pow(g, x, q) * pow(h, r, q) % q
        return (c, r)