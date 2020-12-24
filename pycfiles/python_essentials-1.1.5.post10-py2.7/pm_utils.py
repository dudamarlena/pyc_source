# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/pm_utils.py
# Compiled at: 2015-12-24 21:26:45
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
import subprocess as sp, os, sys, tempfile, re, augeas, check_os, file_line_utils
aptuptodate = False
apt_invalid = False
dpkglock = '/var/lib/dpkg/lock'
apt_get = 'apt-get'
add_apt_repository = 'add-apt-repository'
assume_yes_default = False
skip_apt_update_default = False
install_recommends_default = True
install_suggests_default = False
APT_OUTPUT_CONSOLE = 1
APT_OUTPUT_TMP_FILE = 2
APT_OUTPUT = APT_OUTPUT_CONSOLE
PACKAGE_MANAGER_APT_GET = 'apt-get'

def dpkg_check_package_installed(package_name):

    def __dpkg_check_package_installed_returncode__():
        return_code = sp.call(['dpkg', '-s', package_name], stdout=sp.PIPE, stderr=sp.PIPE)
        return return_code == 0

    def __dpkg_check_package_installed_output__():
        dpkg_output = sp.check_output(['dpkg', '-s', package_name])
        ret_value = 'Package: %s\nStatus: install ok installed' % (package_name,) in dpkg_output
        return ret_value

    ret_value = __dpkg_check_package_installed_returncode__()
    return ret_value


def upgrade(package_manager=PACKAGE_MANAGER_APT_GET, assume_yes=assume_yes_default, skip_apt_update=skip_apt_update_default, install_recommends=install_recommends_default, install_suggests=install_suggests_default):
    if package_manager == PACKAGE_MANAGER_APT_GET:
        aptupdate(skip_apt_update)
        command_list = [apt_get, 'dist-upgrade']
        options_command_list = __generate_apt_options_command_list__(assume_yes=assume_yes, install_recommends=install_recommends, install_suggests=install_suggests)
        sp.check_call(command_list + options_command_list)
    else:
        raise RuntimeError('package_manager %s not yet supported' % (package_manager,))


def install_apt_get_build_dep(packages, package_manager='apt-get', assume_yes=assume_yes_default, skip_apt_update=skip_apt_update_default):
    if packages == None or not type(packages) == type([]):
        raise Exception('packages has to be not None and a list')
    if len(packages) == 0:
        return 0
    else:
        aptupdate(skip_apt_update)
        for package in packages:
            apt_get_output = sp.check_output([apt_get, '--dry-run', 'build-dep', package]).strip()
            apt_get_output_lines = apt_get_output.split('\n')
            build_dep_packages = []
            for apt_get_output_line in apt_get_output_lines:
                if apt_get_output_line.startswith('  '):
                    build_dep_packages += re.split('[\\s]+', apt_get_output_line)

            build_dep_packages = [ x for x in build_dep_packages if x != '' ]
            install_packages(build_dep_packages, package_manager, assume_yes, skip_apt_update=skip_apt_update)

        return


def check_packages_installed(packages, package_manager='apt-get', skip_apt_update=skip_apt_update_default):
    package_managers = ['apt-get']
    if package_manager == 'apt-get':
        for package in packages:
            package_installed = dpkg_check_package_installed(package)
            if not package_installed:
                return False

        return True
    raise Exception('package_manager has to be one of ' + str(package_managers))


def install_packages(packages, package_manager='apt-get', assume_yes=assume_yes_default, skip_apt_update=skip_apt_update_default, install_recommends=install_recommends_default, install_suggests=install_suggests_default, preexec_fn=None):
    if check_packages_installed(packages, package_manager, skip_apt_update=skip_apt_update):
        return 0
    return __package_manager_action__(packages, package_manager, ['install'], assume_yes, skip_apt_update=skip_apt_update, install_recommends=install_recommends, install_suggests=install_suggests, preexec_fn=preexec_fn)


def reinstall_packages(packages, package_manager='apt-get', assume_yes=assume_yes_default, skip_apt_update=skip_apt_update_default, stdout=None, preexec_fn=None):
    return __package_manager_action__(packages, package_manager, ['--reinstall', 'install'], assume_yes, skip_apt_update=skip_apt_update, stdout=None, preexec_fn=preexec_fn)


def remove_packages(packages, package_manager='apt-get', assume_yes=assume_yes_default, skip_apt_update=skip_apt_update_default, preexec_fn=None):
    return __package_manager_action__(packages, package_manager, ['remove'], assume_yes, skip_apt_update=skip_apt_update, preexec_fn=preexec_fn)


def __generate_apt_options_command_list__(assume_yes=assume_yes_default, install_recommends=install_recommends_default, install_suggests=install_suggests_default):
    command_list = []
    if not install_recommends:
        command_list.append('--no-install-recommends')
    if install_suggests:
        command_list.append('--install-suggests')
    if assume_yes:
        command_list.append('--assume-yes')
    return command_list


def __package_manager_action__(packages, package_manager, package_manager_action, assume_yes, skip_apt_update=skip_apt_update_default, stdout=None, install_recommends=install_recommends_default, install_suggests=install_suggests_default, preexec_fn=None):
    """quiet flag doesn't make sense because update can't be performed quietly obviously (maybe consider to switch to apt-api)
    @args packages a list of command to be inserted after the package manager command and default options and before the package list
    @args preexec_fn a function to be passed to the `preexec_fn` argument of `subprocess.Popen`
    """
    if not "<type 'list'>" == str(type(packages)) and str(type(packages)) != "<class 'list'>":
        raise ValueError("packages isn't a list")
    if len(packages) == 0:
        return 0
    if package_manager == 'apt-get':
        aptupdate(skip_apt_update)
        command_list = [apt_get]
        options_command_list = __generate_apt_options_command_list__(assume_yes=assume_yes, install_recommends=install_recommends, install_suggests=install_suggests)
        sp.check_call(command_list + options_command_list + package_manager_action + packages, preexec_fn=preexec_fn)
    elif package_manager == 'yast2':
        sp.check_call(['/sbin/yast2', '--' + package_manager_action] + packages, preexec_fn=preexec_fn)
    elif package_manager == 'zypper':
        sp.check_call(['zypper', package_manager_action] + packages, preexec_fn=preexec_fn)
    elif package_manager == 'equo':
        sp.check_call(['equo', package_manager_action] + packages, preexec_fn=preexec_fn)
    else:
        raise ValueError(str(package_manager) + ' is not a supported package manager')


def invalidate_apt():
    global apt_invalid
    global aptuptodate
    logger.debug('invalidating apt status (update forced at next package manager action)')
    apt_invalid = True
    aptuptodate = False


def aptupdate(skip=skip_apt_update_default, force=False):
    global aptuptodate
    if not aptuptodate and not skip or force or apt_invalid:
        print 'updating apt sources'
        apt_stdout = None
        if APT_OUTPUT == APT_OUTPUT_TMP_FILE:
            apt_get_update_log_file_tuple = tempfile.mkstemp('libinstall_apt_get_update.log')
            logger.info('logging output of apt-get update to %s' % apt_get_update_log_file_tuple[1])
            apt_stdout = apt_get_update_log_file_tuple[0]
        sp.check_call([apt_get, '--quiet', 'update'], stdout=apt_stdout)
        aptuptodate = True
    return


valid_source_line_types = [
 'deb', 'deb-src']

def __validate_apt_source_function_params_augeas_root__(augeas_root, sources_dir_path, sources_file_path):
    if augeas_root is None:
        raise ValueError("augeas_root mustn't be None")
    if not os.path.exists(augeas_root):
        raise ValueError("augeas_root '%s' doesn't exist" % (augeas_root,))
    if not os.path.isdir(augeas_root):
        raise ValueError("augeas_root '%s' isn't a directory, but has to be" % augeas_root)
    if not os.path.exists(sources_dir_path):
        raise ValueError("sources_dir_path '%s' doesn't exist" % (
         sources_dir_path,))
    if not os.path.exists(sources_file_path):
        raise ValueError("sources_file_path '%s' doesn't exist" % (
         sources_file_path,))
    return


def __validate_apt_source_function_params_type__(the_type):
    if the_type not in valid_source_line_types:
        raise ValueError("the_type '%s' isn't a valid source line type (has to be one of %s)" % (the_type, valid_source_line_types))


def check_apt_source_line_added(uri, component, distribution, the_type, augeas_root='/'):
    sources_dir_path = os.path.join(augeas_root, 'etc/apt/sources.list.d')
    sources_file_path = os.path.join(augeas_root, 'etc/apt/sources.list')
    __validate_apt_source_function_params_augeas_root__(augeas_root, sources_dir_path, sources_file_path)
    __validate_apt_source_function_params_type__(the_type)
    a = augeas.Augeas(root=augeas_root)

    def __search__():
        for sources_dir_file in [ os.path.join(sources_dir_path, x) for x in os.listdir(sources_dir_path) ]:
            commented_in_lines = a.match('/files/%s/*' % (os.path.relpath(sources_dir_file, augeas_root),))
            for commented_in_line in commented_in_lines:
                if a.get('%s/uri' % (commented_in_line,)) == uri and a.get('%s/component' % (commented_in_line,)) == component and a.get('%s/distribution' % (commented_in_line,)) == distribution and a.get('%s/type' % (commented_in_line,)) == the_type:
                    return True

        return False

    match_found = __search__()
    if match_found:
        return True
    if not match_found:
        commented_in_lines = a.match('/files/%s/*' % (os.path.relpath(sources_file_path, augeas_root),))
        match_found = False
        for commented_in_line in commented_in_lines:
            if a.get('%s/uri' % (commented_in_line,)) == uri and a.get('%s/component' % (commented_in_line,)) == component and a.get('%s/distribution' % (commented_in_line,)) == distribution and a.get('%s/type' % (commented_in_line,)) == the_type:
                a.close()
                return True

    a.close()
    return False


def add_apt_source_line(uri, component, distribution, the_type, augeas_root='/'):
    sources_dir_path = os.path.join(augeas_root, 'etc/apt/sources.list.d')
    sources_file_path = os.path.join(augeas_root, 'etc/apt/sources.list')
    __validate_apt_source_function_params_augeas_root__(augeas_root, sources_dir_path, sources_file_path)
    __validate_apt_source_function_params_type__(the_type)
    a = augeas.Augeas(root=augeas_root)
    a.set('/files/etc/apt/sources.list/01/distribution', distribution)
    a.set('/files/etc/apt/sources.list/01/type', the_type)
    a.set('/files/etc/apt/sources.list/01/uri', uri)
    a.set('/files/etc/apt/sources.list/01/component', component)
    a.save()
    a.close()