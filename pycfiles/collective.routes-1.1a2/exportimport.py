# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/roundabout/exportimport.py
# Compiled at: 2008-12-14 05:59:09
from Products.CMFCore.utils import getToolByName

def import_various(context):
    if not context.readDataFile('collective.roundabout.txt'):
        return
    site = context.getSite()
    kupu = getToolByName(site, 'kupu_library_tool')
    paragraph_styles = list(kupu.getParagraphStyles())
    new_styles = [
     ('roundabout', 'RoundAbout|img')]
    to_add = dict(new_styles)
    for style in paragraph_styles:
        css_class = style.split('|')[(-1)]
        if css_class in to_add:
            del to_add[css_class]

    if to_add:
        paragraph_styles += [ '%s|%s' % (v, k) for (k, v) in new_styles if k in to_add ]
        kupu.configure_kupu(parastyles=paragraph_styles)