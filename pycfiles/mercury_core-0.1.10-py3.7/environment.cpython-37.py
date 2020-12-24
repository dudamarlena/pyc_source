# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/behave/api/features/environment.py
# Compiled at: 2018-09-26 16:15:23
# Size of source mod 2**32: 4203 bytes
import datetime, logging, os, unittest
from collections import defaultdict
from src.tests.behave.common.config import get_conflagration
LOGS_DIR = os.environ.get('BEHAVE_LOGS_DIR', './logs')

class Loggers(object):

    def __init__(self, loglevel=logging.DEBUG):
        self.feature = logging.getLogger('behave.feature')
        self.feature.setLevel(loglevel)
        self.scenario = logging.getLogger('behave.scenario')
        self.scenario.setLevel(loglevel)
        self.step = logging.getLogger('behave.step')
        self.step.setLevel(loglevel)
        self.all = logging.getLogger('behave.all')
        self.all.setLevel(loglevel)


def before_all(context):
    """
    :type context: behave.runner.Context
    """
    context.cfg = get_conflagration()
    context.config.setup_logging()
    context.logger = Loggers()
    product = context.config.paths[0].split('/')[(-1)]
    timestamp = str(datetime.datetime.now()).translate(str.maketrans(' :', '__'))
    product_dir = os.path.join(LOGS_DIR, product)
    current_log_dir = os.path.join(product_dir, timestamp)
    for dir_ in (LOGS_DIR, product_dir, current_log_dir):
        if not os.path.exists(dir_):
            os.mkdir(dir_)

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename=(os.path.join(current_log_dir, 'behave.master.log')),
      mode='w')
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(logging.Formatter(fmt='%(asctime)s - %(levelname)s:  %(name)s: %(message)s'))
    root_logger.addHandler(handler)
    context.base_url = context.cfg.MERCURY.mercury_api_endpoint
    context.json_location = context.cfg.TEST_DATA.json_api_data_location
    context.services = defaultdict(dict)
    context.check = unittest.TestCase()
    context.logger.all.info('++++++++++++++++')
    context.logger.all.info('TESTS STARTED! (Endpoint {0})'.format(context.base_url))
    context.logger.all.info('++++++++++++++++')


def after_all(context):
    """
    :type context: behave.runner.Context
    """
    context.logger.all.info('++++++++++++++++')
    context.logger.all.info('TESTS FINISHED!')
    context.logger.all.info('++++++++++++++++')


def before_feature(context, feature):
    """
    :type context: behave.runner.Context
    :type feature: behave.model.Feature
    """
    context.logger.feature.info('++++++++')
    context.logger.feature.info('Feature: {}'.format(feature.name))
    context.logger.feature.info('++++++++')


def after_feature(context, feature):
    """
    :type context: behave.runner.Context
    :type feature: behave.model.Feature
    """
    context.logger.feature.info('Feature Completed: {}'.format(feature.name))


def before_scenario(context, scenario):
    """
    :type context: behave.runner.Context
    :type scenario: behave.model.Scenario
    """
    context.logger.scenario.info('   +++++++++')
    context.logger.scenario.info('   Scenario: {}'.format(scenario.name))
    context.logger.scenario.info('   +++++++++')


def after_scenario(context, scenario):
    """
    :type context: behave.runner.Context
    :type scenario: behave.model.Scenario
    """
    context.logger.scenario.info('   Scenario Completed: {}'.format(scenario.name))


def before_step(context, step):
    """
    :type context: behave.runner.Context
    :type step: behave.model.Step
    """
    context.logger.step.info('            {} {}'.format(step.keyword, step.name))


def after_step(context, step):
    """
    :type context: behave.runner.Context
    :type step: behave.model.Step
    """
    if step.status == 'failed':
        context.logger.step.info('              ---------')
        context.logger.step.info('              - FAILED: {} {}'.format(step.keyword, step.name))
        context.logger.step.info('              ---------')
    else:
        context.logger.step.info('              - passed')