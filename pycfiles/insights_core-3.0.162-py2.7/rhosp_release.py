# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/rhosp_release.py
# Compiled at: 2019-11-14 13:57:46
"""
RhospRelease - file ``/etc/rhosp-release``
==========================================

This module provides plugins access to file ``/etc/rhosp-release``

Typical content of file ``/etc/rhosp-release`` is::

    Red Hat OpenStack Platform release 14.0.0 RC (Rocky)

This module parses the file content and stores data in the dict ``self.release``
with keys ``product``, ``version``, and ``code_name``.

Examples:
    >>> release.product
    'Red Hat OpenStack Platform'
    >>> release.version
    '14.0.0'
    >>> release.code_name
    'Rocky'
"""
from insights import Parser, parser
from insights.specs import Specs

@parser(Specs.rhosp_release)
class RhospRelease(Parser):
    """Parses the content of file ``/etc/rhosp-release``."""

    def parse_content(self, content):
        product, _, version_name = [ v.strip() for v in content[0].partition('release') ]
        version_name_split = [ v.strip() for v in version_name.split(None, 1) ]
        self.release = {'product': product, 
           'version': version_name_split[0], 
           'code_name': version_name_split[1].split()[(-1)].strip('()')}
        return

    @property
    def version(self):
        """string: Version of RHOSP."""
        return self.release['version']

    @property
    def product(self):
        """string: Product full name."""
        return self.release['product']

    @property
    def code_name(self):
        """string: Release code name."""
        return self.release['code_name']