# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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