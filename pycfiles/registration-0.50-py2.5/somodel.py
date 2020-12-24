# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/registration/ormmanager/tests/somodel.py
# Compiled at: 2008-07-04 10:34:30
from sqlobject import *
from datetime import datetime
from turbogears import testutil, database
database.set_db_uri('sqlite:///:memory:')
__connection__ = hub = database.PackageHub('somodel')

class Group(SQLObject):
    """
    An ultra-simple group definition.
    """

    class sqlmeta:
        table = 'tg_group'

    group_name = UnicodeCol(length=16, alternateID=True, alternateMethodName='by_group_name')
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)
    users = RelatedJoin('User', intermediateTable='user_group', joinColumn='group_id', otherColumn='user_id')


class User(SQLObject):
    """
    Reasonably basic User definition. Probably would want additional 
    attributes.
    """

    class sqlmeta:
        table = 'tg_user'

    user_name = UnicodeCol(length=16, alternateID=True, alternateMethodName='by_user_name')
    email_address = UnicodeCol(length=255, alternateID=True, alternateMethodName='by_email_address')
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)
    groups = RelatedJoin('Group', intermediateTable='user_group', joinColumn='user_id', otherColumn='group_id')