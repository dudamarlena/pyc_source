# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/os_release.py
# Compiled at: 2019-05-16 13:41:33
"""
OsRelease - file ``/etc/os-release``
====================================

This module provides plugins access to file ``/etc/os-release``.

Typical content of file ``/etc/os-release`` is::

    NAME="Red Hat Enterprise Linux Server"
    VERSION="7.2 (Maipo)"
    ID="rhel"
    ID_LIKE="fedora"
    VERSION_ID="7.2"
    PRETTY_NAME="Employee SKU"
    ANSI_COLOR="0;31"
    CPE_NAME="cpe:/o:redhat:enterprise_linux:7.2:GA:server"
    HOME_URL="https://www.redhat.com/"
    BUG_REPORT_URL="https://bugzilla.redhat.com/"

    REDHAT_BUGZILLA_PRODUCT="Red Hat Enterprise Linux 7"
    REDHAT_BUGZILLA_PRODUCT_VERSION=7.2
    REDHAT_SUPPORT_PRODUCT="Red Hat Enterprise Linux"
    REDHAT_SUPPORT_PRODUCT_VERSION="7.2"

Note:
    The /etc/os-release is not exist in RHEL6 and prior versions.

This module parses the file content and stores it as a `dict` in the `data`
attribute.

Examples:
    >>> os_rls_content = '''
    ... Red Hat Enterprise Linux Server release 7.2 (Maipo)
    ... '''.strip()
    >>> from insights.tests import context_wrap
    >>> shared = {OsRelease: OsRelease(context_wrap(os_rls_content))}
    >>> rls = shared[OsRelease]
    >>> data = rls.data
    >>> assert data.get("VARIANT_ID") is None
    >>> assert data.get("VERSION") == "7.2 (Maipo)"
"""
from .. import Parser, parser, get_active_lines, LegacyItemAccess
from insights.specs import Specs

@parser(Specs.os_release)
class OsRelease(LegacyItemAccess, Parser):
    """Parses the content of file ``/etc/os-release``."""

    def parse_content(self, content):
        data = {}
        for line in get_active_lines(content):
            k, _, v = line.partition('=')
            if _ == '=' and k:
                data[k] = v.strip('"') if v else None

        self.data = data
        return