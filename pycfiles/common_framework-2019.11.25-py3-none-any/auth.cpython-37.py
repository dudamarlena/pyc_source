# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/marc/Git/common-framework/common/auth.py
# Compiled at: 2019-01-16 19:53:03
# Size of source mod 2**32: 4097 bytes
import logging
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import Group
import django.utils.translation as _
import common.settings as settings
logger = logging.getLogger(__name__)

class LdapAuthenticationBackend(ModelBackend):
    __doc__ = '\n    Authentification via LDAP\n    '

    def authenticate(self, request=None, username=None, password=None, **kwargs):
        return settings.LDAP_ENABLE is False or password or None
        try:
            import ldap3 as ldap
            ldap_server = ldap.Server(settings.LDAP_HOST)
            login = settings.LDAP_LOGIN.format(username=username)
            ldap_connection = ldap.Connection(ldap_server, user=login, password=password, auto_bind=True)
            with ldap_connection:
                ldap_connection.bind()
                filter = settings.LDAP_FILTER.format(username=username)
                if ldap_connection.search((settings.LDAP_BASE),
                  filter,
                  attributes=(settings.LDAP_ATTRIBUTES)):
                    attributes = ldap_connection.response[0].get('attributes', {})
                    User = get_user_model()
                    username = username and username.lower()
                    user, created = User.objects.get_or_create(username=username)
                    user.set_password(password)

                    def set_value(obj, name, value):
                        item = getattr(type(obj), name, None)
                        if item:
                            if not isinstance(item, property):
                                setattr(obj, name, value)

                    set_value(user, 'first_name', attributes['givenName'])
                    set_value(user, 'last_name', attributes['sn'])
                    set_value(user, 'email', attributes['mail'])
                    set_value(user, 'is_active', True)
                    set_value(user, 'is_superuser', False)
                    set_value(user, 'is_staff', False)
                    group_names = [group.split(',')[0].split('=')[1] for group in attributes['memberOf']]
                    if username in settings.LDAP_ADMIN_USERS or set(group_names) & set(settings.LDAP_ADMIN_GROUPS):
                        set_value(user, 'is_superuser', True)
                        set_value(user, 'is_staff', True)
                    if username in settings.LDAP_STAFF_USERS or set(group_names) & set(settings.LDAP_STAFF_GROUPS):
                        set_value(user, 'is_staff', True)
                    user.save()
                    if hasattr(User, 'groups'):
                        non_ldap_groups = list(user.groups.exclude(name__startswith=(settings.LDAP_GROUP_PREFIX)))
                        user.groups.clear()
                        for group_name in group_names:
                            group, created = Group.objects.get_or_create(name=('{}{}'.format(settings.LDAP_GROUP_PREFIX, group_name)))
                            user.groups.add(group)

                        (user.groups.add)(*non_ldap_groups)
                    return user
                logger.info(_('Utilisateur {username} non trouvé dans le répertoire LDAP.').format(username=username))
                return
        except Exception as erreur:
            try:
                logger.warning(_("Erreur lors de l'authentification LDAP : {erreur}").format(erreur=erreur))
                return
            finally:
                erreur = None
                del erreur