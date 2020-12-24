# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/gateway_acl/database.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Jan 17, 2012

@package: gateway acl
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the database settings.
"""
from ..sql_alchemy.db_application import metas, bindApplicationSession
from acl.meta.metadata_acl import meta
from ally.container import ioc

@ioc.entity
def binders():
    return [
     bindApplicationSession]


@ioc.before(metas)
def updateMetasForACL():
    metas().append(meta)