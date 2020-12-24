# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_dracut_modules.py
# Compiled at: 2020-04-23 14:49:03
import doctest
from insights.tests import context_wrap
from insights.parsers import dracut_modules
from insights.parsers.dracut_modules import DracutModuleKdumpCaptureService
KDUMP_CAPTURE_SERVICE = ('\n[Unit]\nDescription=Kdump Vmcore Save Service\nAfter=dracut-initqueue.service dracut-pre-mount.service dracut-mount.service dracut-pre-pivot.service\nBefore=initrd-cleanup.service\nConditionPathExists=/etc/initrd-release\nOnFailure=emergency.target\nOnFailureIsolate=yes\n\n[Service]\nEnvironment=DRACUT_SYSTEMD=1\nEnvironment=NEWROOT=/sysroot\nType=oneshot\nExecStart=/bin/kdump.sh\nStandardInput=null\nStandardOutput=syslog\nStandardError=syslog+console\nKillMode=process\nRemainAfterExit=yes\n\n# Bash ignores SIGTERM, so we send SIGHUP instead, to ensure that bash\n# terminates cleanly.\nKillSignal=SIGHUP\n').strip()

def test_dracut_kdump_capture():
    kdump_service_conf = DracutModuleKdumpCaptureService(context_wrap(KDUMP_CAPTURE_SERVICE))
    assert 'Unit' in kdump_service_conf.sections()
    assert 'dracut-initqueue.service' in kdump_service_conf.get('Unit', 'After')


def test_doc():
    failed_count, tests = doctest.testmod(dracut_modules, globs={'config': dracut_modules.DracutModuleKdumpCaptureService(context_wrap(KDUMP_CAPTURE_SERVICE))})
    assert failed_count == 0