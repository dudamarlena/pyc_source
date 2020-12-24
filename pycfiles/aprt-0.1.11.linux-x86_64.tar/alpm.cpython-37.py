# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/aprt/alpm.py
# Compiled at: 2019-08-02 08:01:39
# Size of source mod 2**32: 4098 bytes
import libarchive, os
from .package import Package, package_from_name

def parse_alpm_dict(blob):
    """
        Parse a blob of text as ALPM file.
        The results are returned as a dictionary with each key having a list of values.
        """
    result = {}
    key = None
    values = []
    for line in blob.splitlines():
        if len(line) == 0:
            continue
        if line[0] == '%' and line[(-1)] == '%':
            if key is not None:
                result[key] = values
            key = line[1:-1]
            values = []
        else:
            values.append(line)

    if key is not None:
        result[key] = values
    return result


def parse_info_dict(blob):
    """
        Parse a blob of text as .PKGINFO or .BUILDINFO file.
        The results are returned as a dictionary with each key having a list of values.
        """
    result = {}
    for line in blob.splitlines():
        if not len(line) == 0:
            if line[0] == '#':
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            if key not in result:
                result[key] = [
                 value]
            else:
                result[key].append(value)

    return result


def alpm_dict_to_package(data):
    name = data['NAME'][0]
    package = Package(name)
    for key, values in data.items():
        package.add_values(key.lower(), values)

    return package


def read_package_archive(archive):
    data = {}
    pkginfo = False
    buildinfo = False
    for entry in archive:
        if entry.isdir:
            continue
        if entry.pathname == '.PKGINFO':
            pkginfo = True
        else:
            if entry.pathname == '.BUILDINFO':
                buildinfo = True
            else:
                continue
            data.update(parse_info_dict(''.join(map(lambda x: x.decode(), entry.get_blocks()))))
        if pkginfo and buildinfo:
            break

    if not pkginfo:
        raise RuntimeError('Found no .PKGINFO in archive.')
    if not buildinfo:
        raise RuntimeError('Found no .BUILDINFO in archive.')
    package = Package(data.pop('pkgname')[0])
    for key, values in data.items():
        package.add_values(key.lower(), values)

    return package


def read_package_file(filename):
    with libarchive.file_reader(filename) as (archive):
        return read_package_archive(archive)


def read_package_db_archive(archive):
    result = {}
    for entry in archive:
        if entry.isdir:
            continue
        else:
            package = package_from_name(os.path.dirname(entry.pathname))
            if package.name not in result:
                result[package.name] = package
            else:
                package = result[package.name]
        data = parse_alpm_dict(''.join(map(lambda x: x.decode(), entry.get_blocks())))
        for key, values in data.items():
            package.add_values(key.lower(), values)

    return result


def read_package_db_file(filename):
    with libarchive.file_reader(filename) as (archive):
        return read_package_db_archive(archive)