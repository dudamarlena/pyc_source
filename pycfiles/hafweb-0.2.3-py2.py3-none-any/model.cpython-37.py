# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\workspace\mine\python\haf-webmanager\hafweb\model\model.py
# Compiled at: 2019-04-16 07:48:32
# Size of source mod 2**32: 1862 bytes
from haf.common.database import MysqlTool
from sqlalchemy import *
from hafweb.config import *
import json

class Main(Base):
    __tablename__ = 'main'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    begin_time = Column(String)
    end_time = Column(String)
    duration_time = Column(Integer)
    passed = Column(Integer)
    failed = Column(Integer)
    skip = Column(Integer)
    error = Column(Integer)
    suite_name = Column(String)

    def __repr__(self):
        attr_list = [
         'id', 'name', 'begin_time', 'duration_time', 'passed', 'failed', 'skip', 'error', 'suite_name']
        rev = {}
        for attr in attr_list:
            rev[attr] = getattr(self, attr)

        return json.dumps(rev)


class Suite(Base):
    __tablename__ = 'suite'
    id = Column(Integer, primary_key=True)
    main_id = Column(Integer)
    suite_name = Column(String)

    def __repr__(self):
        attr_list = [
         'id', 'main_id', 'suite_name']
        rev = {}
        for attr in attr_list:
            rev[attr] = getattr(self, attr)

        return json.dumps(rev)


class Summary(Base):
    __tablename__ = 'summary'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    passed = Column(Integer)
    failed = Column(Integer)
    skip = Column(Integer)
    all = Column(Integer)
    error = Column(Integer)
    base_url = Column(String)
    begin_time = Column(String)
    end_time = Column(String)
    duration_time = Column(String)
    suite_id = Column(Integer)

    def __repr__(self):
        attr_list = [
         'id', 'name', 'passed', 'failed', 'skip', 'all', 'error', 'base_url', 'begin_time', 'end_time', 'duration_time', 'suite_id']
        rev = {}
        for attr in attr_list:
            rev[attr] = getattr(self, attr)

        return json.dumps(rev)