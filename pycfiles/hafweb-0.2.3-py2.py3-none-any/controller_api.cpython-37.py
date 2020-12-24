# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\workspace\mine\python\haf-webmanager\hafweb\controller\controller_api.py
# Compiled at: 2019-05-11 02:02:42
# Size of source mod 2**32: 4110 bytes
from hafweb.controller.engine import *
from sqlalchemy import *
from datetime import datetime
from hafweb.model.model_api import *
import json

class ControllerApi(object):

    def __init__(self):
        pass

    @classmethod
    def bind_all(cls):
        apicase = ApiCase()
        apicase.metadata.bind = engine_maker.engine
        case_expect = ApiCaseExpect()
        case_expect.metadata.bind = engine_maker.engine
        case_ids = ApiCaseIds()
        case_ids.metadata.bind = engine_maker.engine
        case_request = ApiCaseRequest()
        case_request.metadata.bind = engine_maker.engine
        case_response = ApiCaseResponse()
        case_response.metadata.bind = engine_maker.engine
        case_sqlinfo = ApiCaseSqlinfo()
        case_sqlinfo.metadata.bind = engine_maker.engine
        case_sqlinfo_checklsit = ApiCaseSqlinfoChecklist()
        case_sqlinfo_checklsit.metadata.bind = engine_maker.engine
        case_sqlinfo_config = ApiCaseSqlinfoConfig()
        case_sqlinfo_config.metadata.bind = engine_maker.engine
        case_sqlinfo_script = ApiCaseSqlinfoScript()
        case_sqlinfo_script.metadata.bind = engine_maker.engine
        case_detail = ApiDetail()
        case_detail.metadata.bind = engine_maker.engine

    @classmethod
    def get_case_all(cls):
        with session_close() as (session):
            temp = session.query(ApiCase).all()
            return temp

    @classmethod
    def get_case_by_suite_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCase).filter(ApiCase.suite_id == id).all()
            return temp

    @classmethod
    def get_case_expect_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCaseExpect).filter(ApiCaseExpect.id == id).all()
            return temp

    @classmethod
    def get_case_ids_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCaseIds).filter(ApiCaseIds.id == id).all()
            return temp

    @classmethod
    def get_case_request_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCaseRequest).filter(ApiCaseRequest.id == id).all()
            return temp

    @classmethod
    def get_case_response_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCaseResponse).filter(ApiCaseResponse.id == id).all()
            return temp

    @classmethod
    def get_case_sqlinfo_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCaseSqlinfo).filter(ApiCaseSqlinfo.id == id).all()
            return temp

    @classmethod
    def get_case_sqlinfo_checklist_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCaseSqlinfoChecklist).filter(ApiCaseSqlinfoChecklist.id == id).all()
            return temp

    @classmethod
    def get_case_sqlinfo_config_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCaseSqlinfoConfig).filter(ApiCaseSqlinfoConfig.id == id).all()
            return temp

    @classmethod
    def get_case_sqlinfo_script_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiCaseSqlinfoScript).filter(ApiCaseSqlinfoScript.id == id).all()
            return temp

    @classmethod
    def get_case_detail_by_id(cls, id):
        with session_close() as (session):
            temp = session.query(ApiDetail).filter(ApiDetail.id == id).all()
            return temp

    @classmethod
    def get_case_history_by_id(cls, id, sub_id, case_name, suite_name):
        with session_close() as (session):
            all_cases_ids_id = session.query(ApiCaseIds.id).filter(and_(ApiCaseIds.case_id == id, ApiCaseIds.case_sub_id == sub_id, ApiCaseIds.case_name == case_name)).all()
            temp = session.query(ApiCase).filter(and_(ApiCase.ids_id.in_([x[0] for x in all_cases_ids_id]), ApiCase.bench_name == suite_name)).all()
            return temp