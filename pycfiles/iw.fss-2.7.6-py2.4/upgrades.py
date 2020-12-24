# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/upgrades.py
# Compiled at: 2008-10-23 05:55:17
"""
GS upgrade steps for iw.fss
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from utils import IfInstalled
from zope.app.component.hooks import getSite

@IfInstalled()
def removeFSSTool(setuptool):
    """We don't need it anymore from version 2.7.3"""
    portal = getSite()
    if 'portal_fss' in portal.objectIds():
        portal._delObject('portal_fss')


@IfInstalled()
def addFSSPropertySheet(setuptool):
    """Options are stored in that propertysheet"""
    setuptool.runImportStepFromProfile('profile-iw.fss:default', 'propertiestool', run_dependencies=False)