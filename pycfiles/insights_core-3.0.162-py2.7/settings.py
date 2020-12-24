# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/settings.py
# Compiled at: 2019-05-16 13:41:33
import sys, os, yaml, pkgutil
INSTALL_DIR = os.path.dirname(os.path.abspath(__file__))
NAME = 'insights.yaml'
DEFAULTS_NAME = 'defaults.yaml'

def load_and_read(path):
    if os.path.exists(path):
        with open(path) as (fp):
            return fp.read()


CONFIGS = [
 pkgutil.get_data('insights', 'defaults.yaml'),
 load_and_read(os.path.join('/etc', NAME)),
 load_and_read(os.path.join(os.path.expanduser('~/.local'), NAME)),
 load_and_read('.' + NAME)]
config = {}
for c in CONFIGS:
    if c is None:
        continue
    try:
        y = yaml.safe_load(c)
        for name, section in y.items():
            if name in config:
                config[name].update(section)
            else:
                config[name] = section

    except Exception as e:
        print c
        print e

for k in config['defaults']:
    for section in set(s for s in config if s != 'defaults'):
        if k not in config[section]:
            config[section][k] = config['defaults'][k]

for name, section in config.items():
    setattr(sys.modules[__name__], name, section)