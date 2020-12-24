# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dir2html/get_assets.py
# Compiled at: 2018-11-21 07:15:50
# Size of source mod 2**32: 469 bytes
import os
from pkg_resources import resource_filename

def get_assets():
    assets = []
    assets_dirname = resource_filename(__name__, 'resources/assets')
    for root, dirs, files in os.walk(assets_dirname):
        for file in files:
            try:
                full_path = '{}/{}'.format(os.path.realpath(root), file)
                assets.append(full_path)
            except IOError as e:
                print('Error: {}'.format(e))

    return assets