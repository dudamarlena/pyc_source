# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/plottwist/bootstrap/maya/userSetup.py
# Compiled at: 2020-04-15 09:54:50
# Size of source mod 2**32: 969 bytes
__doc__ = '\nInitialization for Plot Twist Tools\n'
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