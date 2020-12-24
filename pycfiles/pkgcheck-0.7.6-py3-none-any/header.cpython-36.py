# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/header.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 6508 bytes
"""Various file-based header checks."""
from snakeoil.demandload import demand_compile_regexp
from .. import base, results, sources
from . import GentooRepoCheck
demand_compile_regexp('copyright_regex', '^# Copyright (?P<begin>\\d{4}-)?(?P<end>\\d{4}) (?P<holder>.+)$')

class _FileHeaderResult(results.Result):
    __doc__ = 'Generic file header result.'

    def __init__(self, line, **kwargs):
        (super().__init__)(**kwargs)
        self.line = line


class InvalidCopyright(_FileHeaderResult, results.Error):
    __doc__ = 'File with invalid copyright.\n\n    The file does not start with a valid copyright line. Each ebuild or eclass\n    file must start with a copyright line of the form:\n\n        # Copyright YEARS MAIN-CONTRIBUTOR [OTHER-CONTRIBUTOR]... [and others]\n\n    Files in the Gentoo repository must use:\n\n        # Copyright YEARS Gentoo Authors\n    '
    _name = 'InvalidCopyright'

    @property
    def desc(self):
        return f"invalid copyright: {self.line!r}"


class OldGentooCopyright(_FileHeaderResult, results.Warning):
    __doc__ = "File with old Gentoo Foundation copyright.\n\n    The file still assigns copyright to the Gentoo Foundation even though\n    it has been committed after the new copyright policy was approved\n    (2018-10-21).\n\n    Ebuilds and eclasses in Gentoo repository must use 'Gentoo Authors'\n    instead. Files in other repositories may specify an explicit copyright\n    holder instead.\n    "
    _name = 'OldGentooCopyright'

    @property
    def desc(self):
        return f'old copyright, update to "Gentoo Authors": {self.line!r}'


class NonGentooAuthorsCopyright(_FileHeaderResult, results.Error):
    __doc__ = 'File with copyright stating owner other than "Gentoo Authors".\n\n    The file specifies explicit copyright owner, while the Gentoo repository\n    policy specifies that all ebuilds and eclasses must use "Gentoo Authors".\n    If the owner is not listed in metadata/AUTHORS, addition can be requested\n    via bugs.gentoo.org.\n    '
    _name = 'NonGentooAuthorsCopyright'

    @property
    def desc(self):
        return f'copyright line must state "Gentoo Authors": {self.line!r}'


class InvalidLicenseHeader(_FileHeaderResult, results.Error):
    __doc__ = 'File with invalid license header.\n\n    The file does not have with a valid license header.\n\n    Ebuilds and eclasses in the Gentoo repository must use:\n\n        # Distributed under the terms of the GNU General Public License v2\n    '
    _name = 'InvalidLicenseHeader'

    @property
    def desc(self):
        return f"invalid license header: {self.line!r}"


class _HeaderCheck(GentooRepoCheck):
    __doc__ = 'Scan files for incorrect copyright/license headers.'
    _invalid_copyright = InvalidCopyright
    _old_copyright = OldGentooCopyright
    _non_gentoo_authors = NonGentooAuthorsCopyright
    _invalid_license = InvalidLicenseHeader
    known_results = frozenset([
     _invalid_copyright, _old_copyright, _non_gentoo_authors, _invalid_license])
    _item_attr = 'pkg'
    license_header = '# Distributed under the terms of the GNU General Public License v2'

    def args(self, item):
        return {self._item_attr: item}

    def feed(self, item):
        if item.lines:
            line = item.lines[0].strip()
            copyright = copyright_regex.match(line)
            if copyright is None:
                yield (self._invalid_copyright)(line, **self.args(item))
            else:
                if int(copyright.group('end')) >= 2019:
                    if copyright.group('holder') == 'Gentoo Foundation':
                        yield (self._old_copyright)(line, **self.args(item))
                    elif copyright.group('holder') != 'Gentoo Authors':
                        yield (self._non_gentoo_authors)(line, **self.args(item))
                try:
                    line = item.lines[1].strip('\n')
                except IndexError:
                    line = ''

                if line != self.license_header:
                    yield (self._invalid_license)(line, **self.args(item))


class EbuildInvalidCopyright(InvalidCopyright, results.VersionResult):
    __doc__ = InvalidCopyright.__doc__


class EbuildOldGentooCopyright(OldGentooCopyright, results.VersionResult):
    __doc__ = OldGentooCopyright.__doc__


class EbuildNonGentooAuthorsCopyright(NonGentooAuthorsCopyright, results.VersionResult):
    __doc__ = NonGentooAuthorsCopyright.__doc__


class EbuildInvalidLicenseHeader(InvalidLicenseHeader, results.VersionResult):
    __doc__ = InvalidLicenseHeader.__doc__


class EbuildHeaderCheck(_HeaderCheck):
    __doc__ = 'Scan ebuild for incorrect copyright/license headers.'
    _source = sources.EbuildFileRepoSource
    _invalid_copyright = EbuildInvalidCopyright
    _old_copyright = EbuildOldGentooCopyright
    _non_gentoo_authors = EbuildNonGentooAuthorsCopyright
    _invalid_license = EbuildInvalidLicenseHeader
    known_results = frozenset([
     _invalid_copyright, _old_copyright, _non_gentoo_authors, _invalid_license])
    _item_attr = 'pkg'


class EclassInvalidCopyright(InvalidCopyright, results.EclassResult):
    __doc__ = InvalidCopyright.__doc__

    @property
    def desc(self):
        return f"{self.eclass}: {super().desc}"


class EclassOldGentooCopyright(OldGentooCopyright, results.EclassResult):
    __doc__ = OldGentooCopyright.__doc__

    @property
    def desc(self):
        return f"{self.eclass}: {super().desc}"


class EclassNonGentooAuthorsCopyright(NonGentooAuthorsCopyright, results.EclassResult):
    __doc__ = NonGentooAuthorsCopyright.__doc__

    @property
    def desc(self):
        return f"{self.eclass}: {super().desc}"


class EclassInvalidLicenseHeader(InvalidLicenseHeader, results.EclassResult):
    __doc__ = InvalidLicenseHeader.__doc__

    @property
    def desc(self):
        return f"{self.eclass}: {super().desc}"


class EclassHeaderCheck(_HeaderCheck):
    __doc__ = 'Scan eclasses for incorrect copyright/license headers.'
    scope = base.eclass_scope
    _source = sources.EclassRepoSource
    _invalid_copyright = EclassInvalidCopyright
    _old_copyright = EclassOldGentooCopyright
    _non_gentoo_authors = EclassNonGentooAuthorsCopyright
    _invalid_license = EclassInvalidLicenseHeader
    known_results = frozenset([
     _invalid_copyright, _old_copyright, _non_gentoo_authors, _invalid_license])
    _item_attr = 'eclass'