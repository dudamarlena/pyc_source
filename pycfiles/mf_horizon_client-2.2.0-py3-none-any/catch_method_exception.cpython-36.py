# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stanley/IdeaProjects/horizon-python-client/src/mf_horizon_client/utils/catch_method_exception.py
# Compiled at: 2020-05-09 07:13:20
# Size of source mod 2**32: 704 bytes
import functools
from mf_horizon_client.client.error import HorizonError
from mf_horizon_client.utils.terminal_messages import print_failure, print_server_error_details

def catch_errors(f):
    """
    Catches a class-method exception - to be used as a decorator
    """

    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except HorizonError as exception:
            print_failure(f"{str.upper(f.__name__)} request failed to successfully execute. {exception.status_code if exception else None}")
            if exception:
                if exception.message:
                    print_server_error_details(exception.message)

    return func