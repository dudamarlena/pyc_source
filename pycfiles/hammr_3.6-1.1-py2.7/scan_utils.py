# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hammr/utils/scan_utils.py
# Compiled at: 2016-12-15 07:34:25
from texttable import Texttable
from ussclicore.utils import generics_utils

def scan_status(scan):
    if scan.status.complete and not scan.status.error and not scan.status.cancelled:
        return 'Done'
    else:
        if not scan.status.complete and not scan.status.error and not scan.status.cancelled:
            return str(scan.status.percentage) + '%'
        return 'Error'


def scan_table(scanInstances, scan=None):
    table = Texttable(800)
    table.set_cols_dtype(['t', 't', 't', 't'])
    table.header(['Id', 'Name', 'Status', 'Distribution'])
    if scan:
        table.add_row([scan.dbId, '\t' + scan.name, scan_status(scan), ''])
        return table
    for myScannedInstance in scanInstances:
        table.add_row([myScannedInstance.dbId, myScannedInstance.name, '', myScannedInstance.distribution.name + ' ' + myScannedInstance.distribution.version + ' ' + myScannedInstance.distribution.arch])
        scans = generics_utils.order_list_object_by(myScannedInstance.scans.scan, 'name')
        for lscan in scans:
            table.add_row([lscan.dbId, '\t' + lscan.name, scan_status(lscan), ''])

    return table