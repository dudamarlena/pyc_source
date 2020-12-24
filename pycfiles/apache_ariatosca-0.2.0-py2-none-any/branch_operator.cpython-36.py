# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/branch_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2027 bytes
__doc__ = 'Branching operators'
from typing import Union, Iterable, Dict
from airflow.models import BaseOperator, SkipMixin

class BaseBranchOperator(BaseOperator, SkipMixin):
    """BaseBranchOperator"""

    def choose_branch(self, context):
        """
        Subclasses should implement this, running whatever logic is
        necessary to choose a branch and returning a task_id or list of
        task_ids.

        :param context: Context dictionary as passed to execute()
        :type context: dict
        """
        raise NotImplementedError

    def execute(self, context):
        self.skip_all_except(context['ti'], self.choose_branch(context))