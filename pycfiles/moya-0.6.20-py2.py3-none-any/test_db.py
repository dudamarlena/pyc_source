# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tests/test_db.py
# Compiled at: 2015-11-03 12:34:41
from __future__ import unicode_literals
from __future__ import print_function
import unittest
from moya.build import build_server
from moya import db
import os
from os.path import dirname, join, abspath
curdir = dirname(abspath(__file__))
from moya.console import Console
from moya import pilot

class TestDB(unittest.TestCase):

    def setUp(self):
        try:
            os.remove(b'dbtest.sqlite')
        except OSError:
            pass

        build_result = build_server(join(curdir, b'dbtest/'), b'settings.ini')
        archive = build_result.archive
        base_context = build_result.context
        archive.populate_context(build_result.context)
        console = Console()
        db.sync_all(build_result.archive, console)
        context = base_context.clone()
        root = context.root
        root[b'_dbsessions'] = db.get_session_map(archive)
        archive.call(b'dbtest#setup', context, None, id=1)
        db.commit_sessions(context)
        self.archive = build_result.archive
        self.base_context = build_result.context
        self.context = self.base_context.clone()
        archive.populate_context(self.context)
        root = self.context.root
        root[b'_dbsessions'] = db.get_session_map(self.archive)
        return

    def tearDown(self):
        try:
            os.remove(b'dbtest.sqlite')
        except OSError as e:
            pass

    def test_bulk_create(self):
        """Test bulk create of db"""
        context = self.context
        print(context.root.keys())
        obj = self.archive.call(b'dbtest#get_by_id', context, None, id=1)
        self.assertEqual(obj.id, 1)
        obj = self.archive.call(b'dbtest#get_by_id', context, None, id=2)
        self.assertEqual(obj.id, 2)
        obj = self.archive.call(b'dbtest#get_by_title', context, None, title=b'Zen 2')
        self.assertEqual(obj.id, 2)
        return

    def test_owner(self):
        """Test object ownership"""
        context = self.context
        call = self.archive.call
        with pilot.manage(context):
            call(b'dbtest#owner_test', context, None)
            owner = call(b'dbtest#get_owner', context, None, name=b'owner')
            print(owner)
            self.assertEqual(owner.name, b'owner')
            child1 = call(b'dbtest#get_child', context, None, name=b'child1')
            child2 = call(b'dbtest#get_child', context, None, name=b'child2')
            child3 = call(b'dbtest#get_child', context, None, name=b'child3')
            child4 = call(b'dbtest#get_child', context, None, name=b'child4')
            print(child1, child2, child3, child4)
            assert child1, b'child1 should exist'
            assert child2, b'child2 should exist'
            assert child3, b'child3 should exist'
            assert child4, b'child4 should exist'
            assert owner.unowned_child is child1
            assert owner.owned_child is child2
            assert owner.unowned_child_o2o is child3
            assert owner.owned_child_o2o is child4
            call(b'dbtest#delete_owner', context, None, name=b'owner')
            print(owner)
            owner = call(b'dbtest#get_owner', context, None, name=b'owner')
            print(owner)
            assert not owner, (b'owner is {}').format(owner)
            child1 = call(b'dbtest#get_child', context, None, name=b'child1')
            child2 = call(b'dbtest#get_child', context, None, name=b'child2')
            child3 = call(b'dbtest#get_child', context, None, name=b'child1')
            child4 = call(b'dbtest#get_child', context, None, name=b'child2')
            print(child1, child2, child3, child4)
            assert child1, b'child1 should exists'
            assert not child2, b'child2 should not exists'
            assert child3, b'child3 should exists'
            assert not child4, b'child4 should not exists'
        return

    def test_owned(self):
        """Test owned objects"""
        context = self.context
        call = self.archive.call
        with pilot.manage(context):
            call(b'dbtest#make_post', context, None)
            post = call(b'dbtest#get_post', context, None, name=b'post')
            assert post.name == b'post', b"post should be called 'post'"
            assert post.images[0].name == b'images1', b'expected images1'
            images = call(b'dbtest#get_images', context, None, name=b'images1')
            assert images.name == b'images1', b"images should be named 'images1'"
            call(b'dbtest#delete_post', context, None, name=b'post')
            images = call(b'dbtest#get_images', context, None, name=b'images1')
            assert not images, b'images should have been deleted'
        return