# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/klen/Projects/zeta-library/zetalibrary/settings.py
# Compiled at: 2012-08-18 06:07:01
from os import path as op, environ, getcwd
VERSION = '0.5.93'
BASEDIR = op.abspath(op.dirname(__file__))
LIBDIR = op.join(BASEDIR, 'libs')
CUSTOMDIR = environ.get('ZETA_LIBDIR', None)
FORMATS = ['css', 'scss', 'js']
CURRENT_CONFIG = op.join(getcwd(), 'zeta.ini')
HOME_CONFIG = op.join(environ.get('HOME', ''), 'zeta.ini')
COLORS = dict(okgreen='\x1b[92m', warning='\x1b[93m', fail='\x1b[91m', endc='\x1b[0m')