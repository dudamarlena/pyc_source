# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/iniconf.py
# Compiled at: 2015-12-29 03:04:14
# Size of source mod 2**32: 2246 bytes
from __future__ import unicode_literals
from djangofloor.iniconf import OptionParser, bool_setting
__author__ = 'Matthieu Gallet'
INI_MAPPING = [
 OptionParser('DATABASE_ENGINE', 'database.engine'),
 OptionParser('DATABASE_NAME', 'database.name'),
 OptionParser('DATABASE_USER', 'database.user'),
 OptionParser('DATABASE_PASSWORD', 'database.password'),
 OptionParser('DATABASE_HOST', 'database.host'),
 OptionParser('DATABASE_PORT', 'database.port'),
 OptionParser('PDNS_ENGINE', 'powerdns.engine'),
 OptionParser('PDNS_NAME', 'powerdns.name'),
 OptionParser('PDNS_USER', 'powerdns.user'),
 OptionParser('PDNS_PASSWORD', 'powerdns.password'),
 OptionParser('PDNS_HOST', 'powerdns.host'),
 OptionParser('PDNS_PORT', 'powerdns.port'),
 OptionParser('LDAP_BASE_DN', 'ldap.base_dn'),
 OptionParser('LDAP_NAME', 'ldap.name'),
 OptionParser('LDAP_USER', 'ldap.user'),
 OptionParser('LDAP_PASSWORD', 'ldap.password'),
 OptionParser('PENATES_DOMAIN', 'penates.domain'),
 OptionParser('PENATES_COUNTRY', 'penates.country'),
 OptionParser('PENATES_REALM', 'penates.realm'),
 OptionParser('PENATES_ORGANIZATION', 'penates.organization'),
 OptionParser('PENATES_STATE', 'penates.state'),
 OptionParser('PENATES_LOCALITY', 'penates.locality'),
 OptionParser('PENATES_EMAIL_ADDRESS', 'penates.email_address'),
 OptionParser('PENATES_SUBNETS', 'penates.subnets'),
 OptionParser('SERVER_NAME', 'global.server_name'),
 OptionParser('PENATES_KEYTAB', 'global.keytab'),
 OptionParser('PROTOCOL', 'global.protocol'),
 OptionParser('BIND_ADDRESS', 'global.bind_address'),
 OptionParser('LOCAL_PATH', 'global.data_path'),
 OptionParser('ADMIN_EMAIL', 'global.admin_email'),
 OptionParser('TIME_ZONE', 'global.time_zone'),
 OptionParser('LANGUAGE_CODE', 'global.language_code'),
 OptionParser('OFFER_HOST_KEYTABS', 'global.offer_host_keytabs'),
 OptionParser('FLOOR_AUTHENTICATION_HEADER', 'global.remote_user_header'),
 OptionParser('SECRET_KEY', 'global.secret_key'),
 OptionParser('FLOOR_DEFAULT_GROUP_NAME', 'global.default_group'),
 OptionParser('DEBUG', 'global.debug', bool_setting)]