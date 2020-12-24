# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcel/Dropbox/marcel/repos/numphy/numphy/__init__.py
# Compiled at: 2018-05-02 14:15:45
"""
Physics objects backed by NumPy and/or TensorFlow.
"""
__author__ = 'Marcel Rieger'
__email__ = 'python-numphy@googlegroups.com'
__credits__ = ['Benjamin Fischer', 'Marcel Rieger']
__copyright__ = 'Copyright 2018, Marcel Rieger'
__contact__ = 'https://github.com/riga/numphy'
__license__ = 'MIT'
__status__ = 'Development'
__version__ = '0.0.2'
__all__ = [
 'Wrapper', 'Trace', 'DataProxy',
 'is_numpy', 'is_tensorflow', 'map_struct', 'is_lazy_iterable', 'no_value',
 't', 'HAS_NUMPY', 'HAS_TENSORFLOW']
from numphy.core import *
from numphy.util import *
if __name__ == '__main__':
    import numpy as np, tensorflow as tf, uproot

    def jagged_to_rec(tree, keys):
        arrays = tree.arrays(keys)
        formats = [ arrays[key].dtype for key in keys ]
        flat = (1e-05 * np.ones(len(arrays[keys[0]]))).astype({'names': keys, 'formats': formats})
        for key in keys:
            flat[key] = arrays[key]

        return flat


    def rec_to_flat(rec):
        return np.array([ rec[name] for name in rec.dtype.names ])


    f = uproot.open('tree_20.root')
    tree = f['tree']
    jet1 = jagged_to_rec(tree, ['jet1_E', 'jet1_px', 'jet1_py', 'jet1_pz'])
    jet2 = jagged_to_rec(tree, ['jet2_E', 'jet2_px', 'jet2_py', 'jet2_pz'])
    struct = {'jet1': jet1, 
       'jet2': jet2}
    event = Wrapper(struct, attrs=dict(jet1=Wrapper(trace='jet1', attrs=dict(E='jet1_E', px='jet1_px', py='jet1_py', pz='jet1_pz'))))
    tf.enable_eager_execution()
    jet1_tf = Wrapper(tf.constant(rec_to_flat(jet1)), attrs=dict(E=0, px=1, py=2, pz=3))