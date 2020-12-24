# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/matej/workarea/plone.hud/plone.app.hud/src/plone/app/hud/tests/test_best_practices.py
# Compiled at: 2013-09-11 18:28:08
__doc__ = 'Tests for best practices panel.'
from plone import api
from plone.app.hud.testing import IntegrationTestCase
import os, tempfile

class TestBestPractices(IntegrationTestCase):
    """Integration tests for best practices panel."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.best_practices = self.portal.unrestrictedTraverse('@@hud_best_practices')

    def test_check_write_permissions(self):
        tmpdirectory = tempfile.mkdtemp()
        with open(os.path.join(tmpdirectory, 'file0'), 'w') as (f):
            f.write('File zero contents.')
        os.mkdir(os.path.join(tmpdirectory, 'empty_dir'))
        os.mkdir(os.path.join(tmpdirectory, 'somedir'))
        with open(os.path.join(tmpdirectory, 'somedir', 'file1'), 'w') as (f):
            f.write('File one contents.')
        with open(os.path.join(tmpdirectory, 'somedir', 'file2'), 'w') as (f):
            f.write('File two contents.')
        entries = self.best_practices.check_write_permissions(tmpdirectory)
        self.assertEqual(entries, [
         {'absparentpath': tmpdirectory, 
            'whole_parent': True, 
            'contents': None},
         {'absparentpath': os.path.join(tmpdirectory, 'somedir'), 
            'whole_parent': True, 
            'contents': None}])
        for root, dirs, files in os.walk(tmpdirectory, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))

            for name in dirs:
                os.rmdir(os.path.join(root, name))

        os.rmdir(tmpdirectory)
        self.assertFalse(os.path.exists(tmpdirectory))
        return

    def test_get_from_mail_address(self):
        self.assertEqual(None, self.best_practices.get_from_mail_address())
        from zope.component import getUtility
        from Products.CMFCore.interfaces import ISiteRoot
        getUtility(ISiteRoot).email_from_address = 'ovce@xyz.xyz'
        self.assertEqual('ovce@xyz.xyz', self.best_practices.get_from_mail_address())
        return

    def test_count_users_with_roles(self):
        entries = self.best_practices.count_users_with_roles()
        self.assertEqual(entries, {'Manager': 1})
        api.user.create(email='ovce@xyz.xyz', username='ovce')
        api.user.create(email='koze@xyz.xyz', username='koze')
        entries = self.best_practices.count_users_with_roles()
        self.assertEqual(entries, {'Manager': 1})
        api.user.grant_roles(username='ovce', roles=[
         'Reviewer'])
        api.user.grant_roles(username='koze', roles=[
         'Editor', 'Contributor', 'Reviewer'])
        entries = self.best_practices.count_users_with_roles()
        self.assertEqual(entries, {'Manager': 1, 'Editor': 1, 'Contributor': 1, 'Reviewer': 2})

    def test_get_broken_klasses(self):
        self.assertEqual([], self.best_practices.get_broken_klasses())

    def test_check_caching(self):
        self.best_practices.check_caching()
        self.assertFalse(self.best_practices.is_caching_ok)
        self.assertFalse(self.best_practices.is_caching_installed)
        self.assertFalse(self.best_practices.is_caching_enabled)

    def test_check_oldest_transaction(self):
        self.assertEqual(0.0, self.best_practices.check_oldest_transaction())