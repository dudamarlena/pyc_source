# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odmltools/info.py
# Compiled at: 2019-11-15 10:54:05
# Size of source mod 2**32: 357 bytes
import os, json
INSTALL_PATH = os.path.dirname(__file__)
with open(os.path.join(INSTALL_PATH, 'info.json')) as (infofile):
    infodict = json.load(infofile)
VERSION = infodict['VERSION']
AUTHOR = infodict['AUTHOR']
COPYRIGHT = infodict['COPYRIGHT']
CONTACT = infodict['CONTACT']
HOMEPAGE = infodict['HOMEPAGE']
CLASSIFIERS = infodict['CLASSIFIERS']