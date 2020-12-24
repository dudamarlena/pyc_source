# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\test_evaluation.py
# Compiled at: 2016-04-22 04:28:16
# Size of source mod 2**32: 2726 bytes
from unittest import TestCase
from tests.fakes import InMemoryDataStorage
from mad.environment import Environment
from mad.ast.actions import *
from mad.ast.settings import *
from mad.evaluation import Evaluation, Symbols
from mad.simulation.factory import Simulation, Factory
from mad.simulation.tasks import LIFOTaskPool, FIFOTaskPool
from mad.simulation.autoscaling import AutoScaler

class EvaluationTest(TestCase):

    def test_evaluation_of_fail(self):
        environment = Environment()
        result = Evaluation(environment, Fail(), Factory()).result
        self.assertTrue(result.is_erroneous)

    def test_evaluation_of_fifo(self):
        environment = Environment()
        queue = FIFO()
        Evaluation(environment, queue, Factory()).result
        queue = environment.look_up(Symbols.QUEUE).delegate
        self.assertIsInstance(queue, FIFOTaskPool)

    def test_evaluation_of_lifo(self):
        environment = Environment()
        queue = LIFO()
        Evaluation(environment, queue, Factory()).result
        queue = environment.look_up(Symbols.QUEUE).delegate
        self.assertIsInstance(queue, LIFOTaskPool)

    def test_evaluation_of_queue_settings(self):
        settings = Settings(queue=LIFO())
        simulation = Simulation(InMemoryDataStorage(None))
        simulation.evaluate(settings)
        task_pool = simulation.environment.look_up(Symbols.QUEUE).delegate.delegate.delegate
        self.assertIsInstance(task_pool, LIFOTaskPool)

    def test_evaluation_of_autoscaling_settings(self):
        PERIOD = 23
        settings = Settings(autoscaling=Autoscaling(PERIOD, limits=(3, 5)))
        simulation = Simulation(InMemoryDataStorage(None))
        simulation.evaluate(settings)
        autoscaler = simulation.environment.look_up(Symbols.AUTOSCALING)
        self.assertIsInstance(autoscaler, AutoScaler)
        self.assertEqual(PERIOD, autoscaler.period)
        self.assertEqual((3, 5), autoscaler.limits)