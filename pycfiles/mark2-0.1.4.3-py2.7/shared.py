# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/shared.py
# Compiled at: 2013-08-16 22:15:55
import os, pkg_resources

def open_resource(name):
    return pkg_resources.resource_stream('mk2', name)


_config_found = False
if 'MARK2_CONFIG_DIR' in os.environ:
    _config_base = os.environ['MARK2_CONFIG_DIR']
elif 'VIRTUAL_ENV' in os.environ:
    _config_base = os.path.join(os.environ['VIRTUAL_ENV'], '.config', 'mark2')
elif __file__.startswith('/home/'):
    _config_base = os.path.join(os.path.expanduser('~'), '.config', 'mark2')
else:
    _config_base = os.path.join(os.path.join('/etc/mark2'))

def find_config(name, create=True, ignore_errors=False):
    global _config_base
    global _config_found
    if not _config_found:
        if os.path.exists(_config_base):
            _config_found = True
    if create and not _config_found:
        try:
            os.makedirs(_config_base)
            _config_found = True
        except OSError:
            pass

    if not ignore_errors and not _config_found:
        raise ValueError
    return os.path.join(_config_base, name)


def console_repr(e):
    s = '%s %s ' % (e['time'], {'server': '|', 'mark2': '#', 'user': '>'}.get(e['source'], '?'))
    if e['source'] == 'server' and e['level'] != 'INFO':
        s += '[%s] ' % e['level']
    elif e['source'] == 'user':
        s += '(%s) ' % e['user']
    s += '%s' % e['data']
    return s