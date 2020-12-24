# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/internationalization/service.py
# Compiled at: 2013-10-23 08:39:55
"""
Created on Jan 9, 2012

@package: internationalization
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the services setup for internationalization.
"""
from ..plugin.registry import addService
from .db_internationalization import bindInternationalizationSession, bindInternationalizationValidations
from ally.cdm.spec import ICDM
from ally.cdm.support import ExtendPathCDM
from ally.container import support, ioc, bind
from internationalization.scanner import Scanner
from ..cdm.service import contentDeliveryManager
SERVICES = 'internationalization.api.**.I*Service'

@ioc.entity
def binders():
    return [
     bindInternationalizationSession]


bind.bindToEntities('internationalization.impl.**.*Alchemy', binders=binders)
support.createEntitySetup('internationalization.impl.**.*', 'internationalization.*.impl.**.*', Scanner)
support.listenToEntities(SERVICES, listeners=addService(bindInternationalizationValidations), beforeBinding=False)
support.loadAllEntities(SERVICES)

@ioc.entity
def cdmLocale() -> ICDM:
    """
    The content delivery manager (CDM) for the locale files.
    """
    return ExtendPathCDM(contentDeliveryManager(), 'cache/locale/%s')