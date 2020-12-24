# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Multisync/multisync/defaults.py
# Compiled at: 2016-02-26 03:04:57
from __future__ import unicode_literals
__author__ = b'Matthieu Gallet'
FLOOR_INSTALLED_APPS = [
 b'multisync']
FLOOR_URL_CONF = b'multisync.root_urls.urls'
FLOOR_PROJECT_NAME = b'MultiSync'
LDAP_BASE_DN = b'dc=test,dc=example,dc=org'
LDAP_BASE_DN_HELP = b'base dn for searching users and groups, like dc=test,dc=example,dc=org.'
LDAP_GROUP_OU = b'ou=Groups'
LDAP_GROUP_OU_HELP = b'subtree containing groups, like ou=Groups'
LDAP_USER_OU = b'ou=Users'
LDAP_USER_OU_HELP = b'subtree containing users, like ou=Users'
LDAP_NAME = b'ldap://192.168.56.101/'
LDAP_NAME_HELP = b'LDAP url, like ldap://127.0.0.1/ or ldapi:///'
LDAP_USER = b'cn=admin,dc=test,dc=example,dc=org'
LDAP_USER_HELP = b'LDAP user name to bind with'
LDAP_PASSWORD = b'toto'
LDAP_PASSWORD_HELP = b'LDAP password to bind with'
SYNCHRONIZER = b'multisync.django_synchronizers.DjangoSynchronizer'
DATABASES = {b'default': {b'ENGINE': b'{DATABASE_ENGINE}', 
                b'NAME': b'{DATABASE_NAME}', 
                b'USER': b'{DATABASE_USER}', 
                b'PASSWORD': b'{DATABASE_PASSWORD}', 
                b'HOST': b'{DATABASE_HOST}', 
                b'PORT': b'{DATABASE_PORT}'}, 
   b'ldap': {b'ENGINE': b'ldapdb.backends.ldap', 
             b'NAME': b'{LDAP_NAME}', 
             b'USER': b'{LDAP_USER}', 
             b'PASSWORD': b'{LDAP_PASSWORD}'}}
DATABASE_ROUTERS = [
 b'ldapdb.router.Router']
PROSODY_GROUP_FILE = b'{LOCAL_PATH}/groups.ini'
PROSODY_GROUP_FILE_HELP = b'path of the generated Prosody config file. See `https://prosody.im/doc/modules/mod_groups#example` for more info.'
PROSODY_DOMAIN = b'im.example.org'
PROSODY_DOMAIN_HELP = b"Domain to append to the Prosody's usernames"