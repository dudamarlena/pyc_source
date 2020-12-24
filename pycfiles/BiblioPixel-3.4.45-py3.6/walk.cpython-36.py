# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/walk.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 416 bytes
import os

def walk(roots):
    if isinstance(roots, str):
        roots = [
         roots]
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            for f in filenames:
                yield (
                 root, os.path.join(dirpath, f))


def walk_suffix(roots, suffixes):
    for root, filename in walk(roots):
        if any(filename.endswith(s) for s in suffixes):
            yield (
             root, filename)