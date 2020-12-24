# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/entrypoints/entrypoints.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 8262 bytes
"""Discover and load entry points from installed packages."""
from contextlib import contextmanager
import glob
from importlib import import_module
import io, itertools, os.path as osp, re, sys, warnings, zipfile
if sys.version_info[0] >= 3:
    import configparser
else:
    from backports import configparser
entry_point_pattern = re.compile('\n(?P<modulename>\\w+(\\.\\w+)*)\n(:(?P<objectname>\\w+(\\.\\w+)*))?\n\\s*\n(\\[(?P<extras>.+)\\])?\n$\n', re.VERBOSE)
file_in_zip_pattern = re.compile('\n(?P<dist_version>[^/\\\\]+)\\.(dist|egg)-info\n[/\\\\]entry_points.txt$\n', re.VERBOSE)
__version__ = '0.3'

class BadEntryPoint(Exception):
    __doc__ = "Raised when an entry point can't be parsed.\n    "

    def __init__(self, epstr):
        self.epstr = epstr

    def __str__(self):
        return "Couldn't parse entry point spec: %r" % self.epstr

    @staticmethod
    @contextmanager
    def err_to_warnings():
        try:
            yield
        except BadEntryPoint as e:
            warnings.warn(str(e))


class NoSuchEntryPoint(Exception):
    __doc__ = 'Raised by :func:`get_single` when no matching entry point is found.'

    def __init__(self, group, name):
        self.group = group
        self.name = name

    def __str__(self):
        return 'No {!r} entry point found in group {!r}'.format(self.name, self.group)


class CaseSensitiveConfigParser(configparser.ConfigParser):
    optionxform = staticmethod(str)


class EntryPoint(object):

    def __init__(self, name, module_name, object_name, extras=None, distro=None):
        self.name = name
        self.module_name = module_name
        self.object_name = object_name
        self.extras = extras
        self.distro = distro

    def __repr__(self):
        return 'EntryPoint(%r, %r, %r, %r)' % (
         self.name, self.module_name, self.object_name, self.distro)

    def load(self):
        """Load the object to which this entry point refers.
        """
        mod = import_module(self.module_name)
        obj = mod
        if self.object_name:
            for attr in self.object_name.split('.'):
                obj = getattr(obj, attr)

        return obj

    @classmethod
    def from_string(cls, epstr, name, distro=None):
        """Parse an entry point from the syntax in entry_points.txt

        :param str epstr: The entry point string (not including 'name =')
        :param str name: The name of this entry point
        :param Distribution distro: The distribution in which the entry point was found
        :rtype: EntryPoint
        :raises BadEntryPoint: if *epstr* can't be parsed as an entry point.
        """
        m = entry_point_pattern.match(epstr)
        if m:
            mod, obj, extras = m.group('modulename', 'objectname', 'extras')
            if extras is not None:
                extras = re.split(',\\s*', extras)
            return cls(name, mod, obj, extras, distro)
        raise BadEntryPoint(epstr)


class Distribution(object):

    def __init__(self, name, version):
        self.name = name
        self.version = version

    def __repr__(self):
        return 'Distribution(%r, %r)' % (self.name, self.version)


def iter_files_distros(path=None, repeated_distro='first'):
    if path is None:
        path = sys.path
    distro_names_seen = set()
    for folder in path:
        if folder.rstrip('/\\').endswith('.egg'):
            egg_name = osp.basename(folder)
            if '-' in egg_name:
                distro = Distribution(*egg_name.split('-')[:2])
                if repeated_distro == 'first':
                    if distro.name in distro_names_seen:
                        continue
                distro_names_seen.add(distro.name)
            else:
                distro = None
            if osp.isdir(folder):
                ep_path = osp.join(folder, 'EGG-INFO', 'entry_points.txt')
                if osp.isfile(ep_path):
                    cp = CaseSensitiveConfigParser(delimiters=('=', ))
                    cp.read([ep_path])
                    yield (cp, distro)
            else:
                if zipfile.is_zipfile(folder):
                    z = zipfile.ZipFile(folder)
                    try:
                        info = z.getinfo('EGG-INFO/entry_points.txt')
                    except KeyError:
                        continue

                    cp = CaseSensitiveConfigParser(delimiters=('=', ))
                    with z.open(info) as (f):
                        fu = io.TextIOWrapper(f)
                        cp.read_file(fu, source=(osp.join(folder, 'EGG-INFO', 'entry_points.txt')))
                    yield (
                     cp, distro)
        else:
            if zipfile.is_zipfile(folder):
                with zipfile.ZipFile(folder) as (zf):
                    for info in zf.infolist():
                        m = file_in_zip_pattern.match(info.filename)
                        if not m:
                            pass
                        else:
                            distro_name_version = m.group('dist_version')
                            if '-' in distro_name_version:
                                distro = Distribution(*distro_name_version.split('-', 1))
                                if repeated_distro == 'first':
                                    if distro.name in distro_names_seen:
                                        continue
                                distro_names_seen.add(distro.name)
                            else:
                                distro = None
                            cp = CaseSensitiveConfigParser(delimiters=('=', ))
                            with zf.open(info) as (f):
                                fu = io.TextIOWrapper(f)
                                cp.read_file(fu, source=(osp.join(folder, info.filename)))
                            yield (
                             cp, distro)

        for path in itertools.chain(glob.iglob(osp.join(folder, '*.dist-info', 'entry_points.txt')), glob.iglob(osp.join(folder, '*.egg-info', 'entry_points.txt'))):
            distro_name_version = osp.splitext(osp.basename(osp.dirname(path)))[0]
            if '-' in distro_name_version:
                distro = Distribution(*distro_name_version.split('-', 1))
                if repeated_distro == 'first':
                    if distro.name in distro_names_seen:
                        continue
                distro_names_seen.add(distro.name)
            else:
                distro = None
            cp = CaseSensitiveConfigParser(delimiters=('=', ))
            cp.read([path])
            yield (cp, distro)


def get_single(group, name, path=None):
    """Find a single entry point.

    Returns an :class:`EntryPoint` object, or raises :exc:`NoSuchEntryPoint`
    if no match is found.
    """
    for config, distro in iter_files_distros(path=path):
        if group in config and name in config[group]:
            epstr = config[group][name]
            with BadEntryPoint.err_to_warnings():
                return EntryPoint.from_string(epstr, name, distro)

    raise NoSuchEntryPoint(group, name)


def get_group_named(group, path=None):
    """Find a group of entry points with unique names.

    Returns a dictionary of names to :class:`EntryPoint` objects.
    """
    result = {}
    for ep in get_group_all(group, path=path):
        if ep.name not in result:
            result[ep.name] = ep

    return result


def get_group_all(group, path=None):
    """Find all entry points in a group.

    Returns a list of :class:`EntryPoint` objects.
    """
    result = []
    for config, distro in iter_files_distros(path=path):
        if group in config:
            for name, epstr in config[group].items():
                with BadEntryPoint.err_to_warnings():
                    result.append(EntryPoint.from_string(epstr, name, distro))

    return result


if __name__ == '__main__':
    import pprint
    pprint.pprint(get_group_all('console_scripts'))