# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/dummy_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 1238 bytes
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class DummyOperator(BaseOperator):
    __doc__ = '\n    Operator that does literally nothing. It can be used to group tasks in a\n    DAG.\n    '
    ui_color = '#e8f7e4'

    @apply_defaults
    def __init__(self, *args, **kwargs):
        (super(DummyOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        pass