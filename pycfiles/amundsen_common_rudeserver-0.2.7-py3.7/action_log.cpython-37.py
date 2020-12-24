# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/amundsen_common/log/action_log.py
# Compiled at: 2020-02-13 16:36:56
# Size of source mod 2**32: 2910 bytes
import functools, json, logging, socket
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Callable
from flask import current_app as flask_app
from amundsen_common.log import action_log_callback
from amundsen_common.log.action_log_model import ActionLogParams
LOGGER = logging.getLogger(__name__)
EPOCH = datetime(1970, 1, 1, tzinfo=(timezone.utc))
CALLER_RETRIEVAL_INSTANCE_KEY = 'CALLER_RETRIEVAL_INSTANCE'

def action_logging(f: Callable[(..., Any)]) -> Any:
    """
    Decorates function to execute function at the same time triggering action logger callbacks.
    It will call action logger callbacks twice, one for pre-execution and the other one for post-execution.
    Action logger will be called with ActionLogParams

    :param f: function instance
    :return: wrapped function
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        """
        An wrapper for api functions. It creates ActionLogParams based on the function name, positional arguments,
        and keyword arguments.

        :param args: A passthrough positional arguments.
        :param kwargs: A passthrough keyword argument
        """
        metrics = _build_metrics(f.__name__, *args, **kwargs)
        action_log_callback.on_pre_execution(ActionLogParams(**metrics))
        output = None
        try:
            try:
                output = f(*args, **kwargs)
                return output
            except Exception as e:
                try:
                    metrics['error'] = e
                    raise
                finally:
                    e = None
                    del e

        finally:
            metrics['end_epoch_ms'] = get_epoch_millisec()
            try:
                metrics['output'] = json.dumps(output)
            except Exception:
                metrics['output'] = output

            action_log_callback.on_post_execution(ActionLogParams(**metrics))

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug('action has been logged')
    return wrapper


def get_epoch_millisec() -> int:
    return (datetime.now(timezone.utc) - EPOCH) // timedelta(milliseconds=1)


def _build_metrics(func_name: str, *args: Any, **kwargs: Any) -> Dict[(str, Any)]:
    """
    Builds metrics dict from function args
    :param func_name:
    :param args:
    :param kwargs:
    :return: Dict that matches ActionLogParams variable
    """
    metrics = {'command':kwargs.get('command', func_name), 
     'start_epoch_ms':get_epoch_millisec(), 
     'host_name':socket.gethostname(), 
     'pos_args_json':json.dumps(args), 
     'keyword_args_json':json.dumps(kwargs)}
    caller_retriever = flask_app.config.get(CALLER_RETRIEVAL_INSTANCE_KEY, '')
    if caller_retriever:
        metrics['user'] = caller_retriever.get_caller()
    else:
        metrics['user'] = 'UNKNOWN'
    return metrics