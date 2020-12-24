# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/installib/windows.py
# Compiled at: 2016-12-13 08:17:02
from _winreg import *
import win32api, subprocess, os, platform
aReg = ConnectRegistry(None, HKEY_LOCAL_MACHINE)

class Registry(object):

    def __init__(self, display_name=None, contact=None, display_varsion=None, help_telephone=None, help_link=None, url_info_about=None, publisher=None):
        self.display_name = display_name
        self.contact = contact
        self.display_version = display_varsion
        self.help_telephone = help_telephone
        self.help_link = help_link
        self.url_info_about = url_info_about
        self.publisher = publisher


def get_query_value(a_key, label):
    try:
        return QueryValueEx(a_key, label)[0]
    except EnvironmentError:
        return

    return


def get_registry_from(key):
    a_key = OpenKey(aReg, key)
    display_name = get_query_value(a_key, 'DisplayName')
    contact = get_query_value(a_key, 'Contact')
    display_version = get_query_value(a_key, 'DisplayVersion')
    help_telephone = get_query_value(a_key, 'HelpTelephone')
    help_link = get_query_value(a_key, 'HelpLink')
    url_info_about = get_query_value(a_key, 'URLInfoAbout')
    publisher = get_query_value(a_key, 'Publisher')
    return Registry(display_name=display_name, contact=contact, display_varsion=display_version, help_telephone=help_telephone, help_link=help_link, url_info_about=url_info_about, publisher=publisher)


def get_registry_from_wow6432_microsoft_windows_current_version_uninstall(key):
    return get_registry_from('SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\%s' % key)


def get_registry_from_microsoft_windows_current_version_uninstall(key):
    return get_registry_from('SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\%s' % key)


def get_32bit_application_registry_from_microsoft_windows_current_version_uninstall(product_code):
    os_architecture = platform.architecture()[0]
    if os_architecture == '64bit':
        return get_registry_from_wow6432_microsoft_windows_current_version_uninstall(product_code)
    else:
        return get_registry_from_microsoft_windows_current_version_uninstall(product_code)


def get_file_properties(fname):
    """
    Read all properties of the given file return them as a dictionary.
    """
    prop_names = ('Comments', 'InternalName', 'ProductName', 'CompanyName', 'LegalCopyright',
                  'ProductVersion', 'FileDescription', 'LegalTrademarks', 'PrivateBuild',
                  'FileVersion', 'OriginalFilename', 'SpecialBuild')
    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}
    try:
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = '%d.%d.%d.%d' % (fixedInfo['FileVersionMS'] / 65536,
         fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
         fixedInfo['FileVersionLS'] % 65536)
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]
        strInfo = {}
        for propName in prop_names:
            strInfoPath = '\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo
    except:
        pass

    return props


def install_installshield_package(path_to_installer, install_path=None):
    if install_path is None:
        installdir = ''
    else:
        installdir = ' INSTALLDIR=\\"%s\\"' % install_path
    with open(os.devnull, 'w') as (devnull):
        process = subprocess.Popen('"%s" /s /v"/qn%s"' % (path_to_installer, installdir), shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=devnull)
        process.wait()
    return


def uninstall_windows_application(product_code, **kwargs):
    cmd = 'MSIEXEC.EXE /x %s /qn' % product_code
    for k, v in kwargs.iteritems():
        cmd += ' %s="%s"' % (k, v)

    with open(os.devnull, 'w') as (devnull):
        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=devnull)
        process.wait()