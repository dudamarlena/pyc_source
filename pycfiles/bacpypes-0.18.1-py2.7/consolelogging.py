# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bacpypes/consolelogging.py
# Compiled at: 2020-04-20 14:21:19
"""
Console Logging
"""
import os, sys, json, logging, logging.handlers, argparse
from .settings import Settings, settings, os_settings, dict_settings
from .debugging import bacpypes_debugging, LoggingFormatter, ModuleLogger
from ConfigParser import ConfigParser as _ConfigParser
_debug = 0
_log = ModuleLogger(globals())

def ConsoleLogHandler(loggerRef='', handler=None, level=logging.DEBUG, color=None):
    """Add a handler to stderr with our custom formatter to a logger."""
    if isinstance(loggerRef, logging.Logger):
        pass
    elif isinstance(loggerRef, str):
        if not loggerRef:
            loggerRef = _log
        elif loggerRef not in logging.Logger.manager.loggerDict:
            raise RuntimeError('not a valid logger name: %r' % (loggerRef,))
        loggerRef = logging.getLogger(loggerRef)
    else:
        raise RuntimeError('not a valid logger reference: %r' % (loggerRef,))
    if hasattr(loggerRef, 'globs'):
        loggerRef.globs['_debug'] += 1
    elif hasattr(loggerRef.parent, 'globs'):
        loggerRef.parent.globs['_debug'] += 1
    if not handler:
        handler = logging.StreamHandler()
        handler.setLevel(level)
    handler.setFormatter(LoggingFormatter(color))
    loggerRef.addHandler(handler)
    loggerRef.setLevel(level)


@bacpypes_debugging
class ArgumentParser(argparse.ArgumentParser):
    """
    ArgumentParser extends the one with the same name from the argparse module
    by adding the common command line arguments found in BACpypes applications.

        --buggers                       list the debugging logger names
        --debug [DEBUG [DEBUG ...]]     attach a handler to loggers
        --color                         debug in color
        --route-aware                   turn on route aware
    """

    def __init__(self, **kwargs):
        """Follow normal initialization and add BACpypes arguments."""
        if _debug:
            ArgumentParser._debug('__init__')
        argparse.ArgumentParser.__init__(self, **kwargs)
        self.update_os_env()
        if _debug:
            ArgumentParser._debug('    - os environment')
        self.add_argument('--buggers', help='list the debugging logger names', action='store_true')
        self.add_argument('--debug', nargs='*', help='add a log handler to each debugging logger')
        self.add_argument('--color', help='turn on color debugging', action='store_true', default=None)
        self.add_argument('--route-aware', help='turn on route aware', action='store_true', default=None)
        return

    def update_os_env(self):
        """Update the settings with values from the environment, if provided."""
        if _debug:
            ArgumentParser._debug('update_os_env')
        os_settings()
        if _debug:
            ArgumentParser._debug('    - settings: %r', settings)

    def parse_args(self, *args, **kwargs):
        """Parse the arguments as usual, then add default processing."""
        if _debug:
            ArgumentParser._debug('parse_args')
        result_args = argparse.ArgumentParser.parse_args(self, *args, **kwargs)
        self.expand_args(result_args)
        if _debug:
            ArgumentParser._debug('    - args expanded')
        self.interpret_debugging(result_args)
        if _debug:
            ArgumentParser._debug('    - interpreted debugging')
        return result_args

    def expand_args(self, result_args):
        """Expand the arguments and/or update the settings."""
        if _debug:
            ArgumentParser._debug('expand_args %r', result_args)
        if result_args.debug is None:
            if _debug:
                ArgumentParser._debug('    - debug not specified')
        elif not result_args.debug:
            if _debug:
                ArgumentParser._debug('    - debug with no args')
            settings.debug.update(['__main__'])
        else:
            if _debug:
                ArgumentParser._debug('    - debug: %r', result_args.debug)
            settings.debug.update(result_args.debug)
        if result_args.color is None:
            if _debug:
                ArgumentParser._debug('    - color not specified')
        else:
            if _debug:
                ArgumentParser._debug('    - color: %r', result_args.color)
            settings.color = result_args.color
        if result_args.route_aware is None:
            if _debug:
                ArgumentParser._debug('    - route_aware not specified')
        else:
            if _debug:
                ArgumentParser._debug('    - route_aware: %r', result_args.route_aware)
            settings.route_aware = result_args.route_aware
        return

    def interpret_debugging(self, result_args):
        """Take the result of parsing the args and interpret them."""
        if _debug:
            ArgumentParser._debug('interpret_debugging %r', result_args)
            ArgumentParser._debug('    - settings: %r', settings)
        if result_args.buggers:
            loggers = sorted(logging.Logger.manager.loggerDict.keys())
            for loggerName in loggers:
                sys.stdout.write(loggerName + '\n')

            sys.exit(0)
        file_handlers = {}
        for i, debug_name in enumerate(settings.debug):
            color = i % 6 + 2 if settings.color else None
            debug_specs = debug_name.split(':')
            if len(debug_specs) == 1 and not settings.debug_file:
                ConsoleLogHandler(debug_name, color=color)
            else:
                debug_name = debug_specs.pop(0)
                if debug_specs:
                    file_name = debug_specs.pop(0)
                else:
                    file_name = settings.debug_file
                if file_name in file_handlers:
                    handler = file_handlers[file_name]
                else:
                    if debug_specs:
                        maxBytes = int(debug_specs.pop(0))
                    else:
                        maxBytes = settings.max_bytes
                    if debug_specs:
                        backupCount = int(debug_specs.pop(0))
                    else:
                        backupCount = settings.backup_count
                    handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=maxBytes, backupCount=backupCount)
                    handler.setLevel(logging.DEBUG)
                    file_handlers[file_name] = handler
                ConsoleLogHandler(debug_name, handler=handler)

        return result_args


@bacpypes_debugging
class ConfigArgumentParser(ArgumentParser):
    """
    ConfigArgumentParser extends the ArgumentParser with the functionality to
    read in an INI configuration file.

        --ini INI       provide a separate INI file
    """

    def __init__(self, **kwargs):
        """Follow normal initialization and add BACpypes arguments."""
        if _debug:
            ConfigArgumentParser._debug('__init__')
        ArgumentParser.__init__(self, **kwargs)
        self.add_argument('--ini', help='device object configuration file', default=settings.ini)

    def update_os_env(self):
        """Update the settings with values from the environment, if provided."""
        if _debug:
            ConfigArgumentParser._debug('update_os_env')
        ArgumentParser.update_os_env(self)
        settings['ini'] = os.getenv('BACPYPES_INI', 'BACpypes.ini')

    def expand_args(self, result_args):
        """Take the result of parsing the args and interpret them."""
        if _debug:
            ConfigArgumentParser._debug('expand_args %r', result_args)
        config = _ConfigParser()
        config.read(result_args.ini)
        if _debug:
            _log.debug('    - config: %r', config)
        if not config.has_section('BACpypes'):
            raise RuntimeError('INI file with BACpypes section required')
        ini_obj = Settings(dict(config.items('BACpypes')))
        if _debug:
            _log.debug('    - ini_obj: %r', ini_obj)
        setattr(result_args, 'ini', ini_obj)
        ArgumentParser.expand_args(self, result_args)


def _deunicodify_hook(pairs):
    """
    JSON decoding hook to eliminate unicode strings in keys and values.
    """
    new_pairs = []
    for key, value in pairs:
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = [ v.encode('utf-8') if isinstance(v, unicode) else v for v in value ]
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        new_pairs.append((key, value))

    return Settings(new_pairs)


@bacpypes_debugging
class JSONArgumentParser(ArgumentParser):
    """
    JSONArgumentParser extends the ArgumentParser with the functionality to
    read in a JSON configuration file.

        --json JSON    provide a separate JSON file
    """

    def __init__(self, **kwargs):
        """Follow normal initialization and add BACpypes arguments."""
        if _debug:
            JSONArgumentParser._debug('__init__')
        ArgumentParser.__init__(self, **kwargs)
        self.add_argument('--json', help='configuration file', default=settings.json)

    def update_os_env(self):
        """Update the settings with values from the environment, if provided."""
        if _debug:
            JSONArgumentParser._debug('update_os_env')
        ArgumentParser.update_os_env(self)
        settings['json'] = os.getenv('BACPYPES_JSON', 'BACpypes.json')

    def expand_args(self, result_args):
        """Take the result of parsing the args and interpret them."""
        if _debug:
            JSONArgumentParser._debug('expand_args %r', result_args)
        try:
            with open(result_args.json) as (json_file):
                json_obj = json.load(json_file, object_pairs_hook=_deunicodify_hook)
                if _debug:
                    JSONArgumentParser._debug('    - json_obj: %r', json_obj)
        except IOError:
            raise RuntimeError('settings file not found: %r\n' % (settings.json,))

        if 'bacpypes' in json_obj:
            dict_settings(**json_obj.bacpypes)
            if _debug:
                JSONArgumentParser._debug('    - settings: %r', settings)
        setattr(result_args, 'json', json_obj)
        ArgumentParser.expand_args(self, result_args)