# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/dag/base_dag.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2812 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from abc import ABCMeta, abstractmethod, abstractproperty

class BaseDag(object):
    """BaseDag"""
    __metaclass__ = ABCMeta

    @abstractproperty
    def dag_id(self):
        """
        :return: the DAG ID
        :rtype: unicode
        """
        raise NotImplementedError()

    @abstractproperty
    def task_ids(self):
        """
        :return: A list of task IDs that are in this DAG
        :rtype: List[unicode]
        """
        raise NotImplementedError()

    @abstractproperty
    def full_filepath(self):
        """
        :return: The absolute path to the file that contains this DAG's definition
        :rtype: unicode
        """
        raise NotImplementedError()

    @abstractmethod
    def concurrency(self):
        """
        :return: maximum number of tasks that can run simultaneously from this DAG
        :rtype: int
        """
        raise NotImplementedError()

    @abstractmethod
    def is_paused(self):
        """
        :return: whether this DAG is paused or not
        :rtype: bool
        """
        raise NotImplementedError()

    @abstractmethod
    def pickle_id(self):
        """
        :return: The pickle ID for this DAG, if it has one. Otherwise None.
        :rtype: unicode
        """
        raise NotImplementedError


class BaseDagBag(object):
    """BaseDagBag"""

    @abstractproperty
    def dag_ids(self):
        """
        :return: a list of DAG IDs in this bag
        :rtype: List[unicode]
        """
        raise NotImplementedError()

    @abstractmethod
    def get_dag(self, dag_id):
        """
        :return: whether the task exists in this bag
        :rtype: airflow.dag.base_dag.BaseDag
        """
        raise NotImplementedError()