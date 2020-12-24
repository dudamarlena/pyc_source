# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/DebTools/debtools/utils.py
# Compiled at: 2015-07-27 10:57:51
from __future__ import unicode_literals
from distutils.version import LooseVersion
import io, re, tarfile
try:
    import lzma
except ImportError:
    from backports import lzma

from debtools.ar import ArFile
__author__ = b'Matthieu Gallet'

def parse_control_data(control_data, continue_line=b' ', split=b': ', skip_after_blank=False):
    """ Parse a debian control file

    :param control_data:
    :type control_data: :class:`str`
    :param continue_line:
    :type continue_line: :class:`str`
    :param split:
    :type split: :class:`str`
    :param skip_after_blank:
    :type skip_after_blank: :class:`bool`
    :return:
    :rtype: :class:`dict`
    """
    offset = len(continue_line)
    result_data = {}
    key, value = (None, None)
    description = b''
    add_to_description = False
    for line in control_data.splitlines():
        if not line.split() and skip_after_blank:
            add_to_description = True
        if add_to_description:
            description += b'\n'
            description += line
            continue
        if not line or line[0:offset] == continue_line:
            if key is not None:
                value += b'\n'
                value += line[offset:]
        else:
            if key is not None:
                result_data[key] = value
            key, value = line.split(split, 1)
            value = value.lstrip()

    if key is not None:
        result_data[key] = value
    if add_to_description:
        result_data[b'description'] = description
    return result_data


def parse_deps(dep_string):
    """Parse the dependencies of a `.deb` package and return a dict, whose keys are packages names and values are a list of version constraints

     >>> parse_deps("python (>= 2.7), python (<< 2.8), python-stdeb, python-backports.lzma")
     {u'python': [(u'>=', LooseVersion ('2.7')), (u'<<', LooseVersion ('2.8'))], u'python-stdeb': [], u'python-backports.lzma': []}

    :param dep_string:
    :type dep_string: :class:`str`
    :return: dict, whose keys are packages names and values are a list of version constraints
    :rtype: :class:`dict`
    """
    deps = {}
    for dep_info in dep_string.split(b','):
        dep_info = dep_info.strip()
        matcher = re.match(b'^(.*)\\s+\\((>=|<<|>>|==|>=)\\s+(.*)\\)$', dep_info)
        if matcher:
            package_name = matcher.group(1)
            constraint_type = matcher.group(2)
            contraint_value = matcher.group(3)
            deps.setdefault(package_name, []).append((constraint_type, LooseVersion(contraint_value)))
        else:
            deps.setdefault(dep_info, [])

    return deps


def parse_dpkg(dpkg_string):
    """
    >>> parse_dpkg("ii  xfonts-utils     1:7.7~1   amd64  X Window System font utility programs")
    {u'xfonts-utils': LooseVersion ('1:7.7~1')}

    :param dpkg_string:
    :type dpkg_string: :class:`str`
    :return: dict of [package_name, package_version]
    :rtype: :class:`dict`
    """
    installed_packages = {}
    for line in dpkg_string.splitlines():
        matcher = re.match(b'^ii\\s+([^\\s]+)\\s+([^\\s]+)\\s+([^\\s]+)\\s+.*$', line)
        if not matcher:
            continue
        installed_packages[matcher.group(1)] = LooseVersion(matcher.group(2))

    return installed_packages


def check_version_constraint(version_1, op, version_2):
    """
    :param version_1:
    :type version_1: :class:`distutils.version.LooseVersion`
    :param op:
    :type op: :class:`str`
    :param version_2:
    :type version_2: :class:`distutils.version.LooseVersion`
    :return:
    :rtype:
    """
    if op == b'<=':
        return version_1 <= version_2
    if op == b'>=':
        return version_1 >= version_2
    if op == b'<<' or op == b'<':
        return version_1 < version_2
    if op == b'>>' or op == b'>':
        return version_1 > version_2
    if op == b'==' or op == b'=':
        return version_1 == version_2
    if op == b'!=' or op == b'<>':
        return version_1 != version_2
    raise ValueError(b'unknown operator %s %s %s' % (version_1, op, version_2))


def get_subfile(ar_file, name_regexp=b'control.tar.'):
    """Find the file whose names matches the given regexp
    :param ar_file:
    :type ar_file: :class:`ArFile`
    :param name_regexp:
    :type name_regexp: :class:`str`
    :return: the tuple (file descriptor, name)
    :rtype: :class:`tuple`
    """
    for name in ar_file.getnames():
        if re.match(name_regexp, name):
            return (ar_file.extractfile(name), name)

    return (None, None)


def get_control_data(filename):
    """ Extract control data from a `.deb` file
    A `.deb` is an `.ar` file that contains `control.tar.XXX`, that contains a `control` file.

    :param filename: complete filepath of a `.deb` file
    :type filename: :class:`str`
    :return:
    :rtype: :class:`dict`
    """
    deb_file = open(filename, mode=b'rb')
    ar_file = ArFile(filename, mode=b'r', fileobj=deb_file)
    control_file, control_file_name = get_subfile(ar_file, b'^control\\.tar\\..*$')
    mode = b'r:*'
    if control_file_name.endswith(b'.xz') or control_file_name.endswith(b'.lzma'):
        control_file_content = control_file.read()
        control_file_content_uncompressed = lzma.decompress(control_file_content)
        control_file.close()
        control_file = io.BytesIO(control_file_content_uncompressed)
        mode = b'r'
    tar_file = tarfile.open(name=b'control', mode=mode, fileobj=control_file)
    control_data = tar_file.extractfile(b'./control')
    control_data_value = control_data.read().decode(b'utf-8')
    control_data.close()
    tar_file.close()
    ar_file.close()
    deb_file.close()
    parsed_data = parse_control_data(control_data_value)
    return parsed_data