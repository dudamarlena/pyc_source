# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Multisync/multisync/models.py
# Compiled at: 2016-02-26 03:04:57
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.db import models
from ldapdb.models.fields import CharField, IntegerField, ListField, ImageField as ImageField_
import ldapdb.models
__author__ = b'flanker'
name_pattern = b'[a-zA-Z][\\w_\\-]{0,199}'
name_validators = [RegexValidator(b'^%s$' % name_pattern)]

def force_bytestrings(unicode_list):
    """
     >>> force_bytestrings(['test']) == [b'test']
     True
    """
    return [ x.encode(b'utf-8') for x in unicode_list ]


def force_bytestring(x):
    return x.encode(b'utf-8')


class ImageField(ImageField_):

    def get_internal_type(self):
        return b'CharField'


class BaseLdapModel(ldapdb.models.Model):

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return b'%s("%s")' % (self.__class__.__name__, self.name)

    class Meta(object):
        abstract = True


class LdapGroup(BaseLdapModel):
    base_dn = b'%s,%s' % (settings.LDAP_GROUP_OU, settings.LDAP_BASE_DN)
    object_classes = force_bytestrings([b'posixGroup', b'sambaGroupMapping'])
    name = CharField(db_column=force_bytestring(b'cn'), max_length=200, primary_key=True, validators=list(name_validators))
    gid = IntegerField(db_column=force_bytestring(b'gidNumber'), unique=True)
    members = ListField(db_column=force_bytestring(b'memberUid'))
    description = CharField(db_column=force_bytestring(b'description'), max_length=500, blank=True, default=b'')
    group_type = IntegerField(db_column=force_bytestring(b'sambaGroupType'), default=None)
    samba_sid = CharField(db_column=force_bytestring(b'sambaSID'), unique=True, default=b'')


class LdapUser(BaseLdapModel):
    base_dn = b'%s,%s' % (settings.LDAP_USER_OU, settings.LDAP_BASE_DN)
    object_classes = force_bytestrings([b'posixAccount', b'shadowAccount', b'inetOrgPerson', b'sambaSamAccount', b'person',
     b'AsteriskSIPUser'])
    name = CharField(db_column=force_bytestring(b'uid'), max_length=200, primary_key=True, validators=list(name_validators))
    display_name = CharField(db_column=force_bytestring(b'displayName'), max_length=200)
    uid_number = IntegerField(db_column=force_bytestring(b'uidNumber'), default=None, unique=True)
    gid_number = IntegerField(db_column=force_bytestring(b'gidNumber'), default=None)
    login_shell = CharField(db_column=force_bytestring(b'loginShell'), default=b'/bin/bash')
    description = CharField(db_column=force_bytestring(b'description'), default=b'Description')
    jpeg_photo = ImageField(db_column=force_bytestring(b'jpegPhoto'), max_length=10000000)
    phone = CharField(db_column=force_bytestring(b'telephoneNumber'), default=None)
    samba_acct_flags = CharField(db_column=force_bytestring(b'sambaAcctFlags'), default=b'[UX         ]')
    user_smime_certificate = CharField(db_column=force_bytestring(b'userSMIMECertificate'), default=None)
    user_certificate = CharField(db_column=force_bytestring(b'userCertificate'), default=None)
    samba_sid = CharField(db_column=force_bytestring(b'sambaSID'), default=None)
    primary_group_samba_sid = CharField(db_column=force_bytestring(b'sambaPrimaryGroupSID'), default=None)
    home_directory = CharField(db_column=force_bytestring(b'homeDirectory'), default=None)
    mail = CharField(db_column=force_bytestring(b'mail'), default=None)
    samba_domain_name = CharField(db_column=force_bytestring(b'sambaDomainName'), default=None)
    gecos = CharField(db_column=force_bytestring(b'gecos'), max_length=200, default=None)
    cn = CharField(db_column=force_bytestring(b'cn'), max_length=200, default=None, validators=list(name_validators))
    sn = CharField(db_column=force_bytestring(b'sn'), max_length=200, default=None, validators=list(name_validators))
    user_password = CharField(db_column=force_bytestring(b'userPassword'), default=None)
    ast_account_caller_id = CharField(db_column=force_bytestring(b'AstAccountCallerID'), default=None)
    ast_account_context = CharField(db_column=force_bytestring(b'AstAccountContext'), default=b'LocalSets')
    ast_account_DTMF_mode = CharField(db_column=force_bytestring(b'AstAccountDTMFMode'), default=b'rfc2833')
    ast_account_mailbox = CharField(db_column=force_bytestring(b'AstAccountMailbox'), default=None)
    ast_account_NAT = CharField(db_column=force_bytestring(b'AstAccountNAT'), default=b'yes')
    ast_account_qualify = CharField(db_column=force_bytestring(b'AstAccountQualify'), default=b'yes')
    ast_account_type = CharField(db_column=force_bytestring(b'AstAccountType'), default=b'friend')
    ast_account_disallowed_codec = CharField(db_column=force_bytestring(b'AstAccountDisallowedCodec'), default=b'all')
    ast_account_allowed_codec = CharField(db_column=force_bytestring(b'AstAccountAllowedCodec'), default=b'ulaw')
    ast_account_music_on_hold = CharField(db_column=force_bytestring(b'AstAccountMusicOnHold'), default=b'default')


class PenatesserverDjangouser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField(default=False)
    username = models.CharField(unique=True, max_length=250)
    first_name = models.CharField(max_length=30, default=b'')
    last_name = models.CharField(max_length=30, default=b'')
    email = models.CharField(max_length=254, default=b'')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    class Meta(object):
        managed = False
        db_table = b'penatesserver_djangouser'


class PenatesserverDjangouserGroups(models.Model):
    djangouser = models.ForeignKey(PenatesserverDjangouser)
    group_id = models.IntegerField()

    class Meta(object):
        managed = False
        db_table = b'penatesserver_djangouser_groups'
        unique_together = (('djangouser', 'group_id'), )