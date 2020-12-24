# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/process/process_tools.py
# Compiled at: 2019-12-17 00:06:50
# Size of source mod 2**32: 7066 bytes
import logging, time
from concurrent.futures.process import ProcessPoolExecutor
from functools import partial
from multiprocessing.pool import Pool
import dill
from future.utils import lmap, lfilter
from nose.tools import assert_equal
from foxylib.tools.collections.collections_tool import l_singleton2obj, IterTool
from foxylib.tools.log.logger_tools import FoxylibLogger
from foxylib.tools.string.string_tools import format_str

class ProcessToolkit:

    @classmethod
    def _func2dillstr(cls, f):
        return dill.dumps(f)

    @classmethod
    def _dillstr2run(cls, str_dill):
        f = dill.loads(str_dill)
        return f()

    @classmethod
    def max_workers2executor(cls, max_workers):
        return ProcessPoolExecutor(max_workers=max_workers)

    @classmethod
    def _func_list2fak_list_filled(cls, func_list):
        dillstr_list = lmap(cls._func2dillstr, func_list)
        fak_list = [(cls._dillstr2run, [s], {}) for s in dillstr_list]
        return fak_list

    @classmethod
    def _pool_fak_iter2ar_iter(cls, pool, fak_iter):
        for f, a, k in fak_iter:
            ar = pool.apply_async((partial(f)), args=a, kwds=k)
            yield ar

    @classmethod
    def pool_func_iter2ar_iter(cls, pool, f_iter):
        fak_iter = ((f, [], {}) for f in f_iter)
        yield from cls._pool_fak_iter2ar_iter(pool, fak_iter)
        if False:
            yield None

    @classmethod
    def ar_iter2buffered_result_iter(cls, ar_iter, buffer_size):
        logger = FoxylibLogger.func2logger(cls.ar_iter2buffered_result_iter)
        ar_iter_buffered = IterTool.iter2buffered(ar_iter, buffer_size)
        for ar in ar_iter_buffered:
            yield ar.get()

    @classmethod
    def pool_func_iter2buffered_result_iter(cls, pool, func_iter, buffer_size):
        ar_iter = cls.pool_func_iter2ar_iter(pool, func_iter)
        yield from cls.ar_iter2buffered_result_iter(ar_iter, buffer_size)
        if False:
            yield None

    @classmethod
    def func_iter2buffered_result_iter(cls, func_iter, buffer_size):
        logger = FoxylibLogger.func2logger(cls.func_iter2buffered_result_iter)
        with Pool() as (pool):
            yield from cls.pool_func_iter2buffered_result_iter(pool, func_iter, buffer_size)
        if False:
            yield None

    @classmethod
    def func_list2buffered_result_iter(cls, func_list, buffer_size):
        if len(func_list) == 1:
            f = l_singleton2obj(func_list)
            yield f()
        else:
            result_iter = cls.func_iter2buffered_result_iter(func_list, buffer_size)
            yield from result_iter

    @classmethod
    def func_list2result_list_OLD(cls, func_list):
        logger = FoxylibLogger.func2logger(cls.func_list2result_list)
        with Pool() as (pool):
            ar_list = [pool.apply_async(f) for f in func_list]
            output_list = [ar.get() for ar in ar_list]
        return output_list

    @classmethod
    def func_list2result_list(cls, func_list):
        logger = FoxylibLogger.func2logger(cls.func_list2result_list)
        logger.debug({'# func_list': len(func_list)})
        output_iter = cls.func_list2buffered_result_iter(func_list, len(func_list))
        result_list = list(output_iter)
        logger.debug({'# result_list': len(result_list)})
        return result_list

    @classmethod
    def func_list2run_parallel(cls, func_list):
        output_iter = cls.func_list2buffered_result_iter(func_list, len(func_list))
        IterTool.consume(output_iter)

    @classmethod
    def wait(cls, f, *_, **__):
        status_list = (cls.wait_all)([f], *_, **__)
        assert_equal(len(status_list), 1)
        return status_list[0]

    @classmethod
    def wait_all(cls, f_list, sec_timeout, sec_interval):
        logger = FoxylibLogger.func_level2logger(cls.wait_all, logging.DEBUG)
        time_end = time.time() + sec_timeout if sec_timeout is not None else None
        n = len(f_list)
        status_list = [None] * n
        logger.debug(format_str('waiting for {} process for {} secs', len(f_list), sec_timeout))
        while time_end is None or time.time() < time_end:
            for i in range(n):
                if status_list[i] is True:
                    continue
                status_list[i] = f_list[i]()

            if all(status_list):
                break
            logger.debug(format_str('waiting for {}/{} processes for {} secs with {} sec interval', len(lfilter(lambda x: not x, status_list)), len(f_list), '{:.3f}'.format(time_end - time.time()), sec_interval))
            time.sleep(sec_interval)

        return status_list