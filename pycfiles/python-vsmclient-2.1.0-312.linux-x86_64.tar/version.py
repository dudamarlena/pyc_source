# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/openstack/common/version.py
# Compiled at: 2016-06-13 14:11:03
"""
Utilities for consuming the version from pkg_resources.
"""
import pkg_resources

class VersionInfo(object):

    def __init__(self, package):
        """Object that understands versioning for a package
        :param package: name of the python package, such as glance, or
                        python-glanceclient
        """
        self.package = package
        self.release = None
        self.version = None
        self._cached_version = None
        return

    def __str__(self):
        """Make the VersionInfo object behave like a string."""
        return self.version_string()

    def __repr__(self):
        """Include the name."""
        return 'VersionInfo(%s:%s)' % (self.package, self.version_string())

    def _get_version_from_pkg_resources(self):
        """Get the version of the package from the pkg_resources record
        associated with the package."""
        try:
            requirement = pkg_resources.Requirement.parse(self.package)
            provider = pkg_resources.get_provider(requirement)
            return provider.version
        except pkg_resources.DistributionNotFound:
            from vsmclient.openstack.common import setup
            return setup.get_version(self.package)

    def release_string(self):
        """Return the full version of the package including suffixes indicating
        VCS status.
        """
        if self.release is None:
            self.release = self._get_version_from_pkg_resources()
        return self.release

    def version_string(self):
        """Return the short version minus any alpha/beta tags."""
        if self.version is None:
            parts = []
            for part in self.release_string().split('.'):
                if part[0].isdigit():
                    parts.append(part)
                else:
                    break

            self.version = ('.').join(parts)
        return self.version

    canonical_version_string = version_string
    version_string_with_vcs = release_string

    def cached_version_string(self, prefix=''):
        """Generate an object which will expand in a string context to
        the results of version_string(). We do this so that don't
        call into pkg_resources every time we start up a program when
        passing version information into the CONF constructor, but
        rather only do the calculation when and if a version is requested
        """
        if not self._cached_version:
            self._cached_version = '%s%s' % (prefix,
             self.version_string())
        return self._cached_version