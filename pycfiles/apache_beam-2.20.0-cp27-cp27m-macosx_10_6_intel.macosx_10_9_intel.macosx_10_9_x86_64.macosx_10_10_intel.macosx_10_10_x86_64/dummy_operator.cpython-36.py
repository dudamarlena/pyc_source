# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/dummy_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1238 bytes
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DummyOperator(BaseOperator):
    """DummyOperator"""
    ui_color = '#e8f7e4'

    @apply_defaults
    def __init__(self, *args, **kwargs):
        (super(DummyOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        pass