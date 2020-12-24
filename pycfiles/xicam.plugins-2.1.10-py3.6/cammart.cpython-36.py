# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\cammart.py
# Compiled at: 2018-05-17 15:54:05
# Size of source mod 2**32: 4311 bytes
import collections, json
from urllib import parse
import os, sys, requests, yaml
from appdirs import user_config_dir, site_config_dir, user_cache_dir
import platform, subprocess
from . import manager
from . import venvs
op_sys = platform.system()
if op_sys == 'Darwin':
    user_package_registry = os.path.join(user_cache_dir(appname='xicam'), 'packages.yml')
else:
    user_package_registry = os.path.join(user_config_dir(appname='xicam'), 'packages.yml')
site_package_registry = os.path.join(site_config_dir(appname='xicam'), 'packages.yml')

def install(name: str):
    """
    Install a Xi-cam plugin package by querying the Xi-cam package repository with REST.

    Packages are installed into the currently active virtualenv

    Parameters
    ----------
    name : str
        The package name to be installed.
    """
    o = requests.get(f'http://cam.lbl.gov:5000/pluginpackages?where={{"name":"{name}"}}')
    uri = parse.urlparse(json.loads(o.content)['_items'][0]['installuri'])
    failure = True
    if uri.scheme == 'pipgit':
        failure = subprocess.Popen([pippath(), 'install', 'git+https://' + ''.join(uri[1:])]).wait()
    else:
        if uri.scheme == 'pip':
            failure = subprocess.Popen([pippath(), 'install', ''.join(uri[1:])]).wait()
        else:
            if uri.scheme == 'conda':
                raise NotImplementedError
    if not failure:
        pkg_registry[name] = uri.scheme
    manager.collectPlugins()


def uninstall(name: str):
    failure = True
    if name in pkg_registry:
        scheme = pkg_registry[name]
        if scheme in ('pipgit', 'pip'):
            failure = subprocess.Popen([pippath(), 'uninstall', '-y', name]).returncode
        else:
            if scheme == 'conda':
                raise NotImplementedError
    if not failure:
        del pkg_registry[name]
    return not failure


def pippath():
    if platform.system() == 'Windows':
        bindir = 'Scripts'
    else:
        bindir = 'bin'
    return os.path.join(venvs.current_environment, bindir, 'pip')


class pkg_registry(collections.MutableMapping):

    def __init__(self):
        self._store = dict()
        self.update(self._store)
        self.load()
        self.save()

    def __getitem__(self, key):
        return self._store[self.__keytransform__(key)]

    def __setitem__(self, key, value):
        self._store[self.__keytransform__(key)] = value
        self.save()

    def __delitem__(self, key):
        del self._store[self.__keytransform__(key)]
        self.save()

    def __iter__(self):
        return iter(self._store)

    def __len__(self):
        return len(self._store)

    def __keytransform__(self, key):
        return key

    def load(self):
        try:
            with open(user_package_registry, 'r') as (f):
                self._store = yaml.load(f.read())
        except FileNotFoundError:
            pass

    def save(self):
        with open(user_package_registry, 'w') as (f):
            f.write(yaml.dump(self._store))


pkg_registry = pkg_registry()