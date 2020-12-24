# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/auth/users.py
# Compiled at: 2010-06-12 04:30:35
"""User component for authentication. Normally all the components reside under
zeta.comp, but since zeta is using authkit, it is located here. Also it is not
derived from Component class of component architecture.

Expect all the user methods and permission methods for accessing and data
crunching on database.
"""
from __future__ import with_statement
from hashlib import sha1
from sqlalchemy import *
from paste.util.import_string import eval_import
from authkit.users import *
from sqlalchemy.orm import *
from pylons import config
from zeta.auth.perm import permissions
from zeta.model import meta
from zeta.model.schema import t_project, t_project_team, t_user, t_permission_group, at_user_permissions, at_project_admins
from zeta.model.tables import System, User, UserInfo, UserRelation_Type, UserRelation, UserInvitation, PermissionName, PermissionGroup, Attachment
from zeta.lib.error import ZetaUserError, ZetaAuthorizationError, ZetaAuthenticationError
import zeta.lib.helpers as h, zeta.lib.cache as cache
from zeta.comp.attach import AttachComponent
from zeta.comp.project import ProjectComponent
from zeta.comp.timeline import TimelineComponent
from zeta.comp.xsearch import XSearchComponent
gcache_permnames = []
gcache_proj_permnames = []
gcache_site_permnames = []
builtin_all = all
builtin_any = any

class UsersFromZetaDB(Users):
    """Manage User authentication using database defined by zeta.model"""

    def __init__(self, model, encrypt=None):
        if encrypt is None:

            def encrypt(password):
                return sha1(password).hexdigest()

        self.encrypt = encrypt
        if isinstance(model, (str, unicode)):
            model = eval_import(model)
        if not model.meta.userscomp:
            model.meta.userscomp = self
        self.model = model
        self.meta = self.model.meta
        return

    def user_exists(self, user):
        """Returns ``True`` if a user exists with the given username, 
        ``False`` otherwise. Usernames are case insensitive."""
        return self.get_user(user) and True or False

    def role_exists(self, role):
        """Returns ``True`` if the role exists, ``False`` otherwise. Roles are
        case insensitive."""
        return True

    def group_exists(self, group):
        """Returns ``True`` if the group exists, ``False`` otherwise. Groups 
        are case insensitive.
        Note : This group is different from permission group."""
        return True

    def user_has_password(self, user, password):
        """Returns ``True`` if the user has the password specified, ``False`` 
        otherwise. Passwords are case sensitive. Raises an exception if the
        user doesn't exist."""
        user = self.get_user(user)
        if not user:
            raise AuthKitNoSuchUserError('No such user %r' % user.username)
        else:
            if user.disabled:
                return False
            else:
                if unicode(user.password) == self.encrypt(password):
                    return True
                return False

    def user_has_permnames(self, user, permnames, all=False):
        """Returns ``True`` if the user has all the permnames (when all=True)
        or when the user has any of the permnames (when all=False). ``False``
        otherwise. Raises an exception if the user doesn't exist."""
        if isinstance(permnames, (str, unicode)):
            permnames = [
             permnames]
        upn = self.user_permnames(user)
        granted = map(lambda p: p in upn, permnames)
        if all:
            return builtin_all(granted)
        else:
            return builtin_any(granted)

    def user_has_permgroups(self, user, permgroups, all=False):
        """Returns ``True`` if the user has all the permgroups (when all=True)
        or when the user has any of the permgroups (when all=False). ``False``
        otherwise. Raises an exception if the user doesn't exist.
        """
        if isinstance(permgroups, (str, unicode)):
            permgroups = [
             permgroups]
        upg = self.user_permgroups(user)
        granted = map(lambda pg: pg in upg, permgroups)
        if all:
            return builtin_all(granted)
        else:
            return builtin_any(granted)

    def user_has_role(self, user, role):
        """Returns ``True`` if the user has the role specified, ``False`` 
        otherwise. Raises an exception if the user doesn't exist."""
        if not self.user_exists(user):
            raise AuthKitNoSuchUserError('No such user %r' % user.username)
        return True

    def user_has_group(self, user, group):
        """Returns ``True`` if the user has the group specified, ``False`` 
        otherwise."""
        if not self.user_exists(user):
            raise AuthKitNoSuchUserError('No such user %r' % user.username)
        return True

    @staticmethod
    def list_users():
        """Returns a lowercase list of all usernames ordered alphabetically."""
        msession = meta.Session()
        return [ u.username for u in msession.query(User).order_by(User.username)
               ]

    @staticmethod
    def list_emailids():
        """Returns a list of all user emailids in sorted order."""
        msession = meta.Session()
        return [ u.emailid for u in msession.query(User).order_by(User.emailid)
               ]

    @staticmethod
    def list_roles():
        """Returns a lowercase list of all roll names ordered alphabetically."""
        return []

    def user(self, username):
        """Returns a dictionary in the following format:

        .. code-block :: Python
        
            {
                'username': username,
                'group':    None,
                'password': password,
                'roles':    []
            }

        The role names are ordered alphabetically
        Raises an exception if the user doesn't exist.
        Note : This method is used expected by Authkit, while the get_user()
        interface can be used for our native User schema."""
        msession = self.meta.Session()
        username = unicode(username)
        user = msession.query(User).filter_by(username=username).first()
        if user:
            return {'username': user.username, 'group': None, 
               'password': user.password, 
               'roles': []}
        else:
            raise ZetaAuthenticationError('No such user %r' % username)
            return

    def get_userrel_type(self, relationtype=None):
        """Get user relation type identified by,
        `relationtype`, which can be,
            `id` or `userrel_type` or `UserRelation_Type` instance.
        if relationtype==None,
            then return a list of all UserRelation_Type instances.
            
        Return,
            A list UserRelation_Type instances, or
            UserRelation_Type instance."""
        msession = self.meta.Session()
        if isinstance(relationtype, (int, long)):
            relationtype = msession.query(UserRelation_Type).filter_by(id=relationtype).first()
        elif isinstance(relationtype, (str, unicode)):
            relationtype = msession.query(UserRelation_Type).filter_by(userrel_type=relationtype).first()
        elif relationtype == None:
            relationtype = msession.query(UserRelation_Type).all()
        elif isinstance(relationtype, UserRelation_Type):
            pass
        else:
            relationtype = None
        return relationtype

    def get_user(self, user=None, attrload_all=[], attrload=[]):
        """Get user entry identified by,
        `user` which can be,
            `id` or `username` or `User` instance.
        if user=None,
            Then all the registered users will be returned.

        Always eager load, 'userinfo' attribute as well.

        Return,
            A list of User instances, or
            User instance."""
        if isinstance(user, User) and attrload_all == [] and attrload == []:
            return user
        else:
            msession = self.meta.Session()
            if isinstance(user, (int, long)):
                q = msession.query(User).filter_by(id=user)
            elif isinstance(user, (str, unicode)):
                q = msession.query(User).filter_by(username=unicode(user))
            elif isinstance(user, User):
                q = msession.query(User).filter_by(id=user.id)
            else:
                q = None
            if q:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                user = q.first()
            elif user == None:
                q = msession.query(User)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                user = q.all()
            else:
                user = None
            return user

    def get_userrel(self, userrelation=None, userfrom=None, userto=None, reltype=None):
        """Get the user relation entry identified by,
        `userrelation` which can be,
            `id` or `UserRelation` instance.
        if userrelation == None,
            then the UserRelation entries are filtered by `userfrom`, `userto`
            and `reltype` object.

        Return,
            Lists of all UserRelation instances or
            UserRelation instance."""
        userfrom = userfrom and self.get_user(userfrom)
        userto = userto and self.get_user(userto)
        reltype = reltype and self.get_userrel_type(reltype)
        msession = self.meta.Session()
        if isinstance(userrelation, (int, long)):
            userrelations = msession.query(UserRelation).filter_by(id=userrelation).first()
        elif isinstance(userrelation, UserRelation):
            userrelations = userrelation
        elif userfrom or userto or reltype:
            q = msession.query(UserRelation)
            if userfrom:
                q = q.filter_by(userfrom_id=userfrom.id)
            if userto:
                q = q.filter_by(userto_id=userto.id)
            if reltype:
                q = q.filter_by(userreltype_id=reltype.id)
            userrelations = q.all()
        else:
            userrelations = msession.query(UserRelation).all()
        return userrelations

    def user_password(self, user):
        """Returns the password associated with the user or ``None`` if no
        password exists. Raises an exception is the user doesn't exist."""
        user = self.get_user(user)
        return user and user.password or None

    def user_permnames(self, user):
        """Returns a list of all the permission names for the given user 
        ordered alphabetically. Raises an exception if the user doesn't exist."""
        user = self.get_user(user, attrload_all=['permgroups.perm_names'])
        if user:
            return [ p.perm_name for pg in user.permgroups for p in pg.perm_names ]
        raise AuthKitNoSuchUserError('No such user %s' % (user and user.username))

    def user_permgroups(self, user):
        """Returns a list of all the permission groups for the given user 
        ordered alphabetically. Raises an exception if the user doesn't exist."""
        user = self.get_user(user, attrload=['permgroups'])
        if user:
            return [ pg.perm_group for pg in user.permgroups ]
        raise AuthKitNoSuchUserError('No such user %r' % user.username)

    def user_roles(self, user):
        """Returns a list of all the role names for the given user ordered 
        alphabetically. Raises an exception if the user doesn't exist."""
        if not self.user_exists(user):
            raise AuthKitNoSuchUserError('No such user %r' % user.username)
        return []

    def user_group(self, user):
        """Returns the group associated with the user or ``None`` if no group is
        associated. Raises an exception if the user doesn't exist."""
        if not self.user_exists(user):
            raise AuthKitNoSuchUserError('No such user %r' % user.username)
        return

    def userreltype_create(self, userrel_types, byuser=None):
        """Create user relation entries for the relations specified by,
        `userrel_type`
            which can be, a string specifying the relation name or a list of
            such strings"""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        if isinstance(userrel_types, (str, unicode)):
            userrel_types = [
             userrel_types]
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            [ msession.add(UserRelation_Type(unicode(r))) for r in userrel_types ]
        tlcomp.log(byuser, 'added user relation types, `%s`' % (', ').join(userrel_types))

    def user_create(self, user, userinfo=None, update=False):
        """Before creating the user validate the user information.
        `user`     tuple of user account info.
                   (username, emailid, password, timezone)
        `userinfo` tuple of user personal info
                   (fname,   mname, lname, addr1, addr2, city, pcode, state,
                    country, userpanes)
        if update=True,
            An existing user details will be updated.
            In which case `userinfo` can be None . But `user` should
            follow the tuple format.

        Return,
            User instance."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        user = list(user)
        user[0] = user[0].lower()
        u = self.get_user(user[0], attrload=['userinfo'])
        user[2] = user[2] and sha1(user[2]).hexdigest()
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            if update and u or u:
                user[1] != None and setattr(u, 'emailid', user[1])
                user[2] != None and setattr(u, 'password', user[2])
                user[3] != None and setattr(u, 'timezone', user[3])
                uinfo = u.userinfo
                if userinfo:
                    uiattrs = [
                     'firstname', 'middlename', 'lastname',
                     'addressline1', 'addressline2', 'city',
                     'pincode', 'state', 'country', 'userpanes']
                    [ setattr(uinfo, uiattrs[i], userinfo[i]) for i in range(10) if userinfo[i] != None
                    ]
                log = 'updated user preference'
                idxreplace = True
            else:
                u = User(*user)
                userinfo = UserInfo(*userinfo)
                u.userinfo = userinfo
                msession.add(u)
                log = 'registered new user'
                idxreplace = False
        srchcomp = XSearchComponent(compmgr)
        tlcomp.log(u, log)
        srchcomp.indexuser([u], replace=idxreplace)
        cache.invalidate(self.mapfor_usersite)
        return u

    def user_remove(self, user, byuser=None):
        """Remove the user identified by,
        `user` which can be,
            `id` or `username` or `User` instance.
        
        Note : Removing the user could orphan the following items,
                attachment
                project administration
                project components
                tickets prompting the user
                ticket status
                ticket comments
                review author
                review moderator
                review comments
                wiki creator
                wiki author
                wiki comments.
                and much more ....."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        user = self.get_user(user)
        self.user_set_photo(user)
        self.user_set_icon(user)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            msession.delete(user)
        tlcomp.log(byuser, 'removed user `%s`' % user.username)

    def user_set_photo(self, user, photo=None):
        """Attachment object (entry) to be assiociated as user photo for
        `user`. If a photo attachment is already associated with the user,
        then the old attachment is removed and replaced with new photo
        attachment.
        if photo==None,
            then remove the photo attachment."""
        compmgr = h.fromconfig('compmgr')
        attcomp = AttachComponent(compmgr)
        tlcomp = TimelineComponent(compmgr)
        log = ''
        user = self.get_user(user)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            if user:
                if isinstance(user.photofile, Attachment):
                    attcomp.remove_attach(user.photofile, byuser=user)
                    log = 'removed user photo'
                if photo:
                    user.photofile = attcomp.get_attach(photo)
                    photo.uploader = user
                    log = 'uploaded user photo, `%s`' % photo.filename
        log and tlcomp.log(user, log)
        return

    def user_set_icon(self, user, icon=None):
        """Attachment object (entry) to be assiociated as user icon for
        `user`. If an icon attachment is already associated with the user,
        then the old attachment is removed and replaced with new icon
        attachment.
        if icon==None,
            then remove the icon attachment."""
        compmgr = h.fromconfig('compmgr')
        attcomp = AttachComponent(compmgr)
        tlcomp = TimelineComponent(compmgr)
        log = ''
        user = self.get_user(user)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            if user:
                if isinstance(user.iconfile, Attachment):
                    attcomp.remove_attach(user.iconfile, byuser=user)
                    log = 'removed user icon'
                if icon:
                    user.iconfile = attcomp.get_attach(icon)
                    icon.uploader = user
                    log = 'uploaded user icon, `%s`' % icon.filename
        log and tlcomp.log(user, log)
        return

    def user_add_permgroup(self, user, perm_groups, byuser=None):
        """Add the permission group `perm_groups` for user identified by
        `user`. perm_groups must have already been created.
        `perm_groups` must be a list of permission group identified by,
            `perm_group` or PermissionGroup instance
        """
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        if not isinstance(perm_groups, list):
            perm_groups = [
             perm_groups]
        perm_groups = filter(None, perm_groups)
        pgmapper = lambda pg: isinstance(pg, PermissionGroup) and pg.perm_group or pg
        perm_groups = map(pgmapper, perm_groups)
        denormalize = lambda pg: [pg, 'defgrp_' + pg.lower()][pg.isupper()]
        perm_groups = map(denormalize, perm_groups)
        _pglist = []
        [ _pglist.extend([(pg.perm_group, pg), (pg.id, pg)]) for pg in self.get_permgroup()
        ]
        pgdict = dict(_pglist)
        user = self.get_user(user)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            if user:
                perm_groups = filter(None, map(lambda pg: pgdict.get(pg, None), perm_groups))
                user.permgroups.extend(perm_groups)
                log = 'added permission groups to user, `%s`' % (', ').join([ pg.perm_group for pg in perm_groups ])
        cache.invalidate(self.mapfor_usersite)
        tlcomp.log(byuser, log)
        return user

    def user_remove_permgroup(self, user, perm_groups, byuser=None):
        """Add the permission group `perm_groups` for user identified by
        `user`."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        if not isinstance(perm_groups, list):
            perm_groups = [
             perm_groups]
        perm_groups = filter(None, perm_groups)
        pgmapper = lambda pg: isinstance(pg, PermissionGroup) and pg.perm_group or pg
        perm_groups = map(pgmapper, perm_groups)
        denormalize = lambda pg: [pg, 'defgrp_' + pg.lower()][pg.isupper()]
        perm_groups = map(denormalize, perm_groups)
        _pglist = []
        [ _pglist.extend([(pg.perm_group, pg), (pg.id, pg)]) for pg in self.get_permgroup()
        ]
        pgdict = dict(_pglist)
        user = self.get_user(user)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            if user:
                [ user.permgroups.remove(pgdict[pg]) for pg in perm_groups ]
        cache.invalidate(self.mapfor_usersite)
        tlcomp.log(byuser, 'deleted permission groups from user, `%s`' % (', ').join([ pgdict[pg].perm_group for pg in perm_groups ]))
        return user

    def user_add_relation(self, user, relateduser, relationtype, byuser=None):
        """Relate user `user` and user `relateduser` as `relationtype`.
        `user` can be,
            `id` or `username` or `User` instance.
        `relateduser` can be,
            `id` or `username` or `User` instance.
        `relationtype` can be,
            `id` or `userrel_type` or `UserRelation` instance."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        user = self.get_user(user)
        relateduser = self.get_user(relateduser)
        relationtype = self.get_userrel_type(relationtype)
        ur = self.get_userrel(userfrom=user, userto=relateduser, reltype=relationtype)
        msession = self.meta.Session()
        if ur:
            ur = ur[0]
            log = ''
        else:
            with msession.begin(subtransactions=True):
                ur = UserRelation()
                ur.userreltype = relationtype
                ur.userfrom = user
                ur.userto = relateduser
                msession.add(ur)
                log = 'Proposed a relation `%s` to user `%s`' % (
                 relationtype.userrel_type, user.username)
        log and tlcomp.log(byuser, log)
        return ur

    def user_approve_relation(self, userrelations, approve=True, byuser=None):
        """Approve the userrelations identified by 
        `userrelations` which can be,
            `id` or `UserRelation` instance or
            list of `id` and `UserRelation` instances."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        if not isinstance(userrelations, list):
            userrelations = [
             userrelations]
        userrelations = [ self.get_userrel(ur) for ur in userrelations ]
        logs = []
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            for ur in userrelations:
                if not ur:
                    continue
                ur.approved = approve
                logs.append('approved relation `%s` from user `%s`' % (
                 ur.userreltype.userrel_type, ur.userfrom.username))

        [ tlcomp.log(byuser, log) for log in logs ]

    def user_remove_relation(self, userrelations, byuser=None):
        """Remove the userrelations identified by 
        `userrelations` which can be,
            `id` or `UserRelation` instance or
            list of `id` and `UserRelation` instances."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        if not isinstance(userrelations, list):
            userrelations = [
             userrelations]
        userrelations = [ self.get_userrel(ur) for ur in userrelations ]
        logs = []
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            for ur in userrelations:
                if not ur:
                    continue
                logs.append('deleted user %s with relation `%s`' % (
                 ur.userto.username, ur.userreltype.userrel_type))
                msession.delete(ur)

        [ tlcomp.log(byuser, log) for log in logs ]

    def user_set_group(self, user, group, auto_add_group=False):
        """Sets the user's group to the lowercase of ``group`` or ``None``. If
        the group doesn't exist and ``add_if_necessary`` is ``True`` the 
        group will also be added. Otherwise an ``AuthKitNoSuchGroupError`` 
        will be raised. Raises an exception if the user doesn't exist."""
        return

    def user_add_role(self, user, role, auto_add_role=False):
        """Sets the user's role to the lowercase of ``role``. If the role doesn't
        exist and ``add_if_necessary`` is ``True`` the role will also be
        added. Otherwise an ``AuthKitNoSuchRoleError`` will be raised. Raises
        an exception if the user doesn't exist."""
        return

    def user_remove_group(self, user):
        """Sets the group to ``None`` for the user specified by ``user``.
        Raises an exception if the user doesn't exist."""
        return

    def user_remove_role(self, user, role):
        """Removes the role from the user specified by ``user``. Raises 
        an exception if the user doesn't exist."""
        return

    def user_disable(self, user, disable=True, byuser=None):
        """Disable the user identified by,
        `user`, which can be,
            `id` or `username` or `User` instance.
        """
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        user = self.get_user(user)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            user.disabled = disable
        tlcomp.log(byuser, 'disabled user, `%s`' % user.username)

    def inviteuser(self, user, emailid):
        """For `emailid` generate a digest and store it in database"""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        digest = sha1(user.username + emailid + 'erode').hexdigest()
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            uinv = UserInvitation(emailid, digest)
            uinv.byuser = user
            msession.add(uinv)
        tlcomp.log(user, 'Invited user, `%s`' % emailid)
        return digest

    def get_invitation(self, uinv=None):
        """Get `userinvitation` entries"""
        msession = self.meta.Session()
        if isinstance(uinv, (int, long)):
            uinvs = msession.query(UserInvitation).filter_by(id=uinv).first()
        else:
            uinvs = msession.query(UserInvitation).all()
        return uinvs

    def invbydigest(self, digest):
        """Fetch the invitation entry for `digest`"""
        msession = self.meta.Session()
        uinv = msession.query(UserInvitation).filter_by(digest=digest).first()
        return uinv

    def acceptedby(self, user, uinv):
        """`user` has accepted the invitation"""
        user = self.get_user(user)
        msession = self.meta.Session()
        if isinstance(uinv, (int, long)):
            uinv = msession.query(UserInvitation).filter_by(id=uinv).first()
        with msession.begin(subtransactions=True):
            uinv.acceptedby = user.username

    def userbyemailid(self, emailid):
        """Fetch the User object matching `emailid`"""
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            user = msession.query(User).filter_by(emailid=emailid).first()
        return user

    def get_connections(self, user):
        """Process `userconnections` and `connectedusers` for the user identified by,
        `user` which can be,
            `id` or `username` or `User` instance.

        Return a tuple of three dictionaries ( touserrels, fromuserrels, potrels )
        with each dictionary element is a `userrel_type` to list mapping.
            The list mapped in touserrels is a tuple of,
                (user.username, user.id, approved)
            The list mapped in fromuserrels is a tuple of,
                (user.username, user.id, approved)
            The list mapped in potrels is a sequence of username."""
        allusers = [ u.username for u in self.get_user() ]
        user = self.get_user(user, attrload_all=[
         'userconnections.userreltype',
         'userconnections.userto',
         'connectedusers.userreltype',
         'connectedusers.userfrom'])
        reltypes = [ rt.userrel_type for rt in self.get_userrel_type() ]
        touserrels = dict([ (rt, []) for rt in reltypes ])
        fromuserrels = dict([ (rt, []) for rt in reltypes ])
        potrels = dict([ (rt, allusers[:]) for rt in reltypes ])
        for ur in user.userconnections:
            touserrels[ur.userreltype.userrel_type].append((
             ur.userto.username, ur.id, ur.approved))
            if ur.userto.username in potrels[ur.userreltype.userrel_type]:
                potrels[ur.userreltype.userrel_type].remove(ur.userto.username)

        for ur in user.connectedusers:
            fromuserrels[ur.userreltype.userrel_type].append((
             ur.userfrom.username, ur.id, ur.approved))

        return (
         touserrels, fromuserrels, potrels)

    def projectnames(self, user):
        """Generate a list of projects that the `user` is associated with,
        if `user` is User object, it is assumed that `projecteams.project` and
        `adminprojects` attributes are -- eagerloaded.
        """
        if isinstance(user, User):
            names = [ pt.project.projectname for pt in user.projectteams ] + [ p.projectname for p in user.adminprojects ]
        elif isinstance(user, (int, long)):
            oj = t_project.outerjoin(t_project_team).outerjoin(at_project_admins, at_project_admins.c.projectid == t_project.c.id)
            q = select([t_project.c.projectname], bind=meta.engine).select_from(oj).where(or_(t_project_team.c.user_id == user, at_project_admins.c.adminid == user))
            names = [ tup[0] for tup in q.execute().fetchall() ]
        elif isinstance(user, (str, unicode)):
            tbl_auser = t_user.alias('adminuser')
            oj = t_project.outerjoin(t_project_team).outerjoin(t_user, t_project_team.c.user_id == t_user.c.id).outerjoin(at_project_admins, at_project_admins.c.projectid == t_project.c.id).outerjoin(tbl_auser, at_project_admins.c.adminid == tbl_auser.c.id)
            q = select([t_project.c.projectname], bind=meta.engine).select_from(oj).where(or_(t_user.c.username == user, tbl_auser.c.username == user))
            names = [ tup[0] for tup in q.execute().fetchall() ]
        return list(set(names))

    def ustatus(self, users):
        """Alternate API to crunch userstatus by passing a prefetched list of
        users from DB"""
        return self._userstatus(users=users)

    def siteadmin(self):
        """Fetch data from database and crunch them for user, site-level
        administration
            Return, 
                ( usernames, userpermissionmap, userstatus )
        """
        allperms = self.site_permnames
        status = {'enabled': [], 'disabled': []}
        x_users = ['admin']
        lookup = ['enabled', 'disabled']
        userperms = {}
        permmap = {}
        usernames = []
        oj = t_user.outerjoin(at_user_permissions).outerjoin(t_permission_group)
        stmt = select([t_user.c.username, t_user.c.disabled,
         t_permission_group.c.perm_group], bind=meta.engine).select_from(oj)
        for tup in stmt.execute().fetchall():
            if tup[0] in x_users:
                continue
            userperms.setdefault(tup[0], []).append(self.normalize_perms(tup[2]))
            status[lookup[tup[1]]].append(tup[0])
            usernames.append(tup[0])

        permmap = dict([ (u, [sorted(filter(None, userperms[u])), sorted(list(set(allperms).difference(userperms[u])))]) for u in userperms
                       ])
        usernames = list(set(usernames))
        status['enabled'] = list(set(status['enabled']))
        status['disabled'] = list(set(status['disabled']))
        return (
         sorted(usernames), permmap, status)

    def _usernames(self):
        """list of registered `username`"""
        stmt = select([t_user.c.username], bind=meta.engine)
        return [ tup[0] for tup in stmt.execute().fetchall() ]

    def _reltypes(self):
        """Sorted list of `userrel_type`"""
        msession = self.meta.Session()
        rels = msession.query(UserRelation_Type).order_by(UserRelation_Type.userrel_type)
        return [ r.userrel_type for r in rels ]

    def _userstatus(self, users=[]):
        """UnSorted dictionary of disabled and enabled `usernames`"""
        d = {'enabled': [], 'disabled': []}
        x_users = [
         'admin']
        lookup = ['enabled', 'disabled']
        if users:
            [ d[lookup[u.disabled]].append(u.username) for u in [ u for u in users if u.username not in x_users ] ]
        else:
            stmt = select([t_user.c.username, t_user.c.disabled], bind=meta.engine)
            [ d[lookup[tup[1]]].append(tup[0]) for tup in stmt.execute().fetchall() if tup[0] not in x_users
            ]
        return d

    def permname_exists(self, perm_name):
        """Returns ``True`` if the PermissionName with perm_name exists,
        ``False`` otherwise. Permission Names are all in upper case."""
        p = self.get_permname(perm_name)
        return bool(p)

    def permgroup_exists(self, perm_group):
        """Returns ``True`` if the PermissionGroup with perm_group exists,
        ``False`` otherwise. Permission Groups are all in lower case."""
        pg = self.get_permgroup(perm_group)
        return bool(pg)

    @staticmethod
    def list_permnames():
        """Returns a uppercase list of all PermissionNames ordered
        alphabetically."""
        global gcache_permnames
        if not gcache_permnames:
            msession = meta.Session()
            gcache_permnames = [ p.perm_name for p in msession.query(PermissionName).order_by(PermissionName.perm_name)
                               ]
        return gcache_permnames

    @staticmethod
    def list_permgroups():
        """Returns a lowercase list of all PermissionGroups ordered
        alphabetically."""
        msession = meta.Session()
        return [ pg.perm_group for pg in msession.query(PermissionGroup).order_by(PermissionGroup.perm_group)
               ]

    def get_permname(self, perm_name=None):
        """Get the PermissionName instance identified by,
        `perm_name` which can be,
            `id` or `perm_name` or `PermissionName` instance.
        if perm_name=None,
            PermissionName instance. or
            List of PermissionName instances
        """
        msession = self.meta.Session()
        if isinstance(perm_name, (int, long)):
            perm_name = msession.query(PermissionName).filter_by(id=perm_name).first()
        elif isinstance(perm_name, (str, unicode)):
            perm_name = msession.query(PermissionName).filter_by(perm_name=perm_name).first()
        elif perm_name == None:
            perm_name = msession.query(PermissionName).all()
        elif isinstance(perm_name, PermissionName):
            pass
        else:
            perm_name = None
        return perm_name

    def get_permgroup(self, perm_group=None, attrload=[], attrload_all=[]):
        """Get the PermissionGroup instance identified by,
        `perm_group` which can be,
            `id` or `perm_group` or `PermissionGroup` instance.
        if perm_group=None,
            PermissionGroup instance. or
            List of PermissionGroup instances"""
        if isinstance(perm_group, PermissionGroup) and attrload == [] and attrload_all == []:
            return perm_group
        else:
            msession = self.meta.Session()
            if isinstance(perm_group, (int, long)):
                q = msession.query(PermissionGroup).filter_by(id=perm_group)
            elif isinstance(perm_group, (str, unicode)):
                perm_group = perm_group.isupper() and 'defgrp_' + perm_group.lower() or perm_group
                q = msession.query(PermissionGroup).filter_by(perm_group=unicode(perm_group))
            elif isinstance(perm_group, PermissionGroup):
                q = msession.query(PermissionGroup).filter_by(id=perm_group.id)
            else:
                q = None
            if q:
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                perm_group = q.first()
            elif perm_group == None:
                q = msession.query(PermissionGroup)
                q = q.options(*[ eagerload_all(e) for e in attrload_all ])
                q = q.options(*[ eagerload(e) for e in attrload ])
                perm_group = q.all()
            else:
                perm_group = None
            return perm_group

    def create_permname(self, perm_name, byuser=None):
        """Add entries for perm_name in permission_name table. Check before
        adding and add the corresponding 'defgrp_...' permission group as
        well."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            perm_name = perm_name.upper()
            if not self.get_permname(perm_name):
                p = PermissionName(perm_name)
                pg = PermissionGroup('defgrp_' + perm_name.lower())
                msession.add(p)
                msession.add(pg)
                pg.perm_names = [p]
        tlcomp.log(byuser, 'created new permission name `%s`' % perm_name)
        return (
         p, pg)

    def change_permname(self, perm_name, new_name, byuser=None):
        """Change `perm_name` name."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        pn = self.get_permname(perm_name)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            pn.perm_name = new_name
        tlcomp.log(byuser, 'changed permission name name to `%s`' % new_name)
        return pn

    def create_apppermissions(self, permissions, byuser=None):
        """Create all the permission names implemented by the application."""
        [ self.create_permname(aperm.perm_name, byuser=byuser) for compname in permissions.keys() for aperm in permissions[compname]
        ]

    def create_permgroup(self, perm_group, byuser=None):
        """Add an entry for perm_group in permission_group table."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            pg = PermissionGroup(perm_group.lower())
            msession.add(pg)
        tlcomp.log(byuser, 'created new permission group `%s`' % perm_group)
        return pg

    def change_permgroup(self, perm_group, new_name, byuser=None):
        """Change the perm_group name."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        pg = self.get_permgroup(perm_group)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            pg.perm_group = new_name
        tlcomp.log(byuser, 'changed permission group name to `%s`' % new_name)
        return pg

    def add_permnames_togroup(self, perm_group, perm_names, append=True, byuser=None):
        """Add the specified list of permission names `perm_names` to already
        created `perm_group`."""
        compmgr = h.fromconfig('compmgr')
        projcomp = ProjectComponent(compmgr)
        tlcomp = TimelineComponent(compmgr)
        perm_group = self.get_permgroup(perm_group)
        if not isinstance(perm_names, list):
            perm_names = [
             perm_names]
        perm_names = filter(None, perm_names)
        pnmapper = lambda pn: isinstance(pn, PermissionName) and pn.perm_name or pn
        perm_names = map(pnmapper, perm_names)
        _pnlist = []
        [ _pnlist.extend([(pn.perm_name, pn), (pn.id, pn)]) for pn in self.get_permname()
        ]
        pndict = dict(_pnlist)
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            if append:
                perm_group.perm_names.extend([ pndict[pn] for pn in perm_names ])
            else:
                perm_group.perm_names = [ pndict[pn] for pn in perm_names ]
        cache.invalidate(self.mapfor_usersite)
        cache.invalidate(projcomp.mapfor_teamperms)
        tlcomp.log(byuser, 'added permnames to permgroup %s,\n%s' % (
         perm_group,
         (', ').join([ pndict[pn].perm_name for pn in perm_names ])))
        return

    def remove_permnames_fromgroup(self, perm_group, perm_names, byuser=None):
        """Remove the specified list of permission names `perm_names` from already
        created `perm_group`."""
        compmgr = h.fromconfig('compmgr')
        projcomp = ProjectComponent(compmgr)
        tlcomp = TimelineComponent(compmgr)
        perm_group = self.get_permgroup(perm_group)
        if not isinstance(perm_names, list):
            perm_names = [
             perm_names]
        perm_names = filter(None, perm_names)
        pnmapper = lambda pn: isinstance(pn, PermissionName) and pn.perm_name or pn
        perm_names = map(pnmapper, perm_names)
        _pnlist = []
        [ _pnlist.extend([(pn.perm_name, pn), (pn.id, pn)]) for pn in self.get_permname()
        ]
        pndict = dict(_pnlist)
        pndict = dict([ (pn.perm_name, pn) for pn in self.get_permname() ])
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            [ perm_group.perm_names.remove(pndict[pn]) for pn in perm_names ]
        cache.invalidate(self.mapfor_usersite)
        cache.invalidate(projcomp.mapfor_teamperms)
        tlcomp.log(byuser, 'deleted permnames from permgroup %s,\n%s' % (
         perm_group,
         (', ').join([ pndict[pn].perm_name for pn in perm_names ])))
        return

    def remove_permgroup(self, perm_groups, byuser=None):
        """Remove permission group identified by,
        `perm_groups` which can be,
            `id` or `perm_group` or `PermissionGroup` instance.
            list of id` or `perm_group` or `PermissionGroup` instance."""
        compmgr = h.fromconfig('compmgr')
        tlcomp = TimelineComponent(compmgr)
        if not isinstance(perm_groups, list):
            perm_groups = [
             perm_groups]
        pgroups = []
        msession = self.meta.Session()
        with msession.begin(subtransactions=True):
            for pg in perm_groups:
                pg = self.get_permgroup(pg)
                if pg:
                    pgroups.append(pg.perm_group)
                    [ msession.delete(projectperm) for projectperm in pg.projectperms
                    ]
                    [ msession.delete(projteamperm) for projteamperm in pg.projteamperms
                    ]
                    msession.delete(pg)

        tlcomp.log(byuser, 'deleted permission groups,\n`%s`' % (', ').join(pgroups))
        return

    def normalize_perms(self, perms):
        """Since the permission names are mapped to 'defgrp_' permission
        groups, this function differentiates the permission names from
        permission groups and returns the normalised version of permission
        list.
        `perms` is a list of permission groups / permission names as strings. 
        """
        if isinstance(perms, list):
            normalizedperms = []
            for p in perms:
                if p[:7] == 'defgrp_':
                    normalizedperms.append(p[7:].upper())
                else:
                    normalizedperms.append(p)

            return sorted(normalizedperms)
        if isinstance(perms, (str, unicode)):
            return [perms, perms[7:].upper()][(perms[:7] == 'defgrp_')]

    def userpermission_map(self, usernames=[], allusers=[]):
        """Return a dictionary of
            { username : [ [ perm_groups ... ], [ ^ perm_groups ... ] ]
              ...
            }
        Only site permissions (for each user) are covered by this function.
        """
        allperms = self.site_permnames
        oj = t_user.outerjoin(at_user_permissions).outerjoin(t_permission_group)
        stmt = select([t_user.c.username, t_permission_group.c.perm_group], bind=meta.engine).select_from(oj)
        userperms = {}
        [ userperms.setdefault(tup[0], []).append(self.normalize_perms(tup[1])) for tup in stmt.execute().fetchall()
        ]
        permmap = dict([ (u, [sorted(filter(None, userperms[u])), sorted(list(set(allperms).difference(userperms[u])))]) for u in userperms
                       ])
        if usernames:
            [ permmap.pop(u) for u in permmap.keys() if u not in usernames ]
        return permmap

    @cache.cache('mapfor_usersite', useargs=False)
    def mapfor_usersite(self):
        """Generate the permission map for site users"""
        maps = {}
        skipusers = [
         'admin', 'anonymous']
        users = self.get_user(attrload_all=['permgroups.perm_names'])
        for u in users:
            if u.username in skipusers:
                continue
            maps[u.username] = [ pn.perm_name for pg in u.permgroups for pn in pg.perm_names
                               ]

        return maps

    def _perm_names(self):
        """Sorted list of all permission names in the database."""
        global gcache_permnames
        if not gcache_permnames:
            msession = meta.Session()
            gcache_permnames = [ p.perm_name for p in msession.query(PermissionName).order_by(PermissionName.perm_name)
                               ]
        return gcache_permnames

    def _proj_permnames(self):
        """Sorted list of all permission names that have project context"""
        global gcache_proj_permnames
        if not gcache_proj_permnames:
            permnames = self._perm_names()
            gcache_proj_permnames = [ a.perm_name for comp in permissions for a in permissions[comp] if a.project if a.perm_name in permnames
                                    ]
        return gcache_proj_permnames

    def _site_permnames(self):
        """Sorted list of all permission names that only have site context"""
        global gcache_site_permnames
        if not gcache_site_permnames:
            permnames = self._perm_names()
            gcache_site_permnames = [ a.perm_name for comp in permissions for a in permissions[comp] if not a.project if a.perm_name in permnames
                                    ]
        return gcache_site_permnames

    def _perm_groups(self):
        """Sorted list of all permission groups in the database"""
        msession = self.meta.Session()
        return [ pg.perm_group for pg in msession.query(PermissionGroup).order_by(PermissionGroup.perm_group)
               ]

    def _mappedpgroups(self):
        """unsorted list of permission groups that are one-to-one mapped to
        permission groups"""
        return [ pg.perm_group for pg in self.get_permgroup() if pg.perm_group[:7] == 'defgrp_'
               ]

    def _custompgroups(self):
        """unsorted list of permission groups that are created by users"""
        return [ pg.perm_group for pg in self.get_permgroup() if pg.perm_group[:7] != 'defgrp_'
               ]

    def _pgmap(self):
        """unsorted dictionary of permission maps
            { perm_group : [ [ perm_name, perm_name ...],
                             [ x_perm_name, x_perm_name ... ]
                           ],
              ...
            }
        """
        allpermnames = self.perm_names
        pgmap = {}
        msession = self.meta.Session()
        permgroups = self.get_permgroup(attrload=['perm_names'])
        for pg in permgroups:
            if pg.perm_group[:7] == 'defgrp_':
                continue
            permnames = [ p.perm_name for p in pg.perm_names ]
            x_permnames = list(set(allpermnames).difference(set(permnames)))
            pgmap.setdefault(pg.id, [
             pg.perm_group, permnames, x_permnames])

        return pgmap

    def _pgroupsbytype(self):
        """mapped permission groups and custom permission groups as a
        dictionary of,
            { 'mapped' : [ sorted list of permission group names ],
              'custom' : [ sorted list of permission group names ]
            }
        names"""
        d = {'mapped': [], 'custom': []}
        for pgroup in self._perm_groups():
            if pgroup[:7] == 'defgrp_':
                d['mapped'].append(pgroup)
            else:
                d['custom'].append(pgroup)

        d['mapped'].sort()
        d['custom'].sort()
        return d

    def _sitepgroups(self, permgroups=None):
        """Prune all the permission groups that contain project-level permission
        names and return those that have only site-level permission names"""
        permgroups = permgroups == None and self.get_permgroup(attrload=['perm_names']) or permgroups
        projpnames = self.proj_permnames
        for pg in permgroups[:]:
            for pn in pg.perm_names:
                if pn.perm_name in projpnames:
                    permgroups.remove(pg)
                    break

        return permgroups

    def _projpgroups(self, permgroups=None):
        """Prune all the permission groups that contain site-level permission
        names and return those that have only project-level permission
        names"""
        permgroups = permgroups == None and self.get_permgroup(attrload=['perm_names']) or permgroups
        sitepnames = self.site_permnames
        for pg in permgroups[:]:
            for pn in pg.perm_names:
                if pn.perm_name in sitepnames:
                    permgroups.remove(pg)
                    break

        return permgroups

    def documentof(self, user, search='xapian'):
        """Make a document for 'user' entry to create a searchable index
            [ metadata, attributes, document ], where

            metadata   : { key, value } pairs to be associated with document
            attributes : searchable { key, value } pairs to be associated with
                         document
            document   : [ list , of, ... ] document string, with increasing
                         weightage
        """
        user = self.get_user(user, attrload=['userinfo'])
        uinfo = user.userinfo
        metadata = {'doctype': 'user', 'id': user.id}
        attributes = search == 'xapian' and [
         'XID:user_%s' % user.id,
         'XCLASS:site', 'XCLASS:user',
         'XUSER:%s' % user.username,
         'XEMAIL:%s' % user.emailid,
         'XTZONE:%s' % user.timezone,
         'XCITY:%s' % uinfo.city,
         'XSTATE:%s' % uinfo.state,
         'XCOUNTRY:%s' % uinfo.country,
         'XPINCODE:%s' % uinfo.pincode] or []
        attrs = (' ').join([ getattr(user, a) for a in [
         'username', 'emailid', 'timezone']
                           ])
        cont1 = attrs + ' ' + (' ').join([ getattr(uinfo, a) or '' for a in [
         'firstname', 'middlename', 'lastname',
         'addressline1', 'addressline2', 'city',
         'state', 'country', 'pincode']
                                         ])
        cont2 = attrs + ' ' + (' ').join([ getattr(uinfo, a) or '' for a in [
         'city', 'state', 'country', 'pincode']
                                         ])
        document = [
         cont1, cont2]
        return [
         metadata, attributes, document]

    reltypes = property(_reltypes)
    usernames = property(_usernames)
    userstatus = property(_userstatus)
    perm_names = property(_perm_names)
    proj_permnames = property(_proj_permnames)
    site_permnames = property(_site_permnames)
    perm_groups = property(_perm_groups)
    mappedpgroups = property(_mappedpgroups)
    custompgroups = property(_custompgroups)
    mixedpnames = property(lambda self: self._perm_names() + self._custompgroups())
    pgmap = property(_pgmap)
    sitepgroups = property(_sitepgroups)
    projpgroups = property(_projpgroups)