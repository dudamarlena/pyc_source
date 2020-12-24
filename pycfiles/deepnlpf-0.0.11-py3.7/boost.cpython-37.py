# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/core/boost.py
# Compiled at: 2020-04-18 23:34:36
# Size of source mod 2**32: 626 bytes
"""[boost]
    https://realpython.com/python-concurrency/
"""
import psutil, pathos, ray
import pathos.pools as pp
import deepnlpf.log as log
from tqdm import tqdm

class Boost(object):

    def __init__(self):
        self.cpu_count = psutil.cpu_count()

    def multithreading(self, function, args, threads=4):
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=threads) as (executor):
            result = list(tqdm((executor.map(function, args)), desc='Processing sentence(s)'))
        return result