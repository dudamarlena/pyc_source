# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gridjug/test/failing.py
# Compiled at: 2015-08-24 13:16:46
# Size of source mod 2**32: 306 bytes
from time import sleep
from jug import TaskGenerator

@TaskGenerator
def is_prime(n):
    sleep(0.1)
    if n == 6:
        raise RuntimeError
    for j in range(2, n - 1):
        if n % j == 0:
            return False

    return True


primes10 = list(map(is_prime, range(2, 11)))