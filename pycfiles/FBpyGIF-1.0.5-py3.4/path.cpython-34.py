# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/FBpyGIF/path.py
# Compiled at: 2017-09-05 07:56:56
# Size of source mod 2**32: 603 bytes


def rec_list_dir(path, rec=True):
    from os.path import isdir, isfile, exists
    from imghdr import what
    rst = []
    if exists(path):
        if isdir(path) and rec:
            from os import listdir
            from os.path import join
            for f in listdir(path):
                rst += rec_list_dir(join(path, f))

    else:
        if isfile(path):
            if what(path):
                rst += [path]
        return rst


def rrec_list_dir(path, rec=True):
    l = []
    for p in path:
        l += rec_list_dir(p)

    return l


def move_file(fpath, trgdir):
    from os import rename
    from os.path import join, basename
    rename(fpath, join(trgdir, basename(fpath)))