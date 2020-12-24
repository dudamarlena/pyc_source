# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grafoleancollector/collector.py
# Compiled at: 2020-04-12 08:11:23
# Size of source mod 2**32: 18634 bytes
import sys, requests, logging, time, math
from datetime import datetime, timedelta
from pytz import utc
from abc import abstractmethod
import concurrent.futures, traceback
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.base import BaseTrigger
from apscheduler.executors.base import BaseExecutor
from apscheduler.events import JobExecutionEvent, EVENT_JOB_MISSED, EVENT_JOB_ERROR, EVENT_JOB_EXECUTED

class MultipleIntervalsTrigger(BaseTrigger):
    __doc__ = "\n        This is a class extends APScheduler's BaseTrigger:\n        - triggers at multiple intervals\n        - aligns every invocation to a second (to make calculation of intervals easier)\n        - multiple intervals, when aligned, cause only a single job invocation\n        - remembers which intervals have caused the invocation; the list is cleared after\n          `forget_affecting_after` seconds\n        - if start_ts is specified, it allows aligning jobs' start time; start_ts should be in the past\n    "
    __slots__ = ('intervals', 'start_ts', 'affecting_intervals', 'forget_affecting_after')

    def __init__(self, intervals, forget_affecting_after=300, start_ts=None):
        if not intervals:
            raise Exception('At least one interval must be specified')
        self.intervals = list(set([int(i) for i in intervals]))
        self.forget_affecting_after = forget_affecting_after
        now = int(time.time())
        self.start_ts = now if start_ts is None else int(start_ts)
        if self.start_ts > now:
            logging.warning('Job aligning with start_ts failed! Parameter start_ts must be in the past, never in the future.')
            self.start_ts = now
        self.affecting_intervals = {}

    def get_next_fire_time(self, previous_fire_time, now):
        elapsed_time = now.timestamp() - self.start_ts
        next_fires_for_intervals = [int(math.ceil(elapsed_time / interval) * interval) for interval in self.intervals]
        min_next_fire = min(next_fires_for_intervals)
        next_fire_ts = self.start_ts + min_next_fire
        self.affecting_intervals[next_fire_ts] = []
        for i, next_fire_for_interval in enumerate(next_fires_for_intervals):
            if next_fire_for_interval == min_next_fire:
                self.affecting_intervals[next_fire_ts].append(self.intervals[i])

        self._cleanup(now.timestamp() - self.forget_affecting_after)
        return datetime.fromtimestamp(next_fire_ts, tz=utc)

    def _cleanup(self, limit_ts):
        for ts in list(self.affecting_intervals.keys()):
            if ts < limit_ts:
                del self.affecting_intervals[ts]


class IntervalsAwareProcessPoolExecutor(BaseExecutor):
    __doc__ = "\n        This class merges APScheduler's BasePoolExecutor and ProcessPoolExecutor,\n        because we need to use our own version of `run_job` (with a small detail\n        changed - additional parameter passed). Unfortunately there is probably no\n        cleaner way to do this at the moment.\n    "

    def __init__(self, max_workers=10):
        super().__init__()
        self._pool = concurrent.futures.ProcessPoolExecutor(int(max_workers))

    def _do_submit_job(self, job, run_times):
        """
        This function is copy-pasted from apscheduler/executors/pool.py
        (`BasePoolExecutor._do_submit_job()`). The difference is that it calls our own
        version of `run_job`.
        """

        def callback(f):
            exc, tb = f.exception_info() if hasattr(f, 'exception_info') else (
             f.exception(), getattr(f.exception(), '__traceback__', None))
            if exc:
                self._run_job_error(job.id, exc, tb)
            else:
                self._run_job_success(job.id, f.result())

        f = self._pool.submit(IntervalsAwareProcessPoolExecutor.run_job, job, job._jobstore_alias, run_times, self._logger.name)
        f.add_done_callback(callback)

    def shutdown(self, wait=True):
        self._pool.shutdown(wait)

    @staticmethod
    def run_job(job, jobstore_alias, run_times, logger_name):
        """
        This function is copy-pasted from apscheduler/executors/base.py (`run_job()`). It is defined
        as static method here, and only the invocation of the job (`job.func()` call) was changed.

        The reason for this is that we need to pass `affecting_intervals` from the trigger to the job
        function, so it can decide which parts of the job need to be run. SNMPCollector needs this
        so it can fetch data either separately, or for all of the task at the same time, when their
        intervals align.

        The changes are in a single block and are marked with a comment.

        ---
        Called by executors to run the job. Returns a list of scheduler events to be dispatched by the
        scheduler.
        """
        events = []
        logger = logging.getLogger(logger_name)
        for run_time in run_times:
            if job.misfire_grace_time is not None:
                difference = datetime.now(utc) - run_time
                grace_time = timedelta(seconds=(job.misfire_grace_time))
                if difference > grace_time:
                    events.append(JobExecutionEvent(EVENT_JOB_MISSED, job.id, jobstore_alias, run_time))
                    logger.warning('Run time of job "%s" was missed by %s', job, difference)
                    continue
            logger.info('Running job "%s" (scheduled at %s)', job, run_time)
            try:
                affecting_intervals = job.trigger.affecting_intervals[run_time.timestamp()]
                retval = (job.func)(affecting_intervals, **job.kwargs)
            except BaseException:
                exc, tb = sys.exc_info()[1:]
                formatted_tb = ''.join(traceback.format_tb(tb))
                events.append(JobExecutionEvent(EVENT_JOB_ERROR, (job.id), jobstore_alias, run_time, exception=exc,
                  traceback=formatted_tb))
                logger.exception('Job "%s" raised an exception', job)
                traceback.clear_frames(tb)
                del tb
            else:
                events.append(JobExecutionEvent(EVENT_JOB_EXECUTED, (job.id), jobstore_alias, run_time, retval=retval))
                logger.info('Job "%s" executed successfully', job)

        return events

    def _run_job_error(self, job_id, exc, traceback=None):
        """
            > Called by the executor with the exception if there is an error  calling `run_job`.

            Sometimes we start getting traceback, after which collector no longer works:
            -----
                2019-10-04 19:45:38 | ERR | Error submitting job "SNMPCollector.do_snmp (trigger: <collector.MultipleIntervalsTrigger object at 0x7fd866b9aee8>, next run at: 2019-10-04 19:45:38 UTC)" to executor "iaexecutor"
                Traceback (most recent call last):
                File "/usr/local/lib/python3.6/site-packages/apscheduler/schedulers/base.py", line 974, in _process_jobs
                    executor.submit_job(job, run_times)
                File "/usr/local/lib/python3.6/site-packages/apscheduler/executors/base.py", line 71, in submit_job
                    self._do_submit_job(job, run_times)
                File "./collector.py", line 92, in _do_submit_job
                File "/usr/local/lib/python3.6/concurrent/futures/process.py", line 452, in submit
                    raise BrokenProcessPool('A child process terminated '
                concurrent.futures.process.BrokenProcessPool: A child process terminated abruptly, the process pool is not usable anymore
            -----

            The idea is that we remember that we are in this state, so that we can make Docker health check fail.
        """
        super()._run_job_error(job_id, exc, traceback)
        if 'BrokenProcessPool' in exc.__class__.__name__:
            open('/tmp/fail_health_check', 'a').close()


def send_results_to_grafolean(backend_url, bot_token, account_id, values):
    url = '{}/accounts/{}/values/?b={}'.format(backend_url, account_id, bot_token)
    if len(values) == 0:
        logging.warning('No results available to be sent to Grafolean, skipping.')
        return
    logging.info('Sending results to Grafolean')
    try:
        r = requests.post(url, json=values)
        r.raise_for_status()
        logging.info('Results sent: {}'.format(values))
    except:
        logging.exception('Error sending data to Grafolean')


class Collector(object):
    __slots__ = ('backend_url', 'bot_token', 'scheduler', 'known_jobs', 'jobs_refresh_interval',
                 'user_id')

    def __init__(self, backend_url, bot_token, jobs_refresh_interval):
        self.backend_url = backend_url
        self.bot_token = bot_token
        self.jobs_refresh_interval = jobs_refresh_interval
        self.known_jobs = {}
        self._fetch_user_id()

    def _fetch_user_id(self):
        r = requests.get('{}/profile/?b={}'.format(self.backend_url, self.bot_token))
        if r.status_code != 200:
            raise Exception('Invalid bot token or network error, got status {} while retrieving {}/profile'.format(r.status_code, self.backend_url))
        j = r.json()
        self.user_id = j['user_id']

    @abstractmethod
    def jobs(self):
        """
            Returns a list of (job_id, intervals, job_func, job_data) tuples. Usually calls
            `fetch_job_configs` to get input data.
        """
        pass

    def fetch_job_configs(self, protocol):
        """
            Returns pairs (account_id, entity_info), where entity_info is everything needed for collecting data
            from the entity - credentials and list of sensors (with intervals) for selected protocol.
            The data is cleaned up as much as possible, so that it only contains the things necessary for collectors
            to do their job.
        """
        requests_session = requests.Session()
        r = requests_session.get('{}/accounts/?b={}'.format(self.backend_url, self.bot_token))
        if r.status_code != 200:
            raise Exception('Invalid bot token or network error, got status {} while retrieving {}/accounts'.format(r.status_code, self.backend_url))
        j = r.json()
        accounts_ids = [a['id'] for a in j['list']]
        for account_id in accounts_ids:
            r = requests_session.get('{}/accounts/{}/entities/?b={}'.format(self.backend_url, account_id, self.bot_token))
            if r.status_code != 200:
                raise Exception('Network error, got status {} while retrieving {}/accounts/{}/entities'.format(r.status_code, self.backend_url, account_id))
            j = r.json()
            entities_ids = [e['id'] for e in j['list'] if e['entity_type'] == 'device']
            for entity_id in entities_ids:
                r = requests_session.get('{}/accounts/{}/entities/{}?b={}'.format(self.backend_url, account_id, entity_id, self.bot_token))
                if r.status_code != 200:
                    raise Exception('Network error, got status {} while retrieving {}/accounts/{}/entities/{}'.format(r.status_code, self.backend_url, account_id, entity_id))
                entity_info = r.json()
                if protocol not in entity_info['protocols']:
                    pass
                else:
                    if entity_info['protocols'][protocol].get('bot', None) is not None:
                        if entity_info['protocols'][protocol]['bot'] != self.user_id:
                            continue
                    if not entity_info['protocols'][protocol]['credential']:
                        continue
                credential_id = entity_info['protocols'][protocol]['credential']
                if not entity_info['protocols'][protocol]['sensors']:
                    pass
                else:
                    r = requests_session.get('{}/accounts/{}/credentials/{}?b={}'.format(self.backend_url, account_id, credential_id, self.bot_token))
                    if r.status_code != 200:
                        raise Exception('Network error, got status {} while retrieving {}/accounts/{}/credentials/{}'.format(r.status_code, self.backend_url, account_id, credential_id))
                    credential = r.json()
                    entity_info['credential_details'] = credential['details']
                    sensors = []
                    for sensor_info in entity_info['protocols'][protocol]['sensors']:
                        sensor_id = sensor_info['sensor']
                        r = requests_session.get('{}/accounts/{}/sensors/{}?b={}'.format(self.backend_url, account_id, sensor_id, self.bot_token))
                        if r.status_code != 200:
                            raise Exception('Network error, got status {} while retrieving {}/accounts/{}/sensors/{}'.format(r.status_code, self.backend_url, account_id, sensor['sensor']))
                        sensor = r.json()
                        if sensor_info['interval'] is not None:
                            interval = sensor_info['interval']
                        else:
                            if sensor['default_interval'] is not None:
                                interval = sensor['default_interval']
                            else:
                                interval = None
                        del sensor['default_interval']
                        sensors.append({'sensor_details':sensor['details'], 
                         'sensor_id':sensor_id, 
                         'interval':interval})

                    entity_info['sensors'] = sensors
                    del entity_info['protocols']
                    entity_info['account_id'] = account_id
                    entity_info['entity_id'] = entity_info['id']
                    del entity_info['id']
                    yield entity_info

        requests_session.close()

    def refresh_jobs(self):
        wanted_jobs = set()
        for next_job in self.jobs():
            if len(next_job) == 4:
                job_id, intervals, job_func, job_data = next_job
                start_ts = None
            else:
                job_id, intervals, job_func, job_data, start_ts = next_job
            wanted_jobs.add(job_id)
            if self.known_jobs.get(job_id) == job_data:
                pass
            else:
                self.known_jobs[job_id] = job_data
                trigger = MultipleIntervalsTrigger(intervals, start_ts=start_ts)
                logging.info(f"Adding job: {job_id}")
                self.scheduler.add_job(job_func, id=job_id, trigger=trigger, executor='iaexecutor', kwargs=job_data, replace_existing=True)

        existing_jobs = set(self.known_jobs.keys())
        to_be_removed = existing_jobs - wanted_jobs
        for job_id in to_be_removed:
            del self.known_jobs[job_id]
            self.scheduler.remove_job(job_id)

    def execute(self):
        """
            Calls self.jobs() to get the list of the jobs, and executes them by using
            `MultipleIntervalsTrigger`. Blocking.
        """
        job_defaults = {'coalesce':True, 
         'max_instances':100}
        self.scheduler = BackgroundScheduler(job_defaults=job_defaults, timezone=utc)
        self.scheduler.add_executor(IntervalsAwareProcessPoolExecutor(10), 'iaexecutor')
        try:
            try:
                self.scheduler.start()
                while True:
                    try:
                        self.refresh_jobs()
                    except:
                        logging.exception('Error refreshing jobs.')

                    time.sleep(self.jobs_refresh_interval)

            except KeyboardInterrupt:
                logging.info('Got exit signal, exiting.')

        finally:
            self.scheduler.shutdown()