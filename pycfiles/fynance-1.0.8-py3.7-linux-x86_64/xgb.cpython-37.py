# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/models/xgb.py
# Compiled at: 2019-09-25 08:14:47
# Size of source mod 2**32: 2189 bytes
__all__ = [
 'XGB', 'XGBData']

class XGB:

    def __init__(self, X, y, **kwargs):
        """ Setting data to XGBoot model.

        Parameters
        ----------
        X, y : np.ndarray[ndim=2, dtype=np.float64]
            Respectively features with shape `(T, N)` and target with shape
            `(T, 1)` of the model.
        kwargs : dict, optional
            Parameters of DMatrix object, cf XGBoost documentation [1]_.

        References
        ----------
        .. [1] https://xgboost.readthedocs.io/en/latest/python/python_api.html

        """
        self.data = XGBData(X, label=y, **kwargs)

    def run(self, n, s, **params):
        train = self.data[:-n]
        estim = self.data[:s]


class XGBData:
    __doc__ = ' Set data for XGBoost models. '

    def __getitem__(self, key):
        """ Slice the DMatrix and return a new DMatrix that only contains `key`.

        Parameters
        ----------
        key : slice
            Slice to be selected.

        Returns
        -------
        res : DMatrix
            A new DMatrix containing only selected indices.

        """
        start = 0 if key.start is None else key.start
        step = 1 if key.step is None else key.step
        stop = self.num_row() if key.stop is None else key.stop
        if step < 0:
            stop, start = start - 1, stop + 1
        if stop < 0:
            stop += self.num_row() + 1
        return self.slice(list(range(start, stop, step)))


def train_xgb--- This code section failed: ---

 L.  80         0  LOAD_FAST                'bst'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    10  'to 10'

 L.  81         8  JUMP_FORWARD         10  'to 10'
             10_0  COME_FROM             8  '8'
             10_1  COME_FROM             6  '6'

Parse error at or near `COME_FROM' instruction at offset 10_0