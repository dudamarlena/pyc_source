# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_base_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3346 bytes
import json
from typing import Iterable
from airflow.contrib.hooks.sagemaker_hook import SageMakerHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SageMakerBaseOperator(BaseOperator):
    __doc__ = '\n    This is the base operator for all SageMaker operators.\n\n    :param config: The configuration necessary to start a training job (templated)\n    :type config: dict\n    :param aws_conn_id: The AWS connection ID to use.\n    :type aws_conn_id: str\n    '
    template_fields = [
     'config']
    template_ext = ()
    ui_color = '#ededed'
    integer_fields = []

    @apply_defaults
    def __init__(self, config, aws_conn_id='aws_default', *args, **kwargs):
        (super(SageMakerBaseOperator, self).__init__)(*args, **kwargs)
        self.aws_conn_id = aws_conn_id
        self.config = config
        self.hook = None

    def parse_integer(self, config, field):
        if len(field) == 1:
            if isinstance(config, list):
                for sub_config in config:
                    self.parse_integer(sub_config, field)

                return
            else:
                head = field[0]
                if head in config:
                    config[head] = int(config[head])
                return
        else:
            if isinstance(config, list):
                for sub_config in config:
                    self.parse_integer(sub_config, field)

                return
            head, tail = field[0], field[1:]
            if head in config:
                self.parse_integer(config[head], tail)

    def parse_config_integers(self):
        for field in self.integer_fields:
            self.parse_integer(self.config, field)

    def expand_role(self):
        pass

    def preprocess_config(self):
        self.log.info('Preprocessing the config and doing required s3_operations')
        self.hook = SageMakerHook(aws_conn_id=(self.aws_conn_id))
        self.hook.configure_s3_resources(self.config)
        self.parse_config_integers()
        self.expand_role()
        self.log.info('After preprocessing the config is:\n {}'.format(json.dumps((self.config), sort_keys=True, indent=4, separators=(',',
                                                                                                                                       ': '))))

    def execute(self, context):
        raise NotImplementedError('Please implement execute() in sub class!')