# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/manager/pipeline_manager.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 2009 bytes
from arch.api.utils.core_utils import json_loads
from fate_flow.settings import stat_logger
from fate_flow.utils import job_utils, detect_utils

def pipeline_dag_dependency(job_info):
    try:
        detect_utils.check_config(job_info, required_arguments=['party_id', 'role'])
        if job_info.get('job_id'):
            jobs = job_utils.query_job(job_id=(job_info['job_id']), party_id=(job_info['party_id']), role=(job_info['role']))
            if not jobs:
                raise Exception('query job {} failed'.format(job_info.get('job_id', '')))
            job = jobs[0]
            job_dsl_parser = job_utils.get_job_dsl_parser(dsl=(json_loads(job.f_dsl)), runtime_conf=(json_loads(job.f_runtime_conf)),
              train_runtime_conf=(json_loads(job.f_train_runtime_conf)))
        else:
            job_dsl_parser = job_utils.get_job_dsl_parser(dsl=(job_info.get('job_dsl', {})), runtime_conf=(job_info.get('job_runtime_conf', {})),
              train_runtime_conf=(job_info.get('job_train_runtime_conf', {})))
        return job_dsl_parser.get_dependency(role=(job_info['role']), party_id=(int(job_info['party_id'])))
    except Exception as e:
        try:
            stat_logger.exception(e)
            raise e
        finally:
            e = None
            del e