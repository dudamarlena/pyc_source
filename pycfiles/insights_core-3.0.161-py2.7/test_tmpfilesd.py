# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_tmpfilesd.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.tmpfilesd import TmpFilesD
from insights.tests import context_wrap
SAP_CONF = ('\n# systemd tmpfiles exclude file for SAP\n# SAP software stores some important files\n# in /tmp which should not be deleted\n\n# Exclude SAP socket and lock files\nx /tmp/.sap*\n\n# Exclude HANA lock file\nx /tmp/.hdb*lock\n').strip()

def test_tmpfilesd():
    ctx = context_wrap(SAP_CONF, path='/etc/tmpfiles.d/sap.conf')
    data = TmpFilesD(ctx)
    assert len(data.files) == 2
    assert data.files == ['/tmp/.sap*', '/tmp/.hdb*lock']
    assert data.rules == [
     {'type': 'x', 'mode': None, 
        'path': '/tmp/.sap*', 
        'uid': None, 
        'gid': None, 
        'age': None, 
        'argument': None},
     {'type': 'x', 'path': '/tmp/.hdb*lock', 
        'mode': None, 
        'uid': None, 
        'gid': None, 
        'age': None, 
        'argument': None}]
    assert data.file_path == '/etc/tmpfiles.d/sap.conf'
    assert data.file_name == 'sap.conf'
    return


def test_find_file():
    ctx = context_wrap(SAP_CONF, path='/etc/tmpfiles.d/sap.conf')
    data = TmpFilesD(ctx)
    assert data.find_file('.sap*') == [
     {'path': '/tmp/.sap*', 'type': 'x', 'mode': None, 'age': None, 
        'gid': None, 'uid': None, 'argument': None}]
    assert data.find_file('.hdb*lock') == [
     {'path': '/tmp/.hdb*lock', 'type': 'x', 'mode': None, 
        'uid': None, 'gid': None, 'age': None, 
        'argument': None}]
    assert data.find_file('bar') == []
    return