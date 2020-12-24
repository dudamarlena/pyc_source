# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/flashpoint/sitecustomize.py
# Compiled at: 2016-06-30 06:13:10
import os, sys, imp
from tingyun.config.start_log import log_bootstrap
from tingyun.logistics.mapper import ENV_CONFIG_FILE
log_bootstrap('Ting Yun Bootstrap = %s' % __file__)
log_bootstrap('working_directory = %r' % os.getcwd())
boot_directory = os.path.dirname(__file__)
root_directory = os.path.dirname(boot_directory)
log_bootstrap('root dir is: %s' % boot_directory)
path = list(sys.path)
if boot_directory in path:
    del path[path.index(boot_directory)]
try:
    filename, pathname, description = imp.find_module('sitecustomize', path)
except ImportError:
    pass
else:
    imp.load_module('sitecustomize', filename, pathname, description)

config_file = os.environ.get(ENV_CONFIG_FILE, None)
log_bootstrap('get config  %s' % config_file, close=True)
if config_file is None:
    private_config = '/opt/tingyun.ini'
    if os.path.isfile(private_config):
        config_file = private_config
        log_bootstrap('used for specified config file[%s] in emergency!' % config_file, close=True)
if config_file is not None:
    if root_directory not in sys.path:
        sys.path.insert(0, root_directory)
    import tingyun.startup
    tingyun.startup.preheat_fight(config_file=config_file)