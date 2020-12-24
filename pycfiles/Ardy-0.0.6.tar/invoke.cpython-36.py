# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/prometeo/projects/ardy/ardy/core/invoke/invoke.py
# Compiled at: 2018-03-24 11:47:25
# Size of source mod 2**32: 1522 bytes
from __future__ import unicode_literals, print_function
import importlib, os, sys, time
from ardy.config import ConfigMixin
from ardy.utils.log import logger
from tests.mocks_utils import MockContext

class Invoke(ConfigMixin):

    def __init__(self, *args, **kwargs):
        (super(Invoke, self).__init__)(*args, **kwargs)

    def run(self, lambda_name, local=True):
        lambda_config = self.config.get_lambda_by_name(lambda_name)
        if local:
            result = self._run_local_lambda(lambda_config)

    def _run_local_lambda(self, lambda_config):
        prev_folder = os.getcwd()
        os.chdir(self.config.get_projectdir())
        sys.path.append(self.config.get_projectdir())
        lambda_name = lambda_config['FunctionName']
        lambda_handler = self.import_function(lambda_config['Handler'])
        start = time.time()
        results = lambda_handler({}, MockContext(lambda_name))
        end = time.time()
        os.chdir(prev_folder)
        logger.info('{0}'.format(results))
        logger.info('\nexecution time: {:.8f}s\nfunction execution timeout: {:2}s'.format(end - start, lambda_config['Timeout']))

    def import_function(self, name):
        components = name.split('.')
        module = importlib.import_module('.'.join(components[:-1]))
        return getattr(module, components[(-1)])