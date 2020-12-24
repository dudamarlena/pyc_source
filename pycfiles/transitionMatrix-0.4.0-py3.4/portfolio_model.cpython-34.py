# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/examples/python/portfolio_model.py
# Compiled at: 2018-10-21 10:12:31
# Size of source mod 2**32: 1064 bytes
import transitionMatrix.portfolio_model_lib.model as vs
print('p=', vs.vasicek_base(10, 0, 0.3414, 0.2))