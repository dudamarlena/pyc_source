# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sagemaker_base_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3346 bytes
import json
from typing import Iterable
from airflow.contrib.hooks.sagemaker_hook import SageMakerHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SageMakerBaseOperator(BaseOperator):
    """SageMakerBaseOperator"""
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