# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tigre/Utilities/order_subsets.py
# Compiled at: 2017-06-20 08:49:49
from __future__ import division
import numpy as np

def order_subsets(angles, blocksize, mode):
    if blocksize == 1 or blocksize == None:
        index_alpha = np.arange(len(angles))
        if mode == 'ordered' or mode == None:
            return (angles, index_alpha)
        if mode == 'random':
            np.random.shuffle(index_alpha)
            return (
             angles[index_alpha], index_alpha)
        if mode == 'angularDistance':
            index_alpha = np.argsort(angles)
            new_index = [
             index_alpha[0]]
            new_angles = [angles[index_alpha[0]]]
            angles = np.delete(angles[index_alpha], 0)
            index_alpha = np.delete(index_alpha, 0)
            for i in range(len(angles)):
                compangle = new_angles[i]
                angles_min = np.argmin(abs(abs(angles - compangle) - np.pi / 2))
                new_angles.append(angles[angles_min])
                new_index.append(index_alpha[angles_min])
                angles = np.delete(angles, angles_min)
                index_alpha = np.delete(index_alpha, angles_min)

            print (len(new_angles), len(new_index))
            return (
             np.array(new_angles, dtype=np.float32), np.array(new_index, dtype=np.float32))
        raise NameError('OrdStrat string not recognised: ' + mode)
    elif blocksize > 1:
        oldindex = np.arange(len(angles))
        index_alpha = [ oldindex[i:i + blocksize] for i in range(0, len(oldindex), blocksize) ]
        block_alpha = [ angles[i:i + blocksize] for i in range(0, len(angles), blocksize) ]
        if mode == 'ordered' or mode == None:
            return (block_alpha, index_alpha)
        if mode == 'random':
            new_order = np.random.shuffle(np.arange(len(index_alpha)))
            return (
             block_alpha[new_order], index_alpha[new_order])
        if mode == 'angularDistance':
            raise NameError('Angular distance not implemented for blocksize >1 (yet!)')
        else:
            raise NameError('OrdStrat string not recognised: ' + mode)
    return