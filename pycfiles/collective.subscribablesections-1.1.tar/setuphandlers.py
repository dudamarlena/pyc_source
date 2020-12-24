# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/collective/subrip2html/setuphandlers.py
# Compiled at: 2010-12-28 11:04:55
try:
    import pysrt
except ImportError:
    pysrt = False

from Products.CMFCore.utils import getToolByName
from collective.subrip2html.transform import SrtToHtml
from collective.subrip2html.mimetype import SubRipMimetype

def setupVarious(context):
    if not context.readDataFile('collective.subrip2html_various.txt'):
        return
    site = context.getSite()
    addMimetype(site)
    addTransforms(site)


def addMimetype(site):
    mr_tool = getToolByName(site, 'mimetypes_registry')
    mr_tool.register(SubRipMimetype())


def addTransforms(site):
    if not pysrt:
        site.plone_log("Can't install srt_to_html transform: pysrt module not found")
        raise ImportError("Can't install srt_to_html transform: pysrt module not found")
    pt_tool = getToolByName(site, 'portal_transforms')
    pt_tool.registerTransform(SrtToHtml())
    site.plone_log('Installed srt_to_html transform')