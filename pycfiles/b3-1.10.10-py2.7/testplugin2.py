# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\fakeplugins\testplugin2.py
# Compiled at: 2016-03-08 18:42:10
from b3.plugin import Plugin

class Testplugin2Plugin(Plugin):
    requiresConfigFile = False
    requiresParsers = ['Dummy']