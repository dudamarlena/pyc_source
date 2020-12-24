# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/defaults.py
# Compiled at: 2016-02-24 03:58:19
# Size of source mod 2**32: 4784 bytes
from __future__ import unicode_literals
from djangofloor.utils import FilePath, DirectoryPath
__author__ = 'flanker'
SESSION_REDIS_PREFIX = 'session'
SESSION_REDIS_HOST = '{REDIS_HOST}'
SESSION_REDIS_PORT = '{REDIS_PORT}'
SESSION_REDIS_DB = 10
FLOOR_INSTALLED_APPS = [
 'penatesserver', 'rest_framework', 'penatesserver.powerdns']
FLOOR_INDEX = 'penatesserver.views.index'
FLOOR_URL_CONF = 'penatesserver.root_urls.urls'
FLOOR_PROJECT_NAME = 'Penates Server'
TEST_RUNNER = 'penatesserver.tests.ManagedModelTestRunner'
SECRET_KEY = 'cLc7rCD75uO6uFVr6ojn6AYTm2DGT2t7hb7OH5Capk29kcdy7H'
REST_FRAMEWORK = {'DEFAULT_MODEL_SERIALIZER_CLASS': 'rest_framework.serializers.HyperlinkedModelSerializer', 
 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer', 'penatesserver.renderers.ListAdminRenderer',
 'rest_framework.renderers.BrowsableAPIRenderer'), 
 'DEFAULT_PERMISSION_CLASSES': [
                                'rest_framework.permissions.AllowAny']}
OPENSSL_PATH = 'openssl'
PKI_PATH = DirectoryPath('{LOCAL_PATH}/pki')
SSH_KEYGEN_PATH = 'ssh-keygen'
LDAP_BASE_DN = 'dc=test,dc=example,dc=org'
PENATES_COUNTRY = 'FR'
PENATES_ORGANIZATION = 'example.org'
PENATES_DOMAIN = 'test.example.org'
PENATES_STATE = 'Ile-de-France'
PENATES_LOCALITY = 'Paris'
PENATES_EMAIL_ADDRESS = 'admin@{PENATES_DOMAIN}'
PENATES_REALM = 'EXAMPLE.ORG'
PENATES_KEYTAB = FilePath('{PKI_PATH}/private/kadmin.keytab')
PENATES_LOCKFILE = FilePath('{PKI_PATH}/pki/lockfile')
PENATES_PRINCIPAL = 'penatesserver/admin@{PENATES_REALM}'
RUNNING_TESTS = False
PENATES_SUBNETS = '10.19.1.0/24,10.19.1.1\n10.8.0.0/16,10.8.0.1'
LDAP_NAME = 'ldap://192.168.56.101/'
LDAP_USER = 'cn=admin,dc=test,dc=example,dc=org'
LDAP_PASSWORD = 'toto'
PDNS_USER = 'powerdns'
PDNS_PASSWORD = 'toto'
PDNS_HOST = 'localhost'
PDNS_PORT = '5432'
PDNS_ENGINE = 'django.db.backends.sqlite3'
PDNS_NAME = FilePath('{DATA_PATH}/pdns.sqlite3')
PDNS_ADMIN_PREFIX = 'admin.'
PDNS_INFRA_PREFIX = 'infra.'
KERBEROS_IMPL = 'heimdal'
DATABASES = {'default': {'ENGINE': '{DATABASE_ENGINE}', 
             'NAME': '{DATABASE_NAME}', 
             'USER': '{DATABASE_USER}', 
             'PASSWORD': '{DATABASE_PASSWORD}', 
             'HOST': '{DATABASE_HOST}', 
             'PORT': '{DATABASE_PORT}'}, 
 'ldap': {'ENGINE': 'ldapdb.backends.ldap', 
          'NAME': '{LDAP_NAME}', 
          'USER': '{LDAP_USER}', 
          'PASSWORD': '{LDAP_PASSWORD}'}, 
 'powerdns': {'ENGINE': '{PDNS_ENGINE}', 
              'NAME': '{PDNS_NAME}', 
              'USER': '{PDNS_USER}', 
              'PASSWORD': '{PDNS_PASSWORD}', 
              'HOST': '{PDNS_HOST}', 
              'PORT': '{PDNS_PORT}'}}
STORE_CLEARTEXT_PASSWORDS = False
OFFER_HOST_KEYTABS = True
DATABASE_ROUTERS = ['ldapdb.router.Router', 'penatesserver.routers.PowerdnsManagerDbRouter']
AUTH_USER_MODEL = 'penatesserver.DjangoUser'
DEBUG = False
AUTHENTICATION_BACKENDS = [
 'penatesserver.backends.DefaultGroupRemoteUserBackend',
 'django.contrib.auth.backends.ModelBackend',
 'allauth.account.auth_backends.AuthenticationBackend']