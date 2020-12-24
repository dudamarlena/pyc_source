# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/apps/permission_app.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2148 bytes
from flask import Flask, request
from fate_flow.settings import stat_logger
from fate_flow.utils.api_utils import get_json_result
from fate_flow.utils.authentication_utils import modify_permission, PrivilegeAuth
manager = Flask(__name__)

@manager.errorhandler(500)
def internal_server_error(e):
    stat_logger.exception(e)
    return get_json_result(retcode=100, retmsg=(str(e)))


@manager.route('/grant/privilege', methods=['post'])
def grant_permission():
    modify_permission(request.json)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/delete/privilege', methods=['post'])
def delete_permission():
    modify_permission((request.json), delete=True)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/query/privilege', methods=['post'])
def query_privilege():
    privilege_dict = PrivilegeAuth.get_permission_config(request.json.get('src_party_id'), request.json.get('src_role'))
    return get_json_result(retcode=0, retmsg='success', data={'src_party_id':request.json.get('src_party_id'),  'role':request.json.get('src_role'), 
     'privilege_role':privilege_dict.get('privilege_role', []), 
     'privilege_command':privilege_dict.get('privilege_command', []), 
     'privilege_component':privilege_dict.get('privilege_component', [])})