# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Bep/languages/languages.py
# Compiled at: 2015-11-21 16:05:19
import datetime, subprocess, locale
from os.path import join

class Language(object):
    """ Language agnostic Base class. """

    def execute_shell_cmd(self, lang, cmd):
        """ Executes the cmd per lang specified to use. """
        encoding = locale.getdefaultlocale()[1]
        try:
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        except OSError:
            print ('\nError: Cannot use {} to process packages.').format(lang)
            raise SystemExit

        out, err = p.communicate()
        out = out.decode(encoding)
        return out

    def _create_record_log_file(self, pkg_type_logs_dir, pkg_name, pkg_branch_name):
        """ Creates the a record of everything that was processed in a pkg log file. """
        time_stamp = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
        record_file = join(pkg_type_logs_dir, pkg_name, pkg_branch_name, ('log_{0}.txt').format(time_stamp))
        return record_file


class Python(Language):
    """ Language subclass for installing python specific packages"""

    def __init__(self):
        self.system_default = 'python'
        self.setup_file = 'setup.py'

    def get_lang_cmd(self, lang_arg):
        """ Gets the lang specific cmd to use to process pkgs. """
        get_version_cmd = [
         lang_arg, '-c', 'import sys; print(sys.version[0:3])']
        version = self.execute_shell_cmd(lang_arg, get_version_cmd)
        if lang_arg in [self.system_default, 'python3']:
            lang_cmd = ('{0}{1}').format(self.system_default, str(version.strip()))
        else:
            lang_cmd = lang_arg
        return lang_cmd

    def get_install_cmd(self, pkg_name, branch_name, lang_cmd, record_file):
        """ To install packages from specified languages, in a user's home directory (~/.local
            in *nix, elsewhere on windows), which is seen by the env before the system-wide
            installed packages) """
        install_cmd = ('{0} {1} install --user --record {2}').format(lang_cmd, self.setup_file, record_file)
        return install_cmd