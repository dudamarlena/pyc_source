# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/async_evaluatable.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 1916 bytes
import logging
logger = logging.getLogger(__name__)
import functools
from pyxrd.generic.asynchronous.cancellable import Cancellable
from pyxrd.generic.asynchronous.has_async_calls import HasAsyncCalls

class AsyncEvaluatable(HasAsyncCalls, Cancellable):

    def do_async_evaluation(self, iter_func, eval_func, data_func, result_func):
        """ 
            Utility that combines a submit and fetch cycle in a single function
            call.
            iter_func is a generation callback (generates solutions)
            data_func transforms the given solutions to something eval_func can 
              work with (this can be a pass-through operation)
            eval_func evaluates a single (generated) solution (this must be
              picklable)
            result_func receives each solution and its residual as arguments
            
        """
        if not callable(iter_func):
            raise AssertionError
        else:
            if not callable(eval_func):
                raise AssertionError
            elif not callable(data_func):
                raise AssertionError
            assert callable(result_func)
        results = []
        solutions = []
        for solution in iter_func():
            result = self.submit_async_call(functools.partial(eval_func, data_func(solution)))
            solutions.append(solution)
            results.append(result)
            if self._user_cancelled():
                break

        for solution, result in zip(solutions, map(self.fetch_async_result, results)):
            result_func(solution, result)

        del results
        import gc
        gc.collect()
        return solutions