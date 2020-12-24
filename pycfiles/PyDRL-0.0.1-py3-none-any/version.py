# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pydrizzle\version.py
# Compiled at: 2014-04-16 14:31:18
__doc__ = 'This is an automatically generated file created by stsci.distutils.hooks.version_setup_hook.\nDo not modify this file by hand.\n'
__all__ = [
 '__version__', '__vdate__', '__svn_revision__', '__svn_full_info__',
 '__setup_datetime__']
import datetime
__version__ = '6.4.3'
__vdate__ = 'unspecified'
__svn_revision__ = 'Unable to determine SVN revision'
__svn_full_info__ = 'unknown'
__setup_datetime__ = datetime.datetime(2014, 4, 16, 14, 31, 18, 897000)
stsci_distutils_version = '0.3.7'
if '.dev' in __version__:

    def update_svn_info():
        """Update the SVN info if running out of an SVN working copy."""
        global __svn_full_info__
        global __svn_revision__
        import os, string, subprocess
        path = os.path.abspath(os.path.dirname(__file__))
        run_svnversion = True
        try:
            pipe = subprocess.Popen(['svn', 'info', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, _ = pipe.communicate()
            if pipe.returncode == 0:
                lines = []
                for line in stdout.splitlines():
                    line = line.decode('latin1').strip()
                    if not line:
                        continue
                    lines.append(line)

                if not lines:
                    __svn_full_info__ = [
                     'unknown']
                else:
                    __svn_full_info__ = lines
            else:
                run_svnversion = False
        except OSError:
            run_svnversion = False

        if run_svnversion:
            for line in __svn_full_info__:
                if line.startswith('Working Copy Root Path'):
                    path = line.split(':', 1)[1].strip()
                    break

            try:
                pipe = subprocess.Popen(['svnversion', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, _ = pipe.communicate()
                if pipe.returncode == 0:
                    stdout = stdout.decode('latin1').strip()
                    if stdout and stdout[0] in string.digits:
                        __svn_revision__ = stdout
            except OSError:
                pass

        if isinstance(__svn_full_info__, list):
            __svn_full_info__ = ('\n').join(__svn_full_info__)


    update_svn_info()
    del update_svn_info