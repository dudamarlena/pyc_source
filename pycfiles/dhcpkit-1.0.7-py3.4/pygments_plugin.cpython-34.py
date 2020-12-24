# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/ipv6/server/pygments_plugin.py
# Compiled at: 2016-12-12 22:28:22
# Size of source mod 2**32: 1465 bytes
"""
Extensions to Pygments to correctly parse DHCPKit config files
"""
import re
from pygments.lexer import RegexLexer, bygroups
from pygments.token import Comment, Keyword, Name, String, Text
__all__ = [
 'DHCPKitConfLexer']

class DHCPKitConfLexer(RegexLexer):
    __doc__ = '\n    Lexer for configuration files following the DHCPKit config file format.\n    '
    name = 'DHCPKitConf'
    aliases = ['dhcpkitconf', 'dhcpkit']
    flags = re.MULTILINE | re.IGNORECASE
    tokens = {'root': [
              (
               '\\s+', Text),
              (
               '(#.*?)$', Comment),
              (
               '(<[^\\s>]+)(?:(\\s+)(.*?))?(>)',
               bygroups(Name.Tag, Text, String, Name.Tag)),
              (
               '([a-z][\\w-]*)(\\s+)',
               bygroups(Name.Builtin, Text), 'value'),
              (
               '\\.+', Text)], 
     'value': [
               (
                '\\\\\\n', Text),
               (
                '$', Text, '#pop'),
               (
                '\\\\', Text),
               (
                '[^\\S\\n]+', Text),
               (
                '/([a-z0-9][\\w./-]+)', String.Other),
               (
                '(on|off|yes|no|true|false|critical|error|warn|warning|info|debug-packets|debug-handling|debug|notset|authpriv|auth|cron|daemon|ftp|kern|lpr|mail|news|security|syslog|uucp|local[0-7]|udp|dgram|tcp|stream|hourly|hour|daily|day|weekly|week|size|user|group)\\b',
                Keyword),
               (
                '"([^"\\\\]*(?:\\\\.[^"\\\\]*)*)"', String.Double),
               (
                '[^\\s"\\\\]+', Text)]}