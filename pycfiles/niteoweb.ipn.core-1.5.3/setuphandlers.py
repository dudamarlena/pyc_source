# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/nw1/niteoweb.ipn.core/src/niteoweb/ipn/core/setuphandlers.py
# Compiled at: 2013-09-25 09:25:26
"""Custom import step for niteoweb.ipn.core."""
from plone import api
from niteoweb.ipn.core import VALIDITY
from niteoweb.ipn.core import DISABLED

def setupVarious(context):
    """Custom Python code ran when installing niteoweb.ipn.core.

    @param context:
        Products.GenericSetup.context.DirectoryImportContext instance
    """
    if context.readDataFile('niteoweb.ipn.core.marker.txt') is None:
        return
    else:
        groupdata = api.portal.get_tool('portal_groupdata')
        if not groupdata.hasProperty(VALIDITY):
            groupdata.manage_addProperty(VALIDITY, -1, 'int')
        api.group.create(groupname=DISABLED)
        return