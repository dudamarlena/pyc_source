# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/engal/identitymodel.py
# Compiled at: 2006-09-14 12:53:06
from datetime import datetime
from sqlobject import *
from turbogears import identity
from turbogears.database import PackageHub
from engal import util
hub = PackageHub('engal')
__connection__ = hub

class Visit(SQLObject):
    __module__ = __name__

    class sqlmeta:
        __module__ = __name__
        table = 'visit'

    visit_key = StringCol(length=40, alternateID=True, alternateMethodName='by_visit_key')
    created = DateTimeCol(default=datetime.now)
    expiry = DateTimeCol()

    def lookup_visit(cls, visit_key):
        try:
            return cls.by_visit_key(visit_key)
        except SQLObjectNotFound:
            return

        return

    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(SQLObject):
    __module__ = __name__
    visit_key = StringCol(length=40, alternateID=True, alternateMethodName='by_visit_key')
    user_id = IntCol()


class Group(SQLObject):
    """
    An ultra-simple group definition.
    """
    __module__ = __name__

    class sqlmeta:
        __module__ = __name__
        table = 'tg_group'

    group_name = UnicodeCol(length=16, alternateID=True, alternateMethodName='by_group_name')
    display_name = UnicodeCol(length=255)
    created = DateTimeCol(default=datetime.now)
    users = RelatedJoin('User', intermediateTable='user_group', joinColumn='group_id', otherColumn='user_id')
    permissions = RelatedJoin('Permission', joinColumn='group_id', intermediateTable='group_permission', otherColumn='permission_id')


class User(SQLObject):
    """
    Reasonably basic User definition. Probably would want additional attributes.
    """
    __module__ = __name__

    class sqlmeta:
        __module__ = __name__
        table = 'tg_user'

    user_name = UnicodeCol(length=16, alternateID=True, alternateMethodName='by_user_name')
    email_address = UnicodeCol(length=255, alternateID=True, alternateMethodName='by_email_address')
    display_name = UnicodeCol(length=255)
    password = UnicodeCol(length=40)
    created = DateTimeCol(default=datetime.now)
    groups = RelatedJoin('Group', intermediateTable='user_group', joinColumn='user_id', otherColumn='group_id')

    def _get_permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)

        return perms

    def _set_password(self, cleartext_password):
        """Runs cleartext_password through the hash algorithm before saving."""
        hash = identity.encrypt_password(cleartext_password)
        self._SO_set_password(hash)

    def set_password_raw(self, password):
        """Saves the password as-is to the database."""
        self._SO_set_password(password)

    def getRandomPhoto(self):
        return util.choice(self.photos)

    def getRandomPhotos(self, number=3):
        return util.sample(self.photos, 3)


User.sqlmeta.addJoin(SQLMultipleJoin('Photo', joinColumn='owner_id', joinMethodName='photos'))
User.sqlmeta.addJoin(SQLMultipleJoin('PhotoSet', joinColumn='user_id', joinMethodName='photosets'))

class Permission(SQLObject):
    __module__ = __name__
    permission_name = UnicodeCol(length=16, alternateID=True, alternateMethodName='by_permission_name')
    description = UnicodeCol(length=255)
    groups = RelatedJoin('Group', intermediateTable='group_permission', joinColumn='permission_id', otherColumn='group_id')