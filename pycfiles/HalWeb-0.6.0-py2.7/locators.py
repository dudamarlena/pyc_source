# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/locators.py
# Compiled at: 2011-12-25 05:31:43
import os
from os.path import join as pjoin
from config import proj_settings as settings

def LocateControllerModule(packageName):
    return pjoin(settings.CONTROLLERS_DIR, BasePathFromName(packageName) + settings.CONTROLLER_MODULE_SUFIX + '.py')


def LocateModelModule(packageName):
    return pjoin(settings.MODELS_DIR, BasePathFromName(packageName) + settings.MODEL_MODULE_SUFIX + '.py')


def LocateFormModelModule(packageName):
    return pjoin(settings.FORM_MODELS_DIR, BasePathFromName(packageName) + settings.MODEL_FORM_MODULE_SUFIX + '.py')


def LocatePagesDir(packageName):
    return pjoin(settings.PAGE_VIEWS_DIR, BasePathFromName(packageName))


def LocateFormsDir(packageName):
    return pjoin(settings.FORM_VIEWS_DIR, BasePathFromName(packageName))


def BasePathFromName(packageName, sep=os.path.sep, splitter='.'):
    return sep.join(packageName.split(splitter))


def locate(packageName, mvcSegment):
    return eval('Locate' + mvcSegment)(packageName)