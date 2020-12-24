# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/3.7/site-packages/tripgo_parser/multitripgo.py
# Compiled at: 2020-01-23 00:29:38
# Size of source mod 2**32: 963 bytes
import tripgoparserv2 as tgp, pandas as pd, logging, os
from functools import partial
from multiprocessing.pool import Pool
import multiprocessing
from time import time
logging.basicConfig(level=(logging.DEBUG), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger('requests').setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)

def getCompiledResults(i):
    csv = pd.read_csv('70120.csv')
    jsonData = tgp.openJson(csv.tripid[i], str(int(csv.startime[i]))).open()
    data = tgp.ODPair(jsonData, csv.tripid[i], str(int(csv.startime[i]))).compiled_results
    return data


def main():
    ts = time()
    with Pool(processes=4) as (pool):
        results = pool.map(getCompiledResults, range(10000))
        df = pd.DataFrame(results)
        df.to_csv('tester.csv')
    logging.info('Took %s seconds', time() - ts)


if __name__ == '__main__':
    main()