# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/bootstrap/maya/userSetup.py
# Compiled at: 2020-04-15 09:54:50
# Size of source mod 2**32: 969 bytes
"""
Initialization for Plot Twist Tools
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
print('=' * 100)
print('| Plot Twist ArtellaPipe | > Loading Plot Twist Tools')
try:
    import plottwist.loader
    from maya import cmds
    cmds.evalDeferred('plottwist.loader.init(import_libs=True)')
    print('| Plot Twist ArtellaPipe | Plot Twist loaded successfully!')
    print('=' * 100)
except Exception as e:
    try:
        import plottwist.loader
        plottwist.loader.init(import_libs=True)
        print('| Plot Twist Pipeline | Plot Twist loaded successfully!')
        print('=' * 100)
    except Exception as exc:
        import traceback
        print('ERROR: Impossible to load Plot Twist Tools, contact TD!')
        print('{} | {}'.format(exc, traceback.format_exc()))