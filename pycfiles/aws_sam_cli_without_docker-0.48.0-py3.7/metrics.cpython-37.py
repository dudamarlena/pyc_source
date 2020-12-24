# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/telemetry/metrics.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 3821 bytes
"""
Provides methods to generate and send metrics
"""
import platform, logging
from timeit import default_timer
from samcli.cli.context import Context
from samcli.commands.exceptions import UserException
from samcli.cli.global_config import GlobalConfig
from .telemetry import Telemetry
LOG = logging.getLogger(__name__)

def send_installed_metric():
    LOG.debug('Sending Installed Metric')
    telemetry = Telemetry()
    telemetry.emit('installed', {'osPlatform':platform.system(),  'telemetryEnabled':_telemetry_enabled()})


def track_command(func):
    """
    Decorator to track execution of a command. This method executes the function, gathers all relevant metrics,
    reports the metrics and returns.

    If you have a Click command, you can track as follows:

    .. code:: python
        @click.command(...)
        @click.options(...)
        @track_command
        def hello_command():
            print('hello')

    """

    def wrapped(*args, **kwargs):
        if not _telemetry_enabled():
            return func(*args, **kwargs)
        telemetry = Telemetry()
        exception = None
        return_value = None
        exit_reason = 'success'
        exit_code = 0
        duration_fn = _timer()
        try:
            return_value = func(*args, **kwargs)
        except UserException as ex:
            try:
                exception = ex
                exit_code = ex.exit_code
                if ex.wrapped_from is None:
                    exit_reason = type(ex).__name__
                else:
                    exit_reason = ex.wrapped_from
            finally:
                ex = None
                del ex

        except Exception as ex:
            try:
                exception = ex
                exit_code = 255
                exit_reason = type(ex).__name__
            finally:
                ex = None
                del ex

        ctx = Context.get_current_context()
        telemetry.emit('commandRun', {'awsProfileProvided':bool(ctx.profile), 
         'debugFlagProvided':bool(ctx.debug), 
         'region':ctx.region or '', 
         'commandName':ctx.command_path, 
         'duration':duration_fn(), 
         'exitReason':exit_reason, 
         'exitCode':exit_code})
        if exception:
            raise exception
        return return_value

    return wrapped


def _timer():
    """
    Timer to measure the elapsed time between two calls in milliseconds. When you first call this method,
    we will automatically start the timer. The return value is another method that, when called, will end the timer
    and return the duration between the two calls.

    ..code:
    >>> import time
    >>> duration_fn = _timer()
    >>> time.sleep(5)  # Say, you sleep for 5 seconds in between calls
    >>> duration_ms = duration_fn()
    >>> print(duration_ms)
        5010

    Returns
    -------
    function
        Call this method to end the timer and return duration in milliseconds

    """
    start = default_timer()

    def end():
        return int(max(default_timer() - start, 0) * 1000)

    return end


def _telemetry_enabled():
    gc = GlobalConfig()
    return bool(gc.telemetry_enabled)