# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test/load.py
# Compiled at: 2019-01-08 04:08:38
# Size of source mod 2**32: 95 bytes
import pickle
trainer = pickle.load(open('output/snapshot_iter_3750.pkl', 'rb'))
trainer.run()