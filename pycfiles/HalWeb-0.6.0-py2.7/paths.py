# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/baseProject/lib/paths.py
# Compiled at: 2012-01-02 08:54:04
"""
Created on 04.1.2010

@author: KMihajlov
"""
import os, os.path as p
from os.path import join as pjoin
import conf.settings as settings
from lib.halicea import cache
os.path.sep = '/'
os.pathsep = '/'

def GetTemplateDir(template_type):
    return p.join(settings.PAGE_VIEWS_DIR, template_type)


def getViewsDict(directory, base=''):
    result = {}
    memResult = cache.get('paths_ViewsDict_' + directory)
    if memResult is None:
        if os.path.exists(directory) and os.path.isdir(directory):
            for f in os.listdir(directory):
                rf = os.path.join(directory, f)
                if os.path.isfile(rf):
                    result[f[:f.rindex('.')]] = os.path.abspath(rf)

        cache.set(key='paths_ViewsDict', item=result)
        memResult = result
    return memResult


def GetBasesDict():
    result = getViewsDict(settings.BASE_VIEWS_DIR, settings.VIEWS_RELATIVE_DIR)
    return result


def GetBlocksDict():
    result = getViewsDict(settings.BLOCK_VIEWS_DIR, settings.VIEWS_RELATIVE_DIR)
    result.update(__blocksDict__)
    return result


def GetFormsDict(dir):
    result = getViewsDict(p.join(settings.FORM_VIEWS_DIR, dir), settings.VIEWS_RELATIVE_DIR)
    return result


__blocksDict__ = {'blLogin': pjoin(settings.BLOCK_VIEWS_DIR, 'login_menu.inc.html'), 
   'mnTopMenu': pjoin(settings.BLOCK_VIEWS_DIR, 'top_menu.inc.html'), 
   'mnMainMenu': pjoin(settings.BLOCK_VIEWS_DIR, 'menu.bl.inc.html')}
__pluginsDict__ = {'plQuestionarySmall': {'path': '../../lib/plugins/questionaryPlugin', 'view': 'questionaryView.html', 
                          'controller': ''}}