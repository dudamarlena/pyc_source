# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Bep/run.py
# Compiled at: 2015-11-20 10:06:42
import argparse, os
from os.path import join
import sys, copy
from collections import OrderedDict
from Bep.core import usage
from Bep.core.release_info import __version__, name
from Bep.core import utils
from Bep.cmds import install, list_packages, remove_packages, turn_off, turn_on, update_packages
usr_home_dir = os.path.expanduser('~')
top_level_dir = join(usr_home_dir, ('.{}').format(name))
installed_pkgs_dir = join(top_level_dir, 'installed_pkgs')
install_logs_dir = join(top_level_dir, '.install_logs')
install_dirs = dict(installed_pkgs_dir=installed_pkgs_dir, install_logs_dir=install_logs_dir)
packages_file = ('.{}_packages').format(name)
packages_file_path = join(usr_home_dir, packages_file)
repo_choices = [
 'github', 'bitbucket', 'local']
other_choices = ['packages']
possible_choices = repo_choices + other_choices

def main():
    top_parser = argparse.ArgumentParser(description=name.upper(), formatter_class=argparse.RawDescriptionHelpFormatter, epilog=usage.epilog_use)
    top_parser.add_argument('--version', action='version', version=('%(prog)s {}').format(__version__))
    top_parser.add_argument('-l', '--language', nargs='?', default='python', help=usage.lang_use)
    group = top_parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', action='store_true', help=usage.verbose_use)
    group.add_argument('-q', '--quiet', action='store_true', help=usage.quiet_use)

    def check_for_all_error(cmd_arg):
        if cmd_arg in ('all', 'All', 'ALL', '--All', '--ALL'):
            raise SystemExit('\nError: Did you mean to specifiy --all instead?')

    build_up_subparsers = True
    additional_args = []
    cmds_that_accept_all_arg = ['update', 'remove', 'turn_off']
    for cmd in cmds_that_accept_all_arg:
        if cmd in sys.argv:
            for i in sys.argv:
                check_for_all_error(i)

            if '--all' in sys.argv:
                build_up_subparsers = False
                top_parser.add_argument('--all', action='store_true', help=usage.all_use)
                args = top_parser.parse_known_args()
                args, additional_args = args
                if len(additional_args) > 1:
                    error_all_arg = '--all can only be called with one of the following args:\n\t'
                    error_all_arg = error_all_arg + '{update, remove, turn_off}'
                    top_parser.error(error_all_arg)

    everything_already_installed = utils.all_pkgs_and_branches_for_all_pkg_types_already_installed(installed_pkgs_dir)
    any_of_this_pkg_already_installed = lambda pkg_to_process: utils.lang_and_pkg_type_and_pkg_and_branches_tuple(pkg_to_process, everything_already_installed)
    cmds_that_can_display_how_to = cmds_that_accept_all_arg + ['turn_on']
    for cmd in cmds_that_can_display_how_to:
        if cmd in sys.argv and '--all' not in sys.argv:
            if '-h' not in sys.argv and '--help' not in sys.argv:
                args = top_parser.parse_known_args()
                args, additional_args = args
                if len(additional_args) == 2:
                    additional_args_copy = copy.copy(additional_args)
                    additional_args_copy.remove(cmd)
                    potential_pkg_to_proc = additional_args_copy[0]
                    if any_of_this_pkg_already_installed(potential_pkg_to_proc):
                        print (' **** This is how to {} {} ****').format(cmd, potential_pkg_to_proc)
                        build_up_subparsers = False
                    elif potential_pkg_to_proc not in possible_choices:
                        error_msg = ('cannot {} {}: not a currently installed package.\n').format(cmd, potential_pkg_to_proc)
                        error_msg = error_msg + ('[Execute `{} list` to see installed packages.]').format(name)
                        top_parser.error(error_msg)
                else:
                    additional_args = []

    if build_up_subparsers:
        top_subparser = top_parser.add_subparsers(title='Commands', description='[ These are the commands that can be passed to %(prog)s ]', help='[ Command specific help info ]')
        parser_list = top_subparser.add_parser('list', help=usage.list_use)
        parser_list.add_argument('list_arg', action='store_true', help=usage.list_sub_use)

        class CheckIfCanBeInstalled(argparse.Action):
            """ makes sure a repo to install has both a user_name and repo_name:
                    eg. ipython/ipython
                or is an actual path to a repo on the local filesystem"""

            def __call__(self, parser, namespace, arg_value, option_string=None):
                pkg_type = parser.prog.split(' ')[(-1)]
                if utils.check_if_valid_pkg_to_install(arg_value, pkg_type):
                    setattr(namespace, self.dest, arg_value)
                elif pkg_type == 'local':
                    error_msg = '\n\tIs not a path that exists on local filesystem.'
                    raise parser.error(arg_value + error_msg)
                else:
                    error_msg = '\nneed to make sure a username and repo_name are specified, like so:\n\tusername/repo_name'
                    raise parser.error(arg_value + error_msg)

        cmd_help = vars(usage.cmd_help)
        for cmd in ['install', 'update', 'remove', 'turn_off', 'turn_on']:
            if cmd == 'install':
                install_parser = top_subparser.add_parser(cmd, help=usage.install_use.format(packages_file), formatter_class=argparse.RawTextHelpFormatter)
                install_parser.set_defaults(top_subparser=cmd)
                install_subparser = install_parser.add_subparsers(dest='pkg_type', help=usage.install_sub_use.format(packages_file))
                for c in repo_choices:
                    pkg_type_to_install = install_subparser.add_parser(c)
                    pkg_type_to_install.add_argument('pkg_to_install', action=CheckIfCanBeInstalled)
                    if c == 'github':
                        pkg_type_to_install.add_argument('repo_type', default='git', nargs='?')
                    elif c == 'bitbucket':
                        pkg_type_to_install.add_argument('repo_type', choices=['git', 'hg'])
                    pkg_type_to_install.add_argument('-b', '--branch', dest='branch', default=None)

                for c in other_choices:
                    if c == 'packages':
                        pkg_type_to_install = install_subparser.add_parser(c, help=usage.packages_file_use.format(packages_file))

            else:
                subparser_parser = top_subparser.add_parser(cmd, help=cmd_help[('{}_use').format(cmd)], formatter_class=argparse.RawTextHelpFormatter)
                subparser_parser.set_defaults(top_subparser=cmd)
                this_cmds_help = cmd_help[('{}_sub_use').format(cmd)].format(name=name)
                subparsers_subparser = subparser_parser.add_subparsers(dest='pkg_type', help=this_cmds_help)
                for c in repo_choices:
                    pkg_type_to_proc = subparsers_subparser.add_parser(c)
                    pkg_type_to_proc.add_argument(('pkg_to_{}').format(cmd))
                    pkg_type_to_proc.add_argument('-b', '--branch', dest='branch', default=None)

        args = top_parser.parse_args()
        if 'top_subparser' in args and args.top_subparser == 'install':
            if 'branch' in args and args.branch == None:
                if args.pkg_type == 'local':
                    branch, repo_type = utils.get_checked_out_local_branch(args.pkg_to_install)
                    args.repo_type = repo_type
                else:
                    branch = utils.get_default_branch(args.repo_type)
                args.branch = branch
            elif 'branch' in args and args.branch != None:
                if args.pkg_type == 'local':
                    error_msg = 'for `local` packages a branch cannot be specified;\n'
                    error_msg = error_msg + 'check out the desired branch from the repo itself, then install.'
                    raise top_parser.error(error_msg)
        elif 'top_subparser' in args and args.top_subparser != 'install':
            if 'branch' in args and args.branch == None:
                error_msg = 'need to make sure a branch is specified;\n'
                error_msg = error_msg + ('[Execute `{} list` to see installed packages and branches.]').format(name)
                raise top_parser.error(error_msg)

    class noise(object):
        verbose = args.verbose
        quiet = args.quiet

    if noise.quiet:
        print '-' * 60
    kwargs = dict(packages_file=packages_file, packages_file_path=packages_file_path, noise=noise, install_dirs=install_dirs, installed_pkgs_dir=installed_pkgs_dir)
    if 'top_subparser' in args and args.top_subparser == 'install':
        any_pkgs_processed = install.install_cmd(args, **kwargs)
    everything_already_installed = utils.all_pkgs_and_branches_for_all_pkg_types_already_installed(installed_pkgs_dir)
    if not everything_already_installed:
        raise SystemExit('\nNo packages installed.')
    else:
        if 'list_arg' in args:
            list_packages.list_cmd(everything_already_installed, noise)
        else:
            actions_to_take = {}
            for lang_dir_name, pkg_type_dict in everything_already_installed.items():
                for pkg_type, pkgs_and_branches in pkg_type_dict.items():
                    any_pkgs_processed = False
                    pkgs_status = utils.pkgs_and_branches_for_pkg_type_status(pkgs_and_branches)
                    pkgs_and_branches_on = pkgs_status['pkg_branches_on']
                    pkgs_and_branches_off = pkgs_status['pkg_branches_off']
                    kwargs = dict(lang_dir_name=lang_dir_name, pkg_type=pkg_type, noise=noise, install_dirs=install_dirs, pkgs_and_branches_on=pkgs_and_branches_on, pkgs_and_branches_off=pkgs_and_branches_off, additional_args=additional_args, everything_already_installed=everything_already_installed)
                    if 'pkg_to_update' in args or 'update' in additional_args:
                        any_pkgs_processed = update_packages.update_cmd(args, **kwargs)
                    elif 'pkg_to_remove' in args or 'remove' in additional_args:
                        any_pkgs_processed = remove_packages.remove_cmd(args, **kwargs)
                    elif 'pkg_to_turn_off' in args or 'turn_off' in additional_args:
                        any_pkgs_processed = turn_off.turn_off_cmd(args, **kwargs)
                    elif 'pkg_to_turn_on' in args or 'turn_on' in additional_args:
                        any_pkgs_processed = turn_on.turn_on_cmd(args, **kwargs)
                    if any_pkgs_processed:
                        if type(any_pkgs_processed) == dict:
                            actions_to_take.update(any_pkgs_processed)

        if actions_to_take:
            if len(actions_to_take) == 1:
                alert, cmd = actions_to_take.items()[0]
                option = ('\n* {}\n{}\n').format(alert, cmd)
                print option
                if not (cmd.startswith('****') and cmd.endswith('****')):
                    print '-' * 60
                    msg = 'The above version is installed, would you like to run the\ncommand [y/N]? '
                    response = raw_input(msg)
                    if response:
                        response = response.lower()
                        if response in ('y', 'yes'):
                            utils.cmd_output(cmd)
                        elif response in ('n', 'no'):
                            print '\nBye then.'
                        else:
                            raise SystemExit(('\nError: {}: not valid input').format(response))
                    else:
                        print '\nOk, bye then.'
            elif len(actions_to_take) > 1:
                actions_to_take_with_num_keys = {}
                for num, alert_key in enumerate(actions_to_take, start=1):
                    actions_to_take_with_num_keys[num] = (
                     alert_key, actions_to_take[alert_key])

                actions_to_take_with_num_keys = OrderedDict(sorted(actions_to_take_with_num_keys.items(), key=lambda t: t[0]))
                for num_key, alert_and_cmd_tuple_val in actions_to_take_with_num_keys.items():
                    if num_key == 1:
                        print ''
                    alert, cmd = alert_and_cmd_tuple_val
                    option = ('{}. {}\n{}\n').format(num_key, alert, cmd)
                    print option

                print '-' * 60
                msg = "The versions above are installed.  If you'd like to run the command\n"
                msg = msg + 'for an item, enter the number (if not, then just hit enter to exit). '
                response = raw_input(msg)
                if response:
                    try:
                        response = int(response)
                    except ValueError:
                        raise SystemExit(('\nError: invalid response: {}').format(response))

                    if response in range(1, len(actions_to_take_with_num_keys) + 1):
                        cmd = actions_to_take_with_num_keys[response][1]
                        if cmd.startswith('****') and cmd.endswith('****'):
                            print ('\nNo command to process,\n{}').format(cmd)
                        else:
                            utils.cmd_output(cmd)
                    else:
                        raise SystemExit(('\nError: invalid response: {}').format(response))
                else:
                    print '\nOk, bye then.'
    return