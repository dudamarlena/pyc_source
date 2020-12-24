# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eggbasket/validators.py
# Compiled at: 2008-07-13 16:55:56
import os
from os.path import exists, join
import turbogears as tg
from eggbasket.util import is_package_dir, is_package_file

class ValidPackage(tg.validators.FancyValidator):
    """Validator checking if a package name refers to a valid package directory.
    """
    messages = {'notFound': 'Package not found: %(package)s'}

    def _to_python(self, value, state):
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        if not is_package_dir(join(pkg_root, value)):
            if is_package_dir(join(pkg_root, value.lower())):
                value = value.lower()
            else:
                raise tg.validators.Invalid(self.message('notFound', state, package=value), value, state)
        return value


class ValidPackageFile(tg.validators.FancyValidator):
    """Validator checking if a file name refers to a valid package file.

    Must be used as a chained validator.
    """
    messages = {'notFound': 'Package file not found: %(filename)s'}

    def validate_python(self, value, state):
        filename = value['filename']
        pkg_root = tg.config.get('eggbasket.package_root', os.getcwd())
        pkg_dir = join(pkg_root, value['package'])
        pkg_file = join(pkg_dir, filename)
        if not exists(pkg_file) or not is_package_file(pkg_file):
            message = self.message('notFound', state, filename=filename)
            errors = dict(filename=message)
            raise tg.validators.Invalid(message, value, state, error_dict=errors)


class PackageFileSchema(tg.validators.Schema):
    """Schema for package file spec consisting of package and file name."""
    package = ValidPackage
    filename = tg.validators.UnicodeString
    chained_validators = [
     ValidPackageFile]


__all__ = [
 'PackageFileSchemaValidPackage',
 'ValidPackageFile']