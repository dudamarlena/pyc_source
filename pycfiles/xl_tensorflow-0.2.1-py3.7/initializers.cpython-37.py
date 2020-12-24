# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xl_tensorflow\layers\initializers.py
# Compiled at: 2020-04-24 21:32:26
# Size of source mod 2**32: 683 bytes
DENSE_KERNEL_INITIALIZER = {'class_name':'VarianceScaling', 
 'config':{'scale':0.3333333333333333, 
  'mode':'fan_out', 
  'distribution':'uniform'}}
CONV_KERNEL_INITIALIZER = {'class_name':'VarianceScaling', 
 'config':{'scale':2.0, 
  'mode':'fan_out', 
  'distribution':'normal'}}