# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/mvcPaths.py
# Compiled at: 2011-12-25 05:31:43
import config

def getTemplatesDirs(magicType):
    MvcTemplateDirs = {}
    MvcTemplateDirs.update(config.MvcTemplateDirs)
    for k, v in MvcTemplateDirs.iteritems():
        MvcTemplateDirs[k] = v.replace('{{magicLevel}}', magicType)

    return MvcTemplateDirs


def getTemplateFiles(magicType):
    MvcTemplateFiles = {}
    MvcTemplateFiles.update(config.MvcTemplateFiles)
    for k, v in MvcTemplateFiles.iteritems():
        MvcTemplateFiles[k] = v.replace('{{magicLevel}}', magicType)

    return MvcTemplateFiles