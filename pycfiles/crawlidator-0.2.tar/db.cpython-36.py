# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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