# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/clients/tests/test_scanning.py
# Compiled at: 2020-04-14 20:27:46
"""Unit tests for client scanning."""
from __future__ import unicode_literals
import os
from rbtools.clients import scan_usable_client
from rbtools.clients.git import GitClient
from rbtools.clients.svn import SVNClient
from rbtools.clients.tests import SCMClientTests
from rbtools.utils.process import execute

class ScanningTests(SCMClientTests):
    """Unit tests for client scanning."""

    def test_scanning_nested_repos_1(self):
        """Testing scan_for_usable_client with nested repositories (git inside
        svn)
        """
        git_dir = os.path.join(self.testdata_dir, b'git-repo')
        svn_dir = os.path.join(self.testdata_dir, b'svn-repo')
        clone_dir = self.chdir_tmp()
        execute([b'svn', b'co', b'file://%s' % svn_dir, b'svn-repo'], env=None, ignore_errors=False, extra_ignore_errors=())
        svn_clone_dir = os.path.join(clone_dir, b'svn-repo')
        git_clone_dir = os.path.join(svn_clone_dir, b'git-repo')
        os.mkdir(git_clone_dir)
        execute([b'git', b'clone', git_dir, git_clone_dir], env=None, ignore_errors=False, extra_ignore_errors=())
        os.chdir(git_clone_dir)
        repository_info, tool = scan_usable_client({}, self.options)
        self.assertEqual(repository_info.local_path, os.path.realpath(git_clone_dir))
        self.assertEqual(type(tool), GitClient)
        return

    def test_scanning_nested_repos_2(self):
        """Testing scan_for_usable_client with nested repositories (svn inside
        git)
        """
        git_dir = os.path.join(self.testdata_dir, b'git-repo')
        svn_dir = os.path.join(self.testdata_dir, b'svn-repo')
        clone_dir = self.chdir_tmp()
        git_clone_dir = os.path.join(clone_dir, b'git-repo')
        os.mkdir(git_clone_dir)
        execute([b'git', b'clone', git_dir, git_clone_dir], env=None, ignore_errors=False, extra_ignore_errors=())
        svn_clone_dir = os.path.join(git_clone_dir, b'svn-repo')
        os.chdir(git_clone_dir)
        execute([b'svn', b'co', b'file://%s' % svn_dir, b'svn-repo'], env=None, ignore_errors=False, extra_ignore_errors=())
        os.chdir(svn_clone_dir)
        repository_info, tool = scan_usable_client({}, self.options)
        self.assertEqual(repository_info.local_path, os.path.realpath(svn_clone_dir))
        self.assertEqual(type(tool), SVNClient)
        return