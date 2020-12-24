# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/internationalization/db_internationalization.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 17, 2012\n\n@package: internationalization\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the database settings for the application database.\n'
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