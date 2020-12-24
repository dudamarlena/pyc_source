# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/easycluster/solaris_service.py
# Compiled at: 2019-04-18 17:28:18
import sys, os, signal, subprocess, traceback, tempfile, easycluster as _core
from easycluster import linux_service
if _core.PYTHON3:
    NAME = 'EasyCluster-Py3'
    SUFFIX = '-py3'
else:
    NAME = 'EasyCluster'
    SUFFIX = ''
KEY_PATH = '/etc/easycluster_service%s.key' % SUFFIX
SVC_NAME = 'network/easycluster%s' % SUFFIX
SERVICE_XML = '<?xml version="1.0"?>\n<!DOCTYPE service_bundle SYSTEM "/usr/share/lib/xml/dtd/service_bundle.dtd.1">\n<service_bundle type=\'manifest\' name=\'easycluster%(suffix)s\'>\n  <service name=\'network/easycluster%(suffix)s\' type=\'service\' version=\'1\'>\n    <create_default_instance enabled=\'false\' />\n\n    <single_instance />\n\n    <dependency name=\'fs-local\'\n\t\tgrouping=\'require_all\'\n\t\trestart_on=\'none\'\n\t\ttype=\'service\'>\n      <service_fmri\n          value=\'svc:/system/filesystem/local\' />\n    </dependency>\n\n    <dependency name=\'fs-autofs\'\n\t\tgrouping=\'optional_all\'\n\t\trestart_on=\'none\'\n\t\ttype=\'service\'>\n      <service_fmri value=\'svc:/system/filesystem/autofs\' />\n    </dependency>\n\n    <dependency name=\'net-loopback\'\n\t\tgrouping=\'require_all\'\n\t\trestart_on=\'none\'\n\t\ttype=\'service\'>\n      <service_fmri value=\'svc:/network/loopback\' />\n    </dependency>\n\n    <dependency name=\'net-physical\'\n\t\tgrouping=\'require_all\'\n\t\trestart_on=\'none\'\n\t\ttype=\'service\'>\n      <service_fmri value=\'svc:/network/physical:default\' />\n    </dependency>\n\n    <dependency name=\'utmp\'\n\t\tgrouping=\'require_all\'\n\t\trestart_on=\'none\'\n\t\ttype=\'service\'>\n      <service_fmri value=\'svc:/system/utmp\' />\n    </dependency>\n\n    <exec_method\n        type=\'method\'\n        name=\'start\'\n        exec=\'%(exe)s -m %(mod)s start\'\n        timeout_seconds=\'60\'/>\n\n    <exec_method\n        type=\'method\'\n        name=\'stop\'\n        exec=\'%(exe)s -m %(mod)s stop\'\n        timeout_seconds=\'60\' />\n\n    <exec_method\n        type=\'method\'\n        name=\'refresh\'\n        exec=\'%(exe)s -m %(mod)s restart\'\n        timeout_seconds=\'60\' />\n\n    <property_group name=\'sysconfig\' type=\'application\'>\n      <stability value=\'Unstable\' />\n      <propval name=\'group\' type=\'astring\' value=\'network\' />\n      <propval name=\'reconfigurable\' type=\'boolean\' value=\'true\' />\n    </property_group>\n\n    <stability value=\'Evolving\' />\n    <template>\n      <common_name>\n        <loctext xml:lang=\'C\'>\n          EasyCluster%(suffix)s\n        </loctext>\n      </common_name>\n    </template>\n  </service>\n</service_bundle>\n'

def check_call(prog):
    rc = subprocess.call(prog)
    if rc != 0:
        raise OSError('%s exited with code %d' % (prog[0], rc))


def install_service():
    xml = SERVICE_XML % dict(exe=sys.executable, mod=__name__, suffix=SUFFIX)
    if query_service_installed():
        return
    fd, temp_path = tempfile.mkstemp(suffix='.xml')
    os.write(fd, xml)
    os.close(fd)
    try:
        os.chmod(temp_path, 493)
        for prog in (['svccfg', 'validate', temp_path],
         [
          'svccfg', 'import', temp_path]):
            check_call(prog)

    finally:
        try:
            os.unlink(temp_path)
        except EnvironmentError:
            pass


def uninstall_service():
    if query_service_installed():
        check_call(['svcadm', 'disable', '-s', SVC_NAME])
        check_call(['svccfg', 'delete', SVC_NAME])


def start_service():
    rc, txt = _service_status()
    if rc == 0:
        if txt.startswith('online'):
            return
        if txt.startswith('maintenance'):
            check_call(['svcadm', 'clear', SVC_NAME])
        check_call(['svcadm', 'enable', '-s', SVC_NAME])
    else:
        raise OSError('EasyCluster service not installed')


def stop_service():
    if query_service_installed():
        check_call(['svcadm', 'disable', '-s', SVC_NAME])


def _service_status():
    proc = subprocess.Popen(['svcs', SVC_NAME], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    rc = proc.wait()
    return (rc, out.splitlines()[(-1)])


def query_service_installed():
    rc, out = _service_status()
    return rc == 0


if __name__ == '__main__':
    sys.exit(linux_service.init_main())