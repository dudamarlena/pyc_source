# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mukulhase/Dev/github/webwhatsapp-scripts/webwhatsapi/wapi_js_wrapper.py
# Compiled at: 2018-05-27 06:05:33
# Size of source mod 2**32: 3001 bytes
import os
from selenium.common.exceptions import WebDriverException
from six import string_types

class JsException(Exception):

    def __init__(self, message=None):
        super(Exception, self).__init__(message)


class WapiJsWrapper(object):
    __doc__ = '\n    Wraps JS functions in window.WAPI for easier use from python\n    '

    def __init__(self, driver):
        self.driver = driver

    def __getattr__(self, item):
        """
        Finds functions in window.WAPI

        :param item: Function name
        :return: Callable function object
        :rtype: JsFunction
        """
        wapi_functions = dir(self)
        if item not in wapi_functions:
            raise AttributeError("Function {0} doesn't exist".format(item))
        return JsFunction(item, self.driver)

    def __dir__(self):
        """
        Reloads wapi.js and returns its functions

        :return: List of functions in window.WAPI
        """
        try:
            script_path = os.path.dirname(os.path.abspath(__file__))
        except NameError:
            script_path = os.getcwd()

        with open(os.path.join(script_path, 'js', 'wapi.js'), 'r') as (script):
            self.driver.execute_script(script.read())
        result = self.driver.execute_script('return window.WAPI')
        if result:
            return result.keys()
        else:
            return []


class JsArg(object):
    __doc__ = '\n    Represents a JS function argument\n    '

    def __init__(self, obj):
        """
        Constructor

        :param obj: Python object to represent
        """
        self.obj = obj

    def __str__(self):
        """
        Casts self.obj from python type to valid JS literal

        :return: JS literal represented in a string
        """
        if isinstance(self.obj, string_types):
            return repr(str(self.obj))
        else:
            if isinstance(self.obj, bool):
                return str(self.obj).lower()
            return str(self.obj)


class JsFunction(object):
    __doc__ = '\n    Callable object represents functions in window.WAPI\n    '

    def __init__(self, function_name, driver):
        self.driver = driver
        self.function_name = function_name

    def __call__(self, *args, **kwargs):
        if len(args):
            command = 'return WAPI.{0}({1}, arguments[0])'.format(self.function_name, ','.join([str(JsArg(arg)) for arg in args]))
        else:
            command = 'return WAPI.{0}(arguments[0])'.format(self.function_name)
        try:
            return self.driver.execute_async_script(command)
        except WebDriverException as e:
            if e.msg == 'Timed out':
                raise Exception('Phone not connected to Internet')
            raise JsException('Error in function {0} ({1}). Command: {2}'.format(self.function_name, e.msg, command))