# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_scheduling.py
# Compiled at: 2016-03-16 03:48:56
# Size of source mod 2**32: 3656 bytes
from unittest import TestCase
from mad.scheduling import Scheduler

class DummyAction:

    def __init__(self, schedule):
        self.schedule = schedule
        self.calls = []

    def __call__(self, *args, **kwargs):
        self.calls.append(self.schedule.time_now)

    def was_called_once_at(self, time):
        return len(self.calls) == 1 and self.calls[0] == time

    def was_called_at(self, times):
        return self.calls == times


class SchedulerTest(TestCase):
    __doc__ = '\n    Specification of the scheduler component\n    '

    def test_scheduling_an_action_at_a_given_time(self):
        schedule = Scheduler()
        action = DummyAction(schedule)
        schedule.at(10, action)
        schedule.simulate_until(20)
        self.assertEqual(10, schedule.time_now)
        self.verify_calls([10], action)

    def test_scheduling_action_in_the_past_is_forbidden(self):
        schedule = Scheduler(20)
        action = DummyAction(schedule)
        with self.assertRaises(ValueError):
            schedule.at(10, action)

    def test_scheduling_an_action_after_a_delay(self):
        schedule = Scheduler()
        action = DummyAction(schedule)
        schedule.after(5, action)
        schedule.simulate_until(20)
        self.assertEqual(5, schedule.time_now)
        self.verify_calls([5], action)

    def test_scheduling_an_object_is_forbidden(self):
        schedule = Scheduler()
        action = 'This is not a callable!'
        with self.assertRaises(ValueError):
            schedule.at(10, action)

    def test_scheduling_twice_an_action_at_a_given_time(self):
        schedule = Scheduler()
        action = DummyAction(schedule)
        schedule.at(5, action)
        schedule.at(5, action)
        schedule.simulate_until(20)
        self.assertLessEqual(5, schedule.time_now)
        self.verify_calls([5, 5], action)

    def test_scheduling_an_action_with_a_given_period(self):
        schedule = Scheduler()
        action = DummyAction(schedule)
        schedule.every(5, action)
        schedule.simulate_until(20)
        self.assertLessEqual(20, schedule.time_now)
        self.verify_calls([5, 10, 15, 20], action)

    def test_simulation_orders_events(self):
        schedule = Scheduler()
        action = DummyAction(schedule)
        schedule.at(10, action)
        schedule.at(5, action)
        schedule.simulate_until(20)
        self.verify_calls([5, 10], action)

    def test_scheduling_at_a_non_integer_time(self):
        schedule = Scheduler()
        action = DummyAction(schedule)
        with self.assertRaises(ValueError):
            schedule.at('now', action)

    def verify_calls(self, expectation, action):
        self.assertTrue(action.was_called_at(expectation), 'Action called on %s' % str(action.calls))


if __name__ == '__main__':
    from unittest import main
    main()