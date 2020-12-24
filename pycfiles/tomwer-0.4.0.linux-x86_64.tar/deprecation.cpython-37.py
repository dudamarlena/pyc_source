# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/utils/deprecation.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 4758 bytes
"""Bunch of useful decorators"""
__authors__ = [
 'Jerome Kieffer', 'H. Payno', 'P. Knobel']
__license__ = 'MIT'
__date__ = '26/02/2018'
import sys, logging, functools, traceback
depreclog = logging.getLogger('silx.DEPRECATION')
deprecache = set([])

def deprecated(func=None, reason=None, replacement=None, since_version=None, only_once=True, skip_backtrace_count=1):
    """
    Decorator that deprecates the use of a function

    :param str reason: Reason for deprecating this function
        (e.g. "feature no longer provided",
    :param str replacement: Name of replacement function (if the reason for
        deprecating was to rename the function)
    :param str since_version: First *silx* version for which the function was
        deprecated (e.g. "0.5.0").
    :param bool only_once: If true, the deprecation warning will only be
        generated one time. Default is true.
    :param int skip_backtrace_count: Amount of last backtrace to ignore when
        logging the backtrace
    """

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            name = func.func_name if sys.version_info[0] < 3 else func.__name__
            deprecated_warning(type_='Function', name=name,
              reason=reason,
              replacement=replacement,
              since_version=since_version,
              only_once=only_once,
              skip_backtrace_count=skip_backtrace_count)
            return func(*args, **kwargs)

        return wrapper

    if func is not None:
        return decorator(func)
    return decorator


def deprecated_warning(type_, name, reason=None, replacement=None, since_version=None, only_once=True, skip_backtrace_count=0):
    """
    Function to log a deprecation warning

    :param str type_: Nature of the object to be deprecated:
        "Module", "Function", "Class" ...
    :param name: Object name.
    :param str reason: Reason for deprecating this function
        (e.g. "feature no longer provided",
    :param str replacement: Name of replacement function (if the reason for
        deprecating was to rename the function)
    :param str since_version: First *silx* version for which the function was
        deprecated (e.g. "0.5.0").
    :param bool only_once: If true, the deprecation warning will only be
        generated one time for each different call locations. Default is true.
    :param int skip_backtrace_count: Amount of last backtrace to ignore when
        logging the backtrace
    """
    if not depreclog.isEnabledFor(logging.WARNING):
        return
    msg = '%s %s is deprecated'
    if since_version is not None:
        msg += ' since silx version %s' % since_version
    msg += '.'
    if reason is not None:
        msg += ' Reason: %s.' % reason
    if replacement is not None:
        msg += " Use '%s' instead." % replacement
    msg += '\n%s'
    limit = 2 + skip_backtrace_count
    backtrace = ''.join(traceback.format_stack(limit=limit)[0])
    backtrace = backtrace.rstrip()
    if only_once:
        data = (
         msg, type_, name, backtrace)
        if data in deprecache:
            return
        deprecache.add(data)
    depreclog.warning(msg, type_, name, backtrace)