# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miph/Development/logdog/python-logdog/logdog/pollers/fake_watcher.py
# Compiled at: 2015-02-28 20:13:01
from datetime import timedelta
import logging
from tornado import gen
from tornado.concurrent import is_future
from logdog.core.roles.pollers import BasePoller
logger = logging.getLogger(__name__)

class FakeWatcher(BasePoller):
    defaults = BasePoller.defaults.copy_and_update(poll_sleep_policy='utils.sleep-policies.default', greedy_file_reading=False, sleep_delay=2.5)

    def __init__(self, app, **config):
        super(FakeWatcher, self).__init__(app, **config)
        self.poll_sleep_policy = self.app.config.find_and_construct_class(name=self.config.poll_sleep_policy)

    def __str__(self):
        return ('{!s}:WATCHER').format(self.pipe)

    def _prepare_message(self, data):
        msg = super(FakeWatcher, self)._prepare_message(data)
        msg.source = getattr(self.input, 'name', msg.source)
        return msg

    @gen.coroutine
    def poll(self):
        from faker import Faker
        fake = Faker()
        greedy_file_reading_enabled = self.config.greedy_file_reading
        while self.started:
            data = fake.random_element({fake.text() + '\n': 0.99, '': 0.01})
            if data:
                try:
                    data = self._prepare_message(data)
                    ret = self._forward(data)
                    if is_future(ret):
                        yield gen.with_timeout(timedelta(seconds=10), ret)
                except Exception as e:
                    logger.exception(e)

                self.poll_sleep_policy.reset()
                if not greedy_file_reading_enabled:
                    yield gen.moment
            else:
                logger.debug('[%s] Sleep on watching %ss.', self, self.poll_sleep_policy.cur_interval)
                yield self.poll_sleep_policy.sleep()