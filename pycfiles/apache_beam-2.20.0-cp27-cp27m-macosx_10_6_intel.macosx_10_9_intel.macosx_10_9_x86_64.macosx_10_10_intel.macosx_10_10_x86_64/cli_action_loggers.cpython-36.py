# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/cli_action_loggers.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3753 bytes
__doc__ = '\nAn Action Logger module. Singleton pattern has been applied into this module\nso that registered callbacks can be used all through the same python process.\n'
from __future__ import absolute_import
import logging
from typing import List, Callable
from airflow.utils.db import create_session

def register_pre_exec_callback(action_logger):
    """
    Registers more action_logger function callback for pre-execution.
    This function callback is expected to be called with keyword args.
    For more about the arguments that is being passed to the callback,
    refer to airflow.utils.cli.action_logging()
    :param action_logger: An action logger function
    :return: None
    """
    logging.debug('Adding %s to pre execution callback', action_logger)
    __pre_exec_callbacks.append(action_logger)


def register_post_exec_callback(action_logger):
    """
    Registers more action_logger function callback for post-execution.
    This function callback is expected to be called with keyword args.
    For more about the arguments that is being passed to the callback,
    refer to airflow.utils.cli.action_logging()
    :param action_logger: An action logger function
    :return: None
    """
    logging.debug('Adding %s to post execution callback', action_logger)
    __post_exec_callbacks.append(action_logger)


def on_pre_execution(**kwargs):
    """
    Calls callbacks before execution.
    Note that any exception from callback will be logged but won't be propagated.
    :param kwargs:
    :return: None
    """
    logging.debug('Calling callbacks: %s', __pre_exec_callbacks)
    for cb in __pre_exec_callbacks:
        try:
            cb(**kwargs)
        except Exception:
            logging.exception('Failed on pre-execution callback using %s', cb)


def on_post_execution(**kwargs):
    """
    Calls callbacks after execution.
    As it's being called after execution, it can capture status of execution,
    duration, etc. Note that any exception from callback will be logged but
    won't be propagated.
    :param kwargs:
    :return: None
    """
    logging.debug('Calling callbacks: %s', __post_exec_callbacks)
    for cb in __post_exec_callbacks:
        try:
            cb(**kwargs)
        except Exception:
            logging.exception('Failed on post-execution callback using %s', cb)


def default_action_log(log, **_):
    """
    A default action logger callback that behave same as www.utils.action_logging
    which uses global session and pushes log ORM object.
    :param log: An log ORM instance
    :param **_: other keyword arguments that is not being used by this function
    :return: None
    """
    with create_session() as (session):
        session.add(log)


__pre_exec_callbacks = []
__post_exec_callbacks = []
register_pre_exec_callback(default_action_log)