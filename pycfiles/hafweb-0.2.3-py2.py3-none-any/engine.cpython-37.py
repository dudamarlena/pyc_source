# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\workspace\mine\python\haf-webmanager\hafweb\controller\engine.py
# Compiled at: 2019-04-09 07:43:12
# Size of source mod 2**32: 698 bytes
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *
from hafweb.config import *
import functools
from contextlib import contextmanager
from haf.common.sigleton import *

class EngineMaker(metaclass=SingletonType):
    engine = None
    maker = None

    def __init__(self):
        super().__init__()

    def bind_sql_server(self, args):
        self.engine = create_engine(f"mysql+pymysql://{args.sql_server}")
        self.maker = sessionmaker(bind=(self.engine))


engine_maker = EngineMaker()

@contextmanager
def session_close():
    try:
        session = engine_maker.maker()
        yield session
    finally:
        session.close()