# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fundamentals/fmultiprocess.py
# Compiled at: 2020-04-17 06:44:40
"""
*A function to quickly add multiprocessing to any program*

:Author:
    David Young
"""
from __future__ import division
from past.utils import old_div
import sys, os
os.environ['TERM'] = 'vt100'
from fundamentals import tools
from multiprocess import cpu_count, Pool
from functools import partial
import inspect, psutil

def fmultiprocess(log, function, inputArray, poolSize=False, timeout=3600, **kwargs):
    """multiprocess pool

    **Key Arguments**

    - ``log`` -- logger
    - ``function`` -- the function to multiprocess
    - ``inputArray`` -- the array to be iterated over
    - ``poolSize`` -- limit the number of CPU that are used in multiprocess job
    - ``timeout`` -- time in sec after which to raise a timeout error if the processes have not completed
    

    **Return**

    - ``resultArray`` -- the array of results
    

    **Usage**

    ```python
    from fundamentals import multiprocess
    # DEFINE AN INPUT ARRAY
    inputArray = range(10000)
    results = multiprocess(log=log, function=functionName, poolSize=10, timeout=300,
                          inputArray=inputArray, otherFunctionKeyword="cheese")
    ```
    
    """
    log.debug('starting the ``multiprocess`` function')
    if not poolSize:
        poolSize = psutil.cpu_count()
    if poolSize:
        p = Pool(processes=poolSize)
    else:
        p = Pool()
    cpuCount = psutil.cpu_count()
    chunksize = int(old_div(len(inputArray) + 1, cpuCount * 3))
    if chunksize == 0:
        chunksize = 1
    if 'log' in inspect.getargspec(function)[0]:
        mapfunc = partial(function, log=log, **kwargs)
        resultArray = p.map_async(mapfunc, inputArray, chunksize=chunksize)
    else:
        mapfunc = partial(function, **kwargs)
        resultArray = p.map_async(mapfunc, inputArray, chunksize=chunksize)
    resultArray = resultArray.get(timeout=timeout)
    p.close()
    p.join()
    log.debug('completed the ``multiprocess`` function')
    return resultArray