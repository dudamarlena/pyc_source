# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/christian/PycharmProjects/Yeti/yeti/robot.py
# Compiled at: 2015-09-22 15:44:59
# Size of source mod 2**32: 1741 bytes
import wpilib
from robotpy_ext.misc import asyncio_policy
from os.path import join, abspath, dirname
from yeti import Engine

class YetiRobot(wpilib.IterativeRobot):
    __doc__ = '\n    A standard robot class that starts a yeti engine.\n    '
    config_dir = ''
    config_file = 'yeti.yml'
    asyncio_policy.patch_asyncio_policy()

    def robotInit(self):
        self.engine = Engine()
        self.engine.load_config(join(abspath(dirname(__file__)), 'default.yml'))
        self.engine.load_config(join(self.config_dir, self.config_file))
        self.engine.spawn_thread()

    def teleopInit(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('teleop_init'))
        self.engine.thread_coroutine(self.engine.run_tagged_methods('enabled_init'))

    def teleopPeriodic(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('teleop_periodic'))
        self.engine.thread_coroutine(self.engine.run_tagged_methods('enabled_periodic'))

    def autonomousInit(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('autonomous_periodic'))
        self.engine.thread_coroutine(self.engine.run_tagged_methods('enabled_init'))

    def autonomousPeriodic(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('autonomous_periodic'))
        self.engine.thread_coroutine(self.engine.run_tagged_methods('enabled_periodic'))

    def disabledInit(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('disabled_periodic'))

    def disabledPeriodic(self):
        self.engine.thread_coroutine(self.engine.run_tagged_methods('disabled_periodic'))