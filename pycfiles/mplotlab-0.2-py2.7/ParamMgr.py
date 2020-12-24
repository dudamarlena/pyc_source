# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mplotlab\utils\ParamMgr.py
# Compiled at: 2016-02-07 09:44:32
from ConfigParser import ConfigParser
import os
defaultParams = {'version': '0.1'}
paramFile = os.path.join(os.path.dirname(__file__), 'params.cfg')
configParser = ConfigParser(defaultParams)
configParser.read(paramFile)