# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/Documents/workspace/Yeti/yeti/robot.py
# Compiled at: 2016-02-18 19:57:13
# Size of source mod 2**32: 1810 bytes
import wpilib
from os.path import join, abspath, dirname
from yeti import Engine
from robotpy_ext.misc import asyncio_policy

class YetiRobot(wpilib.IterativeRobot):
    __doc__ = '\n    A standard robot class that starts a yeti engine.\n    '
    config_dir = ''
    config_file = 'yeti.yml'

    def robotInit(self):
        self.engine = Engine(asyncio_policy.FPGATimedEventLoop)
        self.engine.load_config(join(abspath(dirname(__file__)), 'default.yml'))
        self.engine.load_config(join(self.config_dir, self.config_file))
        self.engine.spawn_thread()
        self.engine.thread_coroutine(self.engine.run_tagged_methods('main_loop'))

    def teleopInit(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('teleop_init'))
        self.engine.thread_coroutine(self.engine.run_tagged_methods('enabled_init'))

    def teleopPeriodic(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('teleop_periodic'))
        self.engine.thread_coroutine(self.engine.run_tagged_methods('enabled_periodic'))
        wpilib.Timer.delay(0.01)

    def autonomousInit(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('autonomous_init'))
        self.engine.thread_coroutine(self.engine.run_tagged_methods('enabled_init'))

    def autonomousPeriodic(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('autonomous_periodic'))
        self.engine.thread_coroutine(self.engine.run_tagged_methods('enabled_periodic'))
        wpilib.Timer.delay(0.01)

    def disabledInit(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('disabled_init'))

    def disabledPeriodic(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('disabled_periodic'))
        wpilib.Timer.delay(0.01)