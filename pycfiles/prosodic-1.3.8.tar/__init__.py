# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: meters/__init__.py
# Compiled at: 2019-06-02 18:11:41
import os, imp
meter_dir = os.path.dirname(__file__)
d = {}
for fn in os.listdir(meter_dir):
    if not fn.endswith('.py') or fn.startswith('_'):
        continue
    idx = fn.replace('.py', '').replace('-', '_')
    d[idx] = imp.load_source(idx, os.path.join(meter_dir, fn))