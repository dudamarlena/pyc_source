# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/linkexchange/config.py
# Compiled at: 2011-04-19 15:47:33
r"""
>>> import StringIO
>>> from linkexchange import config
>>> cfg_lines = [
...   '[options]',
...   'host=example.com',
...   '',
...   '[client-1]',
...   'type=sape',
...   'user=user12345',
...   'db_driver.type=mem',
...   'server-1=http://server1.com',
...   'server-2=http://server2.com',
...   '',
...   '[client-2]',
...   'type=linkfeed',
...   'user=user12345',
...   'db_driver.type=shelve',
...   'db_driver.filename=linkfeed-XXX.db',
...   '',
...   '[formatter-1]',
...   'type=inline',
...   'count=none',
...   'delimiter=u" | "',
...   ]
>>> vars = {}
>>> cfg_file = StringIO.StringIO('\n'.join(cfg_lines))
>>> result = config.file_config(vars, cfg_file)
>>> result == [cfg_file]
True
>>> vars['options']['host']
'example.com'
>>> vars['platform'].clients[0].user
'user12345'
>>> vars['platform'].clients[0].server_list[0]
'http://server1.com'
>>> vars['platform'].clients[0].server_list[1]
'http://server2.com'
>>> vars['platform'].clients[1].db_driver.filename
'linkfeed-XXX.db'
>>> vars['formatters'][0].count
>>> vars['formatters'][0].delimiter
u' | '
>>> import os, tempfile
>>> cfg_fd, cfg_file = tempfile.mkstemp()
>>> os.close(cfg_fd)
>>> open(cfg_file, 'w').write('\n'.join(cfg_lines))
>>> result = config.file_config(vars, cfg_file)
>>> result == [cfg_file]
True
>>> os.unlink(cfg_file)
>>> result = config.file_config(vars, cfg_file)
>>> result == []
True
"""
import sys, ConfigParser, shlex
from linkexchange.utils import load_plugin
from linkexchange.platform import Platform

class ConfigError(Exception):
    """Configuration error"""
    pass


def file_config(vars, fname, defaults=None, prefix='', default_encoding='utf-8'):
    if defaults is None:
        defaults = {}
    cp = ConfigParser.ConfigParser(defaults)
    try:
        if hasattr(cp, 'readfp') and hasattr(fname, 'readline'):
            cp.readfp(fname)
            result = [fname]
        else:
            result = cp.read(fname)
            if sys.version_info < (2, 4):
                if cp.sections():
                    if type(fname) == list:
                        result = fname
                    else:
                        result = [
                         fname]
                else:
                    result = []
    except (ConfigParser.MissingSectionHeaderError,
     ConfigParser.ParsingError) as e:
        raise ConfigError('Parsing error: %s' % str(e))

    if not result:
        return result
    else:
        _clients = []
        _formatters = []
        _options = {}
        try:
            encoding = cp.get('options', 'config_encoding')
        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError):
            encoding = default_encoding

        for sec in cp.sections():
            opts = dict([ (o, cp.get(sec, o)) for o in cp.options(sec) if o not in defaults
                        ])
            cn = fn = None
            if sec == 'client':
                cn = 1
            elif sec.startswith('client-'):
                cn = int(sec.split('-', 1)[1])
            elif sec == 'formatter':
                fn = 1
            elif sec.startswith('formatter-'):
                fn = int(sec.split('-', 1)[1])
            elif sec == 'options':
                for k, v in opts.items():
                    _options[k] = _eval_value(v, encoding)

            if cn:
                _clients.extend([None] * max(0, cn - len(_clients)))
                _clients[cn - 1] = _parse_plugin_spec(opts, encoding)
            if fn:
                _formatters.extend([None] * max(0, fn - len(_formatters)))
                _formatters[fn - 1] = _parse_plugin_spec(opts, encoding)

        def load_client(spec):
            try:
                return load_plugin('linkexchange.clients', spec)
            except ImportError:
                raise ConfigError('Client not found: %s' % spec[0])

        def load_formatter(spec):
            try:
                return load_plugin('linkexchange.formatters', spec)
            except ImportError:
                raise ConfigError('Formatter not found: %s' % spec[0])

        clients = [ load_client(x) for x in _clients if x is not None ]
        vars[prefix + 'platform'] = Platform(clients)
        vars[prefix + 'formatters'] = [ load_formatter(x) for x in _formatters if x is not None
                                      ]
        vars[prefix + 'options'] = _options
        return result


def _eval_value(value, encoding):
    value = value.strip()
    try:
        return int(value)
    except ValueError:
        pass

    try:
        return long(value)
    except ValueError:
        pass

    try:
        return float(value)
    except ValueError:
        pass

    value_lower = value.lower()
    if value_lower in ('true', 'on', 'enabled'):
        return True
    else:
        if value_lower in ('false', 'off', 'disabled'):
            return False
        if value_lower == 'none':
            return None
        conv_str = lambda x: x
        unquote_str = lambda x: x
        if value.endswith('"'):
            if value.startswith('u"'):
                conv_str = lambda x: unicode(x, encoding)
                value = value[1:]
            if value.startswith('"'):
                unquote_str = lambda x: ('').join(shlex.split(x))
        return conv_str(unquote_str(value))


def _parse_plugin_spec(dic, encoding):
    opts = {}
    compound = {}
    for k, v in dic.items():
        if '.' in k:
            k1, k2 = k.split('.', 1)
            compound.setdefault(k1, {})
            compound[k1][k2] = v
        elif k.endswith('_list'):
            opts[k] = [ _eval_value(x, encoding) for x in v.split(',') ]
        elif '-' in k and k.split('-')[(-1)].isdigit():
            a, n = k.split('-')
            kk = a + '_list'
            nn = int(n) - 1
            opts.setdefault(kk, [])
            opts[kk].extend([None] * max(0, nn - len(opts[kk]) + 1))
            opts[kk][nn] = _eval_value(v, encoding)
        else:
            opts[k] = _eval_value(v, encoding)

    for k, v in compound.items():
        opts[k] = _parse_plugin_spec(v, encoding)

    return (
     opts.pop('type'), [], opts)


if __name__ == '__main__':
    import doctest
    doctest.testmod()