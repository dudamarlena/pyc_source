# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridjug/test/primes.py
# Compiled at: 2015-08-24 13:16:46
# Size of source mod 2**32: 261 bytes
from jug import TaskGenerator
from time import sleep

@TaskGenerator
def is_prime(n):
    sleep(0.1)
    for j in range(2, n - 1):
        if n % j == 0:
            return False

    return True


primes10 = list(map(is_prime, range(2, 11)))