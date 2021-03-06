# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/vermeul/openbis/obis/src/python/obis/dm/git.py
# Compiled at: 2019-05-21 15:45:31
# Size of source mod 2**32: 6957 bytes
import shutil, os
from pathlib import Path
from .utils import run_shell, cd
from .command_result import CommandResult, CommandException
from .checksum import ChecksumGeneratorCrc32, ChecksumGeneratorGitAnnex

class GitWrapper(object):
    __doc__ = 'A wrapper on commands to git and git annex.'

    def __init__(self, git_path=None, git_annex_path=None, find_git=None, data_path=None, metadata_path=None, invocation_path=None):
        self.git_path = git_path
        self.git_annex_path = git_annex_path
        self.data_path = data_path
        self.metadata_path = metadata_path

    def _git(self, params, strip_leading_whitespace=True, relative_repo_path=''):
        """ all git invocations need to go through this method
        since it sets --work-tree and '--git-dir.
         """
        cmd = [
         self.git_path]
        if self.data_path is not None:
            if self.metadata_path is not None:
                git_dir = os.path.join(self.metadata_path, relative_repo_path, '.git')
                cmd += ['--work-tree', self.data_path, '--git-dir', git_dir]
        cmd += params
        return run_shell(cmd, strip_leading_whitespace=strip_leading_whitespace)

    def can_run(self):
        """Return true if the perquisites are satisfied to run (git and git annex)"""
        if self.git_path is None:
            return False
        else:
            if self.git_annex_path is None:
                return False
            else:
                if self._git(['help']).failure():
                    return False
                if self._git(['annex', 'help']).failure():
                    return False
            return True

    def git_init(self):
        result = self._git(['init'])
        self.git_ignore('.obis')
        self.git_ignore('.obis_restorepoint')
        return result

    def git_status(self, path=None):
        if path is None:
            return self._git(['annex', 'status'], strip_leading_whitespace=False)
        else:
            return self._git(['annex', 'status', path], strip_leading_whitespace=False)

    def git_annex_init(self, desc, git_annex_backend=None):
        """ Configures annex in a git repository."""
        cmd = [
         'annex', 'init', '--version=5']
        if desc is not None:
            cmd.append(desc)
        result = self._git(cmd)
        if result.failure():
            return result
        cmd = [
         'config', 'annex.thin', 'true']
        result = self._git(cmd)
        if result.failure():
            return result
        cmd = [
         'annex', 'direct']
        result = self._git(cmd)
        if result.failure():
            return result
        else:
            cmd = ['config', '--unset', 'core.bare']
            result = self._git(cmd)
            if result.failure():
                return result
            attributes_src = os.path.join(os.path.dirname(__file__), 'git-annex-attributes')
            attributes_dst = '.git/info/attributes'
            shutil.copyfile(attributes_src, attributes_dst)
            self._apply_git_annex_backend(attributes_dst, git_annex_backend)
            return result

    def initial_commit(self):
        return self._git(['commit', '--allow-empty', '-m', 'Initial commit.'])

    def _apply_git_annex_backend(self, filename, git_annex_backend):
        if git_annex_backend is not None:
            lines = []
            file = open(filename, 'r')
            for line in file:
                if 'annex.backend' in line:
                    lines.append('* annex.backend=' + git_annex_backend + '\n')
                else:
                    lines.append(line)

            file.close()
            file = open(filename, 'w')
            file.writelines(lines)
            file.close()

    def git_add(self, path):
        return self._git(['annex', 'add', path, '--include-dotfiles'])

    def git_commit(self, msg):
        return self._git(['commit', '--allow-empty', '-m', msg])

    def git_top_level_path(self):
        return self._git(['rev-parse', '--show-toplevel'])

    def git_commit_hash(self):
        return self._git(['rev-parse', '--short', 'HEAD'])

    def git_ls_tree(self):
        return self._git(['ls-tree', '--full-tree', '-r', 'HEAD'])

    def git_checkout(self, path_or_hash, relative_repo_path=''):
        if relative_repo_path:
            return self._git(['checkout', path_or_hash], relative_repo_path=relative_repo_path)
        else:
            return self._git(['checkout', path_or_hash])

    def git_reset_to(self, commit_hash):
        return self._git(['reset', commit_hash])

    def git_ignore(self, path):
        result = self._git(['check-ignore', path])
        if result.returncode == 1:
            with open('.git/info/exclude', 'a') as (gitignore):
                gitignore.write(path)
                gitignore.write('\n')


class GitRepoFileInfo(object):
    __doc__ = 'Class that gathers checksums and file lengths for all files in the repo.'

    def __init__(self, git_wrapper):
        self.git_wrapper = git_wrapper

    def contents(self, git_annex_hash_as_checksum=False):
        """Return a list of dicts describing the contents of the repo.
        :return: A list of dictionaries
          {'crc32': checksum,
           'checksum': checksum other than crc32
           'checksumType': type of checksum
           'fileLength': size of the file,
           'path': path relative to repo root.
           'directory': False
          }"""
        files = self.file_list()
        cksum = self.cksum(files, git_annex_hash_as_checksum)
        return cksum

    def file_list(self):
        tree = self.git_wrapper.git_ls_tree()
        if tree.failure() or len(tree.output) == 0:
            return []
        else:
            lines = tree.output.split('\n')
            files = [line.split('\t')[(-1)].strip() for line in lines]
            return files

    def cksum(self, files, git_annex_hash_as_checksum=False):
        if git_annex_hash_as_checksum == False:
            checksum_generator = ChecksumGeneratorCrc32(self.git_wrapper.data_path, self.git_wrapper.metadata_path)
        else:
            checksum_generator = ChecksumGeneratorGitAnnex(self.git_wrapper.data_path, self.git_wrapper.metadata_path)
        checksums = []
        for file in files:
            checksum = checksum_generator.get_checksum(file)
            checksums.append(checksum)

        return checksums