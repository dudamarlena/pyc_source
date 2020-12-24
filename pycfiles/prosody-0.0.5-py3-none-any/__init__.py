# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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