# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turboblog/plugins.py
# Compiled at: 2007-03-25 08:41:47
import pkg_resources

def get_sidebar_plugins():
    sidebar_plugins = []
    for entrypoint in pkg_resources.iter_entry_points('turboblog.plugins.sidebar'):
        engine = entrypoint.load()
        sidebar_plugins += [engine()]

    return sidebar_plugins