# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./pkgtools/utils.py
# Compiled at: 2013-10-09 08:55:47
# Size of source mod 2**32: 742 bytes
import os

def name_ext(path):
    p, e = os.path.splitext(path)
    if p.endswith('.tar'):
        return (p[:-4], '.tar' + e)
    return (
     p, e)


def name(path):
    return name_ext(path)[0]


def ext(path):
    return name_ext(path)[1]


def zip_files(zf, search='egg-info'):
    names = [n for n in zf.namelist() if search in n]
    fobj_list = [zf.read(n) for n in names]
    return list(zip(fobj_list, map(os.path.basename, names)))


def tar_files(tf):
    names = [n for n in tf.getnames() if 'egg-info' in n and not n.endswith('egg-info')]
    fobj_list = [tf.extractfile(n).read() for n in names]
    return list(zip(fobj_list, map(os.path.basename, names)))