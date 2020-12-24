# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sage/fatedoc/FATE/fate_flow/driver/dag_scheduler.py
# Compiled at: 2020-04-28 09:16:53
# Size of source mod 2**32: 2396 bytes
import threading
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from arch.api.utils.log_utils import schedule_logger
from fate_flow.driver.job_controller import TaskScheduler
from fate_flow.manager.queue_manager import BaseQueue

class DAGScheduler(threading.Thread):

    def __init__(self, queue, concurrent_num=1):
        super(DAGScheduler, self).__init__()
        self.concurrent_num = concurrent_num
        self.queue = queue
        self.job_executor_pool = ThreadPoolExecutor(max_workers=concurrent_num)

    def run(self):
        if not self.queue.is_ready():
            schedule_logger().error('queue is not ready')
            return False
        all_jobs = []
        while True:
            try:
                if len(all_jobs) == self.concurrent_num:
                    for future in as_completed(all_jobs):
                        all_jobs.remove(future)
                        break

                job_event = self.queue.get_event()
                schedule_logger(job_event['job_id']).info('schedule job {}'.format(job_event))
                future = self.job_executor_pool.submit(DAGScheduler.handle_event, job_event)
                future.add_done_callback(DAGScheduler.get_result)
                all_jobs.append(future)
            except Exception as e:
                try:
                    schedule_logger().exception(e)
                finally:
                    e = None
                    del e

    def stop(self):
        self.job_executor_pool.shutdown(True)

    @staticmethod
    def handle_event(job_event):
        try:
            return (TaskScheduler.run_job)(**job_event)
        except Exception as e:
            try:
                schedule_logger(job_event.get('job_id')).exception(e)
                return False
            finally:
                e = None
                del e

    @staticmethod
    def get_result(future):
        future.result()