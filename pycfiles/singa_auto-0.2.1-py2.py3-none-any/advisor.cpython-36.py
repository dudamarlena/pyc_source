# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/singa_auto/worker/advisor.py
# Compiled at: 2020-04-23 12:22:03
# Size of source mod 2**32: 8024 bytes
import logging, os
from typing import Dict
import time, traceback
from singa_auto.utils.auth import superadmin_client
from singa_auto.meta_store import MetaStore
from singa_auto.model import load_model_class
from singa_auto.advisor import make_advisor, BaseAdvisor
from singa_auto.redis import TrainCache, ParamCache
LOOP_SLEEP_SECS = 0.1

class InvalidSubTrainJobError(Exception):
    pass


logger = logging.getLogger(__name__)

class _WorkerInfo:

    def __init__(self):
        self.trial_id = None


class AdvisorWorker:

    def __init__(self, service_id):
        self._monitor = _SubTrainJobMonitor(service_id)
        self._redis_host = os.environ['REDIS_HOST']
        self._redis_port = os.environ['REDIS_PORT']
        self._train_cache = None
        self._param_cache = None
        self._advisor = None
        self._worker_infos = {}

    def start(self):
        self._monitor.pull_job_info()
        self._train_cache = TrainCache(self._monitor.sub_train_job_id, self._redis_host, self._redis_port)
        self._param_cache = ParamCache(self._monitor.sub_train_job_id, self._redis_host, self._redis_port)
        self._advisor = self._make_advisor()
        logger.info(f'Starting advisor for sub train job "{self._monitor.sub_train_job_id}"...')
        self._notify_start()
        while True:
            self._fetch_results()
            if not self._make_proposals():
                self._notify_budget_reached()
                break
            time.sleep(LOOP_SLEEP_SECS)

    def stop(self):
        self._notify_stop()
        try:
            self._train_cache.clear_all()
        except:
            logger.error('Error clearing train cache:')
            logger.error(traceback.format_exc())

        try:
            self._param_cache.clear_all_params()
        except:
            logger.error('Error clearing params cache:')
            logger.error(traceback.format_exc())

    def _notify_start(self):
        superadmin_client().send_event('sub_train_job_advisor_started', sub_train_job_id=(self._monitor.sub_train_job_id))

    def _make_advisor(self):
        clazz = self._monitor.model_class
        budget = self._monitor.budget
        knob_config = clazz.get_knob_config()
        advisor = make_advisor(knob_config, budget)
        logger.info(f'Using advisor "{type(advisor).__name__}"...')
        return advisor

    def _fetch_results(self):
        for worker_id, info in self._worker_infos.items():
            if info.trial_id is None:
                pass
            else:
                result = self._train_cache.take_result(worker_id)
                if result is None:
                    pass
                else:
                    self._advisor.feedback(worker_id, result)
                    info.trial_id = None

    def _make_proposals(self):
        worker_ids = self._train_cache.get_workers()
        for worker_id in worker_ids:
            if worker_id not in self._worker_infos:
                self._worker_infos[worker_id] = _WorkerInfo()
            worker_info = self._worker_infos[worker_id]
            proposal = self._train_cache.get_proposal(worker_id)
            if proposal is not None:
                pass
            else:
                trial_no, trial_id = self._monitor.create_next_trial(worker_id)
                proposal = self._advisor.propose(worker_id, trial_no)
                if proposal is None:
                    return False
                proposal.trial_id = trial_id
                self._train_cache.create_proposal(worker_id, proposal)
            worker_info.trial_id = trial_id

        return True

    def _notify_budget_reached(self):
        superadmin_client().send_event('sub_train_job_budget_reached', sub_train_job_id=(self._monitor.sub_train_job_id))

    def _notify_stop(self):
        superadmin_client().send_event('sub_train_job_advisor_stopped', sub_train_job_id=(self._monitor.sub_train_job_id))


class _SubTrainJobMonitor:
    __doc__ = '\n        Manages fetching & updating of metadata\n    '

    def __init__(self, service_id: str, meta_store: MetaStore=None):
        self.sub_train_job_id = None
        self.budget = None
        self.model_class = None
        self._num_trials = None
        self._meta_store = meta_store or MetaStore()
        self._service_id = service_id
        self._model_id = None

    def pull_job_info(self):
        service_id = self._service_id
        logger.info('Reading job info from meta store...')
        with self._meta_store:
            sub_train_job = self._meta_store.get_sub_train_job_by_advisor(service_id)
            if sub_train_job is None:
                raise InvalidSubTrainJobError('No sub train job associated with advisor "{}"'.format(service_id))
            train_job = self._meta_store.get_train_job(sub_train_job.train_job_id)
            if train_job is None:
                raise InvalidSubTrainJobError('No such train job with ID "{}"'.format(sub_train_job.train_job_id))
            model = self._meta_store.get_model(sub_train_job.model_id)
            if model is None:
                raise InvalidSubTrainJobError('No such model with ID "{}"'.format(sub_train_job.model_id))
            logger.info(f'Using model "{model.name}"...')
            logger.info(f'Using budget "{train_job.budget}"...')
            trials = self._meta_store.get_trials_of_sub_train_job(sub_train_job.id)
            self.sub_train_job_id = sub_train_job.id
            self.budget = train_job.budget
            self.model_class = load_model_class(model.model_file_bytes, model.model_class)
            self._num_trials = len(trials)
            self._model_id = model.id

    def create_next_trial(self, worker_id):
        self._num_trials += 1
        trial_no = self._num_trials
        with self._meta_store:
            trial = self._meta_store.create_trial(self.sub_train_job_id, trial_no, self._model_id, worker_id)
            self._meta_store.commit()
            trial_id = trial.id
            logger.info(f'Created trial #{trial_no} of ID "{trial_id}" in meta store')
            return (trial_no, trial_id)