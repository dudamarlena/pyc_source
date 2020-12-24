# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/vyper/util.py
# Compiled at: 2019-11-12 13:45:02
# Size of source mod 2**32: 1910 bytes
import logging, os, pathlib, toml, yaml
try:
    import ujson as json
except ImportError:
    import json

try:
    FileNotFoundError
except NameError:
    FileNotFoundError = OSError

log = logging.getLogger('vyper.util')

class ConfigParserError(Exception):
    __doc__ = 'Denotes failing to parse configuration file.'

    def __init__(self, message, *args):
        self.message = message
        (super(ConfigParserError, self).__init__)(message, *args)

    def __str__(self):
        return 'While parsing config: {0}'.format(self.message)


def abs_pathify(in_path):
    log.info('Trying to resolve absolute path to {0}'.format(in_path))
    try:
        return pathlib.Path(in_path).resolve()
    except FileNotFoundError as e:
        try:
            log.error('Couldn"t discover absolute path: {0}'.format(e))
            return ''
        finally:
            e = None
            del e


def exists(path):
    try:
        os.stat(str(path))
        return True
    except FileNotFoundError:
        return False


def unmarshall_config_reader(r, d, config_type):
    config_type = config_type.lower()
    if config_type in ('yaml', 'yml'):
        try:
            f = yaml.safe_load(r)
            try:
                d.update(yaml.safe_load(f))
            except AttributeError:
                d.update(f)

        except Exception as e:
            try:
                raise ConfigParserError(e)
            finally:
                e = None
                del e

    else:
        if config_type == 'json':
            try:
                f = json.loads(r)
                d.update(f)
            except Exception as e:
                try:
                    raise ConfigParserError(e)
                finally:
                    e = None
                    del e

        else:
            if config_type == 'toml':
                try:
                    try:
                        d.update(toml.loads(r))
                    except TypeError:
                        try:
                            d.update(toml.load(r))
                        except TypeError:
                            d.update(r)

                except Exception as e:
                    try:
                        raise ConfigParserError(e)
                    finally:
                        e = None
                        del e

            return d