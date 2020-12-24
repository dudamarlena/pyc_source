# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sushineAI\losses.py
# Compiled at: 2019-12-16 03:36:41
# Size of source mod 2**32: 422 bytes
"""
@author: zhangX
@license: (C) Copyright 1999-2019, NJ_LUCULENT Corporation Limited.
@contact: 494677221@qq.com
@file: losses.py
@time: 2019/12/16 16:31
@desc:
"""
import keras.backend as k

def rmse(y_true, y_pred):
    return k.sqrt(k.mean((k.square(y_pred - y_true)), axis=(-1)))


def mse(y_true, y_pred):
    return k.mean((k.square(y_pred - y_true)), axis=(-1))


loss = {'rmse':rmse, 
 'mse':mse}