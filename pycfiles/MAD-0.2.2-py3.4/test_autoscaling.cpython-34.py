# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_autoscaling.py
# Compiled at: 2016-04-05 03:36:19
# Size of source mod 2**32: 2329 bytes
from unittest import TestCase
from mock import MagicMock, PropertyMock
from mad.evaluation import Service
from mad.simulation.autoscaling import RuleBasedStrategy

class AutoScalingTests(TestCase):

    def test_decrease_worker_count(self):
        autoscaling = RuleBasedStrategy(70, 80)
        service = self.prepare_service(worker_count=5, utilisation=50.0)
        autoscaling.adjust(service)
        service.set_worker_count.assert_called_once_with(4)

    def test_increase_when_utilisation_too_high(self):
        autoscaling = RuleBasedStrategy(70, 80)
        service = self.prepare_service(worker_count=5, utilisation=99.0)
        autoscaling.adjust(service)
        service.set_worker_count.assert_called_once_with(5)

    def test_do_not_decrease_below_minimum(self):
        autoscaling = RuleBasedStrategy(1, 5, 70, 80)
        service = self.prepare_service(worker_count=1, utilisation=50.0)
        autoscaling.adjust(service)
        service.set_worker_count.assert_called_once_with(1)

    def test_do_not_exceed_capacity(self):
        autoscaling = RuleBasedStrategy(1, 5, 70, 80)
        service = self.prepare_service(worker_count=5, utilisation=99.0)
        autoscaling.adjust(service)
        service.set_worker_count.assert_called_once_with(5)

    def prepare_service(self, worker_count, utilisation):
        service = MagicMock(Service)
        type(service).utilisation = PropertyMock(return_value=utilisation)
        type(service).worker_count = PropertyMock(return_value=worker_count)
        service.set_worker_count = MagicMock()
        return service