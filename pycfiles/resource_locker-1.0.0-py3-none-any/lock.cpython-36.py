# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alelog01/git/resource_locker/src/resource_locker/core/lock.py
# Compiled at: 2018-02-01 06:38:36
# Size of source mod 2**32: 5807 bytes
import logging, retrying
from .exceptions import RequirementNotMet
from .requirement import Requirement
from resource_locker.factories.meta import LockFactoryMeta
from resource_locker.factories.redis import RedisLockFactory
from resource_locker.reporter import RedisReporter
from resource_locker.reporter import Timer
from resource_locker.reporter import DummyReporter

class Lock:
    lock_of_locks_key = 'lock_of_locks'

    def __init__(self, *requirements, block=True, lock_factory=None, reporter_class=None, **params):
        self.options = dict(logger=(logging.getLogger(__name__)),
          auto_renewal=True,
          expire=120,
          timeout=None,
          stop_max_delay=300000,
          wait_exponential_max=5000,
          wait_exponential_multiplier=500,
          wait_random_min=100,
          wait_random_max=1000,
          retry_on_exception=(lambda x: isinstance(x, RequirementNotMet)))
        self.options.update(params)
        if not block:
            self.options['stop_max_attempt_number'] = 0
        self.timeout = self.options['timeout']
        self.logger = self.options['logger']
        self.reporter_class = reporter_class or DummyReporter
        self.lock_factory = lock_factory or RedisLockFactory()
        self._obtained = []
        self._unique_keys = set()
        self._lol = self.lock_factory.new_lock((self.lock_of_locks_key), expire=60, auto_renewal=(bool(self.timeout)))
        self._requirements = []
        for req in requirements:
            self.add_requirement(req)

        self.acquire_timer = Timer()
        self.release_timer = Timer()

    def add_requirement(self, req):
        if not isinstance(req, Requirement):
            req = Requirement(req, need=(self.options.get('need')))
        req.validate()
        for p in req.potentials:
            if p.key in self._unique_keys:
                raise ValueError(f"Must have unique keys, got two {repr(p.key)}")
            self._unique_keys.add(p.key)

        self._requirements.append(req)

    def _all_fulfilled_iter(self):
        for r in self._requirements:
            for p in r.fulfilled:
                yield p

    def _acquire_one(self, potential):
        if potential.is_fulfilled or potential.is_rejected:
            self.logger.info('potential %s is already %s', potential, 'fulfilled' if potential.is_fulfilled else 'rejected')
            return
        else:
            lock = (self.lock_factory.new_lock)((potential.key), **self.options)
            acq_kwargs = dict(blocking=(bool(self.timeout)))
            if self.timeout:
                acq_kwargs.update(dict(timeout=(self.timeout)))
            self.logger.info('getting %s, timeout %s', potential.key, self.timeout)
            reporter = (self.reporter_class)(**potential.tags)
            reporter.lock_requested()
            if (lock.acquire)(**acq_kwargs):
                potential.fulfill()
                self._obtained.append(lock)
            else:
                reporter.lock_failed()
                potential.reject()
                self.logger.warning('didnt get lock %s', potential.key)

    def _acquire_all(self):
        for requirement in self._requirements:
            for potential in requirement.prioritised_potentials(self.lock_factory.get_lock_list()):
                if requirement.validate():
                    if requirement.is_fulfilled:
                        break
                self._acquire_one(potential=potential)

            complete = requirement.validate() and requirement.is_fulfilled
            assert complete

        return self._requirements

    def _release_all(self):
        for partial in self._obtained:
            try:
                partial.release()
            except Exception:
                self.logger.exception('partial lock release failed, lock state may be affected:')

        self._obtained.clear()
        for r in self._requirements:
            r.reset()

    def _acquire_or_release(self):
        if not self._requirements:
            return self._requirements
        with self._lol:
            try:
                return self._acquire_all()
            except Exception:
                self.logger.warning('lock acquisition failed, releasing all partial locks')
                self._release_all()
                raise

    def acquire(self):
        """Acquire the Lock as configured"""
        opts = {k:v for k, v in self.options.items() if k in frozenset({'retry_on_exception', 'stop_max_delay', 'wait_random_min', 'stop_max_attempt_number', 'wrap_exception', 'wait_random_max', 'wait_exponential_multiplier', 'wait_fixed', 'wait_exponential_max'}) if k in frozenset({'retry_on_exception', 'stop_max_delay', 'wait_random_min', 'stop_max_attempt_number', 'wrap_exception', 'wait_random_max', 'wait_exponential_multiplier', 'wait_fixed', 'wait_exponential_max'})}
        with self.acquire_timer:
            success = (retrying.Retrying)(**opts).call(self._acquire_or_release)
        for p in self._all_fulfilled_iter():
            (self.reporter_class)(**p.tags).lock_success(self.acquire_timer.duration)

        self.release_timer.start()
        return success

    def release(self):
        """Release the Lock"""
        self.release_timer.stop()
        for p in self._all_fulfilled_iter():
            (self.reporter_class)(**p.tags).lock_released(self.release_timer.duration)

        self._release_all()

    def __enter__(self):
        return self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()