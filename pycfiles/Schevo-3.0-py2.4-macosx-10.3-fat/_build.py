# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/icon/_build.py
# Compiled at: 2007-03-21 14:34:39
"""Do a one-time build of default.png

For copyright, license, and warranty, see bottom of file.
"""
if __name__ == '__main__':
    f = file('default.png', 'rb')
    default_png = f.read()
    f.close()
    f = file('_default_png.py', 'wU')
    f.write('DEFAULT_PNG = %r\n' % default_png)
    f.close()