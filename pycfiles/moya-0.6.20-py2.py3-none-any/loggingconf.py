# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/loggingconf.py
# Compiled at: 2016-12-08 16:29:22
from __future__ import print_function
from __future__ import unicode_literals
import io
from os.path import abspath, join, dirname, normpath
import logging
from logging import handlers
import fs.path
from fs.errors import FSError
from . import iniparse
from . import errors
MemoryHandler = handlers.MemoryHandler
log = logging.getLogger(b'moya.startup')
DEFAULT_LOGGING = b'\n\n[logger:root]\nhandlers=moyaconsole\n\n[logger:moya]\nlevel=DEBUG\n\n[logger:moya.startup]\n\n[logger:moya.signal]\n\n[logger:sqlalchemy.engine]\nhandlers=moyaconsole\nlevel=WARN\npropagate=no\n\n[handler:moyaconsole]\nclass=moya.logtools.MoyaConsoleHandler\nformatter=simple\nargs=(sys.stdout,)\n\n[handler:stdout]\nclass=StreamHandler\nformatter=simple\nargs=(sys.stdout,)\n\n[formatter:simple]\nformat=%(asctime)s:%(name)s:%(levelname)s: %(message)s\ndatefmt=[%d/%b/%Y %H:%M:%S]\n\n'

def _resolve(name):
    """Resolve a dotted name to a global object."""
    name = name.split(b'.')
    used = name.pop(0)
    found = __import__(used)
    for n in name:
        used = used + b'.' + n
        try:
            found = getattr(found, n)
        except AttributeError:
            __import__(used)
            found = getattr(found, n)

    return found


_logging_level_names = {0: b'NOTSET', 10: b'DEBUG', 
   20: b'INFO', 
   30: b'WARNING', 
   40: b'ERROR', 
   50: b'CRITICAL', 
   b'NOTSET': 0, 
   b'DEBUG': 10, 
   b'INFO': 20, 
   b'WARN': 30, 
   b'WARNING': 30, 
   b'ERROR': 40, 
   b'CRITICAL': 50}

def init_logging_fs(logging_fs, path, disable_existing_loggers=True, use_default=True):
    ini_path = path
    ini_stack = []
    parsed_default = False
    while 1:
        try:
            with logging_fs.open(path, b'rt') as (ini_file):
                s = iniparse.parse(ini_file)
        except FSError:
            if use_default:
                s = iniparse.parse(DEFAULT_LOGGING)
                parsed_default = True
            else:
                raise errors.LoggingSettingsError((b'unable to read logging settings file "{}" from {}').format(path, logging_fs.desc(b'/')))

        ini_stack.append(s)
        if b'extends' in s[b'']:
            path = fs.path.join(fs.path.dirname(path), s[b''][b'extends'])
        else:
            break

    _init_logging(ini_path, ini_stack, disable_existing_loggers)
    if parsed_default:
        log.warn(b'%s not found, using default logging', path)


def init_logging(path, disable_existing_loggers=True):
    """Sane logging.ini"""
    ini_path = path
    ini_stack = []
    visited = set()
    while 1:
        path = abspath(normpath(path))
        if path in visited:
            raise errors.LoggingSettingsError(b'recursive extends in logging ini')
        try:
            with io.open(path, b'rt') as (ini_file):
                s = iniparse.parse(ini_file)
            visited.add(path)
        except IOError:
            raise errors.LoggingSettingsError((b'unable to read logging settings file "{}"').format(path))

        ini_stack.append(s)
        if b'extends' in s[b'']:
            path = join(dirname(path), s[b''][b'extends'])
        else:
            break

    _init_logging(ini_path, ini_stack, disable_existing_loggers)


def _init_logging(path, ini_stack, disable_existing_loggers=True):
    ini_path = path
    ini_stack = ini_stack[::-1]
    ini = ini_stack[0]
    for extend_ini in ini_stack[1:]:
        for section_name, section in extend_ini.items():
            if section_name in ini:
                ini[section_name].update(section)
            else:
                ini[section_name] = section

    def get(section_name, key, default=Ellipsis):
        try:
            value = ini[section_name][key]
        except KeyError:
            if default is Ellipsis:
                raise errors.LoggingSettingsError((b'unable to initialize logging (required key [{}]/{} was not found in "{}")').format(section_name, key, ini_path))
            return default

        return value

    def getint(section_name, key, default=Ellipsis):
        value = get(section_name, key, default)
        if not value.isdigit():
            raise errors.LoggingSettingsError((b'unable to initialize logging (setting [{}]/{} should be an integer in "{path}")').format(section_name, key, ini_path))
        return int(value)

    def getbool(section_name, key, default=Ellipsis):
        value = get(section_name, key, default).strip().lower()
        if value in ('yes', 'true'):
            return True
        if value in ('no', 'false'):
            return False
        raise errors.LoggingSettingsError((b'unable to initialize logging (section [{}]/{} is not a valid boolean in "{path}"').format(section_name, key, ini_path))

    logging._acquireLock()
    try:
        _handlers = {}
        _formatters = {}
        _loggers = {}
        for section_name in ini:
            if not section_name:
                continue
            what, _, name = section_name.partition(b':')
            if what == b'handler':
                _handlers[name] = section_name
            elif what == b'formatter':
                _formatters[name] = section_name
            elif what == b'logger':
                _loggers[name] = section_name
            else:
                raise errors.LoggingSettingsError((b'unable to initialize logging (section [{}] is not valid in "{}")').format(section_name, ini_path))

        formatters = {}
        for formatter_name, section_name in _formatters.items():
            opts = ini[section_name]
            if b'format' in opts:
                fs = get(section_name, b'format')
            else:
                fs = None
            if b'datefmt' in opts:
                dfs = get(section_name, b'datefmt')
            else:
                dfs = None
            c = logging.Formatter
            if b'class' in opts:
                class_name = get(section_name, b'class')
                if class_name:
                    c = _resolve(class_name)
            f = c(fs, dfs)
            formatters[formatter_name] = f

        handlers = {}
        handlers[b'null'] = logging.NullHandler()
        fixups = []
        for handler_name, section_name in _handlers.items():
            klass = get(section_name, b'class')
            opts = ini[section_name]
            if b'formatter' in opts:
                fmt = get(section_name, b'formatter')
            else:
                fmt = b''
            try:
                kass = eval(klass, vars(logging))
            except (AttributeError, NameError):
                kass = _resolve(klass)

            args = get(section_name, b'args', b'()')
            try:
                args = eval(args, vars(logging))
            except Exception as e:
                raise errors.LoggingSettingsError((b"error parsing logger '{}' args {} ({})").format(kass, args, e))

            try:
                h = kass(*args)
            except Exception as e:
                raise errors.LoggingSettingsError((b"error constructing logger '{}' with args {!r} ({})").format(kass, args, e))

            if b'level' in opts:
                level = get(section_name, b'level')
                h.setLevel(_logging_level_names[level])
            if len(fmt):
                h.setFormatter(formatters[fmt])
            if issubclass(kass, MemoryHandler):
                if b'target' in opts:
                    target = get(section_name, b'target')
                else:
                    target = b''
                if len(target):
                    fixups.append((h, target))
            handlers[handler_name] = h

        for h, t in fixups:
            h.setTarget(handlers[t])

        if b'root' not in _loggers:
            raise errors.LoggingSettingsError((b'unable to initialize logging (section [logger:root] is missing from "{}")').format(ini_path))
        llist = list(_loggers.keys())
        llist.remove(b'root')
        root = logging.root
        log = root
        section_name = b'logger:root'
        opts = ini[section_name]
        if b'level' in opts:
            level = get(section_name, b'level')
            log.setLevel(_logging_level_names[level])
        for h in root.handlers[:]:
            root.removeHandler(h)

        if b'handlers' in opts:
            hlist = [ h.strip() for h in get(section_name, b'handlers', b'null').split(b',') ]
            for hand in hlist:
                try:
                    log.addHandler(handlers[hand])
                except KeyError:
                    raise errors.LoggingSettingsError((b'unable to initialize logging (handler \'{}\' not found in "{}")').format(hand, ini_path))

        existing = list(root.manager.loggerDict.keys())
        existing.sort()
        child_loggers = []
        for log in llist:
            section_name = (b'logger:{}').format(log)
            qn = get(section_name, b'qualname', log)
            opts = ini[section_name]
            if b'propagate' in opts:
                propagate = 1 if getbool(section_name, b'propagate') else 0
            else:
                propagate = 1
            logger = logging.getLogger(qn)
            if qn in existing:
                i = existing.index(qn) + 1
                prefixed = qn + b'.'
                pflen = len(prefixed)
                num_existing = len(existing)
                while i < num_existing:
                    if existing[i][:pflen] == prefixed:
                        child_loggers.append(existing[i])
                    i += 1

                existing.remove(qn)
            if b'level' in opts:
                level = get(section_name, b'level', b'NOTSET')
                if level not in _logging_level_names:
                    raise errors.LoggingSettingsError((b"unknown logging level '{}' in  [{}]").format(level, section_name))
                logger.setLevel(_logging_level_names[level])
            for h in logger.handlers[:]:
                logger.removeHandler(h)

            logger.propagate = propagate
            logger.disabled = 0
            if b'handlers' in opts:
                hlist = [ h.strip() for h in get(section_name, b'handlers', b'null').split(b',') ]
                for hand in hlist:
                    try:
                        logger.addHandler(handlers[hand])
                    except KeyError:
                        raise errors.LoggingSettingsError((b'unable to initialize logging (handler \'{}\' not found in "{}")').format(hand, ini_path))

        for log in existing:
            logger = root.manager.loggerDict[log]
            if log in child_loggers:
                logger.level = logging.NOTSET
                logger.handlers = []
                logger.propagate = 1
            else:
                logger.disabled = disable_existing_loggers

    finally:
        logging._releaseLock()

    return