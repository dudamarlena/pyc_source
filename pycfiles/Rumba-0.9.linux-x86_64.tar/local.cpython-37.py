# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/rumba/testbeds/local.py
# Compiled at: 2018-08-31 05:12:48
# Size of source mod 2**32: 2334 bytes
import rumba.model as mod
import rumba.log as log
from rumba.executors.local import LocalExecutor
logger = log.get_logger(__name__)

class Testbed(mod.Testbed):
    __doc__ = '\n    Local testbed, does not do anything. In the case of the Ouroboros\n    plugin this is useful since the Ouroboros plugin will simply create\n    processes locally. Also useful for debugging in the other plugins.\n    '

    def __init__(self, exp_name='foo', username='bar', proj_name='rumba', password=''):
        """
        Initializes the parent class.

        :param exp_name: The experiment name.
        :param username: User of the experiment.
        :param proj_name: Project name of the experiment.
        :param password: Password of the user.
        """
        mod.Testbed.__init__(self, exp_name, username, password, proj_name)
        self.executor = LocalExecutor(self)

    def _swap_in(self, experiment):
        """
        Does not actually swap the experiment in.

        :param experiment: The experiment object.
        """
        logger.info('Experiment swapped in')

    def _swap_out(self, experiment):
        """
        Does not actually swap the experiment out.

        :param experiment: The experiment object.
        """
        logger.info('Experiment swapped out')