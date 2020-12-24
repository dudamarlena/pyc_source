# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Bep/core/utils.py
# Compiled at: 2015-11-21 14:39:32
import os
from os.path import join
import glob, copy, subprocess, locale

def cmd_output(cmd):
    """ Delivers all captured output to stdout from running the specified cmd.

    cmd:  str of the full command to run when performing action.
    """
    encoding = locale.getdefaultlocale()[1]
    cmd = cmd.split(' ')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in p.stdout:
        line = line.decode(encoding)
        print line.rstrip()

    return_val = p.wait()
    return return_val


def cmd_output_capture_all(cmd):
    """ Captures all output that would be delivered to stdout from running the specified cmd.

    cmd:  str of the full command to run when performing action.
    """
    encoding = locale.getdefaultlocale()[1]
    cmd = cmd.split(' ')
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode(encoding)
    err = err.decode(encoding)
    returncode = p.returncode
    if returncode != 0:
        print ('Error: are you sure {} is installed?').format(cmd[0])
    return dict(out=out, err=err, returncode=returncode)


status = lambda x: ('\n\n{0}\n{1}\n{0}').format('-' * 65, x)

def when_not_quiet_mode(output, be_quiet=False):
    """ Delivers output to stdout when not in quiet verbosity mode. """
    if not be_quiet:
        print ('{0}').format(output)
    elif be_quiet:
        pass


def check_if_valid_pkg_to_install(usrname_and_repo_name, pkg_type=None):
    """ Checks if the repo given is a legit name to actually proceed with during
    an install.

    usrname_and_repo_name:  str of the usrname/repo_name that was specified for install.
    pkg_type:  str of the pkg type that given for install
    """
    if pkg_type == 'local':
        if os.path.exists(usrname_and_repo_name):
            return usrname_and_repo_name
        else:
            return False

    else:
        usrname_and_repo_name = usrname_and_repo_name.split('/')
        if len(usrname_and_repo_name) == 2:
            usrname, repo_name = usrname_and_repo_name
            return (
             usrname, repo_name)
        return False


def get_default_branch(repo_type):
    """ Returns the correct default name for the specified repo_type.

    repo_type:  str of the type of repo to install.
    """
    if repo_type == 'git':
        default_branch = 'master'
    elif repo_type in ('hg', 'bzr'):
        default_branch = 'default'
    else:
        raise SystemExit(('Error: {} not a recognized repo type').format(repo_type))
    return default_branch


def get_checked_out_local_branch(local_pkg_to_install_path):
    """ When doing an install from the local file-system, this returns
    the currently checked out branch to install from that repo.

    local_pkg_to_install_path:  str path to local pkg's repo to install.
    """
    contents_of_branch_install_dir = os.listdir(local_pkg_to_install_path)
    os.chdir(local_pkg_to_install_path)
    if '.hg' in contents_of_branch_install_dir:
        cmd = 'hg branch'
        outdict = cmd_output_capture_all(cmd)
        output = outdict['out'].splitlines()
        return (
         output[0], 'hg')
    if '.git' in contents_of_branch_install_dir:
        cmd = 'git branch'
        outdict = cmd_output_capture_all(cmd)
        output = outdict['out'].splitlines()
        cur_branch = [ b for b in output if b.startswith('* ') ][0]
        return (
         cur_branch.lstrip('* '), 'git')
    if '.bzr' in contents_of_branch_install_dir:
        cmd = 'bzr branches'
        outdict = cmd_output_capture_all(cmd)
        output = outdict['out'].splitlines()
        cur_branch = [ b for b in output if b.startswith('* ') ][0]
        b = cur_branch.lstrip('* (').rstrip(')')
        return (
         b, 'bzr')
    print ('Error: {} not a recognized repository.').format(local_pkg_to_install_path)
    raise SystemExit


def all_pkgs_and_branches_for_all_pkg_types_already_installed(installed_pkgs_dir):
    """ Builds up info on all pkgs and branches installed for all pkg_types for a
        specific version of the lang specified for the pkg to install.

    installed_pkgs_dir:  the absolute path to the where the downloaded and built pkgs are stored.
    """
    all_pkgs_and_branches_for_all_pkg_types_already_installed = {}
    retrieve_paths = lambda dir_to_glob, how_to_glob='*': glob.glob(join(dir_to_glob, how_to_glob))
    langs_paths = retrieve_paths(installed_pkgs_dir)
    for lang_path in langs_paths:
        lang_name = os.path.basename(lang_path)
        all_pkgs_and_branches_for_all_pkg_types_already_installed.update({lang_name: {}})
        pkg_types_paths = retrieve_paths(lang_path)
        for pkg_type_path in pkg_types_paths:
            pkg_type_name = os.path.basename(pkg_type_path)
            all_pkgs_and_branches_for_all_pkg_types_already_installed[lang_name].update({pkg_type_name: {}})
            pkg_names_paths = retrieve_paths(pkg_type_path)
            for pkg_name_path in pkg_names_paths:
                pkg_name = os.path.basename(pkg_name_path)
                all_pkgs_and_branches_for_all_pkg_types_already_installed[lang_name][pkg_type_name].update({pkg_name: []})
                branches_paths = retrieve_paths(pkg_name_path) + retrieve_paths(pkg_name_path, '.*')
                for branch_path in branches_paths:
                    branch_name = os.path.basename(branch_path)
                    all_pkgs_and_branches_for_all_pkg_types_already_installed[lang_name][pkg_type_name][pkg_name].append(branch_name)

    return all_pkgs_and_branches_for_all_pkg_types_already_installed


def pkgs_and_branches_for_pkg_type_status(pkgs_and_branches_installed_for_pkg_type_lang):
    """ Tells whether branches for the packages are turned on or off

    pkgs_and_branches_installed_for_pkg_type_lang:  dict of each pkg and branch installed
        for the lang version specified to process
    """
    all_pkg_branches_with_hidden_raw = {}
    all_pkg_branches_with_hidden_renamed = {}
    pkg_branches_on = {}
    pkg_branches_off = {}
    for pkg_installed, branches in pkgs_and_branches_installed_for_pkg_type_lang.items():
        all_pkg_branches_with_hidden_raw.update({pkg_installed: []})
        all_pkg_branches_with_hidden_renamed.update({pkg_installed: []})
        pkg_branches_on.update({pkg_installed: []})
        pkg_branches_off.update({pkg_installed: []})
        for branch in branches:
            all_pkg_branches_with_hidden_raw[pkg_installed].append(branch)
            if not branch.startswith('.__'):
                pkg_branches_on[pkg_installed].append(branch)
                all_pkg_branches_with_hidden_renamed[pkg_installed].append(branch)
            elif branch.startswith('.__'):
                branch_off = branch.lstrip('.__')
                pkg_branches_off[pkg_installed].append(branch_off)
                all_pkg_branches_with_hidden_renamed[pkg_installed].append(branch_off)

    pkg_branches = dict(all_pkg_branches_with_hidden_raw=all_pkg_branches_with_hidden_raw, all_pkg_branches_with_hidden_renamed=all_pkg_branches_with_hidden_renamed, pkg_branches_on=pkg_branches_on, pkg_branches_off=pkg_branches_off)
    return pkg_branches


def branches_installed_for_given_pkgs_lang_ver(lang_cmd, pkg_to_process_name, everything_already_installed):
    """ Returns a list of all branches that are installed for a specific pkg,
    for a specific version of the lang across all pkg types.

    lang_cmd:  str of the lang version to process.
    pkg_to_process_name:  str of the pkg name to process.
    everything_already_installed:  dict of all installed packages by lang_version, pkg_type, pkg_name,
        and branches installed for that hierarchy.
    """
    all_branches_installed_for_pkgs_lang_ver = []
    if lang_cmd in everything_already_installed:
        pkg_types_dict = everything_already_installed[lang_cmd]
    else:
        return all_branches_installed_for_pkgs_lang_ver
    for pkg_type, pkgs_dict in pkg_types_dict.items():
        branches_list = pkgs_dict.get(pkg_to_process_name, [])
        for branch in branches_list:
            all_branches_installed_for_pkgs_lang_ver.append(branch)

    return all_branches_installed_for_pkgs_lang_ver


def lang_and_pkg_type_and_pkg_and_branches_tuple(pkg_to_process, everything_already_installed):
    """ Gives back a tuple with all installed versions of a package, for different pkg_types and
    for different branches.

    pkg_to_process:  str of the pkg name to process.
    everything_already_installed:  dict of all installed packages by lang_version, pkg_type, pkg_name,
        and branches installed for that hierarchy.

    """
    lang_pkg_type_pkg_and_branches_for_lang = []
    for lang_installed, pkg_types_dict in everything_already_installed.items():
        for installed_pkg_type, pkg_and_branches_dict in pkg_types_dict.items():
            if pkg_to_process in pkg_and_branches_dict:
                installed_pkg_name = pkg_to_process
                branches_list = pkg_and_branches_dict[pkg_to_process]
                for branch in branches_list:
                    lang_pkg_type_pkg_and_branches_for_lang.append((
                     lang_installed, installed_pkg_type, installed_pkg_name, branch))

    return lang_pkg_type_pkg_and_branches_for_lang


def branch_name_flattener(branch_name):
    """ Returns platform safe branch name for installation dir name (eg. without '/' in it).

    branch_name:  str of branch to process.
    """
    if branch_name:
        branch = branch_name.split('/')
        if len(branch) == 1:
            branch = branch[0]
        elif len(branch) >= 1:
            branch = ('_').join(branch)
        return branch


def package_processor(args, additional_args, pkg_type_already_installed, how_to_func, processing_func, process_str, everything_already_installed):
    """ This is used by the cmdline arg passed into the script to decide whether to proceed
    with the command or to bail.

    args:  a class inst of the argparse namespace with the arguments parsed to use during the install.
    additional_args:  list of additional args parsed from the the argparse arguments.
    pkg_type_already_installed:  str of the name of the pkg type that is already installed.
    how_to_func:  func callable that displays alternative method of processing of cmd.
    processing_func:  func callable that is the long way to process the specified cmd.
    process_str:  str of cmd specified at cmdlin to process
    everything_already_installed:  dict of all installed packages by lang_version, pkg_type, pkg_name,
        and branches installed for that hierarchy.
    """
    arg_action = ('pkg_to_{}').format(process_str)
    if arg_action in args:
        pkg_name_to_process = vars(args)[arg_action]
    else:
        additional_args_copy = copy.copy(additional_args)
        additional_args_copy.remove(process_str)
        pkg_to_potentially_proc = additional_args_copy[0]
        pkg_name_to_process = pkg_to_potentially_proc
    pkg_to_process = os.path.basename(pkg_name_to_process)
    all_installed_for_pkg = lang_and_pkg_type_and_pkg_and_branches_tuple(pkg_name_to_process, everything_already_installed)
    if 'pkg_type' not in args:
        if all_installed_for_pkg:
            any_pkg_how_to_suggested = how_to_func(pkg_name_to_process, all_installed_for_pkg)
            return any_pkg_how_to_suggested
    elif 'pkg_type' in args:
        was_a_pkg_processed = False
        branch_to_process = branch_name_flattener(args.branch)
        pkg_type_to_process = args.pkg_type
        if pkg_type_to_process == pkg_type_already_installed:
            was_a_pkg_processed = processing_func(args.language, pkg_to_process, branch_to_process)
            return was_a_pkg_processed
    return was_a_pkg_processed