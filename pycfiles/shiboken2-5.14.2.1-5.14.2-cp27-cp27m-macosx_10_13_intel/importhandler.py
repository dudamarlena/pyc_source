# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/qt/work/pyside/pyside-setup/pyside2_install/py2.7-qt5.14.2-64bit-release/lib/python2.7/site-packages/shiboken2/files.dir/shibokensupport/signature/importhandler.py
# Compiled at: 2020-04-24 02:55:46
from __future__ import print_function, absolute_import
try:
    from PySide2.support import deprecated
    have_deprecated = True
except ImportError:
    have_deprecated = False

def finish_import(module):
    if have_deprecated and module.__name__.startswith('PySide2.'):
        try:
            name = 'fix_for_' + module.__name__.split('.')[1]
            func = getattr(deprecated, name, None)
            if func:
                func(module)
        except Exception as e:
            name = e.__class__.__name__
            print(72 * '*')
            print('Error in deprecated.py, ignored:')
            print(('    {name}: {e}').format(**locals()))

    return