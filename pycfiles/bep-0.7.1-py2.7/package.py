# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Bep/package.py
# Compiled at: 2015-11-20 11:21:17
import os
from os.path import join
from site import USER_BASE as user_base
import shutil, subprocess, sys, glob, itertools, locale
from six.moves.urllib.request import urlopen
from Bep.languages import languages
from Bep.core.release_info import name
from Bep.core import utils

class Package(object):

    def __init__(self, lang_arg, pkg_type, install_dirs, args, **kwargs):
        if 'python' in lang_arg:
            self.lang_using = languages.Python()
        else:
            print ('\nError: {0} currently not supported.').format(lang_arg)
            raise SystemExit
        self.lang_cmd = self.lang_using.get_lang_cmd(lang_arg)
        self.pkg_type = pkg_type
        self.installed_pkgs_dir = install_dirs['installed_pkgs_dir']
        self.install_logs_dir = install_dirs['install_logs_dir']
        self.lang_install_dir = join(self.installed_pkgs_dir, self.lang_cmd)
        self.lang_logs_dir = join(self.install_logs_dir, self.lang_cmd)
        self.pkg_type_install_dir = join(self.lang_install_dir, self.pkg_type)
        self.pkg_type_logs_dir = join(self.lang_logs_dir, self.pkg_type)

    def __cmd_output(self, cmd, verbose):
        encoding = locale.getdefaultlocale()[1]
        if verbose:
            print cmd
            cmd = cmd.split(' ')
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            for line in p.stdout:
                line = line.decode(encoding)
                print line.rstrip()

            return_val = p.wait()
        else:
            cmd = cmd.split(' ')
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = p.communicate()
            self.out = out.decode(encoding)
            self.err = err.decode(encoding)
            return_val = p.returncode
        return return_val

    def parse_pkg_to_install_name(self, pkg_to_install):

        def strip_end_of_str(str_to_strip):
            if str_to_strip.endswith('/'):
                return str_to_strip.rstrip('/')
            else:
                if str_to_strip.endswith('.git'):
                    return str_to_strip.rstrip('.git')
                return str_to_strip

        pkg_to_install = strip_end_of_str(pkg_to_install)
        pkg_to_install_name = os.path.basename(pkg_to_install)
        return pkg_to_install_name

    def _download_pkg(self, pkg_to_install_name, branch_flattened_name, args, noise):
        """ downloads/clones the specified package branch for installation """
        app_check_cmd = self.application_check_cmd
        app_type = app_check_cmd.split(' ')[0]
        return_val = self.__cmd_output(app_check_cmd, verbose=False)
        if return_val:
            print ('\nError: COULD NOT INSTALL {0} packages; are you sure {1} is installed?').format(args.pkg_type, app_type)
            return
        else:
            pkg_name_dir = join(self.pkg_type_install_dir, pkg_to_install_name)
            if not os.path.isdir(pkg_name_dir):
                os.makedirs(pkg_name_dir)
            utils.when_not_quiet_mode(('Downloading {0} [{1}]').format(pkg_to_install_name, branch_flattened_name), noise.quiet)
            os.chdir(pkg_name_dir)
            return_val = self.__cmd_output(self.install_download_cmd, verbose=noise.verbose)
            if return_val != 0:
                print ('Could not properly download {0} [{1}] with {2}\n').format(pkg_to_install_name, branch_flattened_name, app_type)
                something_downloaded_or_already_in_pkg_name_dir = os.listdir(pkg_name_dir)
                if not something_downloaded_or_already_in_pkg_name_dir:
                    shutil.rmtree(pkg_name_dir)
                    if not os.listdir(self.pkg_type_install_dir):
                        os.rmdir(self.pkg_type_install_dir)
                    os.listdir(self.lang_install_dir) or shutil.rmtree(self.lang_install_dir)
            else:
                try:
                    shutil.rmtree(branch_flattened_name)
                except:
                    pass

                return
            if return_val == 0:
                return True
            return

    def _installation_check(self, pkg_type, pkg_to_install_name, branch_name, everything_already_installed):
        """
        To make sure that only one version of any given package can be turned on (/active) at any given
        time for a specific version of the lang.  If a package branch with the same name as an already
        installed (turned off) pkg branch is attempting to be installed under the same pkg_type, then do
        not allow this; however, do allow it for a pkg branch with the same name as an existing package
        branch, but under a diff pkg type.
        """
        pkg_name = pkg_to_install_name
        all_branches_installed_for_pkgs_lang_ver = utils.branches_installed_for_given_pkgs_lang_ver(self.lang_cmd, pkg_to_install_name, everything_already_installed)
        any_package_branch_on = [ branch for branch in all_branches_installed_for_pkgs_lang_ver if not branch.startswith('.__') ]
        if self.lang_cmd in everything_already_installed:
            lang_installed = self.lang_cmd
            pkg_types_dict = everything_already_installed[self.lang_cmd]
        else:
            return True
        for installed_pkg_type, pkgs_dict in pkg_types_dict.items():
            for installed_pkg_name, branches_list in pkgs_dict.items():
                pkg_branch_names_on_for_pkg_type = [ branch for branch in branches_list if not branch.startswith('.__') ]
                pkg_branch_names_off_for_pkg_type = [ branch.lstrip('.__') for branch in branches_list if branch.startswith('.__') ]
                pkg_branch_names_all_for_pkg_type = pkg_branch_names_on_for_pkg_type + pkg_branch_names_off_for_pkg_type
                if any_package_branch_on:
                    if pkg_name == installed_pkg_name:
                        if pkg_type == installed_pkg_type:
                            if branch_name in pkg_branch_names_on_for_pkg_type:
                                print 'Already installed & turned on.'
                                return False
                            if branch_name in pkg_branch_names_off_for_pkg_type:
                                print 'Already installed & turned off.'
                                return False
                            if branch_name not in pkg_branch_names_all_for_pkg_type:
                                print ('A branch of {0} is already turned on for {1}').format(pkg_name, lang_installed)
                                return False
                            if branch_name in any_package_branch_on:
                                print ('A branch of {0} is already turned on for {1}').format(pkg_name, lang_installed)
                                return False
                        elif pkg_type != installed_pkg_type:
                            if branch_name in pkg_branch_names_on_for_pkg_type:
                                print ('A branch of {0} is already turned on for {1}').format(pkg_name, lang_installed)
                                return False
                            if branch_name not in pkg_branch_names_all_for_pkg_type:
                                print ('A branch of {0} is already turned on for {1}').format(pkg_name, lang_installed)
                                return False
                elif not any_package_branch_on:
                    if pkg_name == installed_pkg_name:
                        if pkg_type == installed_pkg_type:
                            if branch_name in pkg_branch_names_off_for_pkg_type:
                                print 'Already installed & turned off.'
                                return False
                            if branch_name not in pkg_branch_names_off_for_pkg_type:
                                return True

        else:
            return True

    def install(self, pkg_to_install, args, noise, download_pkg=True, everything_already_installed=None):
        """ installs the specified package's branch """

        def do_install(pkg_to_install_name, branch_to_install):
            pkg_install_dir = join(self.pkg_type_install_dir, pkg_to_install_name)
            pkg_logs_dir = join(self.pkg_type_logs_dir, pkg_to_install_name)
            branch_install_dir = join(pkg_install_dir, branch_to_install)
            branch_logs_dir = join(pkg_logs_dir, branch_to_install)
            os.chdir(branch_install_dir)
            record_file = self.lang_using._create_record_log_file(self.pkg_type_logs_dir, pkg_to_install_name, branch_to_install)
            install_cmd = self.lang_using.get_install_cmd(pkg_to_install_name, branch_to_install, self.lang_cmd, record_file)
            contents_of_pkg_branch_dir = os.listdir(branch_install_dir)
            if self.lang_using.setup_file in contents_of_pkg_branch_dir:
                if download_pkg:
                    utils.when_not_quiet_mode(('Building & Installing {0} [{1}]').format(pkg_to_install_name, branch_to_install), noise.quiet)
                elif noise.verbose:
                    print ('Reinstalling {0} [{1}]').format(pkg_to_install_name, branch_to_install)
                if not os.path.isdir(branch_logs_dir):
                    os.makedirs(branch_logs_dir)
                return_val = self.__cmd_output(install_cmd, verbose=noise.verbose)
                if return_val == 0:
                    if download_pkg:
                        print ('Successfully installed {0} [{1}]').format(pkg_to_install_name, branch_to_install)
                    elif noise.verbose:
                        print ('Successfully reinstalled {0} [{1}]').format(pkg_to_install_name, branch_to_install)
                else:
                    if not noise.verbose:
                        try:
                            print ('{0} {1}').format(self.out.rstrip(), self.err.rstrip())
                            print ('\n\tCOULD NOT INSTALL {0} [{1}]').format(pkg_to_install_name, branch_to_install)
                            print '\tA likely cause is a dependency issue.'
                            print '\t...see Traceback for information.'
                        except UnicodeEncodeError:
                            print ('\n\tCOULD NOT INSTALL {0} [{1}]').format(pkg_to_install_name, branch_to_install)
                            print '\tA likely cause is a dependency issue.'

                    if not download_pkg:
                        print ('Removing {0} [{1}]').format(pkg_to_install_name, branch_to_install)
                        print 'Reinstall a fresh install to use the package.'
                    self._remove_install_dirs(pkg_to_install_name, branch_to_install, pkg_install_dir, branch_install_dir, noise)
                    self._remove_log_dirs(pkg_to_install_name, branch_to_install, pkg_logs_dir, branch_logs_dir, noise)
            else:
                print ('\n\tCANNOT INSTALL {0} [{1}]').format(pkg_to_install_name, branch_to_install)
                print ('\tThere is no {0} in this repo.').format(self.lang_using.setup_file)
                if not download_pkg:
                    print ('Removing {0} [{1}]').format(pkg_to_install_name, branch_to_install)
                    print 'Reinstall a fresh install to use the package.'
                self._remove_install_dirs(pkg_to_install_name, branch_to_install, pkg_install_dir, branch_install_dir, noise)

        if download_pkg:
            pkg_to_install_name = self.parse_pkg_to_install_name(args.pkg_to_install)
            download_url = self.download_url.format(pkg_to_install=args.pkg_to_install)
            error_msg = ('Error:  could not get package {} from\n{}').format(pkg_to_install_name, download_url)
            if self.__class__.__name__ != 'LocalRepo':
                try:
                    resp = urlopen(download_url)
                    if resp.getcode() != 200:
                        raise Exception
                except:
                    raise SystemExit(error_msg)

            if args.branch in {'master', 'default'}:
                download_info = download_url
            else:
                download_info = self.download_url_cmd.format(branch=args.branch, download_url=self.download_url)
            branch_flattened_name = utils.branch_name_flattener(args.branch)
            self.install_download_cmd = self.install_download_cmd.format(download_info=download_info, branch=branch_flattened_name)
            print ('\n--> {0}  [{1}]').format(pkg_to_install_name, branch_flattened_name)
            should_it_be_installed = self._installation_check(args.pkg_type, pkg_to_install_name, branch_flattened_name, everything_already_installed)
            if should_it_be_installed:
                if not os.path.isdir(self.pkg_type_install_dir):
                    os.makedirs(self.pkg_type_install_dir)
                if not os.path.isdir(self.pkg_type_logs_dir):
                    os.makedirs(self.pkg_type_logs_dir)
                download_success = self._download_pkg(pkg_to_install_name, branch_flattened_name, args, noise)
                if download_success:
                    do_install(pkg_to_install_name, branch_flattened_name)
        else:
            pkg_to_install_name = pkg_to_install
            branch_to_install = self.branch_to_turn_on_renamed
            do_install(pkg_to_install_name, branch_to_install)

    def update(self, lang_to_update, pkg_to_update_name, branch_to_update, noise):
        """ updates the specified package's branch """
        pkg_update_dir = join(self.pkg_type_install_dir, pkg_to_update_name)
        branch_update_dir = join(pkg_update_dir, branch_to_update)
        os.chdir(branch_update_dir)
        print ('\n--> {0} [{1}]').format(pkg_to_update_name, branch_to_update)
        utils.when_not_quiet_mode('Checking for updates', noise.quiet)
        return_val = self.__cmd_output(self.update_cmd, verbose=False)
        if return_val != 0:
            try:
                print ('{0} {1}').format(self.out.rstrip(), self.err.rstrip())
            except UnicodeEncodeError:
                pass

            print ('\nCould not properly update {0} [{1}]').format(pkg_to_update_name, branch_to_update)
            print 'Likely a network connection error.  Try again in a moment.'
            return
        output = self.out
        output_end = output.splitlines()[(-1)]
        if self.up_to_date_output in output_end:
            print self.up_to_date_output
            return
        if noise.verbose:
            print output.rstrip()
        record_file = self.lang_using._create_record_log_file(self.pkg_type_logs_dir, pkg_to_update_name, branch_to_update)
        update_install_cmd = self.lang_using.get_install_cmd(pkg_to_update_name, branch_to_update, lang_to_update, record_file)
        contents_of_pkg_branch_dir = os.listdir(branch_update_dir)
        if self.lang_using.setup_file in contents_of_pkg_branch_dir:
            return_val = self.__cmd_output(update_install_cmd, verbose=noise.verbose)
        else:
            print ('UPDATE FAILED for {0} [{1}]').format(pkg_to_update_name, branch_to_update)
            print ('There is no longer a {0} to use for installing the package.').format(self.lang_using.setup_file)
            print 'Try removing the package & then reinstalling it.'
            return
        if return_val == 0:
            pkg_logs_dir = join(self.pkg_type_logs_dir, pkg_to_update_name)
            branch_logs_dir = join(pkg_logs_dir, branch_to_update)
            record_fnames = glob.glob(join(branch_logs_dir, 'log_*.txt'))
            record_files = [ open(rec_file, 'r').readlines() for rec_file in record_fnames ]
            record_files_combined = list(set([ rf for rf in itertools.chain.from_iterable(record_files) ]))
            record_file = self.lang_using._create_record_log_file(self.pkg_type_logs_dir, pkg_to_update_name, branch_to_update)
            with open(record_file, 'w') as (f):
                for i in record_files_combined:
                    f.write(i)

            for rf in record_fnames:
                os.remove(rf)

            print ('Successfully updated {0} [{1}]').format(pkg_to_update_name, branch_to_update)
        elif not noise.verbose:
            try:
                print ('{0} {1}').format(self.out.rstrip(), self.err.rstrip())
                print utils.status(('\tUPDATE FAILED for {0} [{1}]').format(pkg_to_update_name, branch_to_update))
                print '\tA likely cause is a dependency issue, eg. needing a (newer) dependency.'
                print '\t...see Traceback for information.'
            except UnicodeEncodeError:
                print utils.status(('\tUPDATE FAILED for {0} [{1}]').format(pkg_to_update_name, branch_to_update))
                print '\tA likely cause is a dependency issue, eg. needing a (newer) dependency.'

    def _remove_installed_files(self, pkg_to_remove_name, branch_to_remove_name, branch_installation_log_files, noise):
        """ remove the files installed in the userbase by using the install log file """
        for branch_install_log in branch_installation_log_files:
            with open(branch_install_log, 'r') as (install_log):
                for ln in install_log:
                    ln = ln.rstrip()
                    if os.path.exists(ln):
                        try:
                            if os.path.isfile(ln):
                                os.remove(ln)
                            elif os.path.isdir(ln):
                                shutil.rmtree(ln)
                        except:
                            if noise.verbose:
                                print ('Error: Exception in removing {0} [{1}] {2}').format(pkg_to_remove_name, branch_to_remove_name, str(sys.exc_info()))

    def _remove_empty_dirs_recursively(self, starting_dir, noise):
        """ recursively removes all empty dirs under the starting_dir """
        for root, dirs, files in os.walk(starting_dir, topdown=False):
            for dir_name in dirs:
                d_path = join(root, dir_name)
                if not os.listdir(d_path):
                    if noise.verbose:
                        print ('Deleting empty dir: {0}').format(d_path)
                    os.rmdir(d_path)

    def _remove_log_dirs(self, pkg_to_remove_name, branch_to_remove_name, pkg_logs_dir, branch_logs_dir, noise):
        if noise.verbose:
            print ('Removing installation log files for {0} [{1}]').format(pkg_to_remove_name, branch_to_remove_name)
        if os.path.isdir(branch_logs_dir):
            shutil.rmtree(branch_logs_dir)

        def remove_dir(dir_to_remove, str_out):
            if os.path.isdir(dir_to_remove):
                if not os.listdir(dir_to_remove):
                    if noise.verbose:
                        print str_out
                    shutil.rmtree(dir_to_remove)

        str_out = ('Removing the package logs dir {0} because there are no branches in it...').format(pkg_to_remove_name)
        remove_dir(pkg_logs_dir, str_out)
        str_out = ('Removing the package type logs dir {0} because there are no packages in it...').format(self.pkg_type_logs_dir)
        remove_dir(self.pkg_type_logs_dir, str_out)
        str_out = ('Removing the language logs dir {0} because there are no package types in it...').format(self.lang_logs_dir)
        remove_dir(self.lang_logs_dir, str_out)

    def _remove_install_dirs(self, pkg_to_remove_name, branch_to_remove_name, pkg_dir, branch_dir, noise):
        if noise.verbose:
            print ('Removing the downloaded package contents for {0} [{1}]').format(pkg_to_remove_name, branch_to_remove_name)
        shutil.rmtree(branch_dir)

        def remove_dir(dir_to_remove, str_out):
            if not os.listdir(dir_to_remove):
                if noise.verbose:
                    print str_out
                shutil.rmtree(dir_to_remove)

        str_out = ('Removing the package dir {0} because there are no branches installed in it...').format(pkg_to_remove_name)
        remove_dir(pkg_dir, str_out)
        str_out = ('Removing the package type dir {0} because there are no packages installed in it...').format(self.pkg_type_install_dir)
        remove_dir(self.pkg_type_install_dir, str_out)
        str_out = ('Removing the language install dir {0} because there are no packages installed in it...').format(self.lang_install_dir)
        remove_dir(self.lang_install_dir, str_out)

    def remove(self, pkg_to_remove_name, branch_to_remove_name, noise):
        """ removes/uninstalls the specified package's branch, and if the last branch is removed from a package dir,
        then the package dir is removed as well.  Likewise, if the last package is removed from a package type, then
        the package type dir is removed.  Likewise for the language dir.  And the same procedure also goes for the
        install_logs dirs; meaning, if they are empty, then they get removed too """
        if branch_to_remove_name.startswith('.__'):
            actual_dir_name_for_branch_to_remove = branch_to_remove_name
            branch_to_remove_name = branch_to_remove_name.lstrip('.__')
        else:
            actual_dir_name_for_branch_to_remove = branch_to_remove_name
        utils.when_not_quiet_mode(('\nRemoving {0} [{1}]').format(pkg_to_remove_name, branch_to_remove_name), noise.quiet)
        if noise.verbose:
            print ('Removing build & installation files for {0} [{1}]').format(pkg_to_remove_name, branch_to_remove_name)
        pkg_logs_dir = join(self.pkg_type_logs_dir, pkg_to_remove_name)
        branch_logs_dir = join(pkg_logs_dir, branch_to_remove_name)
        branch_installation_log_files = glob.glob(join(branch_logs_dir, 'log_*.txt'))
        self._remove_installed_files(pkg_to_remove_name, branch_to_remove_name, branch_installation_log_files, noise)
        self._remove_log_dirs(pkg_to_remove_name, branch_to_remove_name, pkg_logs_dir, branch_logs_dir, noise)
        pkg_dir = join(self.pkg_type_install_dir, pkg_to_remove_name)
        branch_dir = join(pkg_dir, actual_dir_name_for_branch_to_remove)
        self._remove_install_dirs(pkg_to_remove_name, branch_to_remove_name, pkg_dir, branch_dir, noise)
        self._remove_empty_dirs_recursively(user_base, noise)
        print ('Successfully uninstalled {0} [{1}]').format(pkg_to_remove_name, branch_to_remove_name)

    def turn_off(self, pkg_to_turn_off_name, branch_to_turn_off_name, noise):
        """ this makes the package inactive, so that other versions of the same package can be turned on or so
        that a system level package of the same name (if there is one) can be used.  By being inactive, it hides
        the installed pkg (by renaming it as, '.__branch_name'), so that it doesn't need to be re-downloaded &
        re-built if turned back on; note however, it does actually remove the stuff put into userbase to
        remove the branches's files that were installed into the path.  This is nice b/c the downloads and builds
        are what take so long for most package installations."""
        utils.when_not_quiet_mode(('\nTurning off {0} [{1}]').format(pkg_to_turn_off_name, branch_to_turn_off_name), noise.quiet)
        if noise.verbose:
            print ('Removing built & installed files for {0} [{1}]').format(pkg_to_turn_off_name, branch_to_turn_off_name)
        pkg_logs_dir = join(self.pkg_type_logs_dir, pkg_to_turn_off_name)
        branch_logs_dir = join(pkg_logs_dir, branch_to_turn_off_name)
        branch_installation_log_files = glob.glob(join(branch_logs_dir, 'log_*.txt'))
        self._remove_installed_files(pkg_to_turn_off_name, branch_to_turn_off_name, branch_installation_log_files, noise)
        self._remove_log_dirs(pkg_to_turn_off_name, branch_to_turn_off_name, pkg_logs_dir, branch_logs_dir, noise)
        self._remove_empty_dirs_recursively(user_base, noise)
        if noise.verbose:
            print ('Renaming the downloaded package {0} [{1}]').format(pkg_to_turn_off_name, branch_to_turn_off_name)
        pkg_dir = join(self.pkg_type_install_dir, pkg_to_turn_off_name)
        branch_dir = join(pkg_dir, branch_to_turn_off_name)
        branch_to_turn_off_renamed = ('.__{0}').format(branch_to_turn_off_name)
        branch_to_turn_off_renamed_dir = join(pkg_dir, branch_to_turn_off_renamed)
        os.rename(branch_dir, branch_to_turn_off_renamed_dir)
        print ('Successfully turned off {0} [{1}]').format(pkg_to_turn_off_name, branch_to_turn_off_name)

    def _turn_on_check(self, pkg_type, pkg_to_turn_on_name, branch_to_turn_on, everything_already_installed, noise):
        all_branches_installed_for_pkgs_lang_ver = utils.branches_installed_for_given_pkgs_lang_ver(self.lang_cmd, pkg_to_turn_on_name, everything_already_installed)
        any_package_branch_on = [ branch for branch in all_branches_installed_for_pkgs_lang_ver if not branch.startswith('.__') ]
        if any_package_branch_on:
            print ('Cannot turn on {0} {1} [{2}] {3} because').format(pkg_type, pkg_to_turn_on_name, branch_to_turn_on, self.lang_cmd)
            utils.when_not_quiet_mode(('a version of {0} is already turned on for {1}').format(pkg_to_turn_on_name, self.lang_cmd), noise.quiet)
            utils.when_not_quiet_mode(('[Execute `{} list` to see currently turned on packages]').format(name), noise.quiet)
            return False
        else:
            return True

    def turn_on(self, pkg_to_turn_on_name, branch_to_turn_on_name, args, everything_already_installed, noise):
        self.branch_to_turn_on_renamed = branch_to_turn_on_renamed = branch_to_turn_on_name.lstrip('.__')
        utils.when_not_quiet_mode(('\nAttempting to turn on {0} [{1}]').format(pkg_to_turn_on_name, branch_to_turn_on_renamed), noise.quiet)
        should_turn_back_on = self._turn_on_check(self.pkg_type, pkg_to_turn_on_name, branch_to_turn_on_renamed, everything_already_installed, noise)
        if should_turn_back_on:
            if noise.verbose:
                print ('Renaming {0} {1}').format(pkg_to_turn_on_name, branch_to_turn_on_renamed)
            pkg_dir = join(self.pkg_type_install_dir, pkg_to_turn_on_name)
            branch_dir_raw_name = join(pkg_dir, branch_to_turn_on_name)
            branch_dir_renamed = join(pkg_dir, branch_to_turn_on_renamed)
            os.rename(branch_dir_raw_name, branch_dir_renamed)
            if noise.verbose:
                print ('Reinstalling {0} {1}').format(pkg_to_turn_on_name, branch_dir_renamed)
            Package.install(self, pkg_to_turn_on_name, args, noise, download_pkg=False)
            print ('Successfully turned on {0} [{1}]').format(pkg_to_turn_on_name, branch_to_turn_on_renamed)


class Git(Package):

    def __init__(self, lang_arg, pkg_type, install_dirs, args):
        self.repo_type = 'git'
        self.application_check_cmd = ('{} --version').format(self.repo_type)
        super(Git, self).__init__(lang_arg, pkg_type, install_dirs, args)

    def install(self, pkg_to_install, args, noise, **kwargs):
        self.download_url_cmd = '-b {branch} {download_url}'
        self.install_download_cmd = 'git clone {download_info} {branch}'
        Package.install(self, pkg_to_install, args, noise, **kwargs)

    def update(self, lang_to_update, pkg_to_update, branch_to_update, noise):
        self.update_cmd = 'git pull'
        self.up_to_date_output = ('Current branch {} is up to date.').format(branch_to_update)
        Package.update(self, lang_to_update, pkg_to_update, branch_to_update, noise)


class Mercurial(Package):

    def __init__(self, lang_arg, pkg_type, install_dirs, args):
        self.repo_type = 'hg'
        self.application_check_cmd = ('{} --version').format(self.repo_type)
        super(Mercurial, self).__init__(lang_arg, pkg_type, install_dirs, args)

    def install(self, pkg_to_install, args, noise, **kwargs):
        self.download_url_cmd = '-b {branch} {download_url}'
        self.install_download_cmd = 'hg clone {download_info} {branch}'
        Package.install(self, pkg_to_install, args, noise, **kwargs)

    def update(self, lang_to_update, pkg_to_update, branch_to_update, noise):
        self.update_cmd = 'hg pull -u'
        self.up_to_date_output = 'no changes found'
        Package.update(self, lang_to_update, pkg_to_update, branch_to_update, noise)


class Bazaar(Package):

    def __init__(self, lang_arg, pkg_type, install_dirs, args):
        self.repo_type = 'bzr'
        self.application_check_cmd = ('{} --version').format(self.repo_type)
        super(Bazaar, self).__init__(lang_arg, pkg_type, install_dirs, args)

    def install(self, pkg_to_install, args, noise, **kwargs):
        self.download_url_cmd = '{branch} {download_url}'
        self.install_download_cmd = 'bzr branch {download_info} {branch}'
        Package.install(self, pkg_to_install, args, noise, **kwargs)

    def update(self, lang_to_update, pkg_to_update, branch_to_update, noise):
        self.update_cmd = 'bzr pull'
        self.up_to_date_output = 'No revisions or tags to pull.'
        Package.update(self, lang_to_update, pkg_to_update, branch_to_update, noise)


class RepoTypeCheck(Git, Mercurial, Bazaar):

    def install(self, pkg_to_install, args, noise, **kwargs):
        if self.repo_type == 'git':
            Git.install(self, pkg_to_install, args, noise, **kwargs)
        elif self.repo_type == 'hg':
            Mercurial.install(self, pkg_to_install, args, noise, **kwargs)
        elif self.repo_type == 'bzr':
            Bazaar.install(self, pkg_to_install, args, noise, **kwargs)

    def update(self, lang_to_update, pkg_to_update, branch_to_update, noise):
        pkg_install_dir = join(self.pkg_type_install_dir, pkg_to_update)
        branch_install_dir = join(pkg_install_dir, branch_to_update)
        contents_of_branch_install_dir = os.listdir(branch_install_dir)
        if '.git' in contents_of_branch_install_dir:
            Git.update(self, lang_to_update, pkg_to_update, branch_to_update, noise)
        elif '.hg' in contents_of_branch_install_dir:
            Mercurial.update(self, lang_to_update, pkg_to_update, branch_to_update, noise)
        elif '.bzr' in contents_of_branch_install_dir:
            Bazaar.update(self, lang_to_update, pkg_to_update, branch_to_update, noise)


class Github(Git):

    def install(self, pkg_to_install, args, noise, **kwargs):
        self.repo_type = 'git'
        self.download_url = ('https://github.com/{pkg_to_install}').format(pkg_to_install=pkg_to_install)
        Git.install(self, pkg_to_install, args, noise, **kwargs)


class Bitbucket(RepoTypeCheck):

    def install(self, pkg_to_install, args, noise, **kwargs):
        self.repo_type = args.repo_type
        if self.repo_type == 'hg':
            self.download_url = ('https://bitbucket.org/{pkg_to_install}').format(pkg_to_install=pkg_to_install)
        elif self.repo_type == 'git':
            self.download_url = ('https://bitbucket.org/{pkg_to_install}').format(pkg_to_install=pkg_to_install)
        RepoTypeCheck.install(self, pkg_to_install, args, noise, **kwargs)


class LocalRepo(RepoTypeCheck):

    def install(self, pkg_to_install, args, noise, **kwargs):
        self.download_url = pkg_to_install
        self.repo_type = args.repo_type
        RepoTypeCheck.install(self, pkg_to_install, args, noise, **kwargs)


def create_pkg_inst(lang_arg, pkg_type, install_dirs, args=None, packages_file=None):
    """ install_dirs is a dict with the installed_pkgs_dir and the install_logs_dir """
    supported_pkg_types = dict(github=Github, bitbucket=Bitbucket, local=LocalRepo)

    def make_inst(pkg_type_cls):
        return pkg_type_cls(lang_arg, pkg_type, install_dirs, args)

    try:
        return make_inst(supported_pkg_types[pkg_type])
    except KeyError:
        if packages_file:
            not_pkg_type = ('\nError: {0} in your {1} is an unrecognized package type.\n').format(pkg_type, packages_file)
            raise SystemExit(not_pkg_type)
        else:
            not_pkg_type = ('\nError: {0} is an unrecognized package type.\n').format(pkg_type)
            raise SystemExit(not_pkg_type)