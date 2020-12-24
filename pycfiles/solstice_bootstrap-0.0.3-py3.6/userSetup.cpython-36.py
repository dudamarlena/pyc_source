# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/solstice/bootstrap/maya/userSetup.py
# Compiled at: 2020-03-08 13:19:07
# Size of source mod 2**32: 952 bytes
"""
Initialization for Solstice Tools
"""
from __future__ import print_function, division, absolute_import
__author__ = 'Tomas Poveda'
__license__ = 'MIT'
__maintainer__ = 'Tomas Poveda'
__email__ = 'tpovedatd@gmail.com'
print('=' * 100)
print('| Solstice ArtellaPipe | > Loading Solstice Tools')
try:
    import solstice.loader
    from maya import cmds
    cmds.evalDeferred('solstice.loader.init(import_libs=True)')
    print('| Solstice ArtellaPipe | Solstice loaded successfully!')
    print('=' * 100)
except Exception as e:
    try:
        import solstice.loader
        solstice.loader.init(import_libs=True)
        print('| Solstice ArtellaPipe | Solstice loaded successfully!')
        print('=' * 100)
    except Exception as exc:
        import traceback
        print('ERROR: Impossible to load Solstice Tools, contact TD!')
        print('{} | {}'.format(exc, traceback.format_exc()))