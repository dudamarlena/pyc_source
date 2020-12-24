# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_collections.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 1223 bytes
from mediagoblin.tests.tools import fixture_add_collection, fixture_add_user
from mediagoblin.db.models import Collection, User

def test_user_deletes_collection(test_app):
    user = fixture_add_user()
    coll = fixture_add_collection(user=user)
    user = User.query.get(user.id)
    cnt1 = Collection.query.count()
    user.delete()
    cnt2 = Collection.query.count()
    assert cnt1 == cnt2 + 1