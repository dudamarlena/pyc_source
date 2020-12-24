# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/_version_helper.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 5153 bytes
import json, subprocess, sys
from pathlib import Path

class GitInformation(object):
    __doc__ = 'Helper class to handle the git information\n    '

    def __init__(self):
        self.last_commit_info = self.get_last_commit_info()
        self.last_version = self.get_last_version()
        self.hash = self.last_commit_info[0]
        self.author = self.last_commit_info[1]
        self.status = self.get_status()
        self.builder = self.get_build_name()
        self.build_date = self.get_build_date()

    def call(self, arguments):
        """Launch a subprocess to run the bash command

        Parameters
        ----------
        arguments: list
            list of bash commands
        """
        return subprocess.check_output(arguments)

    def get_build_name(self):
        """Return the username and email of the current builder
        """
        try:
            name = self.call(['git', 'config', 'user.name'])
            email = self.call(['git', 'config', 'user.email'])
            name = name.strip()
            email = email.strip()
            return '%s <%s>' % (name.decode('utf-8'), email.decode('utf-8'))
        except Exception:
            return ''

    def get_build_date(self):
        """Return the current datetime
        """
        import time
        return time.strftime('%Y-%m-%d %H:%M:%S +0000', time.gmtime())

    def get_last_commit_info(self):
        """Return the details of the last git commit
        """
        try:
            string = self.call([
             'git', 'log', '-1', '--pretty=format:%h,%an,%ae'])
            string = string.decode('utf-8').split(',')
            hash, username, email = string
            author = '%s <%s>' % (username, email)
            return (hash, author)
        except Exception:
            return ''

    def get_status(self):
        """Return the state of the git repository
        """
        git_diff = self.call(['git', 'diff', '.']).decode('utf-8')
        if git_diff:
            return 'UNCLEAN: Modified working tree'
        else:
            return 'CLEAN: All modifications committed'

    def get_last_version(self):
        """Return the last stable version
        """
        try:
            tag_list = self.call(['git', 'tag']).decode('utf-8').split('\n')
            tag_list = [i for i in tag_list if i.startswith('v')]
            return tag_list[(-1)].split('v')[(-1)]
        except Exception:
            return 'Not found'


class PackageInformation(GitInformation):
    __doc__ = 'Helper class to handle package versions\n    '

    def __init__(self):
        self.package_info = self.get_package_info()
        self.package_dir = self.get_package_dir()

    def get_package_info(self):
        """Return the package information
        """
        if (Path(sys.prefix) / 'conda-meta').is_dir():
            raw = self.call([
             'conda',
             'list',
             '--json',
             '--prefix', sys.prefix])
        else:
            raw = self.call([
             sys.executable,
             '-m', 'pip',
             'list', 'installed',
             '--format', 'json'])
        return json.loads(raw.decode('utf-8'))

    def get_package_dir(self):
        """Return the package directory
        """
        return sys.prefix


def get_version_information(short=False):
    """Grab the version from the .version file

    Parameters
    ----------
    short: Bool
        If True, only return the version. If False, return git hash
    """
    version_file = Path(__file__).parent / '.version'
    string = ''
    try:
        with open(version_file, 'r') as (f):
            f = f.readlines()
            f = [i.strip() for i in f]
        version = [i.split('= ')[1] for i in f if 'last_release' in i][0]
        hash = [i.split('= ')[1] for i in f if 'git_hash' in i][0]
        status = [i.split('= ')[1] for i in f if 'git_status' in i][0]
        if short:
            string += '%s' % version
        else:
            string += '%s: %s %s' % (version, status, hash)
    except IndexError:
        print('No version information found')
    except FileNotFoundError as exc:
        try:
            if _PESUMMARY_SETUP:
                return
        except NameError:
            pass

        raise

    return string