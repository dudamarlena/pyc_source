# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/apps/schedule_app.py
# Compiled at: 2020-05-06 02:27:06
# Size of source mod 2**32: 4248 bytes
from flask import Flask, request
from arch.api.utils.core_utils import base64_decode
from fate_flow.driver.job_controller import JobController
from fate_flow.driver.task_scheduler import TaskScheduler
from fate_flow.settings import stat_logger
from fate_flow.utils.api_utils import get_json_result
from fate_flow.utils.authentication_utils import request_authority_certification
manager = Flask(__name__)

@manager.errorhandler(500)
def internal_server_error(e):
    stat_logger.exception(e)
    return get_json_result(retcode=100, retmsg=(str(e)))


@manager.route('/<job_id>/<role>/<party_id>/create', methods=['POST'])
@request_authority_certification
def create_job(job_id, role, party_id):
    JobController.update_job_status(job_id=job_id, role=role, party_id=(int(party_id)), job_info=(request.json), create=True)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/status', methods=['POST'])
def job_status(job_id, role, party_id):
    JobController.update_job_status(job_id=job_id, role=role, party_id=(int(party_id)), job_info=(request.json), create=False)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/<model_id>/<model_version>/save/pipeline', methods=['POST'])
@request_authority_certification
def save_pipeline(job_id, role, party_id, model_id, model_version):
    JobController.save_pipeline(job_id=job_id, role=role, party_id=party_id, model_id=(base64_decode(model_id)), model_version=(base64_decode(model_version)))
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/kill', methods=['POST'])
def kill_job(job_id, role, party_id):
    JobController.kill_job(job_id=job_id, role=role, party_id=(int(party_id)), job_initiator=(request.json.get('job_initiator', {})),
      timeout=(request.json.get('timeout', False)),
      component_name=(request.json.get('component_name', '')))
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<role>/<party_id>/cancel', methods=['POST'])
def cancel_job(job_id, role, party_id):
    res = JobController.cancel_job(job_id=job_id, role=role, party_id=(int(party_id)), job_initiator=(request.json.get('job_initiator', {})))
    if res:
        return get_json_result(retcode=0, retmsg='cancel job success')
    return get_json_result(retcode=101, retmsg='cancel job failed')


@manager.route('/<job_id>/<role>/<party_id>/<roles>/<party_ids>/clean', methods=['POST'])
@request_authority_certification
def clean(job_id, role, party_id, roles, party_ids):
    JobController.clean_job(job_id=job_id, role=role, party_id=party_id, roles=roles, party_ids=party_ids)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<component_name>/<task_id>/<role>/<party_id>/run', methods=['POST'])
@request_authority_certification
def run_task(job_id, component_name, task_id, role, party_id):
    TaskScheduler.run_task(job_id, component_name, task_id, role, party_id, request.json)
    return get_json_result(retcode=0, retmsg='success')


@manager.route('/<job_id>/<component_name>/<task_id>/<role>/<party_id>/status', methods=['POST'])
def task_status(job_id, component_name, task_id, role, party_id):
    JobController.update_task_status(job_id, component_name, task_id, role, party_id, request.json)
    return get_json_result(retcode=0, retmsg='success')