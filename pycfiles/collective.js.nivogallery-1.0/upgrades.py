# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/js/multizoom/upgrades.py
# Compiled at: 2015-11-25 05:27:38
from Products.CMFCore.utils import getToolByName

def recook_js_resources(context):
    getToolByName(context, 'portal_javascripts').cookResources()