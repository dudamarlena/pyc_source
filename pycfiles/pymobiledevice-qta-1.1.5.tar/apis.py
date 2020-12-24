# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/apis.py
# Compiled at: 2019-02-28 19:19:12
__doc__ = '\nFile name: apis.py\nAuthor: dhilipsiva <dhilipsiva@gmail.com>\nDate created: 2016-06-19\n'
from os import path

def get_lockdown_and_service(udid):
    from pymobiledevice.lockdown import LockdownClient
    lockdown = LockdownClient(udid)
    service = lockdown.startService('com.apple.mobile.installation_proxy')
    return (
     lockdown, service)


def run_command(service, uuid, cmd):
    service.sendPlist(cmd)
    z = service.recvPlist()
    while 'PercentComplete' in z:
        if not z:
            break
        if z.get('Status') == 'Complete':
            return z.get('Status')
        z = service.recvPlist()

    service.close()
    return z


def install_ipa(uuid, ipa_path):
    """
    docstring for install_ipa
    """
    from pymobiledevice.afc import AFCClient
    lockdown, service = get_lockdown_and_service(uuid)
    afc = AFCClient(lockdown=lockdown)
    afc.set_file_contents(path.basename(ipa_path), open(ipa_path, 'rb').read())
    cmd = {'Command': 'Install', 'PackagePath': path.basename(ipa_path)}
    return run_command(service, uuid, cmd)


def uninstall_ipa(uuid, bundle_id):
    lockdown, service = get_lockdown_and_service(uuid)
    cmd = {'Command': 'Uninstall', 'ApplicationIdentifier': bundle_id}
    return run_command(service, uuid, cmd)


def list_ipas(uuid):
    lockdown, service = get_lockdown_and_service(uuid)
    cmd = {'Command': 'Lookup'}
    result = run_command(service, uuid, cmd)
    apps_details = result.get('LookupResult')
    apps = []
    for app in apps_details:
        if apps_details[app]['ApplicationType'] == 'User':
            apps.append(app)

    return apps