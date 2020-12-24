# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__plugin__/superdesk_user/populate_default_data.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on May 27, 2013

@package: superdesk user
@copyright: 2013 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Martin Saturka

Populates default data for the services.
"""
from ally.container import app, ioc
from ..superdesk.db_superdesk import alchemySessionCreator
from superdesk.user.meta.user_type import UserTypeMapped
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import exists

@ioc.config
def standard_user_types():
    """ The standard user types """
    return [
     'standard']


def createUserType(key):
    creator = alchemySessionCreator()
    session = creator()
    assert isinstance(session, Session)
    if not session.query(exists().where(UserTypeMapped.Key == key)).scalar():
        userTypeDb = UserTypeMapped()
        userTypeDb.Key = key
        session.add(userTypeDb)
    session.commit()
    session.close()


@app.populate(priority=ioc.PRIORITY_FIRST)
def populateTypes():
    for oneUserType in standard_user_types():
        createUserType(oneUserType)