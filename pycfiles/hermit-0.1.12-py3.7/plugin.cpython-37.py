# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hermit/plugin.py
# Compiled at: 2019-07-15 12:24:50
# Size of source mod 2**32: 479 bytes
from os import listdir
from os.path import exists, join
from hermit.config import HermitConfig
PluginsLoaded = []
_config = HermitConfig.load()
if exists(_config.plugin_dir):
    for basename in listdir(_config.plugin_dir):
        if basename.endswith('.py'):
            PluginsLoaded.append(basename)
            print('Loading plugin {}'.format(basename))
            exec(open(join(_config.plugin_dir, basename), 'r').read())