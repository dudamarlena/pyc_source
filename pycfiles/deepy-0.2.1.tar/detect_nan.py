# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shu/research/deepy/deepy/utils/detect_nan.py
# Compiled at: 2016-04-20 00:05:45
"""
Detect the source which produces NaN.

Usage
---

conf.theano_mode = DETECT_NAN_MODE

Note
---

Be sure to use theano flag 'optimizer=None'.
"""
import theano, numpy as np

def detect_nan(i, node, fn):
    if str(node.op).startswith('GPU_mrg_uniform'):
        return
    for output in fn.outputs:
        if not isinstance(output[0], np.random.RandomState) and np.isnan(output[0]).any():
            print '*** NaN detected ***'
            theano.printing.debugprint(node)
            print 'Inputs : %s' % [ input[0] for input in fn.inputs ]
            print 'Outputs: %s' % [ output[0] for output in fn.outputs ]
            import pdb
            pdb.set_trace()


DETECT_NAN_MODE = theano.compile.MonitorMode(post_func=detect_nan)