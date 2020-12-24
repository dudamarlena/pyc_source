# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yhat/submodules.py
# Compiled at: 2017-04-26 17:15:42
import os

def detect_explicit_submodules(model_object):
    submodules = []
    files = getattr(model_object, 'FILES', [])
    for f in files:
        basename = os.path.basename(f)
        parent_dir = os.path.dirname(f)
        source = open(f, 'rb').read()
        with open(f, 'rb') as (f):
            source = f.read()
        submodule = {'parent_dir': parent_dir, 
           'name': basename, 
           'source': source}
        submodules.append(submodule)
        directories = parent_dir.split('/')
        for i in range(len(directories) + 1):
            submodules.append({'parent_dir': ('/').join(directories[:i]), 
               'name': '__init__.py', 
               'source': ''})

    return submodules