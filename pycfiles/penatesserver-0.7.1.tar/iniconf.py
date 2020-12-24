# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/iniconf.py
# Compiled at: 2015-12-29 03:04:14
from __future__ import unicode_literals
from djangofloor.iniconf import OptionParser, bool_setting
__author__ = b'Matthieu Gallet'
INI_MAPPING = [
 OptionParser(b'DATABASE_ENGINE', b'database.engine'),
 OptionParser(b'DATABASE_NAME', b'database.name'),
 OptionParser(b'DATABASE_USER', b'database.user'),
 OptionParser(b'DATABASE_PASSWORD', b'database.password'),
 OptionParser(b'DATABASE_HOST', b'database.host'),
 OptionParser(b'DATABASE_PORT', b'database.port'),
 OptionParser(b'PDNS_ENGINE', b'powerdns.engine'),
 OptionParser(b'PDNS_NAME', b'powerdns.name'),
 OptionParser(b'PDNS_USER', b'powerdns.user'),
 OptionParser(b'PDNS_PASSWORD', b'powerdns.password'),
 OptionParser(b'PDNS_HOST', b'powerdns.host'),
 OptionParser(b'PDNS_PORT', b'powerdns.port'),
 OptionParser(b'LDAP_BASE_DN', b'ldap.base_dn'),
 OptionParser(b'LDAP_NAME', b'ldap.name'),
 OptionParser(b'LDAP_USER', b'ldap.user'),
 OptionParser(b'LDAP_PASSWORD', b'ldap.password'),
 OptionParser(b'PENATES_DOMAIN', b'penates.domain'),
 OptionParser(b'PENATES_COUNTRY', b'penates.country'),
 OptionParser(b'PENATES_REALM', b'penates.realm'),
 OptionParser(b'PENATES_ORGANIZATION', b'penates.organization'),
 OptionParser(b'PENATES_STATE', b'penates.state'),
 OptionParser(b'PENATES_LOCALITY', b'penates.locality'),
 OptionParser(b'PENATES_EMAIL_ADDRESS', b'penates.email_address'),
 OptionParser(b'PENATES_SUBNETS', b'penates.subnets'),
 OptionParser(b'SERVER_NAME', b'global.server_name'),
 OptionParser(b'PENATES_KEYTAB', b'global.keytab'),
 OptionParser(b'PROTOCOL', b'global.protocol'),
 OptionParser(b'BIND_ADDRESS', b'global.bind_address'),
 OptionParser(b'LOCAL_PATH', b'global.data_path'),
 OptionParser(b'ADMIN_EMAIL', b'global.admin_email'),
 OptionParser(b'TIME_ZONE', b'global.time_zone'),
 OptionParser(b'LANGUAGE_CODE', b'global.language_code'),
 OptionParser(b'OFFER_HOST_KEYTABS', b'global.offer_host_keytabs'),
 OptionParser(b'FLOOR_AUTHENTICATION_HEADER', b'global.remote_user_header'),
 OptionParser(b'SECRET_KEY', b'global.secret_key'),
 OptionParser(b'FLOOR_DEFAULT_GROUP_NAME', b'global.default_group'),
 OptionParser(b'DEBUG', b'global.debug', bool_setting)]