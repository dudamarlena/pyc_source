# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/pluginconf_d.py
# Compiled at: 2019-05-16 13:41:33
from .. import Parser, parser, get_active_lines, LegacyItemAccess, IniConfigFile
from insights.specs import Specs

@parser(Specs.pluginconf_d)
class PluginConfD(LegacyItemAccess, Parser):
    """Class to parse configuration file under ``pluginconf.d``

    Attributes:
        data (dict): A dict likes
            {
                "main": {
                    "gpgcheck": "1",
                    "enabled": "0",
                    "timeout": "120"
                }
            }
    """

    def parse_content(self, content):
        """
        ---Sample---
        [main]
        enabled = 0
        gpgcheck = 1
        timeout = 120

        # You can specify options per channel, e.g.:
        #
        #[rhel-i386-server-5]
        #enabled = 1
        #
        #[some-unsigned-custom-channel]
        #gpgcheck = 0
        """
        plugin_dict = {}
        section_dict = {}
        key = None
        for line in get_active_lines(content):
            if line.startswith('['):
                section_dict = {}
                plugin_dict[line[1:-1]] = section_dict
            elif '=' in line:
                key, _, value = line.partition('=')
                key = key.strip()
                section_dict[key] = value.strip()
            elif key:
                section_dict[key] = (',').join([section_dict[key], line])

        self.data = plugin_dict
        return

    def __iter__(self):
        for sec in self.data:
            yield sec


@parser(Specs.pluginconf_d)
class PluginConfDIni(IniConfigFile):
    """
    Read yum plugin config files, in INI format, using the standard INI file
    parser class.
    """
    pass