# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/hsi_xfer.py
# Compiled at: 2009-12-08 17:43:28
"""
Parse HSI transfer log files
eg:
Thu Nov 13 11:06:15 2008 gonzo.nersc.gov hsi 17717 22092        LH      0       0.11    200000000       19489.6 7       /proddata/mlw/hsi/hsi_081113_110500_200MB       /home/w/welcome/gonzo/hsi_Thu_11/hsi_081113_110500_200MB_0
Thu Nov 13 11:06:22 2008 gonzo.nersc.gov hsi 17717 22096        HL      0       0.08    200000000       40780.7 0       /dev/null       /home/w/welcome/gonzo/hsi_Thu_11/hsi_081113_110500_200MB_0

"""
__author__ = 'Shreyas Cholia scholia@lbl.gov'
__rcsid__ = '$Id: hsi.py 1030 2008-09-12 19:52:45Z shreyas $'
from logging import DEBUG
import re, time
from netlogger.parsers.base import BaseParser

class Parser(BaseParser):
    """Parse HSI transfer  log files.
    """

    def __init__(self, f, **kwargs):
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)

    def process(self, line):
        try:
            parsed_ts = time.strptime(line[:24])
        except ValueError:
            self.log.debug('Bad Time Format: ' + line)
            return ()

        ts = time.mktime(parsed_ts)
        fields = line.split(None, 16)
        (hostname, util, uid, pid, direction, result, open, data, rate, cos, local, hpss) = fields[5:]
        result = (
         {'ts': ts, 'event': 'hsi.xfer', 'hostname': hostname, 'util': util, 
            'uid': uid, 'pid': pid, 'direction': direction, 'result': result, 
            'open': open, 'data': data, 'rate': rate, 'cos': cos, 
            'local': local, 'hpss': hpss},)
        return result