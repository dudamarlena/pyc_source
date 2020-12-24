# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/models/sharing.py
# Compiled at: 2014-04-28 05:34:58
from pgauth.base import Role
from pgauth.settings import VIEWER_ROLE_ID, EDITOR_ROLE_ID
from djinn_contenttypes.utils import get_object_by_ctype_id

class SharingMixin(object):

    def add_share(self, ctype, cid, mode):
        """ Add share to given ct, with mode """
        from pgevents.settings import SHARE_CONTENT
        from pgevents.events import Events
        if mode == 'viewer':
            role = Role.objects.get(name=VIEWER_ROLE_ID)
            mode = 'bekijken'
        elif mode == 'editor':
            role = Role.objects.get(name=EDITOR_ROLE_ID)
            mode = 'bewerken'
        tgt = get_object_by_ctype_id(ctype, cid)
        if getattr(tgt, 'user', None):
            self.add_local_role(role, tgt.user)
            Events.send(SHARE_CONTENT, self.get_owner(), users=[
             tgt.user], content=self, mode=mode)
        elif getattr(tgt, 'usergroup', None):
            self.add_local_role(role, tgt.usergroup)
            Events.send(SHARE_CONTENT, self.get_owner(), users=tgt.usergroup.members.all(), content=self, mode=mode)
        else:
            raise
        return

    def rm_share(self, ctype, cid, mode):
        """ Remove share to given ct, with mode """
        if mode == 'viewer':
            role = Role.objects.get(name=VIEWER_ROLE_ID)
            mode = 'bekijken'
        elif mode == 'editor':
            role = Role.objects.get(name=EDITOR_ROLE_ID)
            mode = 'bewerken'
        tgt = get_object_by_ctype_id(ctype, cid)
        if getattr(tgt, 'user', None):
            self.rm_local_role(role, tgt.user)
        elif getattr(tgt, 'usergroup', None):
            self.rm_local_role(role, tgt.usergroup)
        else:
            raise
        return

    @property
    def shares(self):
        return self.get_local_roles(role_filter=[
         EDITOR_ROLE_ID, VIEWER_ROLE_ID])

    @property
    def user_shares(self):
        return self.get_local_roles(role_filter=[
         EDITOR_ROLE_ID, VIEWER_ROLE_ID]).filter(user__isnull=False)

    @property
    def group_shares(self):
        return self.get_local_roles(role_filter=[
         EDITOR_ROLE_ID, VIEWER_ROLE_ID]).filter(usergroup__isnull=False)