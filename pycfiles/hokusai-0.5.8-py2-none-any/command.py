# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/lib/command.py
# Compiled at: 2020-04-09 11:50:23
import os, sys, traceback
from functools import wraps
from hokusai.lib.common import print_red, get_verbosity
from hokusai.lib.exceptions import CalledProcessError, HokusaiError
from hokusai.lib.config import config

def command(config_check=True):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if config_check:
                    config.check()
                result = func(*args, **kwargs)
                if result is None:
                    sys.exit(0)
                else:
                    sys.exit(result)
            except HokusaiError as e:
                print_red(e.message)
                sys.exit(e.return_code)
            except SystemExit:
                raise
            except KeyboardInterrupt:
                raise
            except (CalledProcessError, Exception) as e:
                if get_verbosity() or os.environ.get('DEBUG'):
                    print_red(traceback.format_exc(e))
                else:
                    print_red('ERROR: %s' % str(e))
                sys.exit(1)

            return

        return wrapper

    return decorator