# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/app/controller/backend/BackendAPIController.py
# Compiled at: 2016-07-15 00:10:26
from flask import redirect
from . import ADMIN_URL
from app import web
from app.CommonClass.ValidateClass import ValidateClass
from app.models import CobraRules, CobraVuls, CobraProjects
from app.models import CobraWhiteList, CobraTaskInfo, CobraLanguages
__author__ = 'lightless'
__email__ = 'root@lightless.me'

@web.route(ADMIN_URL + '/all_rules_count', methods=['GET'])
def all_rules_count():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    rules_count = CobraRules.query.count()
    return str(rules_count)


@web.route(ADMIN_URL + '/all_vuls_count', methods=['GET'])
def all_vuls_count():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    vuls_count = CobraVuls.query.count()
    return str(vuls_count)


@web.route(ADMIN_URL + '/all_projects_count', methods=['GET'])
def all_projects_count():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    projects_count = CobraProjects.query.count()
    return str(projects_count)


@web.route(ADMIN_URL + '/all_whitelists_count', methods=['GET'])
def all_whitelists_count():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    whitelists_count = CobraWhiteList.query.count()
    return str(whitelists_count)


@web.route(ADMIN_URL + '/all_tasks_count', methods=['GET'])
def all_tasks_count():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    tasks_count = CobraTaskInfo.query.count()
    return str(tasks_count)


@web.route(ADMIN_URL + '/all_languages_count', methods=['GET'])
def all_languages_count():
    if not ValidateClass.check_login():
        return redirect(ADMIN_URL + '/index')
    languages_count = CobraLanguages.query.count()
    return str(languages_count)