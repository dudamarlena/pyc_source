# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_modelmethods.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 7945 bytes
from __future__ import print_function
from mediagoblin.db.base import Session
from mediagoblin.db.models import MediaEntry, User, LocalUser, Privilege, Activity, Generator
from mediagoblin.tests import MGClientTestCase
from mediagoblin.tests.tools import fixture_add_user, fixture_media_entry, fixture_add_activity
try:
    import mock
except ImportError:
    import unittest.mock as mock

import pytest

class FakeUUID(object):
    hex = 'testtest-test-test-test-testtesttest'


UUID_MOCK = mock.Mock(return_value=FakeUUID())
REQUEST_CONTEXT = [
 'mediagoblin/root.html', 'request']

class TestMediaEntrySlugs(object):

    def _setup(self):
        self.chris_user = fixture_add_user('chris')
        self.emily_user = fixture_add_user('emily')
        self.existing_entry = self._insert_media_entry_fixture(title='Beware, I exist!', slug='beware-i-exist')

    def _insert_media_entry_fixture(self, title=None, slug=None, this_id=None, uploader=None, save=True):
        entry = MediaEntry()
        entry.title = title or 'Some title'
        entry.slug = slug
        entry.id = this_id
        entry.actor = uploader or self.chris_user.id
        entry.media_type = 'image'
        if save:
            entry.save()
        return entry

    def test_unique_slug_from_title(self, test_app):
        self._setup()
        entry = self._insert_media_entry_fixture('Totally unique slug!', save=False)
        entry.generate_slug()
        assert entry.slug == 'totally-unique-slug'

    def test_old_good_unique_slug(self, test_app):
        self._setup()
        entry = self._insert_media_entry_fixture('A title here', 'a-different-slug-there', save=False)
        entry.generate_slug()
        assert entry.slug == 'a-different-slug-there'

    def test_old_weird_slug(self, test_app):
        self._setup()
        entry = self._insert_media_entry_fixture(slug='wowee!!!!!', save=False)
        entry.generate_slug()
        assert entry.slug == 'wowee'

    def test_existing_slug_use_id(self, test_app):
        self._setup()
        entry = self._insert_media_entry_fixture('Beware, I exist!!', this_id=9000, save=False)
        entry.generate_slug()
        assert entry.slug == 'beware-i-exist-9000'

    def test_existing_slug_cant_use_id(self, test_app):
        self._setup()

        @mock.patch('uuid.uuid4', UUID_MOCK)
        def _real_test():
            self._insert_media_entry_fixture(slug='beware-i-exist-9000')
            entry = self._insert_media_entry_fixture('Beware, I exist!!', this_id=9000, save=False)
            entry.generate_slug()
            assert entry.slug == 'beware-i-exist-test'

        _real_test()

    def test_existing_slug_cant_use_id_extra_junk(self, test_app):
        self._setup()

        @mock.patch('uuid.uuid4', UUID_MOCK)
        def _real_test():
            self._insert_media_entry_fixture(slug='beware-i-exist-9000')
            self._insert_media_entry_fixture(slug='beware-i-exist-test')
            entry = self._insert_media_entry_fixture('Beware, I exist!!', this_id=9000, save=False)
            entry.generate_slug()
            assert entry.slug == 'beware-i-exist-testtest'

        _real_test()

    def test_garbage_slug(self, test_app):
        r"""
        Titles that sound totally like Q*Bert shouldn't have slugs at
        all.  We'll just reference them by id.

                  ,
                 / \      (@!#?@!)
                |\,/|   ,-,  /
                | |#|  ( ")~
               / \|/ \  L L
              |\,/|\,/|
              | |#, |#|
             / \|/ \|/             |\,/|\,/|\,/|
            | |#| |#| |#|
           / \|/ \|/ \|/           |\,/|\,/|\,/|\,/|
          | |#| |#| |#| |#|
           \|/ \|/ \|/ \|/
        """
        self._setup()
        qbert_entry = self._insert_media_entry_fixture('@!#?@!', save=False)
        qbert_entry.generate_slug()
        assert qbert_entry.slug is None


class TestUserHasPrivilege:

    def _setup(self):
        fixture_add_user('natalie', privileges=[
         'admin', 'moderator', 'active'])
        fixture_add_user('aeva', privileges=[
         'moderator', 'active'])
        self.natalie_user = LocalUser.query.filter(LocalUser.username == 'natalie').first()
        self.aeva_user = LocalUser.query.filter(LocalUser.username == 'aeva').first()

    def test_privilege_added_correctly(self, test_app):
        self._setup()
        admin = Privilege.query.filter(Privilege.privilege_name == 'admin').one()
        assert admin in self.natalie_user.all_privileges
        assert admin not in self.aeva_user.all_privileges

    def test_user_has_privilege_one(self, test_app):
        self._setup()
        assert not self.aeva_user.has_privilege('admin')
        assert self.natalie_user.has_privilege('active')

    def test_allow_admin(self, test_app):
        self._setup()
        assert self.natalie_user.has_privilege('commenter')
        assert not self.natalie_user.has_privilege('commenter', allow_admin=False)


def test_media_data_init(test_app):
    Session.rollback()
    Session.remove()
    media = MediaEntry()
    media.media_type = 'mediagoblin.media_types.image'
    assert media.media_data is None
    media.media_data_init()
    assert media.media_data is not None
    obj_in_session = 0
    for obj in Session():
        obj_in_session += 1
        print(repr(obj))

    assert obj_in_session == 0


class TestUserUrlForSelf(MGClientTestCase):
    usernames = [
     (
      'lindsay', dict(privileges=['active']))]

    def test_url_for_self(self):
        _, request = self.do_get('/', *REQUEST_CONTEXT)
        assert self.user('lindsay').url_for_self(request.urlgen) == '/u/lindsay/'

    def test_url_for_self_not_callable(self):
        _, request = self.do_get('/', *REQUEST_CONTEXT)

        def fake_urlgen():
            pass

        with pytest.raises(TypeError) as (excinfo):
            self.user('lindsay').url_for_self(fake_urlgen())
        assert excinfo.errisinstance(TypeError)
        assert 'object is not callable' in str(excinfo)