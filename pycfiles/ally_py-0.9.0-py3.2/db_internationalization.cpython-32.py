# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/internationalization/db_internationalization.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jan 17, 2012

@package: internationalization
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the database settings for the application database.
"""
from ally.container import ioc, support
from ally.container.binder_op import bindValidations
from ally.support.sqlalchemy.mapper import mappingsOf
from ally.support.sqlalchemy.session import bindSession
from internationalization.meta.metadata_internationalization import meta
from sql_alchemy import database_config
from sql_alchemy.database_config import alchemySessionCreator, metas, database_url
support.include(database_config)
alchemySessionCreator = alchemySessionCreator

@ioc.replace(database_url)
def database_url():
    """This database URL is used for the internationalization tables"""
    return 'sqlite:///workspace/shared/internationalization.db'


@ioc.before(metas)
def updateMetasForInternationalization():
    metas().append(meta)


def bindInternationalizationSession(proxy):
    bindSession(proxy, alchemySessionCreator())


def bindInternationalizationValidations(proxy):
    bindValidations(proxy, mappingsOf(meta))