# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditio/system.py
# Compiled at: 2018-01-28 14:03:35
import os
from shutil import copy2
from . import log
normalise = lambda v, types, fn: v if type(v) in types else fn(v)

def create_dir(path, i=1):
    path = normalise(path, [set, list, tuple], lambda v: v.split('/'))
    folder = ('/').join(path[:i])
    if os.path.exists(folder) is False:
        os.mkdir(folder)
    if i < len(path):
        create_dir(path, i + 1)


def copy(src, dest):
    folder = src
    if os.path.exists(folder) is True:
        files = [ entry for entry in os.listdir(folder) if os.path.isdir('%s/%s' % (src, entry)) is False ]
        for f in files:
            src_file = '%s/%s' % (src, f)
            dst_file = '%s/%s' % (dest, f)
            log('%s ->  %s ' % (src_file, dst_file))
            copy2(src_file, dst_file)

        folders = [ entry for entry in os.listdir(folder) if os.path.isdir('%s/%s' % (folder, entry)) is True ]
        for entry in folders:
            new_src = '%s/%s' % (src, entry)
            new_dest = '%s/%s' % (dest, entry)
            create_dir(new_dest)
            log('copy  %s -->  %s' % (new_src, new_dest))
            copy(new_src, new_dest)