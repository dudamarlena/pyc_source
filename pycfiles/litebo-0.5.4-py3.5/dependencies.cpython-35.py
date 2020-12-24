# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/litebo/utils/dependencies.py
# Compiled at: 2020-04-10 03:57:55
# Size of source mod 2**32: 3366 bytes
import importlib, pkg_resources, re
from distutils.version import LooseVersion
SUBPATTERN = '((?P<operation%d>==|>=|>|<)(?P<version%d>(\\d+)?(\\.[a-zA-Z0-9]+)?(\\.\\d+)?))'
RE_PATTERN = re.compile('^(?P<name>[\\w\\-]+)%s?(,%s)?$' % (SUBPATTERN % (1, 1), SUBPATTERN % (2, 2)))

def verify_packages(packages):
    if not packages:
        return
    if isinstance(packages, str):
        packages = packages.splitlines()
    for package in packages:
        if not package:
            pass
        else:
            match = RE_PATTERN.match(package)
            if match:
                name = match.group('name')
                for group_id in range(1, 3):
                    if 'operation%d' % group_id in match.groupdict():
                        operation = match.group('operation%d' % group_id)
                        version = match.group('version%d' % group_id)
                        _verify_package(name, operation, version)

            else:
                raise ValueError('Unable to read requirement: %s' % package)


def _verify_package(name, operation, version):
    try:
        module = pkg_resources.get_distribution(name)
        installed_version = LooseVersion(module.version)
    except pkg_resources.DistributionNotFound:
        try:
            module = importlib.import_module(name)
            installed_version = LooseVersion(module.__version__)
        except ImportError:
            raise MissingPackageError(name)

    if not operation:
        return
    required_version = LooseVersion(version)
    if operation == '==':
        check = required_version == installed_version
    else:
        if operation == '>':
            check = installed_version > required_version
        else:
            if operation == '<':
                check = installed_version < required_version
            else:
                if operation == '>=':
                    check = installed_version > required_version or installed_version == required_version
                else:
                    if operation == '<=':
                        check = installed_version < required_version or installed_version == required_version
                    else:
                        raise NotImplementedError("operation '%s' is not supported" % operation)
    if not check:
        raise IncorrectPackageVersionError(name, installed_version, operation, required_version)


class MissingPackageError(Exception):
    error_message = "Mandatory package '{name}' not found!"

    def __init__(self, package_name):
        self.package_name = package_name
        super(MissingPackageError, self).__init__(self.error_message.format(name=package_name))


class IncorrectPackageVersionError(Exception):
    error_message = "'{name} {installed_version}' version mismatch ({operation}{required_version})"

    def __init__(self, package_name, installed_version, operation, required_version):
        self.package_name = package_name
        self.installed_version = installed_version
        self.operation = operation
        self.required_version = required_version
        message = self.error_message.format(name=package_name, installed_version=installed_version, operation=operation, required_version=required_version)
        super(IncorrectPackageVersionError, self).__init__(message)