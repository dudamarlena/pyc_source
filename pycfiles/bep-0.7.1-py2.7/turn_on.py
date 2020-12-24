# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Bep/cmds/turn_on.py
# Compiled at: 2015-11-21 14:40:57
from Bep.core.release_info import name
from Bep.core import utils
from Bep import package
command_and_items_to_process_when_multiple_items = {}

def turn_on_cmd(args, additional_args, lang_dir_name, pkg_type, noise, install_dirs, pkgs_and_branches_on, pkgs_and_branches_off, everything_already_installed, **kwargs):
    """ Turns on specified packages.

    Parameters
    ----------
    args:  a class inst of the argparse namespace with the arguments parsed to use during the install.
    additional_args:  list of additional args parsed from the the argparse arguments.
    lang_dir_name:  name of lang_version dir for package to remove.
    pkg_type:  str of pkg_type to remove.
    noise:  noise class inst with the verbosity level for the amount of output to deliver to stdout.
    install_dirs:  dict of install locations for installed pkgs and install logs.
    pkgs_and_branches_on:  dict of all packages and branches currently turned on for this lang_version
        and pkg_type. eg. {'ipython': ['master']}
    pkgs_and_branches_off:  dict of all packages and branches currently turned off for this lang_version
        and pkg_type.
    everything_already_installed:  dict of all installed packages by lang_version, pkg_type, pkg_name,
        and branches installed for that hierarchy.
    """

    def how_to_turn_on_branches(pkg_to_turn_on, all_installed_for_pkg):
        any_how_to_displayed = False
        for quad_tuple in all_installed_for_pkg:
            lang_installed, pkg_type_installed, pkg_name_installed, branch_installed = quad_tuple
            if lang_installed == lang_dir_name and pkg_type_installed == pkg_type:
                if branch_installed.startswith('.__'):
                    branch_installed = branch_installed.lstrip('.__')
                    turn_on_cue = ('Turn on {0} [{1}] {2} with:').format(pkg_to_turn_on, branch_installed, lang_installed)
                    turn_on_cmd = ('{0} -l {1} turn_on {2} {3} --branch={4}').format(name, lang_installed, pkg_type_installed, pkg_name_installed, branch_installed)
                elif not branch_installed.startswith('.__'):
                    turn_on_cue = ('{0} [{1}] {2} already turned on.').format(pkg_name_installed, branch_installed, lang_installed)
                    turn_on_cmd = '**** Already turned on ****'
                command_and_items_to_process_when_multiple_items[turn_on_cue] = turn_on_cmd
                any_how_to_displayed = True

        if any_how_to_displayed:
            return command_and_items_to_process_when_multiple_items
        else:
            return False

    def turn_on_branch(lang_arg, pkg_to_turn_on, branch_to_turn_on):
        a_pkg_was_processed = False
        pkg_inst = package.create_pkg_inst(lang_arg, pkg_type, install_dirs)
        lang_cmd = pkg_inst.lang_cmd
        if lang_dir_name == lang_cmd:
            if pkg_to_turn_on in pkgs_and_branches_on:
                branch_on = pkgs_and_branches_on[pkg_to_turn_on]
                if branch_to_turn_on in branch_on:
                    print ('\n{0} [{1}] {2} already turned on.').format(pkg_to_turn_on, branch_to_turn_on, lang_cmd)
                    a_pkg_was_processed = True
            if pkg_to_turn_on in pkgs_and_branches_off:
                branches_off = pkgs_and_branches_off[pkg_to_turn_on]
                if branch_to_turn_on in branches_off:
                    utils.when_not_quiet_mode(utils.status(('\tTurning on {0} [{1}] {2} {3}').format(pkg_to_turn_on, branch_to_turn_on, lang_dir_name, pkg_type)), noise.quiet)
                    branch_to_turn_on = ('.__{0}').format(branch_to_turn_on)
                    pkg_inst.turn_on(pkg_to_turn_on, branch_to_turn_on, args, everything_already_installed, noise)
                    a_pkg_was_processed = True
            if a_pkg_was_processed:
                return True
            return False

    pkg_was_processed_or_displayed = utils.package_processor(args, additional_args, pkg_type, how_to_func=how_to_turn_on_branches, processing_func=turn_on_branch, process_str='turn_on', everything_already_installed=everything_already_installed)
    return pkg_was_processed_or_displayed