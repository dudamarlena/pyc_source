# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/imports.py
# Compiled at: 2011-12-25 05:31:43
"""
 Importing the settings from the web project
 this is the module that needs to be replaced while testing
 it needs to be called only in the config modueland nowhere else because fo dependencies
"""
import os
from os.path import join as pjoin
from os.path import abspath, dirname

def __getInstallLoc__():
    return dirname(dirname(abspath(__file__)))


INSTALL_LOC = __getInstallLoc__()

def __getProjectInfo__():
    prj = pjoin(os.getcwd(), '.halProject')
    if not os.path.exists(prj):
        prj = pjoin(INSTALL_LOC, '.halProject')
        result = {'templates': pjoin(INSTALL_LOC, 'Templates'), 'project': pjoin(INSTALL_LOC, 'baseProject')}
    else:
        replacementsDict = {'halweb': INSTALL_LOC}
        result = dict(set([ (x.split('=')[0].strip(), x.split('=')[1].strip()) for x in open(prj, 'r').readlines() if x.strip()[0] != '#' and x.strip()
                          ]))
        for k in result.iterkeys():
            for rk in replacementsDict:
                result[k] = result[k].replace('${' + rk + '}', replacementsDict[rk])

    return (
     abspath(dirname(prj)), result)


def __getProjLoc__():
    root, info = __getProjectInfo__()
    return pjoin(root, info['project'])


PROJ_LOC = __getProjLoc__()

def __getTemplatesLoc__():
    root, info = __getProjectInfo__()
    return pjoin(root, info['templates'])


TEMPLATES_LOC = __getTemplatesLoc__()