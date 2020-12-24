# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/__init__.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 454 bytes
import os, pkg_resources
module_path = pkg_resources.resource_filename('jwql', '')
setup_path = os.path.normpath(os.path.join(module_path, '../setup.py'))
try:
    with open(setup_path) as (f):
        data = f.readlines()
    for line in data:
        if 'VERSION =' in line:
            __version__ = line.split(' ')[(-1)].replace("'", '').strip()

except FileNotFoundError:
    print('Could not determine jwql version')
    __version__ = '0.0.0'