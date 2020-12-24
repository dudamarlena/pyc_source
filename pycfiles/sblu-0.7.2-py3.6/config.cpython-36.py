# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sblu/config.py
# Compiled at: 2019-10-14 18:28:00
# Size of source mod 2**32: 672 bytes
from configobj import ConfigObj
from path import Path
DEFAULTS = {'cluspro':{'local_path':None, 
  'username':None, 
  'api_secret':None, 
  'server':'cluspro.bu.edu'}, 
 'ftmap':{'local_path':None, 
  'username':None, 
  'api_secret':None, 
  'server':'ftmap.bu.edu'}, 
 'prms_dir':Path('~/prms').expand()}

def get_config(config_path='~/.sblurc'):
    config = ConfigObj(DEFAULTS)
    config_file = Path(config_path).expand()
    config.filename = config_file
    if config_file.exists():
        config.merge(ConfigObj(config_file))
    else:
        config.write()
    return config