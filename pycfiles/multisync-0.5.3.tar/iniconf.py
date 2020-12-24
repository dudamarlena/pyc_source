# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Multisync/multisync/iniconf.py
# Compiled at: 2016-02-26 03:04:57
from __future__ import unicode_literals
from djangofloor.iniconf import OptionParser
__author__ = b'Matthieu Gallet'
INI_MAPPING = [
 OptionParser(b'DATABASE_ENGINE', b'database.engine'),
 OptionParser(b'DATABASE_NAME', b'database.name'),
 OptionParser(b'DATABASE_USER', b'database.user'),
 OptionParser(b'DATABASE_PASSWORD', b'database.password'),
 OptionParser(b'DATABASE_HOST', b'database.host'),
 OptionParser(b'DATABASE_PORT', b'database.port'),
 OptionParser(b'LDAP_BASE_DN', b'ldap.base_dn'),
 OptionParser(b'LDAP_NAME', b'ldap.name'),
 OptionParser(b'LDAP_USER', b'ldap.user'),
 OptionParser(b'LDAP_PASSWORD', b'ldap.password'),
 OptionParser(b'LDAP_GROUP_OU', b'ldap.group_ou'),
 OptionParser(b'LDAP_USER_OU', b'ldap.user_ou'),
 OptionParser(b'SYNCHRONIZER', b'multisync.synchronizer'),
 OptionParser(b'PROSODY_GROUP_FILE', b'prosody.group_file'),
 OptionParser(b'PROSODY_DOMAIN', b'prosody.domain'),
 OptionParser(b'ADMIN_EMAIL', b'global.admin_email'),
 OptionParser(b'TIME_ZONE', b'global.time_zone'),
 OptionParser(b'LANGUAGE_CODE', b'global.language_code'),
 OptionParser(b'FLOOR_DEFAULT_GROUP_NAME', b'global.default_group')]