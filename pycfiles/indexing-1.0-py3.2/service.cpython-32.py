# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/indexing/service.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Jan 9, 2012

@package: indexing
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services for indexing.
"""
from ..plugin.registry import registerService
from ally.container import support
SERVICES = 'indexing.api.**.I*Service'
support.createEntitySetup('indexing.impl.**.*')
support.listenToEntities(SERVICES, listeners=registerService)
support.loadAllEntities(SERVICES)