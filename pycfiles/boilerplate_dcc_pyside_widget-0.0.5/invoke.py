# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python27\Lib\site-packages\pysideuic\port_v2\invoke.py
# Compiled at: 2014-04-24 00:47:04
from pysideuic.exceptions import NoSuchWidgetError

def invoke(driver):
    """ Invoke the given command line driver.  Return the exit status to be
    passed back to the parent process.
    """
    exit_status = 1
    try:
        exit_status = driver.invoke()
    except IOError as e:
        driver.on_IOError(e)
    except SyntaxError as e:
        driver.on_SyntaxError(e)
    except NoSuchWidgetError as e:
        driver.on_NoSuchWidgetError(e)
    except Exception as e:
        driver.on_Exception(e)

    return exit_status