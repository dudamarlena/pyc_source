# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_systemid.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.systemid import SystemID
SYSTEMID = ('\n<?xml version="1.0"?>\n<params>\n<param>\n<value><struct>\n<member>\n<name>username</name>\n<value><string>testuser</string></value>\n</member>\n<member>\n<name>operating_system</name>\n<value><string>redhat-release-workstation</string></value>\n</member>\n<member>\n<name>description</name>\n<value><string>Initial Registration Parameters: OS: redhat-release-workstation Release: 6Workstation CPU Arch: x86_64</string></value>\n</member>\n<member>\n<name>checksum</name>\n<value><string>b493da72be7cfb7e54c1d58c6aa140c9</string></value>\n</member>\n<member>\n<name>profile_name</name>\n<value><string>example_profile</string></value>\n</member>\n<member>\n<name>system_id</name>\n<value><string>ID-example</string></value>\n</member>\n<member>\n<name>architecture</name>\n<value><string>x86_64</string></value>\n</member>\n<member>\n<name>os_release</name>\n<value><string>6Workstation</string></value>\n</member>\n<member>\n<name>fields</name>\n<value><array><data>\n<value><string>system_id</string></value>\n<value><string>os_release</string></value>\n<value><string>operating_system</string></value>\n<value><string>architecture</string></value>\n<value><string>username</string></value>\n<value><string>type</string></value>\n</data></array></value>\n</member>\n<member>\n<name>type</name>\n<value><string>REAL</string></value>\n</member>\n</struct></value>\n</param>\n</params>\n').strip()

def test_systemid():
    info = SystemID(context_wrap(SYSTEMID, path='/etc/sysconfig/rhn/systemid'))
    assert info.get('username') == 'testuser'
    assert info.get('operating_system') == 'redhat-release-workstation'
    assert info.get('description') == 'Initial Registration Parameters: OS: redhat-release-workstation Release: 6Workstation CPU Arch: x86_64'
    assert info.get('checksum') == 'b493da72be7cfb7e54c1d58c6aa140c9'
    assert info.get('profile_name') == 'example_profile'
    assert info.get('system_id') == 'ID-example'
    assert info.get('architecture') == 'x86_64'
    assert info.get('os_release') == '6Workstation'
    assert info.get('type') == 'REAL'
    assert info.file_name == 'systemid'
    assert info.file_path == '/etc/sysconfig/rhn/systemid'