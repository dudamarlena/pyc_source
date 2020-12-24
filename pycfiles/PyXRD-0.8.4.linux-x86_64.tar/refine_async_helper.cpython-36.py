# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyxrd/refinement/refine_async_helper.py
# Compiled at: 2020-03-07 03:51:50
# Size of source mod 2**32: 926 bytes
from pyxrd.generic.utils import not_none
from pyxrd.refinement.async_evaluatable import AsyncEvaluatable

class RefineAsyncHelper(AsyncEvaluatable):
    __doc__ = '\n        Helper class which can help classes having a refiner object\n        \n    '

    def do_async_evaluation(self, iter_func, eval_func=None, data_func=None, result_func=None):
        assert self.refiner is not None, 'RefineAsyncHelper can only work when a refiner is set!'
        eval_func = not_none(eval_func, self.refiner.residual_callback)
        data_func = not_none(data_func, self.refiner.get_data_object)
        result_func = not_none(result_func, self.refiner.update)
        return super(RefineAsyncHelper, self).do_async_evaluation(iter_func, eval_func, data_func, result_func)