# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/miscprom/__init__.py
# Compiled at: 2018-05-12 00:39:41
# Size of source mod 2**32: 221 bytes
import os, envdir
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'miscprom.standalone.settings')
CONFIG_DIR = os.path.expanduser('~/.config/exporters')
if os.path.exists(CONFIG_DIR):
    envdir.open(CONFIG_DIR)