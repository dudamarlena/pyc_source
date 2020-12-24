# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\workspace\mine\python\haf-webmanager\hafweb\controller\controller_main.py
# Compiled at: 2019-05-14 22:33:33
# Size of source mod 2**32: 2106 bytes
from hafweb.controller.engine import *
from sqlalchemy import *
from datetime import datetime
from hafweb.model.model import *
import json

class Controller(object):

    def __init__(self):
        pass

    @classmethod
    def bind_all(cls):
        main = Main()
        main.metadata.bind = engine_maker.engine
        suite = Suite()
        suite.metadata.bind = engine_maker.engine
        summary = Summary()
        summary.metadata.bind = engine_maker.engine

    @classmethod
    def get_main_all(cls):
        with session_close() as (session):
            temp = session.query(Main).all()
            return temp

    @classmethod
    def get_main_by_test_name(cls, test_name):
        rev = []
        temp = Controller.get_main_all()
        for main in temp:
            *name, y, m, d, t = main.name.split('-')
            name = '-'.join(name)
            date_time = f"{y}-{m}-{d}-{t}"
            if name == test_name:
                rev.append(main)

        return rev

    @classmethod
    def get_main_by_test_id(cls, test_id):
        with session_close() as (session):
            temp = session.query(Main).filter(Main.id == test_id).all()
            return temp

    @classmethod
    def get_main_today(cls):
        with session_close() as (session):
            today = datetime.today().date()
            temp = session.query(Main).filter(Main.begin_time.like(f"{today}%")).all()
            return temp

    @classmethod
    def get_main_by_date(cls, date_time):
        with session_close() as (session):
            temp = session.query(Main).filter(Main.begin_time.like(f"{date_time}%")).all()
            return temp

    @classmethod
    def get_suite_by_main_id(cls, id):
        with session_close() as (session):
            temp = session.query(Suite).filter(Suite.main_id == id).all()
            return temp

    @classmethod
    def get_summary_by_suite_id(cls, id):
        with session_close() as (session):
            temp = session.query(Summary).filter(Summary.suite_id == id).all()
            return temp