# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/locations.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 5414 bytes
"""Locations where we look for configs, install stuff, etc"""
from __future__ import absolute_import
import os, os.path, platform, site, sys, sysconfig
from distutils import sysconfig as distutils_sysconfig
from distutils.command.install import SCHEME_KEYS
from pip._internal.utils import appdirs
from pip._internal.utils.compat import WINDOWS
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.virtualenv import running_under_virtualenv
if MYPY_CHECK_RUNNING:
    from typing import Any, Union, Dict, List, Optional
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
    if not os.path.exists(bin_py):
        bin_py = os.path.join(sys.prefix, 'bin')
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
    scheme = {}
    if isolated:
        extra_dist_args = {'script_args': ['--no-user-cfg']}
    else:
        extra_dist_args = {}
    dist_args = {'name': dist_name}
    dist_args.update(extra_dist_args)
    d = Distribution(dist_args)
    d.parse_config_files()
    i = d.get_command_obj('install', create=True)
    if not i is not None:
        raise AssertionError
    else:
        assert not (user and prefix), 'user={} prefix={}'.format(user, prefix)
        assert not (home and prefix), 'home={} prefix={}'.format(home, prefix)
    i.user = user or i.user
    if user or home:
        i.prefix = ''
    i.prefix = prefix or i.prefix
    i.home = home or i.home
    i.root = root or i.root
    i.finalize_options()
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