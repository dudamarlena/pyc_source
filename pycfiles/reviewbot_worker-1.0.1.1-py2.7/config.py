# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/reviewbot/config.py
# Compiled at: 2018-07-31 04:26:56
from __future__ import print_function, unicode_literals
import imp, os, appdirs
config = {b'pmd_path': None, 
   b'checkstyle_path': None, 
   b'repositories': []}

def init():
    """Load the config file."""
    global config
    config_file = os.path.join(appdirs.site_config_dir(b'reviewbot'), b'config.py')
    print(b'Loading config file %s' % config_file)
    try:
        with open(config_file) as (f):
            config_module = imp.load_module(b'config', f, config_file, (
             b'py', b'r', imp.PY_SOURCE))
            for key in list(config.keys()):
                if hasattr(config_module, key):
                    value = getattr(config_module, key)
                    config[key] = value

    except:
        print(b'Unable to load config, using defaults')