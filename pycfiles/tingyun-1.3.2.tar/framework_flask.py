# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/framework_flask.py
# Compiled at: 2016-08-01 02:23:59
"""Define this module for basic armory for flask

"""
import logging
from tingyun.armoury.trigger.wsgi_entrance import wsgi_application_wrapper
from tingyun.armoury.ammunition.function_tracker import wrap_function_trace
from tingyun.armoury.ammunition.flask_tracker import add_url_rule_wrapper, handle_exception_wrapper
from tingyun.armoury.ammunition.flask_tracker import wrap_register_error, wrap_func_with_request
from tingyun.logistics.basic_wrapper import wrap_function_wrapper
console = logging.getLogger(__name__)

def detect_wsgi_entrance(module):
    """
    :param module:
    :return:
    """
    version = 'xx'
    try:
        import flask
        version = getattr(flask, '__version__', 'xx')
    except Exception as _:
        pass

    wsgi_application_wrapper(module.Flask, '__call__', ('flask', version))


def detect_app_entrance(module):
    """
    :param module:
    :return:
    """
    wrap_function_wrapper(module.Flask, 'add_url_rule', add_url_rule_wrapper)
    wrap_function_wrapper(module.Flask, 'handle_exception', handle_exception_wrapper)
    if hasattr(module.Flask, 'handle_user_exception'):
        wrap_function_wrapper(module.Flask, 'handle_user_exception', handle_exception_wrapper)
    if hasattr(module.Flask, 'full_dispatch_request'):
        wrap_function_trace(module.Flask, 'full_dispatch_request')
    if hasattr(module.Flask, '_register_error_handler'):
        wrap_function_wrapper(module.Flask, '_register_error_handler', wrap_register_error)
    if hasattr(module.Flask, 'before_first_request'):
        wrap_function_wrapper(module.Flask, 'before_first_request', wrap_func_with_request)
    if hasattr(module.Flask, 'before_request'):
        wrap_function_wrapper(module.Flask, 'before_request', wrap_func_with_request)
    if hasattr(module.Flask, 'after_request'):
        wrap_function_wrapper(module.Flask, 'after_request', wrap_func_with_request)
    if hasattr(module.Flask, 'teardown_request'):
        wrap_function_wrapper(module.Flask, 'teardown_request', wrap_func_with_request)


def detect_app_blueprint_entrance(module):
    if hasattr(module.Blueprint, 'before_request'):
        console.info('before blure print request.')
        wrap_function_wrapper(module.Blueprint, 'before_request', wrap_func_with_request)
    if hasattr(module.Blueprint, 'before_app_request'):
        wrap_function_wrapper(module.Blueprint, 'before_app_request', wrap_func_with_request)
    if hasattr(module.Blueprint, 'before_app_first_request'):
        wrap_function_wrapper(module.Blueprint, 'before_app_first_request', wrap_func_with_request)
    if hasattr(module.Blueprint, 'after_request'):
        wrap_function_wrapper(module.Blueprint, 'after_request', wrap_func_with_request)
    if hasattr(module.Blueprint, 'after_app_request'):
        wrap_function_wrapper(module.Blueprint, 'after_app_request', wrap_func_with_request)
    if hasattr(module.Blueprint, 'teardown_request'):
        wrap_function_wrapper(module.Blueprint, 'teardown_request', wrap_func_with_request)
    if hasattr(module.Blueprint, 'teardown_app_request'):
        wrap_function_wrapper(module.Blueprint, 'teardown_app_request', wrap_func_with_request)


def detect_templates(module):
    """
    :param module:
    :return:
    """
    wrap_function_trace(module, '_render')