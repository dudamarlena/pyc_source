# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/security/db_security.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 17, 2012\n\n@package: security\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the database settings for the security database.\n'
from ally.container import ioc, support
from ally.container.binder_op import bindValidations
from ally.support.sqlalchemy.mapper import mappingsOf
from ally.support.sqlalchemy.session import bindSession
from security.meta.metadata_security import meta
from sql_alchemy import database_config
from sql_alchemy.database_config import alchemySessionCreator, metas
support.include(database_config)
alchemySessionCreator = alchemySessionCreator

@ioc.replace(database_url)
def database_url():
    """This database URL is used for the security tables"""
    return 'sqlite:///workspace/shared/security.db'


@ioc.before(metas)
def updateMetasForSecurity():
    metas().append(meta)


def bindSecuritySession(proxy):
    bindSession(proxy, alchemySessionCreator())


def bindSecurityValidations(proxy):
    bindValidations(proxy, mappingsOf(meta))