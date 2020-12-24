# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/gui_action/service.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Feb 23, 2012

@package: ally actions gui 
@copyright: 2011 Sourcefabric o.p.s.
@license:  http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Provides the services setup.
"""
from ..plugin.registry import registerService
from .database import binders
from ally.container import support, bind
SERVICES = 'gui.action.api.**.I*Service'
bind.bindToEntities('gui.action.impl.**.*Alchemy', binders=binders)
support.createEntitySetup('gui.action.impl.**.*')
support.listenToEntities(SERVICES, listeners=registerService)
support.loadAllEntities(SERVICES)