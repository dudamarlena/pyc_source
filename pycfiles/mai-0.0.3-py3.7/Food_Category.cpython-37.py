# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\code\dataprocess\Food_Category.py
# Compiled at: 2020-03-09 21:59:41
# Size of source mod 2**32: 416 bytes
from AI.code.utils.util import photo_process
import os, shutil
food_path = 'I:\\AI\\数据集\\美食分类\\data\\images'
train_data_path = 'data\\goodeat\\train'
val_data_path = 'data\\goodeat\\val'
test_data_path = 'data\\goodeat\\test'
traintest_cent = 0.8
trainval_cent = 0.75
photo_process(food_path, train_data_path, val_data_path, test_data_path, traintest_cent, trainval_cent)