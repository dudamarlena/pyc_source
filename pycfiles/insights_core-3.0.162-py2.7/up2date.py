# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/up2date.py
# Compiled at: 2019-05-16 13:41:33
from .. import Parser, parser, get_active_lines, LegacyItemAccess
from insights.specs import Specs
from insights.util import deprecated

@parser(Specs.up2date)
class Up2Date(LegacyItemAccess, Parser):
    """
    .. warning::
        This parser is deprecated, please use
        :py:class:`insights.parsers.sysconfig.Up2DateSysconfig` instead.

    Class to parse the ``up2date``

    Attributes:
        data (dict): A dict of up2date info which ignores comment lines.
        The first and second line for key word 'serverURL' will be ignored.

    For example:
        serverURL[comment]=Remote server URL
        #serverURL=https://rhnproxy.glb.tech.markit.partners/XMLRPC
        serverURL=https://rhnproxy.glb.tech.markit.partners/XMLRPC
    """

    def __init__(self, *args, **kwargs):
        deprecated(Up2Date, 'Import Up2DateSysconfig from insights.parsers.sysconfig instead')
        super(Up2Date, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        up2date_info = {}
        for line in get_active_lines(content):
            if '[comment]' not in line and '=' in line:
                key, val = line.split('=')
                up2date_info[key.strip()] = val.strip()

        self.data = up2date_info