# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/settings.py
# Compiled at: 2019-12-10 21:56:50
import os, platform, sys
from clocwalk import __version__
DESCRIPTION = 'xsseroot#gmail.com'
BANNER = '==============================================================\n\n_________ .__                               .__   __    \n\\_   ___ \\|  |   ____   ______  _  _______  |  | |  | __\n/    \\  \\/|  |  /  _ \\_/ ___\\ \\/ \\/ /\\__  \\ |  | |  |/ /\n\\     \\___|  |_(  <_> )  \\___\\     /  / __ \\|  |_|    < \n \\______  /____/\\____/ \\___  >\\/\\_/  (____  /____/__|_ \\\n        \\/                 \\/             \\/          \\/\n\n        clocwalk v%s %s\n==============================================================\n' % (__version__, DESCRIPTION)
IS_WIN = platform.system()
PLATFORM = os.name
PYVERSION = sys.version.split()[0]