# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/setuptools/setuptools/_vendor/packaging/tags.py
# Compiled at: 2020-04-16 14:32:33
# Size of source mod 2**32: 12933 bytes
from __future__ import absolute_import
import distutils.util
try:
    from importlib.machinery import EXTENSION_SUFFIXES
except ImportError:
    import imp
    EXTENSION_SUFFIXES = [x[0] for x in imp.get_suffixes()]
    del imp

import platform, re, sys, sysconfig, warnings
INTERPRETER_SHORT_NAMES = {'python':'py', 
 'cpython':'cp', 
 'pypy':'pp', 
 'ironpython':'ip', 
 'jython':'jy'}
_32_BIT_INTERPRETER = sys.maxsize <= 4294967296

class Tag(object):
    __slots__ = [
     '_interpreter', '_abi', '_platform']

    def __init__(self, interpreter, abi, platform):
        self._interpreter = interpreter.lower()
        self._abi = abi.lower()
        self._platform = platform.lower()

    @property
    def interpreter(self):
        return self._interpreter

    @property
    def abi(self):
        return self._abi

    @property
    def platform(self):
        return self._platform

    def __eq__(self, other):
        return self.platform == other.platform and self.abi == other.abi and self.interpreter == other.interpreter

    def __hash__(self):
        return hash((self._interpreter, self._abi, self._platform))

    def __str__(self):
        return '{}-{}-{}'.format(self._interpreter, self._abi, self._platform)

    def __repr__(self):
        return '<{self} @ {self_id}>'.format(self=self, self_id=(id(self)))


def parse_tag(tag):
    tags = set()
    interpreters, abis, platforms = tag.split('-')
    for interpreter in interpreters.split('.'):
        for abi in abis.split('.'):
            for platform_ in platforms.split('.'):
                tags.add(Tag(interpreter, abi, platform_))

    return frozenset(tags)


def _normalize_string(string):
    return string.replace('.', '_').replace('-', '_')


def _cpython_interpreter(py_version):
    return 'cp{major}{minor}'.format(major=(py_version[0]), minor=(py_version[1]))


def _cpython_abis(py_version):
    abis = []
    version = ('{}{}'.format)(*py_version[:2])
    debug = pymalloc = ucs4 = ''
    with_debug = sysconfig.get_config_var('Py_DEBUG')
    has_refcount = hasattr(sys, 'gettotalrefcount')
    has_ext = '_d.pyd' in EXTENSION_SUFFIXES
    if not with_debug:
        if with_debug is None:
            if has_refcount or has_ext:
                debug = 'd'
        if py_version < (3, 8):
            with_pymalloc = sysconfig.get_config_var('WITH_PYMALLOC')
            if with_pymalloc or with_pymalloc is None:
                pymalloc = 'm'
            if py_version < (3, 3):
                unicode_size = sysconfig.get_config_var('Py_UNICODE_SIZE')
                if not unicode_size == 4:
                    if not unicode_size is None or sys.maxunicode == 1114111:
                        ucs4 = 'u'
    elif debug:
        abis.append('cp{version}'.format(version=version))
    abis.insert(0, 'cp{version}{debug}{pymalloc}{ucs4}'.format(version=version,
      debug=debug,
      pymalloc=pymalloc,
      ucs4=ucs4))
    return abis


def _cpython_tags(py_version, interpreter, abis, platforms):
    for abi in abis:
        for platform_ in platforms:
            yield Tag(interpreter, abi, platform_)

    for tag in (Tag(interpreter, 'abi3', platform_) for platform_ in platforms):
        yield tag

    for tag in (Tag(interpreter, 'none', platform_) for platform_ in platforms):
        yield tag

    for minor_version in range(py_version[1] - 1, 1, -1):
        for platform_ in platforms:
            interpreter = 'cp{major}{minor}'.format(major=(py_version[0]),
              minor=minor_version)
            yield Tag(interpreter, 'abi3', platform_)


def _pypy_interpreter():
    return 'pp{py_major}{pypy_major}{pypy_minor}'.format(py_major=(sys.version_info[0]),
      pypy_major=(sys.pypy_version_info.major),
      pypy_minor=(sys.pypy_version_info.minor))


def _generic_abi():
    abi = sysconfig.get_config_var('SOABI')
    if abi:
        return _normalize_string(abi)
    return 'none'


def _pypy_tags(py_version, interpreter, abi, platforms):
    for tag in (Tag(interpreter, abi, platform) for platform in platforms):
        yield tag

    for tag in (Tag(interpreter, 'none', platform) for platform in platforms):
        yield tag


def _generic_tags(interpreter, py_version, abi, platforms):
    for tag in (Tag(interpreter, abi, platform) for platform in platforms):
        yield tag

    if abi != 'none':
        tags = (Tag(interpreter, 'none', platform_) for platform_ in platforms)
        for tag in tags:
            yield tag


def _py_interpreter_range(py_version):
    """
    Yield Python versions in descending order.

    After the latest version, the major-only version will be yielded, and then
    all following versions up to 'end'.
    """
    yield 'py{major}{minor}'.format(major=(py_version[0]), minor=(py_version[1]))
    yield 'py{major}'.format(major=(py_version[0]))
    for minor in range(py_version[1] - 1, -1, -1):
        yield 'py{major}{minor}'.format(major=(py_version[0]), minor=minor)


def _independent_tags(interpreter, py_version, platforms):
    """
    Return the sequence of tags that are consistent across implementations.

    The tags consist of:
    - py*-none-<platform>
    - <interpreter>-none-any
    - py*-none-any
    """
    for version in _py_interpreter_range(py_version):
        for platform_ in platforms:
            yield Tag(version, 'none', platform_)

    yield Tag(interpreter, 'none', 'any')
    for version in _py_interpreter_range(py_version):
        yield Tag(version, 'none', 'any')


def _mac_arch(arch, is_32bit=_32_BIT_INTERPRETER):
    if not is_32bit:
        return arch
    if arch.startswith('ppc'):
        return 'ppc'
    return 'i386'


def _mac_binary_formats(version, cpu_arch):
    formats = [
     cpu_arch]
    if cpu_arch == 'x86_64':
        if version < (10, 4):
            return []
        formats.extend(['intel', 'fat64', 'fat32'])
    else:
        if cpu_arch == 'i386':
            if version < (10, 4):
                return []
            formats.extend(['intel', 'fat32', 'fat'])
        else:
            if cpu_arch == 'ppc64' and not version > (10, 5):
                if version < (10, 4):
                    return []
                formats.append('fat64')
            else:
                if cpu_arch == 'ppc':
                    if version > (10, 6):
                        return []
                    formats.extend(['fat32', 'fat'])
    formats.append('universal')
    return formats


def _mac_platforms(version=None, arch=None):
    version_str, _, cpu_arch = platform.mac_ver()
    if version is None:
        version = tuple(map(int, version_str.split('.')[:2]))
    if arch is None:
        arch = _mac_arch(cpu_arch)
    platforms = []
    for minor_version in range(version[1], -1, -1):
        compat_version = (
         version[0], minor_version)
        binary_formats = _mac_binary_formats(compat_version, arch)
        for binary_format in binary_formats:
            platforms.append('macosx_{major}_{minor}_{binary_format}'.format(major=(compat_version[0]),
              minor=(compat_version[1]),
              binary_format=binary_format))

    return platforms


def _is_manylinux_compatible(name, glibc_version):
    try:
        import _manylinux
        return bool(getattr(_manylinux, name + '_compatible'))
    except (ImportError, AttributeError):
        pass

    return _have_compatible_glibc(*glibc_version)


def _glibc_version_string():
    import ctypes
    process_namespace = ctypes.CDLL(None)
    try:
        gnu_get_libc_version = process_namespace.gnu_get_libc_version
    except AttributeError:
        return
    else:
        gnu_get_libc_version.restype = ctypes.c_char_p
        version_str = gnu_get_libc_version()
        if not isinstance(version_str, str):
            version_str = version_str.decode('ascii')
        return version_str


def _check_glibc_version(version_str, required_major, minimum_minor):
    m = re.match('(?P<major>[0-9]+)\\.(?P<minor>[0-9]+)', version_str)
    if not m:
        warnings.warn('Expected glibc version with 2 components major.minor, got: %s' % version_str, RuntimeWarning)
        return False
    return int(m.group('major')) == required_major and int(m.group('minor')) >= minimum_minor


def _have_compatible_glibc(required_major, minimum_minor):
    version_str = _glibc_version_string()
    if version_str is None:
        return False
    return _check_glibc_version(version_str, required_major, minimum_minor)


def _linux_platforms(is_32bit=_32_BIT_INTERPRETER):
    linux = _normalize_string(distutils.util.get_platform())
    if linux == 'linux_x86_64':
        if is_32bit:
            linux = 'linux_i686'
    manylinux_support = (('manylinux2014', (2, 17)), ('manylinux2010', (2, 12)), ('manylinux1', (2, 5)))
    manylinux_support_iter = iter(manylinux_support)
    for name, glibc_version in manylinux_support_iter:
        if _is_manylinux_compatible(name, glibc_version):
            platforms = [
             linux.replace('linux', name)]
            break
    else:
        platforms = []

    platforms += [linux.replace('linux', name) for name, _ in manylinux_support_iter]
    platforms.append(linux)
    return platforms


def _generic_platforms():
    platform = _normalize_string(distutils.util.get_platform())
    return [platform]


def _interpreter_name():
    name = platform.python_implementation().lower()
    return INTERPRETER_SHORT_NAMES.get(name) or name


def _generic_interpreter(name, py_version):
    version = sysconfig.get_config_var('py_version_nodot')
    if not version:
        version = ''.join(map(str, py_version[:2]))
    return '{name}{version}'.format(name=name, version=version)


def sys_tags():
    """
    Returns the sequence of tag triples for the running interpreter.

    The order of the sequence corresponds to priority order for the
    interpreter, from most to least important.
    """
    py_version = sys.version_info[:2]
    interpreter_name = _interpreter_name()
    if platform.system() == 'Darwin':
        platforms = _mac_platforms()
    else:
        if platform.system() == 'Linux':
            platforms = _linux_platforms()
        else:
            platforms = _generic_platforms()
    if interpreter_name == 'cp':
        interpreter = _cpython_interpreter(py_version)
        abis = _cpython_abis(py_version)
        for tag in _cpython_tags(py_version, interpreter, abis, platforms):
            yield tag

    else:
        if interpreter_name == 'pp':
            interpreter = _pypy_interpreter()
            abi = _generic_abi()
            for tag in _pypy_tags(py_version, interpreter, abi, platforms):
                yield tag

        else:
            interpreter = _generic_interpreter(interpreter_name, py_version)
            abi = _generic_abi()
            for tag in _generic_tags(interpreter, py_version, abi, platforms):
                yield tag

    for tag in _independent_tags(interpreter, py_version, platforms):
        yield tag