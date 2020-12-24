# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/journald_conf.py
# Compiled at: 2019-05-16 13:41:33
"""
Journald configuration files
============================

The journald.conf file is a key=value file with hash comments. Everything is in the [Journal]
section, so sections are ignored.

Only active settings lines are processed, commented out settings are not processed.

Active settings are provided using the `get_active_settings_value` method or
by using the dictionary `contains` functionality.

Options that are commented out are not returned - a rule using this parser has to be aware of which
default value is assumed by systemd if the particular option is not specified.

Note: Precedence logic is implemented in JournaldConfAll combiner, the parser is called for every
file separately.

Parsers provided by this module are:

EtcJournaldConf - file ``/etc/systemd/journald.conf``
-----------------------------------------------------

EtcJournaldConfD - file ``/etc/systemd/journald.conf.d/*.conf``
---------------------------------------------------------------

UsrJournaldConfD - file ``usr/lib/systemd/journald.conf.d/*.conf``
------------------------------------------------------------------

Example:

    >>> conf = shared[EtcJournaldConf]
    >>> conf.get_active_setting_value('Storage')
    'auto'
    >>> 'Storage' in conf.active_settings
    True
"""
from .. import Parser, parser, get_active_lines
from ..parsers import split_kv_pairs
from insights.specs import Specs

class JournaldConf(Parser):
    """
    A parser for accessing journald conf files.
    """

    def __init__(self, *args, **kwargs):
        self.active_lines_unparsed = []
        self.active_settings = {}
        super(JournaldConf, self).__init__(*args, **kwargs)

    def parse_content(self, content):
        """
        Main parsing class method which stores all interesting data from the content.

        Args:
            content (context.content): Parser context content
        """
        self.active_lines_unparsed = get_active_lines(content) if content is not None else []
        self.active_settings = split_kv_pairs(content, use_partition=False) if content is not None else []
        return

    def get_active_setting_value(self, setting_name):
        """
        Access active setting value by setting name.

        Args:
            setting_name (string): Setting name
        """
        return self.active_settings[setting_name]


@parser(Specs.etc_journald_conf)
class EtcJournaldConf(JournaldConf):
    """
    Parser for accessing the ``/etc/systemd/journald.conf`` file.
    """
    pass


@parser(Specs.etc_journald_conf_d)
class EtcJournaldConfD(JournaldConf):
    """
    Parser for accessing the ``/etc/systemd/journald.conf.d/*.conf`` files.
    """
    pass


@parser(Specs.usr_journald_conf_d)
class UsrJournaldConfD(JournaldConf):
    """
    Parser for accessing the ``usr/lib/systemd/journald.conf.d/*.conf`` files.
    """
    pass