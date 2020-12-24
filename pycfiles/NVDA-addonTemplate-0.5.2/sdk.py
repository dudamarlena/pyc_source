# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\MSCommon\sdk.py
# Compiled at: 2016-07-07 03:21:35
__revision__ = 'src/engine/SCons/Tool/MSCommon/sdk.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__doc__ = 'Module to detect the Platform/Windows SDK\n\nPSDK 2003 R1 is the earliest version detected.\n'
import os, SCons.Errors, SCons.Util, common
debug = common.debug
_CURINSTALLED_SDK_HKEY_ROOT = 'Software\\Microsoft\\Microsoft SDKs\\Windows\\CurrentInstallFolder'

class SDKDefinition(object):
    """
    An abstract base class for trying to find installed SDK directories.
    """

    def __init__(self, version, **kw):
        self.version = version
        self.__dict__.update(kw)

    def find_sdk_dir(self):
        """Try to find the MS SDK from the registry.

        Return None if failed or the directory does not exist.
        """
        if not SCons.Util.can_read_reg:
            debug('find_sdk_dir(): can not read registry')
            return
        else:
            hkey = self.HKEY_FMT % self.hkey_data
            debug('find_sdk_dir(): checking registry:%s' % hkey)
            try:
                sdk_dir = common.read_reg(hkey)
            except SCons.Util.WinError as e:
                debug('find_sdk_dir(): no SDK registry key %s' % repr(hkey))
                return

            debug('find_sdk_dir(): Trying SDK Dir: %s' % sdk_dir)
            if not os.path.exists(sdk_dir):
                debug('find_sdk_dir():  %s not on file system' % sdk_dir)
                return
            ftc = os.path.join(sdk_dir, self.sanity_check_file)
            if not os.path.exists(ftc):
                debug('find_sdk_dir(): sanity check %s not found' % ftc)
                return
            return sdk_dir

    def get_sdk_dir(self):
        """Return the MSSSDK given the version string."""
        try:
            return self._sdk_dir
        except AttributeError:
            sdk_dir = self.find_sdk_dir()
            self._sdk_dir = sdk_dir
            return sdk_dir

    def get_sdk_vc_script(self, host_arch, target_arch):
        """ Return the script to initialize the VC compiler installed by SDK
        """
        if host_arch == 'amd64' and target_arch == 'x86':
            host_arch = target_arch
        arch_string = target_arch
        if host_arch != target_arch:
            arch_string = '%s_%s' % (host_arch, target_arch)
        debug('sdk.py: get_sdk_vc_script():arch_string:%s host_arch:%s target_arch:%s' % (arch_string,
         host_arch,
         target_arch))
        file = self.vc_setup_scripts.get(arch_string, None)
        debug('sdk.py: get_sdk_vc_script():file:%s' % file)
        return file


class WindowsSDK(SDKDefinition):
    """
    A subclass for trying to find installed Windows SDK directories.
    """
    HKEY_FMT = 'Software\\Microsoft\\Microsoft SDKs\\Windows\\v%s\\InstallationFolder'

    def __init__(self, *args, **kw):
        SDKDefinition.__init__(self, *args, **kw)
        self.hkey_data = self.version


class PlatformSDK(SDKDefinition):
    """
    A subclass for trying to find installed Platform SDK directories.
    """
    HKEY_FMT = 'Software\\Microsoft\\MicrosoftSDK\\InstalledSDKS\\%s\\Install Dir'

    def __init__(self, *args, **kw):
        SDKDefinition.__init__(self, *args, **kw)
        self.hkey_data = self.uuid


preSDK61VCSetupScripts = {'x86': 'bin\\vcvars32.bat', 'amd64': 'bin\\vcvarsamd64.bat', 
   'x86_amd64': 'bin\\vcvarsx86_amd64.bat', 
   'x86_ia64': 'bin\\vcvarsx86_ia64.bat', 
   'ia64': 'bin\\vcvarsia64.bat'}
SDK61VCSetupScripts = {'x86': 'bin\\vcvars32.bat', 'amd64': 'bin\\amd64\\vcvarsamd64.bat', 
   'x86_amd64': 'bin\\x86_amd64\\vcvarsx86_amd64.bat', 
   'x86_ia64': 'bin\\x86_ia64\\vcvarsx86_ia64.bat', 
   'ia64': 'bin\\ia64\\vcvarsia64.bat'}
SDK70VCSetupScripts = {'x86': 'bin\\vcvars32.bat', 'amd64': 'bin\\vcvars64.bat', 
   'x86_amd64': 'bin\\vcvarsx86_amd64.bat', 
   'x86_ia64': 'bin\\vcvarsx86_ia64.bat', 
   'ia64': 'bin\\vcvarsia64.bat'}
SupportedSDKList = [
 WindowsSDK('7.1', sanity_check_file='bin\\SetEnv.Cmd', include_subdir='include', lib_subdir={'x86': [
          'lib'], 
    'x86_64': [
             'lib\\x64'], 
    'ia64': [
           'lib\\ia64']}, vc_setup_scripts=SDK70VCSetupScripts),
 WindowsSDK('7.0A', sanity_check_file='bin\\SetEnv.Cmd', include_subdir='include', lib_subdir={'x86': [
          'lib'], 
    'x86_64': [
             'lib\\x64'], 
    'ia64': [
           'lib\\ia64']}, vc_setup_scripts=SDK70VCSetupScripts),
 WindowsSDK('7.0', sanity_check_file='bin\\SetEnv.Cmd', include_subdir='include', lib_subdir={'x86': [
          'lib'], 
    'x86_64': [
             'lib\\x64'], 
    'ia64': [
           'lib\\ia64']}, vc_setup_scripts=SDK70VCSetupScripts),
 WindowsSDK('6.1', sanity_check_file='bin\\SetEnv.Cmd', include_subdir='include', lib_subdir={'x86': [
          'lib'], 
    'x86_64': [
             'lib\\x64'], 
    'ia64': [
           'lib\\ia64']}, vc_setup_scripts=SDK61VCSetupScripts),
 WindowsSDK('6.0A', sanity_check_file='include\\windows.h', include_subdir='include', lib_subdir={'x86': [
          'lib'], 
    'x86_64': [
             'lib\\x64'], 
    'ia64': [
           'lib\\ia64']}, vc_setup_scripts=preSDK61VCSetupScripts),
 WindowsSDK('6.0', sanity_check_file='bin\\gacutil.exe', include_subdir='include', lib_subdir='lib', vc_setup_scripts=preSDK61VCSetupScripts),
 PlatformSDK('2003R2', sanity_check_file='SetEnv.Cmd', uuid='D2FF9F89-8AA2-4373-8A31-C838BF4DBBE1', vc_setup_scripts=preSDK61VCSetupScripts),
 PlatformSDK('2003R1', sanity_check_file='SetEnv.Cmd', uuid='8F9E5EF3-A9A5-491B-A889-C58EFFECE8B3', vc_setup_scripts=preSDK61VCSetupScripts)]
SupportedSDKMap = {}
for sdk in SupportedSDKList:
    SupportedSDKMap[sdk.version] = sdk

InstalledSDKList = None
InstalledSDKMap = None

def get_installed_sdks():
    global InstalledSDKList
    global InstalledSDKMap
    debug('sdk.py:get_installed_sdks()')
    if InstalledSDKList is None:
        InstalledSDKList = []
        InstalledSDKMap = {}
        for sdk in SupportedSDKList:
            debug('MSCommon/sdk.py: trying to find SDK %s' % sdk.version)
            if sdk.get_sdk_dir():
                debug('MSCommon/sdk.py:found SDK %s' % sdk.version)
                InstalledSDKList.append(sdk)
                InstalledSDKMap[sdk.version] = sdk

    return InstalledSDKList


SDKEnvironmentUpdates = {}

def set_sdk_by_directory(env, sdk_dir):
    global SDKEnvironmentUpdates
    debug('set_sdk_by_directory: Using dir:%s' % sdk_dir)
    try:
        env_tuple_list = SDKEnvironmentUpdates[sdk_dir]
    except KeyError:
        env_tuple_list = []
        SDKEnvironmentUpdates[sdk_dir] = env_tuple_list
        include_path = os.path.join(sdk_dir, 'include')
        mfc_path = os.path.join(include_path, 'mfc')
        atl_path = os.path.join(include_path, 'atl')
        if os.path.exists(mfc_path):
            env_tuple_list.append(('INCLUDE', mfc_path))
        if os.path.exists(atl_path):
            env_tuple_list.append(('INCLUDE', atl_path))
        env_tuple_list.append(('INCLUDE', include_path))
        env_tuple_list.append(('LIB', os.path.join(sdk_dir, 'lib')))
        env_tuple_list.append(('LIBPATH', os.path.join(sdk_dir, 'lib')))
        env_tuple_list.append(('PATH', os.path.join(sdk_dir, 'bin')))

    for variable, directory in env_tuple_list:
        env.PrependENVPath(variable, directory)


def get_sdk_by_version(mssdk):
    if mssdk not in SupportedSDKMap:
        msg = 'SDK version %s is not supported' % repr(mssdk)
        raise SCons.Errors.UserError(msg)
    get_installed_sdks()
    return InstalledSDKMap.get(mssdk)


def get_default_sdk():
    """Set up the default Platform/Windows SDK."""
    get_installed_sdks()
    if not InstalledSDKList:
        return None
    else:
        return InstalledSDKList[0]


def mssdk_setup_env(env):
    debug('sdk.py:mssdk_setup_env()')
    if 'MSSDK_DIR' in env:
        sdk_dir = env['MSSDK_DIR']
        if sdk_dir is None:
            return
        sdk_dir = env.subst(sdk_dir)
        debug('sdk.py:mssdk_setup_env: Using MSSDK_DIR:%s' % sdk_dir)
    elif 'MSSDK_VERSION' in env:
        sdk_version = env['MSSDK_VERSION']
        if sdk_version is None:
            msg = 'SDK version is specified as None'
            raise SCons.Errors.UserError(msg)
        sdk_version = env.subst(sdk_version)
        mssdk = get_sdk_by_version(sdk_version)
        if mssdk is None:
            msg = 'SDK version %s is not installed' % sdk_version
            raise SCons.Errors.UserError(msg)
        sdk_dir = mssdk.get_sdk_dir()
        debug('sdk.py:mssdk_setup_env: Using MSSDK_VERSION:%s' % sdk_dir)
    elif 'MSVS_VERSION' in env:
        msvs_version = env['MSVS_VERSION']
        debug('sdk.py:mssdk_setup_env:Getting MSVS_VERSION from env:%s' % msvs_version)
        if msvs_version is None:
            debug('sdk.py:mssdk_setup_env thinks msvs_version is None')
            return
        msvs_version = env.subst(msvs_version)
        import vs
        msvs = vs.get_vs_by_version(msvs_version)
        debug('sdk.py:mssdk_setup_env:msvs is :%s' % msvs)
        if not msvs:
            debug('sdk.py:mssdk_setup_env: no VS version detected, bailingout:%s' % msvs)
            return
        sdk_version = msvs.sdk_version
        debug('sdk.py:msvs.sdk_version is %s' % sdk_version)
        if not sdk_version:
            return
        mssdk = get_sdk_by_version(sdk_version)
        if not mssdk:
            mssdk = get_default_sdk()
            if not mssdk:
                return
        sdk_dir = mssdk.get_sdk_dir()
        debug('sdk.py:mssdk_setup_env: Using MSVS_VERSION:%s' % sdk_dir)
    else:
        mssdk = get_default_sdk()
        if not mssdk:
            return
        sdk_dir = mssdk.get_sdk_dir()
        debug('sdk.py:mssdk_setup_env: not using any env values. sdk_dir:%s' % sdk_dir)
    set_sdk_by_directory(env, sdk_dir)
    return


def mssdk_exists(version=None):
    sdks = get_installed_sdks()
    if version is None:
        return len(sdks) > 0
    else:
        return version in sdks