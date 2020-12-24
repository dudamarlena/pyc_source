# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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