# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/crwy/utils/logger.py
# Compiled at: 2020-02-03 23:11:43
import os, sys, logging, logging.config, logging.handlers
from crwy.exceptions import CrwyException
from crwy.settings.default_settings import TEMPLATE_DIR
try:
    import ConfigParser as configparser
except ImportError:
    import configparser

DEFAULT_LOGGER_CONF = './conf/logger.conf'
if sys.version_info[0] == 2:
    BASE_LOGGER_CONF = os.path.join(TEMPLATE_DIR, 'project/logger_py2.conf.tmpl')
else:
    BASE_LOGGER_CONF = os.path.join(TEMPLATE_DIR, 'project/logger_py3.conf.tmpl')
try:
    try:
        logging.config.fileConfig(DEFAULT_LOGGER_CONF)
    except KeyError:
        logging.config.fileConfig(BASE_LOGGER_CONF)

except:
    pass

def _install_handlers_custom(cp, formatters, log_path):
    """Install and return handlers"""
    hlist = cp.get('handlers', 'keys')
    if not len(hlist):
        return {}
    hlist = hlist.split(',')
    hlist = logging.config._strip_spaces(hlist)
    handlers = {}
    fixups = []
    for hand in hlist:
        sectname = 'handler_%s' % hand
        klass = cp.get(sectname, 'class')
        opts = cp.options(sectname)
        if 'formatter' in opts:
            fmt = cp.get(sectname, 'formatter')
        else:
            fmt = ''
        try:
            klass = eval(klass, vars(logging))
        except (AttributeError, NameError):
            klass = logging.config._resolve(klass)

        args = cp.get(sectname, 'args')
        args = eval(args, vars(logging))
        if isinstance(args[0], str):
            args = tuple([log_path] + list(args)[1:])
        h = klass(*args)
        if 'level' in opts:
            level = cp.get(sectname, 'level')
            try:
                h.setLevel(logging._levelNames[level])
            except AttributeError:
                h.setLevel(logging._nameToLevel[level])

        if len(fmt):
            h.setFormatter(formatters[fmt])
        if issubclass(klass, logging.handlers.MemoryHandler):
            if 'target' in opts:
                target = cp.get(sectname, 'target')
            else:
                target = ''
            if len(target):
                fixups.append((h, target))
        handlers[hand] = h

    for h, t in fixups:
        h.setTarget(handlers[t])

    return handlers


def fileConfigWithLogPath(fname=BASE_LOGGER_CONF, log_path=None, defaults=None, disable_existing_loggers=True):
    u"""
    通过拦截重写handler的方式传入log_path，实现日志位置修改
    """
    if not log_path:
        raise CrwyException('Please setup <log_path> first!')
    cp = configparser.ConfigParser(defaults)
    if hasattr(fname, 'readline'):
        cp.read_file(fname)
    else:
        cp.read(fname)
    try:
        formatters = logging.config._create_formatters(cp)
    except configparser.NoSectionError:
        raise CrwyException('Please make sure fname: "%s" is exist.' % fname)

    logging._acquireLock()
    try:
        logging._handlers.clear()
        del logging._handlerList[:]
        handlers = _install_handlers_custom(cp, formatters, log_path)
        logging.config._install_loggers(cp, handlers, disable_existing_loggers)
    finally:
        logging._releaseLock()


class Logger(object):

    @staticmethod
    def file_logger():
        return logging.getLogger('fileLogger')

    @staticmethod
    def rt_logger():
        return logging.getLogger('rtLogger')

    @staticmethod
    def timed_rt_logger():
        return logging.getLogger('timedRtLogger')

    @staticmethod
    def extra_logger(name=None):
        return logging.getLogger(name)