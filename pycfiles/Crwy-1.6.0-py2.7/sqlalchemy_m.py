# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/sql/sqlalchemy_m.py
# Compiled at: 2020-02-03 23:11:43
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from crwy.decorates import cls2singleton
Base = declarative_base()

@cls2singleton
class SqlalchemyHandle(object):
    """
    以ORM的方式连接数据库
    """

    def __init__(self, db_url, **kwargs):
        self.engine = create_engine(db_url, **kwargs)
        DBSession = sessionmaker(bind=self.engine)
        self.session = DBSession()

    def init_table(self):
        return Base.metadata.create_all(self.engine)

    def delete_table(self):
        return Base.metadata.drop_all(self.engine)