# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/collect_exceptions/contrib/django/models.py
# Compiled at: 2015-02-08 22:12:01
import sys, logging
log = logging.getLogger('django')
import traceback
from django.conf import settings as django_settings

def default_exception_collector(exception_str):
    log.error(exception_str)


def my_exception_handler(request, **kwargs):
    try:
        log.debug(dir(request))
        request_info = '%s %s%s\n' % (
         request.method,
         request.get_host(),
         request.get_full_path())
        if request.body:
            request_info = request_info + request.body + '\n'
        type_, value, tb = sys.exc_info()
        exc_info = traceback.format_exception(type_, value, tb)
        einfo = ('').join(exc_info)
        einfo = request_info + einfo
        log.warning(einfo)
        django_settings.COLLECT_EXCEPTIONS_CONFIG['exception_collector'](einfo)
    except Exception as e:
        log.warning(e)


def register_handlers():
    from django.core.signals import got_request_exception
    got_request_exception.connect(my_exception_handler, weak=False)
    log.info('If Celery is installed, register a signal handler')
    if 'djcelery' in django_settings.INSTALLED_APPS:
        try:
            from collect_exceptions.contrib.celery import register_signal
        except ImportError:
            log.warning('Failed to install Celery error handler')
        else:
            try:
                register_signal()
            except Exception:
                log.warning('Failed to install Celery error handler')


def is_config_ok():
    if not getattr(django_settings, 'COLLECT_EXCEPTIONS_CONFIG', None):
        log.warning('no COLLECT_EXCEPTIONS_CONFIG in settings return False')
        return False
    else:
        if not django_settings.COLLECT_EXCEPTIONS_CONFIG.get('EXCEPTION_COLLECTOR', None):
            log.warning('no EXCEPTION_COLLECTOR in COLLECT_EXCEPTIONS_CONFIG return False')
            return False
        return True


def get_mod_func(callback):
    try:
        dot = callback.rindex('.')
    except ValueError:
        return (
         callback, '')

    return (
     callback[:dot], callback[dot + 1:])


def import_module(name):
    log.debug('import_module name = %s' % name)
    __import__(name)
    return sys.modules[name]


def handle_config():
    EXCEPTION_COLLECTOR = django_settings.COLLECT_EXCEPTIONS_CONFIG['EXCEPTION_COLLECTOR']
    mod_name, func_name = get_mod_func(EXCEPTION_COLLECTOR)
    log.info('mod_name = %s  func_name = %s' % (mod_name, func_name))
    try:
        mod = import_module(mod_name)
    except Exception as e:
        log.warning(e)
        log.warning('import_module except return False')
        return False

    try:
        lookup_func = getattr(mod, func_name)
        if not callable(lookup_func):
            log.error('Could not import %s.%s. Func is not callable.' % (
             mod_name, func_name))
            return False
        django_settings.COLLECT_EXCEPTIONS_CONFIG['exception_collector'] = lookup_func
    except AttributeError:
        log.error('Could not import %s.%s. Func is not callable.' % (
         mod_name, func_name))
        return False

    log.info('handle_config return True')
    return True


if is_config_ok():
    ret = handle_config()
    if not ret:
        log.error('collect exceptions package config wrong')
        log.error('check your settings')
else:
    if not getattr(django_settings, 'COLLECT_EXCEPTIONS_CONFIG', None):
        django_settings.COLLECT_EXCEPTIONS_CONFIG = {}
    django_settings.COLLECT_EXCEPTIONS_CONFIG['exception_collector'] = default_exception_collector
register_handlers()