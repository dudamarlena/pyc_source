# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nephele/Config.py
# Compiled at: 2017-08-01 11:05:01
import os, stdplus, yaml
config = {}
configFile = os.path.join(os.path.expanduser('~'), '.nephele', 'config.yaml')

def loadConfig():
    global config
    global configFile
    config = {}
    if os.path.exists(configFile):
        print ('Loading config:{}').format(configFile)
        config = yaml.load(stdplus.readfile(configFile))