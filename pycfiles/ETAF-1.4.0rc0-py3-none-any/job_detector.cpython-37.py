# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/driver/job_detector.py
# Compiled at: 2020-04-28 09:19:05
# Size of source mod 2**32: 3763 bytes
from arch.api.utils.core_utils import get_lan_ip, json_loads
from arch.api.utils.log_utils import schedule_logger
from fate_flow.driver.task_scheduler import TaskScheduler
from fate_flow.settings import detect_logger, API_VERSION
from fate_flow.utils import cron, job_utils, api_utils

class JobDetector(cron.Cron):

    def run_do(self):
        try:
            try:
                running_tasks = job_utils.query_task(status='running', run_ip=(get_lan_ip()))
                stop_job_ids = set()
                for task in running_tasks:
                    try:
                        process_exist = job_utils.check_job_process(int(task.f_run_pid))
                        if not process_exist:
                            detect_logger.info('job {} component {} on {} {} task {} {} process does not exist'.format(task.f_job_id, task.f_component_name, task.f_role, task.f_party_id, task.f_task_id, task.f_run_pid))
                            stop_job_ids.add(task.f_job_id)
                    except Exception as e:
                        try:
                            detect_logger.exception(e)
                        finally:
                            e = None
                            del e

                if stop_job_ids:
                    schedule_logger().info('start to stop jobs: {}'.format(stop_job_ids))
                for job_id in stop_job_ids:
                    jobs = job_utils.query_job(job_id=job_id)
                    if jobs:
                        initiator_party_id = jobs[0].f_initiator_party_id
                        job_work_mode = jobs[0].f_work_mode
                        if len(jobs) > 1:
                            my_party_id = initiator_party_id
                        else:
                            my_party_id = jobs[0].f_party_id
                            initiator_party_id = jobs[0].f_initiator_party_id
                        api_utils.federated_api(job_id=job_id, method='POST',
                          endpoint=('/{}/job/stop'.format(API_VERSION)),
                          src_party_id=my_party_id,
                          dest_party_id=initiator_party_id,
                          src_role=None,
                          json_body={'job_id': job_id},
                          work_mode=job_work_mode)
                        TaskScheduler.finish_job(job_id=job_id, job_runtime_conf=(json_loads(jobs[0].f_runtime_conf)), stop=True)

            except Exception as e:
                try:
                    detect_logger.exception(e)
                finally:
                    e = None
                    del e

        finally:
            detect_logger.info('finish detect running job')