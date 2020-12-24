# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/apibits/version.py
# Compiled at: 2015-08-31 22:18:13
import os
versionfile = os.path.join(os.path.dirname(os.path.dirname(__file__)), '../VERSION')
VERSION = open(versionfile).read()