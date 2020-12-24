# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: src/Products/CMFResource/setuphandlers.py
# Compiled at: 2018-05-16 18:23:05
import logging
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
logger = logging.getLogger(__name__)

@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        return [
         'Products.CMFResource:uninstall']


def post_install(context):
    pass


def uninstall(context):
    pass