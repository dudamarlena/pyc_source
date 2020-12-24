# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vilmos/Projects/python-iptables/iptc/util.py
# Compiled at: 2018-04-16 20:15:05
import re, os, sys, ctypes, ctypes.util
from distutils.sysconfig import get_python_lib
from itertools import product
from subprocess import Popen, PIPE
from sys import version_info
try:
    from sysconfig import get_config_var
except ImportError:

    def get_config_var(name):
        if name == 'SO':
            return '.so'
        raise Exception('Not implemented')


def _insert_ko(modprobe, modname):
    p = Popen([modprobe, modname], stderr=PIPE)
    p.wait()
    return (p.returncode, p.stderr.read(1024))


def _load_ko(modname):
    if not os.path.exists('/proc/modules'):
        return (0, None)
    else:
        modprobe = '/sbin/modprobe'
        try:
            proc = open('/proc/sys/kernel/modprobe')
            modprobe = proc.read(1024)
        except:
            pass

        if modprobe[(-1)] == '\n':
            modprobe = modprobe[:-1]
        return _insert_ko(modprobe, modname)


def load_kernel(name, exc_if_failed=False):
    rc, err = _load_ko(name)
    if rc:
        if not err:
            err = 'Failed to load the %s kernel module.' % name
        if err[(-1)] == '\n':
            err = err[:-1]
        if exc_if_failed:
            raise Exception(err)


def _do_find_library(name):
    if '/' in name:
        try:
            return ctypes.CDLL(name, mode=ctypes.RTLD_GLOBAL)
        except Exception:
            return

    p = ctypes.util.find_library(name)
    if p:
        lib = ctypes.CDLL(p, mode=ctypes.RTLD_GLOBAL)
        return lib
    else:
        try:
            lib = ctypes.CDLL(os.path.join(get_python_lib(), name), mode=ctypes.RTLD_GLOBAL)
            return lib
        except:
            pass

        for p in sys.path:
            try:
                lib = ctypes.CDLL(os.path.join(p, name), mode=ctypes.RTLD_GLOBAL)
                return lib
            except:
                pass

        return


def _find_library(*names):
    if version_info >= (3, 3):
        ext = get_config_var('EXT_SUFFIX')
    else:
        ext = get_config_var('SO')
    for name in names:
        libnames = [
         name, 'lib' + name, name + ext, 'lib' + name + ext]
        libdir = os.environ.get('IPTABLES_LIBDIR', None)
        if libdir is not None:
            libdirs = libdir.split(':')
            libs = [ os.path.join(*p) for p in product(libdirs, libnames) ]
            libs.extend(libnames)
        else:
            libs = libnames
        for n in libs:
            while os.path.islink(n):
                n = os.path.realpath(n)

            lib = _do_find_library(n)
            if lib is not None:
                yield lib

    return


def find_library(*names):
    for lib in _find_library(*names):
        major = 0
        m = re.search('\\.so\\.(\\d+).?', lib._name)
        if m:
            major = int(m.group(1))
        return (
         lib, major)

    return (None, None)