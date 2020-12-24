# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/cli.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4145 bytes
"""
Utilities module for cli
"""
from __future__ import absolute_import
import functools, getpass, json, socket, sys
from argparse import Namespace
from datetime import datetime
from airflow.models import Log
from airflow.utils import cli_action_loggers

def action_logging(f):
    """
    Decorates function to execute function at the same time submitting action_logging
    but in CLI context. It will call action logger callbacks twice,
    one for pre-execution and the other one for post-execution.

    Action logger will be called with below keyword parameters:
        sub_command : name of sub-command
        start_datetime : start datetime instance by utc
        end_datetime : end datetime instance by utc
        full_command : full command line arguments
        user : current user
        log : airflow.models.log.Log ORM instance
        dag_id : dag id (optional)
        task_id : task_id (optional)
        execution_date : execution date (optional)
        error : exception instance if there's an exception

    :param f: function instance
    :return: wrapped function
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        if not args:
            raise AssertionError
        elif not isinstance(args[0], Namespace):
            raise AssertionError('1st positional argument should be argparse.Namespace instance, but {}'.format(args[0]))
        metrics = _build_metrics(f.__name__, args[0])
        (cli_action_loggers.on_pre_execution)(**metrics)
        try:
            try:
                return f(*args, **kwargs)
            except Exception as e:
                metrics['error'] = e
                raise

        finally:
            metrics['end_datetime'] = datetime.utcnow()
            (cli_action_loggers.on_post_execution)(**metrics)

    return wrapper


def _build_metrics(func_name, namespace):
    """
    Builds metrics dict from function args
    It assumes that function arguments is from airflow.bin.cli module's function
    and has Namespace instance where it optionally contains "dag_id", "task_id",
    and "execution_date".

    :param func_name: name of function
    :param namespace: Namespace instance from argparse
    :return: dict with metrics
    """
    metrics = {'sub_command':func_name, 
     'start_datetime':datetime.utcnow(),  'full_command':'{}'.format(list(sys.argv)), 
     'user':getpass.getuser()}
    assert isinstance(namespace, Namespace)
    tmp_dic = vars(namespace)
    metrics['dag_id'] = tmp_dic.get('dag_id')
    metrics['task_id'] = tmp_dic.get('task_id')
    metrics['execution_date'] = tmp_dic.get('execution_date')
    metrics['host_name'] = socket.gethostname()
    extra = json.dumps(dict((k, metrics[k]) for k in ('host_name', 'full_command')))
    log = Log(event=('cli_{}'.format(func_name)),
      task_instance=None,
      owner=(metrics['user']),
      extra=extra,
      task_id=(metrics.get('task_id')),
      dag_id=(metrics.get('dag_id')),
      execution_date=(metrics.get('execution_date')))
    metrics['log'] = log
    return metrics