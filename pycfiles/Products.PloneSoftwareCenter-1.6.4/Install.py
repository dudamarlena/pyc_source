# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/Products/PloneSlimbox/Extensions/Install.py
# Compiled at: 2010-02-19 22:12:19
from cStringIO import StringIO
from Products.CMFCore.DirectoryView import addDirectoryViews
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Extensions.utils import install_subskin
import os, string
from Products.PloneSlimbox.config import *

def install(self):
    """Install Plone Slimbox: Install skin layer, javascript and
    stylesheet
    """
    out = StringIO()
    print >> out, 'Installing %s' % PROJECTNAME
    install_subskin(self, out, GLOBALS)
    print >> out, 'Installed skin'
    csstool = getToolByName(self, 'portal_css')
    csstool.registerStylesheet(id='slimbox2.css', media='screen')
    print >> out, 'Registered stylesheet'
    jstool = getToolByName(self, 'portal_javascripts')
    version = getToolByName(self, 'portal_migration').getFileSystemVersion()
    if version < '3.1':
        jstool.registerScript(id='jquery.min.js')
    jstool.registerScript(id='slimbox2.js')
    print >> out, 'Registered javascript'
    print >> out, 'Installation completed.'
    return out.getvalue()


def uninstall(self):
    out = StringIO()
    skins_tool = getToolByName(self, 'portal_skins')
    skins = skins_tool.getSkinSelections()
    for skin in skins:
        path = skins_tool.getSkinPath(skin)
        path = [ p.strip() for p in path.split(',') if p ]
        while SKINNAME in path:
            path.remove(SKINNAME)

        skins_tool.addSkinSelection(skin, (',').join(path))

    print >> out, 'Uninstalled skin'
    print >> out, 'Uninstalling %s' % PROJECTNAME
    return out.getvalue()