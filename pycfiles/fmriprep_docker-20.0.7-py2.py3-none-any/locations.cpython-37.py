# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-aejasjrz/pip/pip/_internal/locations.py
# Compiled at: 2020-05-05 12:41:47
# Size of source mod 2**32: 6734 bytes
"""Locations where we look for configs, install stuff, etc"""
from __future__ import absolute_import
import os, os.path, platform, site, sys, sysconfig
from distutils import sysconfig as distutils_sysconfig
from distutils.command.install import SCHEME_KEYS
import distutils.command.install as distutils_install_command
from pip._internal.models.scheme import Scheme
from pip._internal.utils import appdirs
from pip._internal.utils.compat import WINDOWS
from pip._internal.utils.typing import MYPY_CHECK_RUNNING, cast
from pip._internal.utils.virtualenv import running_under_virtualenv
if MYPY_CHECK_RUNNING:
    from typing import Dict, List, Optional, Union
    import distutils.cmd as DistutilsCommand
USER_CACHE_DIR = appdirs.user_cache_dir('pip')

def get_major_minor_version():
    """
    Return the major-minor version of the current Python as a string, e.g.
    "3.7" or "3.10".
    """
    return ('{}.{}'.format)(*sys.version_info)


def get_src_prefix():
    if running_under_virtualenv():
        src_prefix = os.path.join(sys.prefix, 'src')
    else:
        try:
            src_prefix = os.path.join(os.getcwd(), 'src')
        except OSError:
            sys.exit('The folder you are executing pip from can no longer be found.')

        return os.path.abspath(src_prefix)


site_packages = sysconfig.get_path('purelib')
if platform.python_implementation().lower() == 'pypy':
    site_packages = distutils_sysconfig.get_python_lib()
try:
    user_site = site.getusersitepackages()
except AttributeError:
    user_site = site.USER_SITE

if WINDOWS:
    bin_py = os.path.join(sys.prefix, 'Scripts')
    bin_user = os.path.join(user_site, 'Scripts')
    bin_py = os.path.exists(bin_py) or os.path.join(sys.prefix, 'bin')
    bin_user = os.path.join(user_site, 'bin')
else:
    bin_py = os.path.join(sys.prefix, 'bin')
    bin_user = os.path.join(user_site, 'bin')
    if sys.platform[:6] == 'darwin':
        if sys.prefix[:16] == '/System/Library/':
            bin_py = '/usr/local/bin'

    def distutils_scheme(dist_name, user=False, home=None, root=None, isolated=False, prefix=None):
        """
    Return a distutils install scheme
    """
        from distutils.dist import Distribution
        dist_args = {'name': dist_name}
        if isolated:
            dist_args['script_args'] = [
             '--no-user-cfg']
        d = Distribution(dist_args)
        d.parse_config_files()
        obj = None
        obj = d.get_command_obj('install', create=True)
        assert obj is not None
        i = cast(distutils_install_command, obj)
        if user:
            if prefix:
                raise AssertionError('user={} prefix={}'.format(user, prefix))
        if home:
            if prefix:
                raise AssertionError('home={} prefix={}'.format(home, prefix))
        i.user = user or i.user
        if user or home:
            i.prefix = ''
        i.prefix = prefix or i.prefix
        i.home = home or i.home
        i.root = root or i.root
        i.finalize_options()
        scheme = {}
        for key in SCHEME_KEYS:
            scheme[key] = getattr(i, 'install_' + key)

        if 'install_lib' in d.get_option_dict('install'):
            scheme.update(dict(purelib=(i.install_lib), platlib=(i.install_lib)))
        if running_under_virtualenv():
            scheme['headers'] = os.path.join(sys.prefix, 'include', 'site', 'python{}'.format(get_major_minor_version()), dist_name)
            if root is not None:
                path_no_drive = os.path.splitdrive(os.path.abspath(scheme['headers']))[1]
                scheme['headers'] = os.path.join(root, path_no_drive[1:])
        return scheme


    def get_scheme(dist_name, user=False, home=None, root=None, isolated=False, prefix=None):
        """
    Get the "scheme" corresponding to the input parameters. The distutils
    documentation provides the context for the available schemes:
    https://docs.python.org/3/install/index.html#alternate-installation

    :param dist_name: the name of the package to retrieve the scheme for, used
        in the headers scheme path
    :param user: indicates to use the "user" scheme
    :param home: indicates to use the "home" scheme and provides the base
        directory for the same
    :param root: root under which other directories are re-based
    :param isolated: equivalent to --no-user-cfg, i.e. do not consider
        ~/.pydistutils.cfg (posix) or ~/pydistutils.cfg (non-posix) for
        scheme paths
    :param prefix: indicates to use the "prefix" scheme and provides the
        base directory for the same
    """
        scheme = distutils_scheme(dist_name, user, home, root, isolated, prefix)
        return Scheme(platlib=(scheme['platlib']),
          purelib=(scheme['purelib']),
          headers=(scheme['headers']),
          scripts=(scheme['scripts']),
          data=(scheme['data']))