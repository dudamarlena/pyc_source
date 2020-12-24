# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nslocalizer/Helpers/xcrun.py
# Compiled at: 2019-02-23 14:43:18
# Size of source mod 2**32: 8212 bytes
import os, sys, struct, hashlib, subprocess, CoreFoundation
from .Logger import Logger
from .Switch import Switch

def hashStringForPath(path) -> str:
    """
    Returns the hash for a project's DerivedData location.

    path is the filesystem path to the .xcodeproj file.
    """
    hash_context = hashlib.md5()
    hash_context.update(path)
    md5_digest_hex = hash_context.digest()
    hash_path = [
     None] * 28
    first_value = struct.unpack('>Q', md5_digest_hex[:8])[0]
    counter = 13
    while counter >= 0:
        hash_path[counter] = chr(first_value % 26 + ord('a'))
        first_value = first_value / 26
        counter -= 1

    second_value = struct.unpack('>Q', md5_digest_hex[8:])[0]
    counter = 27
    while counter > 13:
        hash_path[counter] = chr(second_value % 26 + ord('a'))
        second_value = second_value / 26
        counter -= 1

    hash_path_string = ''.join(hash_path)
    return hash_path_string


def ResolveDerivedDataPath(project) -> str:
    default_dd_path = os.path.expanduser('~/Library/Developer/Xcode/DerivedData/')
    derived_data = CoreFoundation.CFPreferencesCopyAppValue('IDECustomDerivedDataLocation', 'com.apple.dt.Xcode')
    if derived_data is None:
        derived_data = default_dd_path
    else:
        if derived_data[0] != '/':
            derived_data = os.path.join(project.path, derived_data)
    return derived_data


def ResolveBuildLocation(project, sym_root) -> str:
    build_dir_path = ''
    derived_data = ResolveDerivedDataPath(project)
    location_style = CoreFoundation.CFPreferencesCopyAppValue('IDEBuildLocationStyle', 'com.apple.dt.Xcode')
    for case in Switch(location_style):
        if case('Unique'):
            xcodeproj_path = os.path.join(project.projectRoot.obj_path, project.name)
            unique_path = hashStringForPath(xcodeproj_path)
            project_dir_name = os.path.splitext(project.name)[0] + '-' + unique_path + '/Build/Products/'
            build_dir_path = os.path.join(derived_data, project_dir_name)
            break
        if case('Shared'):
            shared_path = CoreFoundation.CFPreferencesCopyAppValue('IDESharedBuildFolderName', 'com.apple.dt.Xcode')
            build_dir_path = os.path.join(derived_data, shared_path)
            break
        if case('Custom'):
            location_type = CoreFoundation.CFPreferencesCopyAppValue('IDECustomBuildLocationType', 'com.apple.dt.Xcode')
            custom_path = CoreFoundation.CFPreferencesCopyAppValue('IDECustomBuildProductsPath', 'com.apple.dt.Xcode')
            for case in Switch(location_type):
                if case('RelativeToDerivedData'):
                    build_dir_path = os.path.join(derived_data, custom_path)
                    break
                if case('RelativeToWorkspace'):
                    build_dir_path = os.path.join(project.path.base_path, custom_path)
                    break
                if case('Absolute'):
                    build_dir_path = custom_path
                    break
                if case():
                    break

        if case('DeterminedByTargets'):
            build_dir_path = os.path.join(project.projectRoot.obj_path, sym_root)
            break
        if case():
            break

    return build_dir_path


def IntermediatesBuildLocation(project, target_name, config_name, sym_root) -> str:
    build_dir_path = ResolveBuildLocation(project, sym_root)
    project_name = project.name.split('.')[0]
    project_dir_path = os.path.join(build_dir_path, project_name + '.build')
    config_dir_path = os.path.join(project_dir_path, config_name)
    target_dir_path = os.path.join(config_dir_path, target_name + '.build')
    return target_dir_path


def ProductsBuildLocation(project, sym_root) -> str:
    """
    Returns the full path to the location of the build products.

    project is the project that the build product is in.

    sym_root is the value of $(SYMROOT) for the current configuration
    """
    build_dir_path = ResolveBuildLocation(project, sym_root)
    return build_dir_path


def resolvePathFromLocation(location_string, path, base_path) -> str:
    path_string = ''
    path_type, item_path = location_string.split(':')
    for case in Switch(path_type):
        if case('group'):
            path = os.path.join(base_path, path)
            path_string = os.path.join(path, item_path)
            break
        if case('absolute'):
            path_string = item_path
            break
        if case('developer'):
            path_string = os.path.join(resolve_developer_path(), item_path)
            break
        if case('container'):
            path_string = os.path.join(base_path, item_path)
            break
        if case():
            Logger.write().error('Invalid item path name!')
            path_string = item_path
            break

    return path_string


def make_subprocess_call(call_args, shell_state=False) -> (str, int):
    error = 0
    output = ''
    try:
        output = subprocess.check_output(call_args, shell=shell_state)
        error = 0
    except subprocess.CalledProcessError as exception:
        try:
            output = str(exception.output)
            error = exception.returncode
        finally:
            exception = None
            del exception

    return (
     output, error)


def make_xcrun_with_args(args_tuple) -> str:
    xcrun_result = make_subprocess_call(('xcrun', ) + args_tuple)
    if xcrun_result[1] != 0:
        Logger.write().error('[xcrun]: Error in exec!')
        sys.exit()
    xcrun_output = str(xcrun_result[0]).rstrip('\n')
    return xcrun_output


def resolve_sdk_path(sdk_name) -> str:
    return make_xcrun_with_args(('--show-sdk-path', '--sdk', sdk_name))


def resolve_developer_path() -> str:
    xcrun_result = make_subprocess_call(('xcode-select', '-p'))
    if xcrun_result[1] != 0:
        Logger.write().error('[xcrun]: Please run Xcode first!')
        sys.exit()
    developer_path = str(xcrun_result[0]).rstrip('\n')
    return developer_path


DEVELOPER_DIR = os.environ.get('DEVELOPER_DIR')
if DEVELOPER_DIR:
    Logger.write().info('DEVELOPER_DIR environment variable is already set, existing value "%s" will be used.' % DEVELOPER_DIR)
else:
    os.environ['DEVELOPER_DIR'] = resolve_developer_path()