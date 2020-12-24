# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jps/launcher.py
# Compiled at: 2016-06-11 06:32:43
from multiprocessing import Process
import importlib

def launch_modules(module_names):
    """launch module.main functions in another process"""
    processes = []
    for module_name in module_names:
        m = importlib.import_module(module_name)
        p1 = Process(target=m.main)
        p1.daemon = True
        p1.start()
        processes.append(p1)

    return processes