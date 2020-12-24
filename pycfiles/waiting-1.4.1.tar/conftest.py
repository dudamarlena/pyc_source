# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/vmalloc/waiting/tests/conftest.py
# Compiled at: 2017-01-31 02:27:24
from forge import Forge
import logging, waiting, pytest
_logger = logging.getLogger(__name__)

@pytest.fixture
def forge(request):
    returned = Forge()

    @request.addfinalizer
    def cleanup():
        returned.verify()
        returned.restore_all_replacements()

    return returned


@pytest.fixture
def timeline(forge):

    class VirtualTimeline(object):

        class FirstTestException(Exception):
            pass

        class SecondTestException(Exception):
            pass

        def __init__(self):
            super(VirtualTimeline, self).__init__()
            self.virtual_time = 0
            self.sleeps_performed = []
            self.predicate_satisfied = False
            self.satisfy_at_time = None
            self.satisfy_after_time = None
            self.predicate_sleep = 0
            return

        def sleep(self, delta):
            self.sleeps_performed.append(delta)
            self.virtual_time += delta
            assert 1000 > len(self.sleeps_performed), 'Infinite loop'

        def time(self):
            return self.virtual_time

        def predicate(self):
            if self.satisfy_at_time is not None and self.satisfy_at_time == self.virtual_time:
                self.predicate_satisfied = True
            if self.satisfy_after_time is not None and self.satisfy_after_time <= self.virtual_time:
                self.predicate_satisfied = True
            self.virtual_time += self.predicate_sleep
            _logger.debug('Predicate: time is now %s', self.virtual_time)
            return self.predicate_satisfied

        def raising_predicate(self):
            if self.virtual_time == 0:
                raise self.FirstTestException()
            return self.predicate()

        def raising_two_exceptions_predicate(self):
            if self.virtual_time == 1:
                raise self.SecondTestException()
            return self.raising_predicate()

    returned = VirtualTimeline()
    forge.replace_with(waiting.time_module, 'sleep', returned.sleep)
    forge.replace_with(waiting.time_module, 'time', returned.time)
    forge.replace_with(waiting.deadlines.time_module, 'time', returned.time)
    return returned


@pytest.fixture
def predicates(forge):
    return [ forge.create_wildcard_mock() for i in range(5) ]