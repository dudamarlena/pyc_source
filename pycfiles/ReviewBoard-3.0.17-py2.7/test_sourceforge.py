# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/hostingsvcs/tests/test_sourceforge.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for the SourceForge hosting service."""
from __future__ import unicode_literals
from reviewboard.hostingsvcs.tests.testcases import ServiceTests

class SourceForgeTests(ServiceTests):
    """Unit tests for the SourceForge hosting service."""
    service_name = b'sourceforge'

    def test_service_support(self):
        """Testing SourceForge service support capabilities"""
        self.assertTrue(self.service_class.supports_bug_trackers)
        self.assertTrue(self.service_class.supports_repositories)

    def test_get_repository_fields_with_bazaar(self):
        """Testing SourceForge.get_repository_fields for Bazaar"""
        self.assertEqual(self.get_repository_fields(b'Bazaar', fields={b'sourceforge_project_name': b'myproj'}), {b'path': b'bzr://myproj.bzr.sourceforge.net/bzrroot/myproj', 
           b'mirror_path': b'bzr+ssh://myproj.bzr.sourceforge.net/bzrroot/myproj'})

    def test_get_repository_fields_with_cvs(self):
        """Testing SourceForge.get_repository_fields for CVS"""
        self.assertEqual(self.get_repository_fields(b'CVS', fields={b'sourceforge_project_name': b'myproj'}), {b'path': b':pserver:anonymous@myproj.cvs.sourceforge.net:/cvsroot/myproj', 
           b'mirror_path': b'myproj.cvs.sourceforge.net/cvsroot/myproj'})

    def test_get_repository_fields_with_mercurial(self):
        """Testing SourceForge.get_repository_fields for Mercurial"""
        self.assertEqual(self.get_repository_fields(b'Mercurial', fields={b'sourceforge_project_name': b'myproj'}), {b'path': b'http://myproj.hg.sourceforge.net:8000/hgroot/myproj', 
           b'mirror_path': b'ssh://myproj.hg.sourceforge.net/hgroot/myproj'})

    def test_get_repository_fields_with_svn(self):
        """Testing SourceForge.get_repository_fields for Subversion"""
        self.assertEqual(self.get_repository_fields(b'Subversion', fields={b'sourceforge_project_name': b'myproj'}), {b'path': b'http://myproj.svn.sourceforge.net/svnroot/myproj', 
           b'mirror_path': b'https://myproj.svn.sourceforge.net/svnroot/myproj'})