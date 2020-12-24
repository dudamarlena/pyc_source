# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sealert.py
# Compiled at: 2019-12-13 11:35:35
from insights.parsers import SkipException
from insights.tests import context_wrap
from insights.parsers.sealert import Sealert, Report
import pytest
INPUT_1 = ('\nbla bla\nble ble\n').strip()
REPORT_1 = ('\nSELinux is preventing rngd from using the dac_override capability.\n\n\n*****  Plugin dac_override (91.4 confidence) suggests **********************\n\nIf you want to help identify if domain needs this access or you have a file with the wrong permissions on your system\nThen turn on full auditing to get path information about the offending file and generate the error again.\nDo\n\nTurn on full auditing\n# auditctl -w /etc/shadow -p w\nTry to recreate AVC. Then execute\n# ausearch -m avc -ts recent\nIf you see PATH record check ownership/permissions on file, and fix it,\notherwise report as a bugzilla.\n\n*****  Plugin catchall (9.59 confidence) suggests **************************\n\nIf you believe that rngd should have the dac_override capability by default.\nThen you should report this as a bug.\nYou can generate a local policy module to allow this access.\nDo\nallow this access for now by executing:\n# ausearch -c \'rngd\' --raw | audit2allow -M my-rngd\n# semodule -X 300 -i my-rngd.pp\n\n\nAdditional Information:\nSource Context                system_u:system_r:rngd_t:s0\nTarget Context                system_u:system_r:rngd_t:s0\nTarget Objects                Unknown [ capability ]\nSource                        rngd\nSource Path                   rngd\nPort                          <Unknown>\nHost                          localhost.localdomain\nSource RPM Packages\nTarget RPM Packages\nPolicy RPM                    selinux-policy-3.14.1-54.fc28.noarch\nSelinux Enabled               True\nPolicy Type                   targeted\nEnforcing Mode                Enforcing\nHost Name                     localhost.localdomain\nPlatform                      Linux localhost.localdomain 4.20.7-100.fc28.x86_64\n                              #1 SMP Wed Feb 6 19:17:09 UTC 2019 x86_64 x86_64\nAlert Count                   10\nFirst Seen                    2019-03-08 13:09:05 CET\nLast Seen                     2019-07-01 15:28:18 CEST\nLocal ID                      a81fca67-2c8d-4cb1-b1c2-a97c0521858d\n\nRaw Audit Messages\ntype=AVC msg=audit(1561987698.393:103): avc:  denied  { dac_override } for  pid=1084 comm="rngd" capability=1 scontext=system_u:system_r:rngd_t:s0 tcontext=system_u:system_r:rngd_t:s0 tclass=capability permissive=0\n\n\nHash: rngd,rngd_t,rngd_t,capability,dac_override\n\n').strip()
REPORT_2 = ('\nSELinux is preventing sh from entrypoint access on the file /usr/bin/podman.\n\n*****  Plugin catchall (100. confidence) suggests **************************\n\nIf you believe that sh should be allowed entrypoint access on the podman file by default.\nThen you should report this as a bug.\nYou can generate a local policy module to allow this access.\nDo\nallow this access for now by executing:\n# ausearch -c \'sh\' --raw | audit2allow -M my-sh\n# semodule -X 300 -i my-sh.pp\n\n\nAdditional Information:\nSource Context unconfined_u:system_r:rpm_script_t:s0-s0:c0.c1023\nTarget Context system_u:object_r:container_runtime_exec_t:s0\nTarget Objects                /usr/bin/podman [ file ]\nSource                        sh\nSource Path                   sh\nPort                          <Unknown>\nHost                          localhost.localdomain\nSource RPM Packages\nTarget RPM Packages           podman-1.1.2-1.git0ad9b6b.fc28.x86_64\nPolicy RPM                    selinux-policy-3.14.1-54.fc28.noarch\nSelinux Enabled               True\nPolicy Type                   targeted\nEnforcing Mode                Enforcing\nHost Name                     localhost.localdomain\nPlatform                      Linux localhost.localdomain 4.20.7-100.fc28.x86_64\n                              #1 SMP Wed Feb 6 19:17:09 UTC 2019 x86_64 x86_64\nAlert Count                   1\nFirst Seen                    2019-07-30 11:15:04 CEST\nLast Seen                     2019-07-30 11:15:04 CEST\nLocal ID                      39a7094b-e402-4d87-9af9-e97eda41219a\n\nRaw Audit Messages\ntype=AVC msg=audit(1564478104.911:4631): avc:  denied  { entrypoint } for  pid=29402 comm="sh" path="/usr/bin/podman" dev="dm-1" ino=955465 scontext=unconfined_u:system_r:rpm_script_t:s0-s0:c0.c1023 tcontext=system_u:object_r:container_runtime_exec_t:s0 tclass=file permissive=0\n\n\nHash: sh,rpm_script_t,container_runtime_exec_t,file,entrypoint\n').strip()
INPUT_2 = ('\n\n{0}\n\n\n\n{1}\n\n').format(REPORT_1, REPORT_2)

def test_report():
    r = Report()
    r.append_line('')
    r.append_line('a')
    r.append_line('b')
    r.append_line('')
    r.append_line('')
    assert len(r.lines) == 5
    assert len(r.lines_stripped()) == 3
    assert r.lines_stripped() == ['', 'a', 'b']
    assert str(r) == 'a\nb'


def test_sealert():
    with pytest.raises(SkipException):
        Sealert(context_wrap(INPUT_1))
    with pytest.raises(SkipException):
        Sealert(context_wrap(''))
    sealert = Sealert(context_wrap(INPUT_2))
    assert len(sealert.reports) == 2
    assert str(sealert.reports[0]) == REPORT_1
    assert str(sealert.reports[1]) == REPORT_2
    assert sealert.reports[0].lines[10] == REPORT_1.split('\n')[10]
    assert sealert.reports[0].lines_stripped() == REPORT_1.split('\n')