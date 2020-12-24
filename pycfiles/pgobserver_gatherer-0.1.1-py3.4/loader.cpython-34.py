# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pgobserver_gatherer/loader.py
# Compiled at: 2016-04-20 09:16:45
# Size of source mod 2**32: 410 bytes
import importlib

def run():
    plugins = [
     'console']
    module = importlib.import_module('pgobserver_gatherer.plugins.console.handler')
    my_class = getattr(module, 'Handler')
    my_instance = my_class()
    my_instance.handle('data')