# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/pymobiledevice/apps.py
# Compiled at: 2019-03-03 16:57:38
from __future__ import print_function
import os, warnings
from pymobiledevice.lockdown import LockdownClient
from pymobiledevice.afc import AFCClient, AFCShell
from optparse import OptionParser
warnings.warn('The libraries upon which this program depends will soon be deprecated in\nfavor of the house_arrest.py and installation_proxy.py libraries.\nSee those files for example program written using the new libraries.')

def house_arrest(lockdown, applicationId):
    try:
        mis = lockdown.startService('com.apple.mobile.house_arrest')
    except:
        lockdown = LockdownClient()
        mis = lockdown.startService('com.apple.mobile.house_arrest')

    if mis == None:
        return
    else:
        mis.sendPlist({'Command': 'VendDocuments', 'Identifier': applicationId})
        res = mis.recvPlist()
        if res.get('Error'):
            print('Unable to Lookup the selected application: You probably trying to access to a system app...')
            return
        return AFCClient(lockdown, service=mis)


def house_arrest_shell(lockdown, applicationId):
    afc = house_arrest(lockdown, applicationId)
    if afc:
        AFCShell(client=afc).cmdloop()


def mobile_install(lockdown, ipaPath):
    afc = AFCClient(lockdown)
    afc.set_file_contents('/' + os.path.basename(ipaPath), open(ipaPath, 'rb').read())
    mci = lockdown.startService('com.apple.mobile.installation_proxy')
    mci.sendPlist({'Command': 'Install', 'PackagePath': os.path.basename(ipaPath)})
    while True:
        z = mci.recvPlist()
        if not z:
            break
        completion = z.get('PercentComplete')
        if completion:
            print('Installing, %s: %s %% Complete' % (ipaPath, z['PercentComplete']))
        if z.get('Status') == 'Complete':
            print('Installation %s\n' % z['Status'])
            break


def list_apps(lockdown):
    mci = lockdown.startService('com.apple.mobile.installation_proxy')
    mci.sendPlist({'Command': 'Lookup'})
    res = mci.recvPlist()
    for app in res['LookupResult'].values():
        if app.get('ApplicationType') != 'System':
            print(app['CFBundleIdentifier'], '=>', app.get('Container'))
        else:
            print(app['CFBundleIdentifier'], '=> N/A')


def get_apps_BundleID(lockdown, appType='User'):
    appList = []
    mci = lockdown.startService('com.apple.mobile.installation_proxy')
    mci.sendPlist({'Command': 'Lookup'})
    res = mci.recvPlist()
    for app in res['LookupResult'].values():
        if app.get('ApplicationType') == appType:
            appList.append(app['CFBundleIdentifier'])

    mci.close()
    return appList


if __name__ == '__main__':
    parser = OptionParser(usage='%prog')
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False, help='List installed applications (non system apps)')
    parser.add_option('-a', '--app', dest='app', action='store', default=None, metavar='APPID', help='Access application files with AFC')
    parser.add_option('-i', '--install', dest='installapp', action='store', default=None, metavar='FILE', help='Install an application package')
    options, args = parser.parse_args()
    if options.list:
        lockdown = LockdownClient()
        list_apps(lockdown)
    elif options.app:
        lockdown = LockdownClient()
        house_arrest_shell(lockdown, options.app)
    elif options.installapp:
        lockdown = LockdownClient()
        mobile_install(lockdown, options.installapp)
    else:
        parser.print_help()