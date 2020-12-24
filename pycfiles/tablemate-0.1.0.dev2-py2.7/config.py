# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tablemate/config.py
# Compiled at: 2015-04-12 20:22:55
""" Configuration utilities.
"""
from __future__ import absolute_import, unicode_literals, print_function
import os, re, sys, click
from ._compat import iteritems
try:
    CLI_PATH = sys.modules[b'__main__'].__file__
except (KeyError, AttributeError):
    CLI_PATH = __file__

CLI_PATH = os.path.dirname(CLI_PATH)
if CLI_PATH.endswith(b'/bin'):
    CLI_PATH = CLI_PATH[:-4]
CLI_PATH = re.sub(b'^' + os.path.expanduser(b'~'), b'~', CLI_PATH)
VERSION_INFO = (b'%(prog)s %(version)s from {} [Python {}]').format(CLI_PATH, (b' ').join(sys.version.split()[:1]))
APP_NAME = None
cli = None

def version_info(ctx=None):
    """Return version information just like --version does."""
    from . import __version__
    prog = ctx.find_root().info_name if ctx else APP_NAME
    version = __version__
    try:
        import pkg_resources
    except ImportError:
        pass

    for dist in pkg_resources.working_set:
        scripts = dist.get_entry_map().get(b'console_scripts') or {}
        for _, entry_point in iteritems(scripts):
            if entry_point.module_name == __package__ + b'.__main__':
                version = dist.version
                break

    return VERSION_INFO % dict(prog=prog, version=version)


def envvar(name, default=None):
    """Return an environment variable specific for this application (using a prefix)."""
    varname = (APP_NAME + b'-' + name).upper().replace(b'-', b'_')
    return os.environ.get(varname, default)


def locations(exists=True, extras=None):
    """Return the location of the config file(s)."""
    result = []
    candidates = [
     (b'/etc/{}.conf').format(APP_NAME),
     os.path.join(click.get_app_dir(APP_NAME) + b'.conf')] + (extras and list(extras) or [])
    for config_file in candidates:
        if config_file and (not exists or os.path.exists(config_file)):
            result.append(config_file)

    return result