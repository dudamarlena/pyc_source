# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.6/site-packages/akamu/config/diglot.py
# Compiled at: 2013-05-14 11:23:00
"""
Manage diglot filesytem from Akara configuration

Requires a configuration section, for example:

class diglot:
    rootPath       = '..'
    datasetName    = '..'
    graphUriFn     = functionName
    transforms4Dir = {
        u'.. FS directory ..' : u'.. FS XSLT path ..'
    }
"""
import akara
from akamu.diglot import Manager

def GetDiglotManager(graphUriFn=None):
    if graphUriFn is None:
        graphUriFn = akara.module_config().get('graphUriFn')
    rootPath = akara.module_config().get('rootPath')
    datasetName = akara.module_config().get('datasetName')
    transforms4Dir = akara.module_config().get('transforms4Dir', {})
    return Manager(rootPath, datasetName, graphUriFn=graphUriFn, transforms4Dir=transforms4Dir)