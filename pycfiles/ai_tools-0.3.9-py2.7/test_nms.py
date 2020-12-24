# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/test_nms.py
# Compiled at: 2018-08-04 12:32:06
import numpy as np
thresh = 0.4
ovr = np.array([0.3, 0.4, 0.5, 0.3])
inds = np.where(ovr <= thresh)[0]
print inds
print inds + 1