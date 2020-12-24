# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sushineAI\sushineAI.py
# Compiled at: 2019-12-16 23:12:40
# Size of source mod 2**32: 2001 bytes
"""
@author: zhangX
@license: (C) Copyright 1999-2019, NJ_LUCULENT Corporation Limited.
@contact: 494677221@qq.com
@file: sushineAI.py
@time: 2019/12/16 16:31
@desc:
"""
from keras.callbacks import ReduceLROnPlateau, TensorBoard, EarlyStopping, ModelCheckpoint
from sushineAI.callbacks import KerasCallBack
import keras
from sushineAI.losses import loss

class SuShineKerasAI:

    def __init__(self, model, **kwargs):
        self.model = model
        self.base_kwargs = kwargs

    def fit(self, kwargs):
        kwargs.update(self.base_kwargs)
        self._compile(kwargs)
        self.model.fit_generator((kwargs.get('train')),
          epochs=(kwargs.get('params').get('epoch')),
          validation_data=(kwargs.get('test')),
          validation_steps=100,
          steps_per_epoch=(kwargs.get('params').get('all_batch')),
          callbacks=[
         ReduceLROnPlateau(monitor='lr', factor=(kwargs.get('params').get('decay_rate')), patience=(kwargs.get('params').get('decay_step', 1))),
         TensorBoard(log_dir=(kwargs.get('save_path') + 'logs')),
         ModelCheckpoint((kwargs.get('save_path') + 'model.h5'), monitor='val_loss',
           verbose=1,
           save_best_only=True),
         KerasCallBack(kwargs.get('test'), kwargs.get('train_info_queue'), kwargs.get('experiment_id'), loss.get(kwargs.get('loss', 'rmse'), loss.get('rmse')))])

    def _compile(self, kwargs):
        self.model.compile(optimizer=(keras.optimizers.Adam(kwargs.get('params').get('learning_rate', 0.001))), loss=(loss.get(kwargs.get('loss', 'rmse'), loss.get('rmse'))))