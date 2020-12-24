# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/apps/table_app.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 2809 bytes
from fate_flow.manager.data_manager import query_data_view, delete_table
from fate_flow.utils.api_utils import get_json_result
from fate_flow.utils import session_utils
from fate_flow.settings import stat_logger
from arch.api.utils.dtable_utils import get_table_info
from arch.api import session
from flask import Flask, request
manager = Flask(__name__)

@manager.errorhandler(500)
def internal_server_error(e):
    stat_logger.exception(e)
    return get_json_result(retcode=100, retmsg=(str(e)))


@manager.route('/delete', methods=['post'])
@session_utils.session_detect()
def table_delete():
    request_data = request.json
    data_views = query_data_view(**request_data)
    table_name = request_data.get('table_name')
    namespace = request_data.get('namespace')
    status = False
    data = []
    if table_name and namespace:
        table = session.get_data_table(name=table_name, namespace=namespace)
        table.destroy()
        data.append({'table_name':table_name,  'namespace':namespace})
        status = True
    else:
        if data_views:
            status, data = delete_table(data_views)
        else:
            return get_json_result(retcode=101, retmsg='no find table')
    return get_json_result(retcode=(0 if status else 101), retmsg=('success' if status else 'failed'), data=data)


@manager.route('/<table_func>', methods=['post'])
@session_utils.session_detect()
def dtable(table_func):
    config = request.json
    if table_func == 'table_info':
        table_name, namespace = get_table_info(config=config, create=(config.get('create', False)))
        if config.get('create', False):
            table_key_count = 0
            table_partition = None
        else:
            table = session.get_data_table(name=table_name, namespace=namespace)
            if table:
                table_key_count = table.count()
                table_partition = table.get_partitions()
            else:
                table_key_count = 0
                table_partition = None
        return get_json_result(data={'table_name':table_name,  'namespace':namespace,  'count':table_key_count,  'partition':table_partition})
    return get_json_result()