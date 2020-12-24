# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/defaults.py
# Compiled at: 2016-02-24 03:58:19
from __future__ import unicode_literals
from djangofloor.utils import FilePath, DirectoryPath
__author__ = b'flanker'
SESSION_REDIS_PREFIX = b'session'
SESSION_REDIS_HOST = b'{REDIS_HOST}'
SESSION_REDIS_PORT = b'{REDIS_PORT}'
SESSION_REDIS_DB = 10
FLOOR_INSTALLED_APPS = [
 b'penatesserver', b'rest_framework', b'penatesserver.powerdns']
FLOOR_INDEX = b'penatesserver.views.index'
FLOOR_URL_CONF = b'penatesserver.root_urls.urls'
FLOOR_PROJECT_NAME = b'Penates Server'
TEST_RUNNER = b'penatesserver.tests.ManagedModelTestRunner'
SECRET_KEY = b'cLc7rCD75uO6uFVr6ojn6AYTm2DGT2t7hb7OH5Capk29kcdy7H'
REST_FRAMEWORK = {b'DEFAULT_MODEL_SERIALIZER_CLASS': b'rest_framework.serializers.HyperlinkedModelSerializer', 
   b'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', 'penatesserver.renderers.ListAdminRenderer',
 'rest_framework.renderers.BrowsableAPIRenderer'), 
   b'DEFAULT_PERMISSION_CLASSES': [
                                 b'rest_framework.permissions.AllowAny']}
OPENSSL_PATH = b'openssl'
PKI_PATH = DirectoryPath(b'{LOCAL_PATH}/pki')
SSH_KEYGEN_PATH = b'ssh-keygen'
LDAP_BASE_DN = b'dc=test,dc=example,dc=org'
PENATES_COUNTRY = b'FR'
PENATES_ORGANIZATION = b'example.org'
PENATES_DOMAIN = b'test.example.org'
PENATES_STATE = b'Ile-de-France'
PENATES_LOCALITY = b'Paris'
PENATES_EMAIL_ADDRESS = b'admin@{PENATES_DOMAIN}'
PENATES_REALM = b'EXAMPLE.ORG'
PENATES_KEYTAB = FilePath(b'{PKI_PATH}/private/kadmin.keytab')
PENATES_LOCKFILE = FilePath(b'{PKI_PATH}/pki/lockfile')
PENATES_PRINCIPAL = b'penatesserver/admin@{PENATES_REALM}'
RUNNING_TESTS = False
PENATES_SUBNETS = b'10.19.1.0/24,10.19.1.1\n10.8.0.0/16,10.8.0.1'
LDAP_NAME = b'ldap://192.168.56.101/'
LDAP_USER = b'cn=admin,dc=test,dc=example,dc=org'
LDAP_PASSWORD = b'toto'
PDNS_USER = b'powerdns'
PDNS_PASSWORD = b'toto'
PDNS_HOST = b'localhost'
PDNS_PORT = b'5432'
PDNS_ENGINE = b'django.db.backends.sqlite3'
PDNS_NAME = FilePath(b'{DATA_PATH}/pdns.sqlite3')
PDNS_ADMIN_PREFIX = b'admin.'
PDNS_INFRA_PREFIX = b'infra.'
KERBEROS_IMPL = b'heimdal'
DATABASES = {b'default': {b'ENGINE': b'{DATABASE_ENGINE}', 
                b'NAME': b'{DATABASE_NAME}', 
                b'USER': b'{DATABASE_USER}', 
                b'PASSWORD': b'{DATABASE_PASSWORD}', 
                b'HOST': b'{DATABASE_HOST}', 
                b'PORT': b'{DATABASE_PORT}'}, 
   b'ldap': {b'ENGINE': b'ldapdb.backends.ldap', 
             b'NAME': b'{LDAP_NAME}', 
             b'USER': b'{LDAP_USER}', 
             b'PASSWORD': b'{LDAP_PASSWORD}'}, 
   b'powerdns': {b'ENGINE': b'{PDNS_ENGINE}', 
                 b'NAME': b'{PDNS_NAME}', 
                 b'USER': b'{PDNS_USER}', 
                 b'PASSWORD': b'{PDNS_PASSWORD}', 
                 b'HOST': b'{PDNS_HOST}', 
                 b'PORT': b'{PDNS_PORT}'}}
STORE_CLEARTEXT_PASSWORDS = False
OFFER_HOST_KEYTABS = True
DATABASE_ROUTERS = [b'ldapdb.router.Router', b'penatesserver.routers.PowerdnsManagerDbRouter']
AUTH_USER_MODEL = b'penatesserver.DjangoUser'
DEBUG = False
AUTHENTICATION_BACKENDS = [
 b'penatesserver.backends.DefaultGroupRemoteUserBackend',
 b'django.contrib.auth.backends.ModelBackend',
 b'allauth.account.auth_backends.AuthenticationBackend']