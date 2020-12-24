# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/test_nms.py
# Compiled at: 2018-08-04 12:32:06
import numpy as np
thresh = 0.4
ovr = np.array([0.3, 0.4, 0.5, 0.3])
inds = np.where(ovr <= thresh)[0]
print inds
print inds + 1