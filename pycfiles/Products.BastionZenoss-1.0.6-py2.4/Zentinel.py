# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/Zentinel.py
# Compiled at: 2011-01-11 16:22:56
import Globals
from Products.CMFCore.utils import UniqueObject, registerToolInterface
from zope.interface import implements
from Products.windowZ.content.Window import Window
from config import ZENTINEL_TOOL
from interfaces import IZentinelTool

class ZentinelTool(UniqueObject, Window):
    """
    The zport wrapped thingy

    This is essentially a place-holder until we fully skin Zenoss
    """
    __module__ = __name__
    meta_type = 'Zentinel Tool'
    portal_type = Window.portal_type
    implements(IZentinelTool)

    def __init__(self, id=ZENTINEL_TOOL):
        Window.__init__(self, id)

    def manage_afterAdd(self, item, container):
        self.update(title='Zenoss Zentinel', catalog_page_content=False, show_reference=False, remoteUrl='/zport/dmd')


Globals.InitializeClass(ZentinelTool)
registerToolInterface(ZENTINEL_TOOL, IZentinelTool)