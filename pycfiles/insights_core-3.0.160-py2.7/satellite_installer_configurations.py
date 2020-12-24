# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/satellite_installer_configurations.py
# Compiled at: 2020-03-25 13:10:41
"""
Satellite installer configuration files
=======================================

Parsers included in this module are:

CustomHiera - file ``/etc/foreman-installer/custom-hiera.yaml``
---------------------------------------------------------------
Parsers the file `/etc/foreman-installer/custom-hiera.yaml`

"""
from insights import parser, YAMLParser
from insights.specs import Specs
from insights.parsers import SkipException

@parser(Specs.satellite_custom_hiera)
class CustomHiera(YAMLParser):
    """
    Class to parse ``/etc/foreman-installer/custom-hiera.yaml``

    Examples:
        >>> 'apache::mod::prefork::serverlimit' in custom_hiera
        True
        >>> custom_hiera['apache::mod::prefork::serverlimit']
        582
    """

    def parse_content(self, content):
        try:
            super(CustomHiera, self).parse_content(content)
        except SkipException:
            pass