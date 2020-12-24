# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.6/site-packages/akamu/config/diglot.py
# Compiled at: 2013-05-14 11:23:00
__doc__ = "\nManage diglot filesytem from Akara configuration\n\nRequires a configuration section, for example:\n\nclass diglot:\n    rootPath       = '..'\n    datasetName    = '..'\n    graphUriFn     = functionName\n    transforms4Dir = {\n        u'.. FS directory ..' : u'.. FS XSLT path ..'\n    }\n"
import akara
from akamu.diglot import Manager

def GetDiglotManager(graphUriFn=None):
    if graphUriFn is None:
        graphUriFn = akara.module_config().get('graphUriFn')
    rootPath = akara.module_config().get('rootPath')
    datasetName = akara.module_config().get('datasetName')
    transforms4Dir = akara.module_config().get('transforms4Dir', {})
    return Manager(rootPath, datasetName, graphUriFn=graphUriFn, transforms4Dir=transforms4Dir)