# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pwclip/lib/system/path.py
# Compiled at: 2020-03-20 08:07:42
# Size of source mod 2**32: 5018 bytes
"""path related functions"""
from re import search
from os import getcwd, chdir, chmod, walk, readlink, utime, stat as osstat
from os.path import expanduser, islink, isfile, isdir, abspath, join as pjoin, exists
from time import time
from shutil import copy2, move
from configparser import ConfigParser as _ConfPars
from json import load as _jsonload
from system.random import randin

def absrelpath(path, base=None):
    """absrelpath for finding absolute paths in optional given base"""
    base = base if base else getcwd()
    path = path.strip("'")
    path = path.strip('"')
    if path.startswith('~'):
        path = expanduser(path)
    if islink(path):
        path = readlink(path)
    if '..' in path or not path.startswith('/'):
        pwd = getcwd()
        chdir(base)
        path = abspath(path)
        chdir(pwd)
    return path.rstrip('/')


def realpaths(pathlist, base=None):
    """realpaths using realpath on multiple input files"""
    base = base if base else getcwd()
    paths = []
    for path in pathlist:
        if isinstance(path, (list, tuple)):
            for _ in path:
                paths = [absrelpath(p, base) for p in path]

        else:
            if isinstance(path, str):
                if ' ' in path:
                    paths = [absrelpath(p.strip(), base) for p in path.strip('[]').split(',')]
                    break
                else:
                    paths.append(absrelpath(path, base))

    return paths


def confpaths(paths, conf, base=''):
    """find configs in paths in base if file exists"""
    return list(set([pjoin(expanduser('~'), path[2:], conf) for path in paths if path.startswith('~/') if isfile(pjoin(expanduser('~'), path[2:], conf))] + [pjoin(base, path[2:], conf) for path in paths if path.startswith('./') if isfile(pjoin(base, path[2:], conf))] + [pjoin(base, path, conf) for path in paths if not path.startswith('/') if not path.startswith('.') if isfile(pjoin(base, path, conf))] + [pjoin(path, conf) for path in paths if path.startswith('/') if isfile(pjoin(path, conf))]))


def confdats(*confs):
    """get ini data from config files"""
    cfg = _ConfPars()
    cfgdats = {}
    for conf in confs:
        cfg.read(conf)
        for section in cfg.sections():
            cfgdats[section] = dict(cfg[section])

    return cfgdats


def jconfdats(*confs):
    """get json data from config files"""
    __dats = {}
    for conf in confs:
        with open(conf, 'r') as (stream):
            for key, val in _jsonload(stream).items():
                __dats[key] = val

    return __dats


def unsorted(files):
    """unsort given files"""
    unsorteds = []
    while len(unsorteds) != len(files):
        f = files[randin(len(files))]
        unsorteds.append(f)

    return unsorteds


def filetime(trg):
    """local file-timestamp method"""
    return (
     int(osstat(trg).st_mtime), int(osstat(trg).st_atime))


def setfiletime(trg, mtime=None, atime=None):
    """local file-timestamp set method"""
    mt, at = filetime(trg)
    if mtime:
        if not atime:
            atime = at
    if atime:
        if not mtime:
            mtime = mt
    utime(trg, (at, mt))


def filerotate(lfile, count=3, force=None):
    """rotate given file by a maximum of count"""
    if not isfile(lfile):
        return False
    else:
        mode = osstat(lfile).st_mode
        mt, at = filetime(lfile)
        act = move
        for i in reversed(range(0, int(count))):
            rtn = False
            old = '%s.%d' % (lfile, i)
            if i == 0:
                old = lfile
            else:
                if i == 1:
                    act = copy2
            new = '%s.%d' % (lfile, int(i + 1))
            if not isfile(old):
                continue
            mode = osstat(old).st_mode
            mt, at = filetime(old)
            if act(old, new):
                rtn = True

        return rtn


def filesiter(folder, random=False, includes=[], excludes=[]):
    """iterate over files for given folder"""
    for d, _, fs in walk(absrelpath(folder)):
        if excludes:
            if [i for i in excludes if search(i, d)]:
                continue
        if includes:
            if not [i for i in includes if search(i, d)]:
                continue
        reordered = sorted if not random else unsorted
        fs = reordered(fs)
        for f in reordered(fs):
            if excludes:
                if [i for i in excludes if search(i, f)]:
                    continue
            if includes:
                if not [i for i in includes if search(i, f)]:
                    continue
            f = pjoin(d, f)
            yield f


def linesiter(target, includes=[], excludes=[]):
    __lns = []
    with open(target, 'r') as (pfh):
        __lns = pfh.readlines()
    for l in __lns:
        if excludes:
            if [i for i in excludes if search(i, l)]:
                continue
        if includes:
            if not [i for i in includes if search(i, l)]:
                continue
        yield l


def findupper(path, name=None, dirs=None, files=None, links=None):
    """find parent directory by given pattern"""
    if not name:
        name = path
        path = getcwd()
    while len(path.split('/')) > 1:
        trg = pjoin(path, name)
        if dirs is None:
            if files is None:
                if links is None:
                    if exists(trg):
                        return trg
        if links:
            if islink(trg):
                return trg
        if files:
            if isfile(trg):
                return trg
        if dirs:
            if isdir(trg):
                return trg
        return findupper('/'.join(p for p in path.split('/')[:-1]), name, dirs, files, links)


def findupperdir(path, name=None):
    """find parent directory by given pattern"""
    return findupper(path, name, dirs=True)