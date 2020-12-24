# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/apps/pipeline_app.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 1281 bytes
from fate_flow.utils.api_utils import get_json_result
from fate_flow.settings import stat_logger
from flask import Flask, request
from fate_flow.manager import pipeline_manager
manager = Flask(__name__)

@manager.errorhandler(500)
def internal_server_error(e):
    stat_logger.exception(e)
    return get_json_result(retcode=100, retmsg=(str(e)))


@manager.route('/dag/dependency', methods=['post'])
def pipeline_dag_dependency():
    dependency = pipeline_manager.pipeline_dag_dependency(request.json)
    if dependency:
        return get_json_result(retcode=0, retmsg='success', data=dependency)
    return get_json_result(retcode=101, retmsg='')