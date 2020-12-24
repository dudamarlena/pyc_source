# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/turntable/spin.py
# Compiled at: 2015-06-01 20:41:57
"""The spin module contains tools to process Record Collections in either series
or parallel.

Thanks to chriskiehl http://chriskiehl.com/article/parallelism-in-one-line/
"""
import multiprocessing as mp
from multiprocessing.dummy import Pool as ThreadPool
import time, pickle, os, shutil, turntable.utils

def series(collection, method, prints=15, *args, **kwargs):
    """
    Processes a collection in series 

    Parameters
    ----------
    collection : list
        list of Record objects
    method : method to call on each Record
    prints : int
        number of timer prints to the screen

    Returns
    -------
    collection : list
        list of Record objects after going through method called
    
    If more than one collection is given, the function is called with an argument list 
    consisting of the corresponding item of each collection, substituting None for 
    missing values when not all collection have the same length.  
    If the function is None, return the original collection (or a list of tuples if multiple collections).
    
    Example
    -------
    adding 2 to every number in a range

    >>> import turntable
    >>> collection = range(100)
    >>> method = lambda x: x + 2
    >>> collection = turntable.spin.series(collection, method)
    
    """
    if 'verbose' in kwargs.keys():
        verbose = kwargs['verbose']
    else:
        verbose = True
    results = []
    timer = turntable.utils.Timer(nLoops=len(collection), numPrints=prints, verbose=verbose)
    for subject in collection:
        results.append(method(subject, *args, **kwargs))
        timer.loop()

    timer.fin()
    return results


def batch(collection, method, processes=None, batch_size=None, quiet=False, kwargs_to_dump=None, args=None, **kwargs):
    """Processes a collection in parallel batches, 
    each batch processes in series on a single process.
    Running batches in parallel can be more effficient that splitting a list across cores as in spin.parallel 
    because of parallel processing has high IO requirements.

    Parameters
    ----------
    collection : list
        i.e. list of Record objects
    method : method to call on each Record
    processes : int
        number of processes to run on [defaults to number of cores on machine]
    batch_size : int
        lenght of each batch [defaults to number of elements / number of processes]

    Returns
    -------
    collection : list
        list of Record objects after going through method called

    Example
    -------
    adding 2 to every number in a range

    >>> import turntable
    >>> collection = range(100)
    >>> def jam(record):
    >>>     return record + 2
    >>> collection = turntable.spin.batch(collection, jam)

    Note
    ----

    lambda functions do not work in parallel

    """
    if processes is None:
        processes = min(mp.cpu_count(), 20, len(collection))
    if batch_size is None:
        batch_size = max(len(collection) // processes, 1)
    print 'size of each batch =', batch_size
    mod = len(collection) % processes
    batch_list = [ collection[x:x + batch_size] for x in xrange(0, len(collection) - mod, batch_size)
                 ]
    if mod != 0:
        batch_list[(len(batch_list) - 1)] += collection[-mod:]
    print 'number of batches =', len(batch_list)
    if args is None:
        args = method
    else:
        if isinstance(args, tuple) == False:
            args = (
             args,)
        args = (
         method,) + args
    if kwargs_to_dump is None:
        res = parallel(batch_list, new_function_batch, processes=processes, args=args, **kwargs)
    else:
        res = process_dump(batch_list, new_function_batch, kwargs_to_dump, processes=processes, args=args, **kwargs)
    returnList = []
    for l in res:
        returnList += l

    return returnList


def new_function_batch(sequence, method, *args, **kwargs):
    proc_name = mp.current_process().name
    print proc_name + ' starts'
    print 'Processing ' + str(len(sequence)) + ' arguments'
    results = []
    timer = turntable.utils.Timer(nLoops=len(sequence), numPrints=10, verbose=False)
    for subject in sequence:
        results.append(method(subject, *args, **kwargs))
        timer.loop()

    timer.fin()
    return results


def thread(function, sequence, cores=None, runSeries=False, quiet=False):
    """sets up the threadpool with map for parallel processing"""
    if cores is None:
        pool = ThreadPool()
    else:
        pool = ThreadPool(cores)
    tic = time.time()
    if runSeries is False:
        try:
            results = pool.map(function, sequence)
            pool.close()
            pool.join()
        except:
            print 'thread Failed... running in series :-('
            results = series(sequence, function)

    else:
        results = series(sequence, function)
    toc = time.time()
    elapsed = toc - tic
    if quiet is False:
        if cores is None:
            print 'Elapsed time: %s  :-)' % str(elapsed)
        else:
            print 'Elapsed time: %s  on %s threads :-)' % (str(elapsed), str(cores))
    return results


def parallel(collection, method, processes=None, args=None, **kwargs):
    """Processes a collection in parallel.

    Parameters
    ----------
    collection : list
        i.e. list of Record objects
    method : method to call on each Record
    processes : int
        number of processes to run on [defaults to number of cores on machine]
    batch_size : int
        lenght of each batch [defaults to number of elements / number of processes]

    Returns
    -------
    collection : list
        list of Record objects after going through method called

    Example
    -------
    adding 2 to every number in a range

    >>> import turntable
    >>> collection = range(100)
    >>> def jam(record):
    >>>     return record + 2
    >>> collection = turntable.spin.parallel(collection, jam)

    Note
    ----

    lambda functions do not work in parallel

    """
    if processes is None:
        processes = min(mp.cpu_count(), 20)
    print 'Running parallel process on ' + str(processes) + ' cores. :-)'
    pool = mp.Pool(processes=processes)
    PROC = []
    tic = time.time()
    for main_arg in collection:
        if args is None:
            ARGS = (
             main_arg,)
        else:
            if isinstance(args, tuple) == False:
                args = (
                 args,)
            ARGS = (
             main_arg,) + args
        PROC.append(pool.apply_async(method, args=ARGS, kwds=kwargs))

    RES = []
    for p in PROC:
        try:
            RES.append(p.get())
        except Exception as e:
            print 'shit happens...'
            print e
            RES.append(None)

    pool.close()
    pool.join()
    toc = time.time()
    elapsed = toc - tic
    print 'Elapsed time: %s  on %s processes :-)' % (str(elapsed), str(processes))
    return RES


def new_function_dumping(args_to_load_names, function, main_arg, *args, **kwargs):
    for name in args_to_load_names:
        f_toread = open('./temp_pickle/' + name + '.pkl', 'r')
        kwargs[name] = pickle.load(f_toread)
        f_toread.close()

    if args is not None:
        res = function(main_arg, *args, **kwargs)
    else:
        res = function(main_arg, **kwargs)
    return res


def process_dump(collection, function, kwargs_to_dump, processes=None, args=None, **kwargs):
    if processes is None:
        processes = min(mp.cpu_count(), 20)
    print 'Running parallel process on ' + str(processes) + ' cores. :-)'
    tic = time.time()
    turntable.utils.create_dir('./temp_pickle/')
    for name, obj in kwargs_to_dump.iteritems():
        f_pkl = open('./temp_pickle/' + name + '.pkl', 'w+')
        pickle.dump(obj, f_pkl)
        f_pkl.close()

    args_to_load_names = kwargs_to_dump.keys()

    def arg_list(main_arg, args):
        if args is None:
            ARGS = (
             args_to_load_names, function, main_arg)
        else:
            if isinstance(args, tuple) == False:
                args = (
                 args,)
            ARGS = (
             args_to_load_names, function, main_arg) + args
        return ARGS

    pool = mp.Pool(processes=processes)
    PROC = []
    for main_arg in collection:
        ARGS = arg_list(main_arg, args)
        PROC.append(pool.apply_async(new_function_dumping, args=ARGS, kwds=kwargs))

    RES = []
    for p in PROC:
        try:
            RES.append(p.get())
        except Exception as e:
            print 'shit happens...'
            print e
            RES.append(None)

    print 'Closing processes...'
    pool.close()
    pool.join()
    if os.path.exists('./temp_pickle/'):
        shturntable.utils.rmtree('./temp_pickle/')
    toc = time.time()
    elapsed = toc - tic
    print 'Elapsed time: %s on %s processes :-)' % (str(elapsed), str(processes))
    return RES