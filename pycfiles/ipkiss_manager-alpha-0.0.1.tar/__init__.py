# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/antonio/Projects/ipkiss_manager/ipkiss_manager/__init__.py
# Compiled at: 2013-01-18 07:49:17
import os
FIXTURES = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fixtures')
if os.name == 'nt':
    LOCAL_DATA_FOLDER = os.path.join(os.environ['appdata'], 'IPKISS_manager')
elif os.name == 'posix':
    LOCAL_DATA_FOLDER = os.path.join(os.environ['HOME'], '.IPKISS_manager')
else:
    raise Exception('Not supported OS family: %s\n.' % os.name)