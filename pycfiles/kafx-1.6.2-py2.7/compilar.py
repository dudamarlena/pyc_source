# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\kafx\compilar.py
# Compiled at: 2012-02-24 20:39:36
import compileall, os
compileall.compile_dir(os.getcwd(), force=True)
print 'Listo, los pyc son tuyos :D'