# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\ast\test_settings.py
# Compiled at: 2016-04-04 08:35:31
# Size of source mod 2**32: 3680 bytes
from unittest import TestCase
from mock import MagicMock, call
from mad.ast.settings import *
from mad.evaluation import Evaluation

class SettingsTest(TestCase):

    def test_default_queue_settings_is_fifo(self):
        settings = Settings()
        self.assertIsInstance(settings.queue, FIFO)

    def test_setting_queue(self):
        settings = Settings(queue=LIFO())
        self.assertIsInstance(settings.queue, LIFO)

    def test_default_throttling_is_none(self):
        settings = Settings()
        self.assertIsInstance(settings.throttling, NoThrottlingSettings)

    def test_specifying_throttling(self):
        tail_drop = TailDropSettings(50)
        settings = Settings(throttling=tail_drop)
        self.assertIs(tail_drop, settings.throttling)

    def test_accept(self):
        settings = Settings()
        evaluation = MagicMock(Evaluation)
        settings.accept(evaluation)
        evaluation.of_settings.assert_called_once_with(settings)

    def test_equality(self):
        self.assertEqual(Settings(queue=FIFO()), Settings(queue=FIFO()))


class AutoscalingSettingsTest(TestCase):

    def test_reject_invalid_limits(self):
        with self.assertRaises(ValueError):
            Autoscaling(period=10, limits=23)

    def test_reject_invalid_period(self):
        with self.assertRaises(ValueError):
            Autoscaling(period='wrong', limits=23)

    def test_evaluation(self):
        settings = Autoscaling()
        evaluation = MagicMock(Evaluation)
        settings.accept(evaluation)
        evaluation.of_autoscaling.assert_called_once_with(settings)


class FIFOTests(TestCase):

    def test_accept(self):
        queue = FIFO()
        evaluation = MagicMock(Evaluation)
        queue.accept(evaluation)
        evaluation.of_fifo.assert_called_once_with(queue)

    def test_equality(self):
        self.assertEqual(FIFO(), FIFO())


class LIFOTests(TestCase):

    def test_accept(self):
        queue = LIFO()
        evaluation = MagicMock(Evaluation)
        queue.accept(evaluation)
        evaluation.of_lifo.assert_called_once_with(queue)

    def test_equality(self):
        self.assertEqual(FIFO(), FIFO())


class NoThrottlingTests(TestCase):

    def test_evaluation(self):
        evaluation = MagicMock(Evaluation)
        throttling = NoThrottlingSettings()
        throttling.accept(evaluation)
        evaluation.of_no_throttling.has_calls([call(throttling)])


class TailDropTests(TestCase):

    def test_should_expose_the_capacity(self):
        capacity = 50
        tail_drop = TailDropSettings(capacity)
        self.assertEqual(capacity, tail_drop.capacity)

    def test_should_switch_to_the_proper_evaluation(self):
        evaluation = MagicMock(Evaluation)
        tail_drop = TailDropSettings(50)
        tail_drop.accept(evaluation)
        evaluation.of_tail_drop.has_calls([call(tail_drop)])