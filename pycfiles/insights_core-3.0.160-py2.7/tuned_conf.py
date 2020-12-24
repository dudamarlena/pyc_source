# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tuned_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
TunedConfIni - file ``/etc/tuned.conf``
=======================================
"""
from insights import IniConfigFile, parser, get_active_lines
from insights.specs import Specs

@parser(Specs.tuned_conf)
class TunedConfIni(IniConfigFile):
    """This class parses the ``/etc/tuned.conf`` file using the
    ``IniConfigFile`` base parser.

    Sample configuration file::

        #
        # Net tuning section
        #
        [NetTuning]
        # Enabled or disable the plugin. Default is True. Any other value
        # disables it.
        enabled=False

        #
        # CPU monitoring section
        #
        [CPUMonitor]
        # Enabled or disable the plugin. Default is True. Any other value
        # disables it.
        # enabled=False

    Examples:
        >>> 'NetTuning' in tuned_obj.sections()
        True
        >>> tuned_obj.get('NetTuning', 'enabled') == "False"
        True
        >>> tuned_obj.getboolean('NetTuning', 'enabled') == False
        True
        >>> sorted(tuned_obj.sections())==sorted(['CPUMonitor', 'NetTuning'])
        True
    """

    def parse_content(self, content, allow_no_value=True):
        content = get_active_lines(content)
        super(TunedConfIni, self).parse_content(content, allow_no_value)