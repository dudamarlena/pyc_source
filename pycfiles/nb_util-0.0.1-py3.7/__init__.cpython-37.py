# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/nb_util/__init__.py
# Compiled at: 2019-12-10 17:09:48
# Size of source mod 2**32: 546 bytes
import joblib
from tqdm import tqdm
import caffeine, platform

def can_caffeinate():
    return platform.system() == 'Darwin'


def do_parallel(fn, loop, n_jobs=-1, progress=True, keep_alive=True):
    if progress:
        loop = tqdm(loop)
    with joblib.Parallel(n_jobs=(-1)) as (par):
        if keep_alive and can_caffeinate():
            caffeine.on(display=True)
            res = par((joblib.delayed(fn)(l) for l in loop))
            caffeine.off()
        else:
            res = par((joblib.delayed(fn)(l) for l in loop))
    return res