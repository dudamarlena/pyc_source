# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/simplified_dot_graph/line_parser.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 1483 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import re
from vipe.graphviz.simplified_dot_graph.connection import Connection

class LineParser:
    _LineParser__node_pattern = re.compile('\\s*"(?P<node>[^\\s"]+)"\\s*\\[.*')
    _LineParser__connection_pattern = re.compile('"(?P<start_node>[^\\s"]+)"(:"(?P<start_port>[^\\s"]+)")?\\s*->\\s*"(?P<end_node>[^\\s"]+)"(:"(?P<end_port>[^\\s"]+)")?.*')

    @staticmethod
    def parse_connection(line):
        match = LineParser._LineParser__connection_pattern.match(line)
        if match is None:
            return
        return Connection(match.group('start_node'), match.group('start_port'), match.group('end_node'), match.group('end_port'))

    @staticmethod
    def parse_node(line):
        match = LineParser._LineParser__node_pattern.match(line)
        if match is None:
            return
        return match.group('node')