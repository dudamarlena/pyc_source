# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/locations.py
# Compiled at: 2019-09-10 15:18:29
"""Locations where we look for configs, install stuff, etc"""
from __future__ import absolute_import
import os, os.path, platform, site, sys, sysconfig
from distutils import sysconfig as distutils_sysconfig
from distutils.command.install import SCHEME_KEYS
from pip._internal.compat import WINDOWS, expanduser
from pip._internal.utils import appdirs
USER_CACHE_DIR = appdirs.user_cache_dir('pip')
DELETE_MARKER_MESSAGE = 'This file is placed here by pip to indicate the source was put\nhere by pip.\n\nOnce this package is successfully installed this source code will be\ndeleted (unless you remove this file).\n'
PIP_DELETE_MARKER_FILENAME = 'pip-delete-this-directory.txt'

def write_delete_marker_file(directory):
    """
    Write the pip delete marker file into this directory.
    """
    filepath = os.path.join(directory, PIP_DELETE_MARKER_FILENAME)
    with open(filepath, 'w') as (marker_fp):
        marker_fp.write(DELETE_MARKER_MESSAGE)


def running_under_virtualenv():
    """
    Return True if we're running inside a virtualenv, False otherwise.

    """
    if hasattr(sys, 'real_prefix'):
        return True
    if sys.prefix != getattr(sys, 'base_prefix', sys.prefix):
        return True
    return False


def virtualenv_no_global():
    """
    Return True if in a venv and no system site packages.
    """
    site_mod_dir = os.path.dirname(os.path.abspath(site.__file__))
    no_global_file = os.path.join(site_mod_dir, 'no-global-site-packages.txt')
    if running_under_virtualenv() and os.path.isfile(no_global_file):
        return True


if running_under_virtualenv():
    src_prefix = os.path.join(sys.prefix, 'src')
else:
    try:
        src_prefix = os.path.join(os.getcwd(), 'src')
    except OSError:
        sys.exit('The folder you are executing pip from can no longer be found.')

    src_prefix = os.path.abspath(src_prefix)
    site_packages = sysconfig.get_path('purelib')
    if platform.python_implementation().lower() == 'pypy':
        site_packages = distutils_sysconfig.get_python_lib()
    try:
        user_site = site.getusersitepackages()
    except AttributeError:
        user_site = site.USER_SITE

user_dir = expanduser('~')
if WINDOWS:
    bin_py = os.path.join(sys.prefix, 'Scripts')
    bin_user = os.path.join(user_site, 'Scripts')
    if not os.path.exists(bin_py):
        bin_py = os.path.join(sys.prefix, 'bin')
        bin_user = os.path.join(user_site, 'bin')
    config_basename = 'pip.ini'
    legacy_storage_dir = os.path.join(user_dir, 'pip')
    legacy_config_file = os.path.join(legacy_storage_dir, config_basename)
else:
    bin_py = os.path.join(sys.prefix, 'bin')
    bin_user = os.path.join(user_site, 'bin')
    config_basename = 'pip.conf'
    legacy_storage_dir = os.path.join(user_dir, '.pip')
    legacy_config_file = os.path.join(legacy_storage_dir, config_basename)
    if sys.platform[:6] == 'darwin' and sys.prefix[:16] == '/System/Library/':
        bin_py = '/usr/local/bin'
site_config_files = [ os.path.join(path, config_basename) for path in appdirs.site_config_dirs('pip')
                    ]
venv_config_file = os.path.join(sys.prefix, config_basename)
new_config_file = os.path.join(appdirs.user_config_dir('pip'), config_basename)

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
    assert not (user and prefix), ('user={} prefix={}').format(user, prefix)
    i.user = user or i.user
    if user:
        i.prefix = ''
    i.prefix = prefix or i.prefix
    i.home = home or i.home
    i.root = root or i.root
    i.finalize_options()
    for key in SCHEME_KEYS:
        scheme[key] = getattr(i, 'install_' + key)

    if 'install_lib' in d.get_option_dict('install'):
        scheme.update(dict(purelib=i.install_lib, platlib=i.install_lib))
    if running_under_virtualenv():
        scheme['headers'] = os.path.join(sys.prefix, 'include', 'site', 'python' + sys.version[:3], dist_name)
        if root is not None:
            path_no_drive = os.path.splitdrive(os.path.abspath(scheme['headers']))[1]
            scheme['headers'] = os.path.join(root, path_no_drive[1:])
    return scheme