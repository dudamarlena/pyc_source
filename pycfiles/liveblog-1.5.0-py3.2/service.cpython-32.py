# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/url_info/service.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Dec 20, 2012

@package: url_info
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mugur Rus

Contains the services for URL info extraction.
"""
from ally.container import support
from ..plugin.registry import registerService
SERVICES = 'url_info.api.*.I*Service'
support.createEntitySetup('url_info.impl.**.*')
support.listenToEntities(SERVICES, listeners=registerService)
support.loadAllEntities(SERVICES)