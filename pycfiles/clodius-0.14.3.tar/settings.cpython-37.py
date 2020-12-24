# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/MyKings/Documents/github/clocwalk/clocwalk/libs/core/settings.py
# Compiled at: 2019-12-10 21:56:50
# Size of source mod 2**32: 957 bytes
import os, platform, sys
from clocwalk import __version__
DESCRIPTION = 'xsseroot#gmail.com'
BANNER = '==============================================================\n\n_________ .__                               .__   __    \n\\_   ___ \\|  |   ____   ______  _  _______  |  | |  | __\n/    \\  \\/|  |  /  _ \\_/ ___\\ \\/ \\/ /\\__  \\ |  | |  |/ /\n\\     \\___|  |_(  <_> )  \\___\\     /  / __ \\|  |_|    < \n \\______  /____/\\____/ \\___  >\\/\\_/  (____  /____/__|_ \\\n        \\/                 \\/             \\/          \\/\n\n        clocwalk v%s %s\n==============================================================\n' % (__version__, DESCRIPTION)
IS_WIN = platform.system()
PLATFORM = os.name
PYVERSION = sys.version.split()[0]