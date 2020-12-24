# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/hsi_ndapi.py
# Compiled at: 2009-12-08 17:43:28
"""
Parse HSI ndapid log files
eg.
Tue Oct 21 06:05:04 2008 gonzo.nersc.gov[18694] hsi: 17717 28074 Username: welcome  UID: 17717  Acct: 17717(17717) Copies: 1 Firewall: off [hsi.3.4.1 Tue Aug 26 15:45:21 PDT 2008][V3.4.1_2008_08_26.01] 

"""
__author__ = 'Shreyas Cholia scholia@lbl.gov'
__rcsid__ = '$Id: hsi.py 1030 2008-09-12 19:52:45Z shreyas $'
from logging import DEBUG
import re, time
from netlogger.parsers.base import BaseParser

class Parser(BaseParser):
    """Parse HSI ndapid log files
    """

    def __init__(self, f, **kwargs):
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)

    def process(self, line):
        try:
            parsed_ts = time.strptime(line[:24])
        except ValueError:
            self.log.debug('Bad Time Format: ' + line)
            return ()
        else:
            ts = time.mktime(parsed_ts)
            fields = line.split(' ', 7)
            pattern = re.compile('(.*)\\[(\\d+)\\]')
            (hostname, pid) = pattern.match(fields[5]).groups()
            util = fields[6].rstrip(':')
            log_msg = fields[7]
            pattern = re.compile('(\\d+) (\\d+) Username: (.+) UID: (\\d+)')
            if pattern.match(log_msg):
                user = pattern.search(log_msg).group(3).strip()
                uid = pattern.search(log_msg).group(4)
                result = ({'ts': ts, 'event': 'hsi.event', 'hostname': hostname, 'pid': pid, 'util': util, 'msg': log_msg, 'user': user, 'uid': uid},)
            result = ({'ts': ts, 'event': 'hsi.event', 'hostname': hostname, 'pid': pid, 'util': util, 'msg': log_msg},)

        return result