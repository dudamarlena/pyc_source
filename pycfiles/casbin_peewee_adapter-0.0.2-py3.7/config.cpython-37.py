# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/casbin_peewee_adapter/config.py
# Compiled at: 2019-07-01 02:45:47
# Size of source mod 2**32: 433 bytes
import peewee as pw, yaml, os
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.yml')
with open(config_path, 'r') as (f):
    settings = yaml.load(f)
DATABASES = settings['db']
DEFAULT_MYSQL_DATABAEE = pw.MySQLDatabase(host=(DATABASES['host']),
  user=(DATABASES['user']),
  passwd=(DATABASES['password']),
  database=(DATABASES['dbname']),
  charset='utf8',
  port=(DATABASES['port']))