# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Bep/actions.py
# Compiled at: 2015-11-19 10:44:36
import os, sys, imp
from Bep.core.release_info import name
from Bep.core import utils
from Bep import package

class Args(object):
    """ create a namespace similar to if "args" that were passed in on cmdline """

    def __init__(self, repo_type, pkg_type, pkg_to_install, language, branch):
        self.repo_type = repo_type
        self.pkg_type = pkg_type
        self.pkg_to_install = pkg_to_install
        self.branch = branch
        self.language = language


def install_action(args, packages_file, packages_file_path, noise, install_dirs, installed_pkgs_dir):
    if args.pkg_type == 'packages':
        try:
            sys.dont_write_bytecode = True
            pkgs_module = imp.load_source(packages_file, packages_file_path)
        except (ImportError, IOError):
            print ('No {0} file installed for use.').format(packages_file)
            if not os.path.isfile(packages_file_path):
                open(packages_file_path, 'a').close()
                print ('So created empty {0} file for installation of packages.').format(packages_file)
            raise SystemExit(('Now add the desired packages to the {} file and re-run install.').format(packages_file))

        def raise_problem(pkg_to_install):
            print ('\nError: cannot process entry in {}:').format(packages_file)
            print ('\t{}\n').format(pkg_to_install)
            print 'Item needs to be specified like such:'
            print ('\t{} [language-->]repoType+userName/packageName[^branch]').format(name)
            print '\nNote: language and branch are both optional, and repoType only needs'
            print "to be specified if it's not ambigious given where the package comes from:"
            print '\teg. for a github install:  ipython/ipython'
            print '\teg. for a github install:  python3.3-->ipython/ipython'
            print '\teg. for a bitbucket install:  hg+mchaput/whoosh'
            print '\teg. for a local install:  git+/home/username/path/to/repo'
            raise SystemExit

        for pkg_type, pkgs_from_pkgs_file in pkgs_module.packages.items():
            utils.when_not_quiet_mode(utils.status(('\t\tInstalling {0} packages').format(pkg_type)), noise.quiet)
            if pkgs_from_pkgs_file:
                for pkg_to_install_entry in pkgs_from_pkgs_file:
                    lang_N_repo_type_N_pkg_to_install_N_branch = pkg_to_install_entry.split('-->')
                    if len(lang_N_repo_type_N_pkg_to_install_N_branch) == 2:
                        lang_arg, repo_type_N_pkg_to_install_N_branch = lang_N_repo_type_N_pkg_to_install_N_branch
                        repo_type_N_pkg_to_install_N_branch = repo_type_N_pkg_to_install_N_branch.split('+')
                        if len(repo_type_N_pkg_to_install_N_branch) == 2:
                            repo_type, pkg_to_install_N_branch = repo_type_N_pkg_to_install_N_branch
                            pkg_to_install_N_branch = pkg_to_install_N_branch.split('^')
                            if len(pkg_to_install_N_branch) == 2:
                                pkg_to_install, branch = pkg_to_install_N_branch
                                legit_pkg_name = utils.check_if_valid_pkg_to_install(pkg_to_install, pkg_type)
                                if legit_pkg_name:
                                    args = Args(repo_type, pkg_type, pkg_to_install, language=lang_arg, branch=branch)
                                else:
                                    raise_problem(pkg_to_install_entry)
                            elif len(pkg_to_install_N_branch) == 1:
                                pkg_to_install = pkg_to_install_N_branch[0]
                                legit_pkg_name = utils.check_if_valid_pkg_to_install(pkg_to_install, pkg_type)
                                if legit_pkg_name:
                                    branch = utils.get_default_branch(repo_type)
                                    args = Args(repo_type, pkg_type, pkg_to_install, language=lang_arg, branch=branch)
                                else:
                                    raise_problem(pkg_to_install_entry)
                            else:
                                raise_problem(pkg_to_install_entry)
                        elif len(repo_type_N_pkg_to_install_N_branch) == 1:
                            pkg_to_install_N_branch = repo_type_N_pkg_to_install_N_branch[0]
                            if pkg_type in ('github', ):
                                repo_type = 'git'
                                pkg_to_install_N_branch = pkg_to_install_N_branch.split('^')
                                if len(pkg_to_install_N_branch) == 2:
                                    pkg_to_install, branch = pkg_to_install_N_branch
                                    legit_pkg_name = utils.check_if_valid_pkg_to_install(pkg_to_install, pkg_type)
                                    if legit_pkg_name:
                                        args = Args(repo_type, pkg_type, pkg_to_install, branch=branch, language=lang_arg)
                                    else:
                                        raise_problem(pkg_to_install_entry)
                                elif len(pkg_to_install_N_branch) == 1:
                                    pkg_to_install = pkg_to_install_N_branch[0]
                                    legit_pkg_name = utils.check_if_valid_pkg_to_install(pkg_to_install, pkg_type)
                                    if legit_pkg_name:
                                        branch = utils.get_default_branch(repo_type)
                                        args = Args(repo_type, pkg_type, pkg_to_install, language=lang_arg, branch=branch)
                                    else:
                                        raise_problem(pkg_to_install_entry)
                                else:
                                    raise_problem(pkg_to_install_entry)
                            else:
                                raise_problem(pkg_to_install_entry)
                        else:
                            raise_problem(pkg_to_install_entry)
                    elif len(lang_N_repo_type_N_pkg_to_install_N_branch) == 1:
                        repo_type_N_pkg_to_install_N_branch = lang_N_repo_type_N_pkg_to_install_N_branch[0]
                        repo_type_N_pkg_to_install_N_branch = repo_type_N_pkg_to_install_N_branch.split('+')
                        if len(repo_type_N_pkg_to_install_N_branch) == 2:
                            repo_type, pkg_to_install_N_branch = repo_type_N_pkg_to_install_N_branch
                            pkg_to_install_N_branch = pkg_to_install_N_branch.split('^')
                            if len(pkg_to_install_N_branch) == 2:
                                pkg_to_install, branch = pkg_to_install_N_branch
                                legit_pkg_name = utils.check_if_valid_pkg_to_install(pkg_to_install, pkg_type)
                                if legit_pkg_name:
                                    args = Args(repo_type, pkg_type, pkg_to_install, language=args.language, branch=branch)
                                else:
                                    raise_problem(pkg_to_install_entry)
                            elif len(pkg_to_install_N_branch) == 1:
                                pkg_to_install = pkg_to_install_N_branch[0]
                                legit_pkg_name = utils.check_if_valid_pkg_to_install(pkg_to_install, pkg_type)
                                if legit_pkg_name:
                                    branch = utils.get_default_branch(repo_type)
                                    args = Args(repo_type, pkg_type, pkg_to_install, language=args.language, branch=branch)
                                else:
                                    raise_problem(pkg_to_install_entry)
                            else:
                                raise_problem(pkg_to_install_entry)
                        elif len(repo_type_N_pkg_to_install_N_branch) == 1:
                            pkg_to_install_N_branch = repo_type_N_pkg_to_install_N_branch[0]
                            if pkg_type in ('github', ):
                                repo_type = 'git'
                                pkg_to_install_N_branch = pkg_to_install_N_branch.split('^')
                                if len(pkg_to_install_N_branch) == 2:
                                    pkg_to_install, branch = pkg_to_install_N_branch
                                    legit_pkg_name = utils.check_if_valid_pkg_to_install(pkg_to_install, pkg_type)
                                    if legit_pkg_name:
                                        args = Args(repo_type, pkg_type, pkg_to_install, language=args.language, branch=branch)
                                    else:
                                        raise_problem(pkg_to_install_entry)
                                elif len(pkg_to_install_N_branch) == 1:
                                    pkg_to_install = pkg_to_install_N_branch[0]
                                    legit_pkg_name = utils.check_if_valid_pkg_to_install(pkg_to_install, pkg_type)
                                    if legit_pkg_name:
                                        branch = utils.get_default_branch(repo_type)
                                        args = Args(repo_type, pkg_type, pkg_to_install, language=args.language, branch=branch)
                                    else:
                                        raise_problem(pkg_to_install_entry)
                                else:
                                    raise_problem(pkg_to_install_entry)
                            else:
                                raise_problem(pkg_to_install_entry)
                        else:
                            raise_problem(pkg_to_install_entry)
                    else:
                        raise_problem(pkg_to_install_entry)
                    everything_already_installed = utils.all_pkgs_and_branches_for_all_pkg_types_already_installed(installed_pkgs_dir)
                    pkg_inst = package.create_pkg_inst(args.language, args.pkg_type, install_dirs, args=args)
                    pkg_inst.install(args.pkg_to_install, args, noise, everything_already_installed=everything_already_installed)

            else:
                utils.when_not_quiet_mode(('\nNo {0} packages specified in {1} to install.').format(pkg_type, packages_file), noise.quiet)

    else:
        utils.when_not_quiet_mode(utils.status(('\t\tInstalling {0} package').format(args.pkg_type)), noise.quiet)
        pkg_inst = package.create_pkg_inst(args.language, args.pkg_type, install_dirs, args=args)
        everything_already_installed = utils.all_pkgs_and_branches_for_all_pkg_types_already_installed(installed_pkgs_dir)
        pkg_inst.install(args.pkg_to_install, args, noise, everything_already_installed=everything_already_installed)


def list_action(everything_already_installed, noise):
    for lang_dir_name, pkg_type_dict in everything_already_installed.items():
        utils.when_not_quiet_mode(('\n{0} packages installed:').format(lang_dir_name), noise.quiet)
        for pkg_type, pkgs_and_branches in pkg_type_dict.items():

            def list_packages():
                any_pkg_listed = False
                for pkg_for_listing, branches in pkgs_and_branches.items():
                    for branch in branches:
                        if branch.startswith('.__'):
                            branch_if_were_on = branch.lstrip('.__')
                            branch_if_were_on = ('[{0}]').format(branch_if_were_on)
                            item_installed = ('  {: >20} {: >25} {: >25} {: >10}').format(pkg_for_listing, branch_if_were_on, pkg_type, '** off')
                        elif not branch.startswith('.__'):
                            branch = ('[{0}]').format(branch)
                            item_installed = ('  {: >20} {: >25} {: >25}').format(pkg_for_listing, branch, pkg_type)
                        any_pkg_listed = True
                        print item_installed

                return any_pkg_listed

            any_pkg_listed = list_packages()

    if not any_pkg_listed:
        utils.when_not_quiet_mode(('\n[ No packages for listing ]').format(pkg_type), noise.quiet)


command_and_items_to_process_when_multiple_items = {}

def update_action(args, additional_args, lang_dir_name, pkg_type, noise, install_dirs, pkgs_and_branches_on, pkgs_and_branches_off, everything_already_installed, **kwargs):
    if 'all' in args:
        msg = ('\t\tUpdating {0} {1} packages').format(lang_dir_name, pkg_type)
        utils.when_not_quiet_mode(utils.status(msg), noise.quiet)
        pkg_inst = package.create_pkg_inst(lang_dir_name, pkg_type, install_dirs, args=args)
        any_pkg_updated = False
        for pkg_to_update, branch_on in pkgs_and_branches_on.items():
            for branch_to_update in branch_on:
                pkg_inst.update(lang_dir_name, pkg_to_update, branch_to_update, noise)
                any_pkg_updated = True

        if any_pkg_updated:
            return True
        msg = ('\nNo {0} {1} packages turned on for updating.').format(lang_dir_name, pkg_type)
        utils.when_not_quiet_mode(msg, noise.quiet)
        return False
    else:

        def how_to_update_branches(pkg_to_update, all_installed_for_pkg):
            any_how_to_displayed = False
            for quad_tuple in all_installed_for_pkg:
                lang_installed, pkg_type_installed, pkg_name_installed, branch_installed = quad_tuple
                if lang_installed == lang_dir_name and pkg_type_installed == pkg_type:
                    if branch_installed.startswith('.__'):
                        branch_installed = branch_installed.lstrip('.__')
                        update_cue = ('{0} [{1}] {2} turned off:').format(pkg_name_installed, branch_installed, lang_installed)
                        update_cmd = '**** Must turn on to update ****'
                    elif not branch_installed.startswith('.__'):
                        update_cue = ('Update {0} [{1}] {2} with:').format(pkg_to_update, branch_installed, lang_installed)
                        update_cmd = ('{0} -l {1} update {2} {3} --branch={4}').format(name, lang_installed, pkg_type_installed, pkg_name_installed, branch_installed)
                    command_and_items_to_process_when_multiple_items[update_cue] = update_cmd
                    any_how_to_displayed = True

            if any_how_to_displayed:
                return command_and_items_to_process_when_multiple_items
            else:
                return False

        def update_branch(lang_arg, pkg_to_update, branch_to_update):
            a_pkg_was_processed = False
            pkg_inst = package.create_pkg_inst(lang_arg, pkg_type, install_dirs)
            lang_cmd = pkg_inst.lang_cmd
            if lang_dir_name == lang_cmd:
                if pkg_to_update in pkgs_and_branches_on:
                    branch_on = pkgs_and_branches_on[pkg_to_update]
                    if branch_to_update in branch_on:
                        utils.when_not_quiet_mode(utils.status(('\tUpdating {0} [{1}] {2} {3}').format(pkg_to_update, branch_to_update, lang_dir_name, pkg_type)), noise.quiet)
                        pkg_inst.update(lang_cmd, pkg_to_update, branch_to_update, noise)
                        a_pkg_was_processed = True
                if pkg_to_update in pkgs_and_branches_off:
                    branches_off = pkgs_and_branches_off[pkg_to_update]
                    if branch_to_update in branches_off:
                        branch_installed = branch_to_update.lstrip('.__')
                        print ('\n{0} [{1}] {2} turned off:  turn on to update.').format(pkg_to_update, branch_installed, lang_cmd)
                        a_pkg_was_processed = True
                if a_pkg_was_processed:
                    return True
                return False

        pkg_was_processed_or_displayed = utils.package_processor(args, additional_args, pkg_type, how_to_func=how_to_update_branches, processing_func=update_branch, process_str='update', everything_already_installed=everything_already_installed)
        return pkg_was_processed_or_displayed


def remove_action(args, additional_args, lang_dir_name, pkg_type, noise, install_dirs, pkgs_and_branches_on, pkgs_and_branches_off, everything_already_installed, **kwargs):

    def remove_pkg_branches(which_pkgs_and_branches_to_remove, branches_type):
        any_pkg_off_removed = False
        for pkg_to_remove, branches in which_pkgs_and_branches_to_remove.items():
            for branch_to_remove in branches:
                if branches_type == 'off':
                    branch_to_remove = ('.__{0}').format(branch_to_remove)
                pkg_inst.remove(pkg_to_remove, branch_to_remove, noise)
                any_pkg_off_removed = True

        return any_pkg_off_removed

    if 'all' in args:
        utils.when_not_quiet_mode(utils.status(('\t\tRemoving {0} {1} packages').format(lang_dir_name, pkg_type)), noise.quiet)
        pkg_inst = package.create_pkg_inst(lang_dir_name, pkg_type, install_dirs)
        any_pkg_on_removed = remove_pkg_branches(pkgs_and_branches_on, branches_type='on')
        any_pkg_off_removed = remove_pkg_branches(pkgs_and_branches_off, branches_type='off')
        if any_pkg_on_removed or any_pkg_off_removed:
            return True
        return False
    else:

        def how_to_remove_branches(pkg_to_remove, all_installed_for_pkg):
            any_how_to_displayed = False
            for quad_tuple in all_installed_for_pkg:
                lang_installed, pkg_type_installed, pkg_name_installed, branch_installed = quad_tuple
                if lang_installed == lang_dir_name and pkg_type_installed == pkg_type:
                    if branch_installed.startswith('.__'):
                        branch_installed = branch_installed.lstrip('.__')
                    remove_cue = ('Remove {0} [{1}] {2} with:').format(pkg_to_remove, branch_installed, lang_installed)
                    remove_cmd = ('{0} -l {1} remove {2} {3} --branch={4}').format(name, lang_installed, pkg_type_installed, pkg_name_installed, branch_installed)
                    command_and_items_to_process_when_multiple_items[remove_cue] = remove_cmd
                    any_how_to_displayed = True

            if any_how_to_displayed:
                return command_and_items_to_process_when_multiple_items
            else:
                return False

        def remove_branch(lang_arg, pkg_to_remove, branch_to_remove):
            pkg_inst = package.create_pkg_inst(lang_arg, pkg_type, install_dirs)
            lang_cmd = pkg_inst.lang_cmd
            if lang_dir_name == lang_cmd:

                def _remove(which_pkgs_and_branches_to_remove, branches_type, branch_to_remove=branch_to_remove):
                    if pkg_to_remove in which_pkgs_and_branches_to_remove:
                        branches_installed = which_pkgs_and_branches_to_remove[pkg_to_remove]
                        if branch_to_remove in branches_installed:
                            utils.when_not_quiet_mode(utils.status(('\tRemoving {0} [{1}] {2} {3}').format(pkg_to_remove, branch_to_remove, lang_dir_name, pkg_type)), noise.quiet)
                            if branches_type == 'off':
                                branch_to_remove = ('.__{0}').format(branch_to_remove)
                            pkg_inst.remove(pkg_to_remove, branch_to_remove, noise)
                            return True
                    else:
                        return False

                a_pkg_on_was_processed = _remove(pkgs_and_branches_on, branches_type='on')
                a_pkg_off_was_processed = _remove(pkgs_and_branches_off, branches_type='off')
                if a_pkg_on_was_processed or a_pkg_off_was_processed:
                    return True
                return False

        pkg_was_processed_or_displayed = utils.package_processor(args, additional_args, pkg_type, how_to_func=how_to_remove_branches, processing_func=remove_branch, process_str='remove', everything_already_installed=everything_already_installed)
        return pkg_was_processed_or_displayed


def turn_off_action(args, additional_args, lang_dir_name, pkg_type, noise, install_dirs, pkgs_and_branches_on, pkgs_and_branches_off, everything_already_installed, **kwargs):

    def turn_off_branches():
        any_pkg_turned_off = False
        for pkg_to_turn_off, branch_on in pkgs_and_branches_on.items():
            if pkg_to_turn_off == name:
                print ('\n**** Cannot use {name} to turn off {name} ****').format(name=name)
                continue
            for branch_to_turn_off in branch_on:
                pkg_inst.turn_off(pkg_to_turn_off, branch_to_turn_off, noise)
                any_pkg_turned_off = True

        return any_pkg_turned_off

    if 'all' in args:
        msg = ('\t\tTurning off {0} {1} packages').format(lang_dir_name, pkg_type)
        utils.when_not_quiet_mode(utils.status(msg), noise.quiet)
        pkg_inst = package.create_pkg_inst(lang_dir_name, pkg_type, install_dirs)
        any_pkg_turned_off = turn_off_branches()
        if any_pkg_turned_off:
            return True
        msg = ('\nNo {0} {1} packages turned on.').format(lang_dir_name, pkg_type)
        utils.when_not_quiet_mode(msg, noise.quiet)
        return False
    else:

        def how_to_turn_off_branches(pkg_to_turn_off, all_installed_for_pkg):
            any_how_to_displayed = False
            for quad_tuple in all_installed_for_pkg:
                lang_installed, pkg_type_installed, pkg_name_installed, branch_installed = quad_tuple
                if lang_installed == lang_dir_name and pkg_type_installed == pkg_type:
                    if branch_installed.startswith('.__'):
                        branch_installed = branch_installed.lstrip('.__')
                        turn_off_cue = ('{0} [{1}] {2} already turned off.').format(pkg_name_installed, branch_installed, lang_installed)
                        turn_off_cmd = '**** Already turned off ****'
                    elif not branch_installed.startswith('.__'):
                        turn_off_cue = ('Turn off {0} [{1}] {2} with:').format(pkg_to_turn_off, branch_installed, lang_installed)
                        turn_off_cmd = ('{0} -l {1} turn_off {2} {3} --branch={4}').format(name, lang_installed, pkg_type_installed, pkg_name_installed, branch_installed)
                    command_and_items_to_process_when_multiple_items[turn_off_cue] = turn_off_cmd
                    any_how_to_displayed = True

            if any_how_to_displayed:
                return command_and_items_to_process_when_multiple_items
            else:
                return False

        def turn_off_branch(lang_arg, pkg_to_turn_off, branch_to_turn_off):
            a_pkg_was_processed = False
            pkg_inst = package.create_pkg_inst(lang_arg, pkg_type, install_dirs)
            lang_cmd = pkg_inst.lang_cmd
            if lang_dir_name == lang_cmd:
                if pkg_to_turn_off in pkgs_and_branches_on:
                    branch_on = pkgs_and_branches_on[pkg_to_turn_off]
                    if pkg_to_turn_off == name:
                        print ('\n**** Cannot use {name} to turn off {name} ****').format(name=name)
                        return True
                    if branch_to_turn_off in branch_on:
                        utils.when_not_quiet_mode(utils.status(('\tTurning off {0} [{1}] {2} {3}').format(pkg_to_turn_off, branch_to_turn_off, lang_dir_name, pkg_type)), noise.quiet)
                        pkg_inst.turn_off(pkg_to_turn_off, branch_to_turn_off, noise)
                        a_pkg_was_processed = True
                if pkg_to_turn_off in pkgs_and_branches_off:
                    branches_off = pkgs_and_branches_off[pkg_to_turn_off]
                    if branch_to_turn_off in branches_off:
                        print ('\n{0} [{1}] {2} already turned off.').format(pkg_to_turn_off, branch_to_turn_off, lang_cmd)
                        a_pkg_was_processed = True
                if a_pkg_was_processed:
                    return True
                return False

        pkg_was_processed_or_displayed = utils.package_processor(args, additional_args, pkg_type, how_to_func=how_to_turn_off_branches, processing_func=turn_off_branch, process_str='turn_off', everything_already_installed=everything_already_installed)
        return pkg_was_processed_or_displayed


def turn_on_action(args, additional_args, lang_dir_name, pkg_type, noise, install_dirs, pkgs_and_branches_on, pkgs_and_branches_off, everything_already_installed, **kwargs):

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