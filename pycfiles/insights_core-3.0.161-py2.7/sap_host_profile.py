# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/sap_host_profile.py
# Compiled at: 2019-05-16 13:41:33
"""
SAPHostProfile - File ``/usr/sap/hostctrl/exe/host_profile``
============================================================

Shared parser for parsing the ``/usr/sap/hostctrl/exe/host_profile`` file.

"""
from .. import Parser, parser, LegacyItemAccess, get_active_lines, add_filter
from insights.parsers import SkipException
from insights.specs import Specs
filter_list = [
 'SAPSYSTEM', 'DIR_']
add_filter(Specs.sap_host_profile, filter_list)

@parser(Specs.sap_host_profile)
class SAPHostProfile(Parser, LegacyItemAccess):
    """
    Class for parsing the `/usr/sap/hostctrl/exe/host_profile` file.

    Typical content of the file is::

        SAPSYSTEMNAME = SAP
        SAPSYSTEM = 99
        service/porttypes = SAPHostControl SAPOscol SAPCCMS
        DIR_LIBRARY = /usr/sap/hostctrl/exe
        DIR_EXECUTABLE = /usr/sap/hostctrl/exe
        DIR_PROFILE = /usr/sap/hostctrl/exe
        DIR_GLOBAL = /usr/sap/hostctrl/exe
        DIR_INSTANCE = /usr/sap/hostctrl/exe
        DIR_HOME = /usr/sap/hostctrl/work

    Examples:
        >>> type(hpf)
        <class 'insights.parsers.sap_host_profile.SAPHostProfile'>
        >>> hpf['SAPSYSTEMNAME']
        'SAP'
        >>> hpf['DIR_HOME']
        '/usr/sap/hostctrl/work'
    """

    def parse_content(self, content):
        self.data = {}
        for line in get_active_lines(content):
            if '=' not in line:
                raise SkipException(("Incorrect line: '{0}'").format(line))
            key, val = line.split('=', 1)
            self.data[key.strip()] = val.strip()