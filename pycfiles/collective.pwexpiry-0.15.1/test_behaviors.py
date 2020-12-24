# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eleddy/buildouts/umich/src/collective.purge_behaviors/collective/purge_behaviors/tests/test_behaviors.py
# Compiled at: 2013-08-13 15:12:15
import unittest2 as unittest
from collective.purge_behaviors.tests import PURGE_INTEGRATION_TESTING
from collective.purge_behaviors.purge import PurgeParentPaths
from collective.purge_behaviors.purge import PurgeSiblingPaths
from collective.purge_behaviors.purge import PurgeContentsPaths
from collective.purge_behaviors.purge import PurgeSitePaths
from plone import api

class TestProfile(unittest.TestCase):
    layer = PURGE_INTEGRATION_TESTING

    def test_purge_parent(self):
        portal = self.layer['portal']
        folder_id = 'base'
        base = api.content.create(type='Folder', id=folder_id, title='Base Folder', container=portal)
        obj = api.content.create(type='Document', title='New Obj', container=base)
        paths = PurgeParentPaths(obj).getRelativePaths()
        self.assertItemsEqual(paths, ['/plone/base/', '/plone/base/view', '/plone/base/folder_listing'])

    def test_purge_siblings(self):
        portal = self.layer['portal']
        folder_id = 'base'
        base = api.content.create(type='Folder', id=folder_id, title='Base Folder', container=portal)
        obj = api.content.create(type='Document', title='New Obj', container=base)
        api.content.create(type='Document', title='New Obj Sibling 1', container=base)
        api.content.create(type='Folder', title='New Obj Sibling 2: Folder Style', container=base)
        paths = PurgeSiblingPaths(obj).getRelativePaths()
        expected_paths = ['/plone/base/new-obj-sibling-1/',
         '/plone/base/new-obj-sibling-1/view',
         '/plone/base/new-obj-sibling-1/document_view',
         '/plone/base/new-obj-sibling-2-folder-style/',
         '/plone/base/new-obj-sibling-2-folder-style/view',
         '/plone/base/new-obj-sibling-2-folder-style/folder_listing']
        self.assertItemsEqual(paths, expected_paths)

    def test_purge_contents(self):
        portal = self.layer['portal']
        folder_id = 'base'
        base = api.content.create(type='Folder', id=folder_id, title='Base Folder', container=portal)
        api.content.create(type='Document', title='New Obj', container=base)
        api.content.create(type='Document', title='content 1', container=base)
        api.content.create(type='Folder', title='Content 2: Folder Style', container=base)
        paths = PurgeContentsPaths(base).getRelativePaths()
        expected_paths = ['/plone/base/new-obj/',
         '/plone/base/new-obj/view',
         '/plone/base/new-obj/document_view',
         '/plone/base/content-1/',
         '/plone/base/content-1/view',
         '/plone/base/content-1/document_view',
         '/plone/base/content-2-folder-style/',
         '/plone/base/content-2-folder-style/view',
         '/plone/base/content-2-folder-style/folder_listing']
        self.assertItemsEqual(paths, expected_paths)

    def test_purge_siteroot(self):
        portal = self.layer['portal']
        folder_id = 'base'
        base = api.content.create(type='Folder', id=folder_id, title='Base Folder', container=portal)
        paths = PurgeParentPaths(base).getRelativePaths()
        self.assertItemsEqual(paths, ['/plone/', '/plone/folder_listing', '/plone/view'])