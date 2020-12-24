# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_up2date.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import Up2DateSysconfig
from insights.tests import context_wrap
UP2DATE = "\n# Automatically generated Red Hat Update Agent config file, do not edit.\n# Format: 1.0\nretrieveOnly[comment]=Retrieve packages only\nretrieveOnly=0\n\n#noSSLServerURL[comment]=''\n#noSSLServerURL=http://192.168.160.23/XMLRPC\n\nwriteChangesToLog[comment]=Log to /var/log/up2date which packages has been added and removed\nwriteChangesToLog=0\n\nstagingContentWindow[comment]=How much forward we should look for future actions. In hours.\nstagingContentWindow=24\n\nnetworkRetries[comment]=Number of attempts to make at network connections before giving up\nnetworkRetries=5\n\nenableProxy[comment]=Use a HTTP Proxy\nenableProxy=0\n\nproxyPassword[comment]=The password to use for an authenticated proxy\nproxyPassword=\n\n*** of system id\nsystemIdPath=/etc/sysconfig/rhn/systemid\n\nuseNoSSLForPackages[comment]=Use the noSSLServerURL for package, package list, and header fetching (disable Akamai)\nuseNoSSLForPackages=0\n\ntmpDir[comment]=Use this Directory to place the temporary transport files\ntmpDir=/tmp\n\n#serverURL[comment]=Remote server URL\n#serverURL=http://192.168.160.23/XMLRPC\n\nskipNetwork[comment]=Skips network information in hardware profile sync during registration.\nskipNetwork=0\n\ndisallowConfChanges[comment]=Config options that can not be overwritten by a config update action\ndisallowConfChanges=noReboot;sslCACert;useNoSSLForPackages;noSSLServerURL;serverURL;disallowConfChanges;\n\n#sslCACert[comment]=The CA cert used to verify the ssl server\n#sslCACert=/usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT\n\nenableProxyAuth[comment]=To use an authenticated proxy or not\nenableProxyAuth=0\n\nversionOverride[comment]=Override the automatically determined system version\nversionOverride=\n\nstagingContent[comment]=Retrieve content of future actions in advance\nstagingContent=1\n\nproxyUser[comment]=The username for an authenticated proxy\nproxyUser=\n\nhostedWhitelist[comment]=RHN Hosted URL's\nhostedWhitelist=\n\ndebug[comment]=Whether or not debugging is enabled\ndebug=0\n\nhttpProxy[comment]=HTTP proxy in host:port format, e.g. squid.redhat.com:3128\nhttpProxy=\n\nnoReboot[comment]=Disable the reboot actions\nnoReboot=0\n\n#serverURL=http://192.168.160.23/XMLRPC\n#noSSLServerURL=http://192.168.160.23/XMLRPC\n#sslCACert=/usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT\nserverURL=http://192.168.160.23/XMLRPC\nnoSSLServerURL=http://192.168.160.23/XMLRPC\nsslCACert=/usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT\n"

def test_get_up2date():
    up2date_info = Up2DateSysconfig(context_wrap(UP2DATE)).data
    assert up2date_info['retrieveOnly'] == '0'
    assert up2date_info['writeChangesToLog'] == '0'
    assert up2date_info['stagingContentWindow'] == '24'
    assert up2date_info['networkRetries'] == '5'
    assert up2date_info['enableProxy'] == '0'
    assert up2date_info['proxyPassword'] is ''
    assert up2date_info['systemIdPath'] == '/etc/sysconfig/rhn/systemid'
    assert up2date_info['useNoSSLForPackages'] == '0'
    assert up2date_info['tmpDir'] == '/tmp'
    assert up2date_info['skipNetwork'] == '0'
    assert up2date_info['disallowConfChanges'] == 'noReboot;sslCACert;useNoSSLForPackages;noSSLServerURL;serverURL;disallowConfChanges;'
    assert up2date_info['enableProxyAuth'] == '0'
    assert up2date_info['versionOverride'] is ''
    assert up2date_info['stagingContent'] == '1'
    assert up2date_info['proxyUser'] is ''
    assert up2date_info['hostedWhitelist'] is ''
    assert up2date_info['debug'] == '0'
    assert up2date_info['httpProxy'] is ''
    assert up2date_info['noReboot'] == '0'
    assert up2date_info['serverURL'] == 'http://192.168.160.23/XMLRPC'
    assert up2date_info['noSSLServerURL'] == 'http://192.168.160.23/XMLRPC'
    assert up2date_info['sslCACert'] == '/usr/share/rhn/RHN-ORG-TRUSTED-SSL-CERT'