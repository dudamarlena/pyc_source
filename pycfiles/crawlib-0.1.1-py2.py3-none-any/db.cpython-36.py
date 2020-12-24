# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/tests/dummy_site_crawler/sql_backend/db.py
# Compiled at: 2019-12-27 19:59:56
# Size of source mod 2**32: 449 bytes
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy_mate import EngineCreator
from .config_init import config
engine = EngineCreator(host=(config.DB_HOST.get_value()),
  port=(config.DB_PORT.get_value()),
  database=(config.DB_DATABASE.get_value()),
  username=(config.DB_USERNAME.get_value()),
  password=(config.DB_PASSWORD.get_value())).create_postgresql_psycopg2()
Session = sessionmaker(bind=engine)