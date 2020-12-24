# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Benutzer\haschtl\Dokumente\GIT\kellerlogger\RTOC\RTLogger\loggerlib.py
# Compiled at: 2019-05-21 18:38:55
# Size of source mod 2**32: 1294 bytes
import numpy as np, pkgutil, logging as log
log.basicConfig(level=(log.INFO))
logging = log.getLogger(__name__)

def npJSONWorkAround(o):
    if isinstance(o, np.int64):
        return int(o)
    else:
        return o


def iter_namespace(ns_pkg):
    return pkgutil.walk_packages(path=(ns_pkg.__path__), prefix=(ns_pkg.__name__ + '.'), onerror=(lambda x: None))


def list_submodules(package_name):
    list_name = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(package_name.__path__, package_name.__name__ + '.'):
        list_name.append(module_name)
        module_name = __import__(module_name, fromlist='dummylist')
        if is_pkg:
            list_submodules(list_name, module_name)

    return list_name


def calcDuration(self, x, maxlen):
    dt = x[(-1)] - x[0]
    l = len(x)
    return dt / l * maxlen