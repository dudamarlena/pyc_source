# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/drink/config.py
# Compiled at: 2011-04-12 18:10:04
__all__ = [
 'BASE_DIR', 'config']
import os, ConfigParser
BASE_DIR = os.path.abspath(os.path.split(__file__)[0])
config = ConfigParser.ConfigParser()
config.read([os.path.join(BASE_DIR, 'settings.ini'),
 os.path.expanduser('~/.drink.ini')])