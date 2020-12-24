# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/roboticslanguage/RoboticsLanguage/RoboticsLanguage/Tools/Exceptions.py
# Compiled at: 2019-09-27 03:30:17
import re, sys
from contextlib import contextmanager

class ReturnException(Exception):
    pass


@contextmanager
def tryToProceed():
    """
  Attempts to proceed when there is an exception. This function is coupled
  with the action 'return' of the exception function. For example:

  from RoboticsLanguage.Tools import Exceptions

  def run_function():
    with Exceptions.exception('test'):
      a = 'a' + 1

    print 'reaches this point'

    with Exceptions.exception('test', action='return'):
      raise Exception('test')

    print 'does not reach this point'

  with Exceptions.tryToProceed():
    run_function()
    print 'does not reach this point'
  print 'reaches this point'

  """
    try:
        yield
    except Exception as e:
        if type(e).__name__ == 'ReturnException':
            pass
        else:
            raise e


@contextmanager
def exception(key='default', code=None, parameters={}, **options):
    """
  Generic exception function used in a 'with' context. Can be used fos system/libraries exceptions,
  or to generate own exceptions. Usage:

  # system error
  with Exceptions.exception('test'):
    a = 'a' + 1

  # forced error
  with Exceptions.exception('forced', action='stop'):
    raise Exception('name')
  """
    try:
        yield
    except Exception as e:
        level = options['level'] if 'level' in options.keys() else 'error'
        action = options['action'] if 'action' in options.keys() else None
        try:
            emitter = re.search("<.*'([^']*)'>", str(type(e))).group(1)
        except:
            emitter = 'unknown'

        showExceptionMessage(emitter, key, e, level, action)
        if action == 'stop':
            sys.exit(1)
        elif action == 'return':
            raise ReturnException

    return


def showExceptionMessage(emitter, key, exception, level, action):
    print 'emitter: ' + emitter
    print 'key: ' + key
    print 'exception: ' + str(exception)
    print 'level: ' + level
    print 'action: ' + str(action)


def raiseException(group, key, code=None, parameters={}):
    with exception(group, code, parameters):
        raise Exception(key)