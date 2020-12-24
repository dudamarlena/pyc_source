# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cw12401/code/work/ampal/src/ampal/ampal_warnings.py
# Compiled at: 2018-04-06 09:04:04
# Size of source mod 2**32: 1270 bytes
from functools import wraps
import warnings

def check_availability(program, test_func, global_settings):

    def function_grabber(f):

        @wraps(f)
        def function_with_check(*args, **kwargs):
            if program in global_settings:
                if 'available' not in global_settings[program]:
                    global_settings[program]['available'] = test_func()
                if global_settings[program]['available']:
                    return f(*args, **kwargs)
            warning_string = '{0} not found, side chains have not been packed.\nCheck that the path to the {0} binary in `.isambard_settings` is correct.\nYou might want to try rerunning `configure.py`'.format(program)
            warnings.warn(warning_string, DependencyNotFoundWarning)

        return function_with_check

    return function_grabber


class NoncanonicalWarning(RuntimeWarning):
    pass


class NotParameterisedWarning(RuntimeWarning):
    pass


class MalformedPDBWarning(RuntimeWarning):
    pass


class DependencyNotFoundWarning(RuntimeWarning):
    pass


warnings.simplefilter('always', DependencyNotFoundWarning)
warnings.simplefilter('once', PendingDeprecationWarning)