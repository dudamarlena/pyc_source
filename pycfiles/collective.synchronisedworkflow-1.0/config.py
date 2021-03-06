# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/config.py
# Compiled at: 2008-12-16 18:21:21
import logging
from Products.CMFCore import permissions
GLOBALS = globals()
PROJECTNAME = 'collective.synchro'
TOOLNAME = 'portal_synchronisation'
ICON = '++resource++portal_synchro.png'
logger = logging.getLogger(PROJECTNAME)
HAS_FSS_27 = False
try:
    from iw.fss import FileSystemStorage
    HAS_FSS_27 = True
except ImportError, e:
    HAS_FSS_27 = False

HAS_FSS_26 = False
try:
    from Products.FileSystemStorage import FileSystemStorage
    HAS_FSS_26 = True
except ImportError, e:
    HAS_FSS_26 = False

HAS_FSS = HAS_FSS_27 or HAS_FSS_26
HAS_PLONE3 = False
try:
    from Products.CMFPlone.migrations import v3_0
    HAS_PLONE3 = True
except ImportError, e:
    HAS_PLONE3 = False

HAS_PLONE25 = False
try:
    from Products.CMFPlone.migrations import v2_5
    HAS_PLONE25 = True
except ImportError, e:
    HAS_PLONE25 = False

if HAS_PLONE3 is False and HAS_PLONE25 is False:
    raise Exception('Please install a good version of plone')
if HAS_PLONE25 and HAS_PLONE3:
    HAS_PLONE25 = False
try:
    from Products.PloneLanguageTool import LanguageTool
    HAS_LANGUAGE_TOOL = True
except:
    HAS_LANGUAGE_TOOL = False

try:
    from Products.LinguaPlone.public import *
    HAS_LINGUA_PLONE = True
except:
    HAS_LINGUA_PLONE = False