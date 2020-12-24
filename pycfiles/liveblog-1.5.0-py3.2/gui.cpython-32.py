# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/superdesk_user/gui.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Feb 2, 2012

@package: superdesk user
@copyright: 2011 Sourcefabric o.p.s.
@license http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the GUI configuration setup for the node presenter plugin.
"""
from ..gui_action.defaults import menuAction
from ..gui_core.gui_core import publishGui, publishedURI, publish
from ally.container import ioc

@publish
def publishJS():
    publishGui('superdesk/user')


@ioc.before(menuAction)
def setActionScripts():
    menuAction().Script = publishedURI('superdesk/user/scripts/js/menu.js')