# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/operators/branch_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2027 bytes
"""Branching operators"""
from typing import Union, Iterable, Dict
from airflow.models import BaseOperator, SkipMixin

class BaseBranchOperator(BaseOperator, SkipMixin):
    __doc__ = '\n    This is a base class for creating operators with branching functionality,\n    similarly to BranchPythonOperator.\n\n    Users should subclass this operator and implement the function\n    `choose_branch(self, context)`. This should run whatever business logic\n    is needed to determine the branch, and return either the task_id for\n    a single task (as a str) or a list of task_ids.\n\n    The operator will continue with the returned task_id(s), and all other\n    tasks directly downstream of this operator will be skipped.\n    '

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