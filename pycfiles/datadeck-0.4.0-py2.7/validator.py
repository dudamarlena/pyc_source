# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/datadeck/gui/util/validator.py
# Compiled at: 2011-11-23 15:46:10
"""
Tools for handling validation of Packages
"""
__author__ = 'dgraziotin'
import dpm, dpm.lib, os

class PackageNonValid(Exception):

    def __init__(self, message, missing_fields=None):
        Exception.__init__(self, message)
        self.missing_fields = missing_fields

    def __str__(self):
        return repr(self.message + self.missing_fields)


class PackageValidator(object):
    """
    Validates a Package to be submitted to CKAN
    """
    MANDATORY_FIELDS = ('name', 'title')

    @classmethod
    def validate(cls, package):
        for field in PackageValidator.MANDATORY_FIELDS:
            attribute = getattr(package, field, None)
            if not attribute:
                raise PackageNonValid('Package misses a mandatory field: ', field)

        return True

    @classmethod
    def already_existing(cls, path, package_name):
        try:
            dpm.lib.load(os.path.join(path, package_name))
        except dpm.DatapkgException:
            return False

        return True