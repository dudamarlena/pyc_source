# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_misc.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 5453 bytes
import pytz, datetime
from werkzeug.datastructures import FileStorage
from .resources import GOOD_JPG
from mediagoblin.db.base import Session
from mediagoblin.media_types import sniff_media
from mediagoblin.submit.lib import new_upload_entry
from mediagoblin.submit.task import collect_garbage
from mediagoblin.db.models import User, MediaEntry, TextComment, Comment
from mediagoblin.tests.tools import fixture_add_user, fixture_media_entry

def test_404_for_non_existent(test_app):
    res = test_app.get('/does-not-exist/', expect_errors=True)
    assert res.status_int == 404


def test_user_deletes_other_comments(test_app):
    user_a = fixture_add_user('chris_a')
    user_b = fixture_add_user('chris_b')
    media_a = fixture_media_entry(uploader=user_a.id, save=False, expunge=False, fake_upload=False)
    media_b = fixture_media_entry(uploader=user_b.id, save=False, expunge=False, fake_upload=False)
    Session.add(media_a)
    Session.add(media_b)
    Session.flush()
    for u in (user_a, user_b):
        for m in (media_a, media_b):
            cmt = TextComment()
            cmt.actor = u.id
            cmt.content = 'Some Comment'
            Session.add(cmt)
            Session.flush()
            link = Comment()
            link.target = m
            link.comment = cmt
            Session.add(link)

    Session.flush()
    usr_cnt1 = User.query.count()
    med_cnt1 = MediaEntry.query.count()
    cmt_cnt1 = Comment.query.count()
    User.query.get(user_a.id).delete(commit=False)
    usr_cnt2 = User.query.count()
    med_cnt2 = MediaEntry.query.count()
    cmt_cnt2 = Comment.query.count()
    assert usr_cnt2 == usr_cnt1 - 1
    assert med_cnt2 == med_cnt1 - 1
    assert cmt_cnt2 == cmt_cnt1 - 3
    User.query.get(user_b.id).delete()
    usr_cnt2 = User.query.count()
    med_cnt2 = MediaEntry.query.count()
    cmt_cnt2 = Comment.query.count()
    assert usr_cnt2 == usr_cnt1 - 2
    assert med_cnt2 == med_cnt1 - 2
    assert cmt_cnt2 == cmt_cnt1 - 4


def test_media_deletes_broken_attachment(test_app):
    user_a = fixture_add_user('chris_a')
    media = fixture_media_entry(uploader=user_a.id, save=False, expunge=False)
    media.attachment_files.append(dict(name='some name', filepath=[
     'does', 'not', 'exist']))
    Session.add(media)
    Session.flush()
    MediaEntry.query.get(media.id).delete()
    User.query.get(user_a.id).delete()


def test_garbage_collection_task(test_app):
    """ Test old media entry are removed by GC task """
    user = fixture_add_user()
    entry_id = 72
    now = datetime.datetime.now(pytz.UTC)
    file_data = FileStorage(stream=open(GOOD_JPG, 'rb'), filename='mah_test.jpg', content_type='image/jpeg')
    media_type, media_manager = sniff_media(file_data, 'mah_test.jpg')
    entry = new_upload_entry(user)
    entry.id = entry_id
    entry.title = 'Mah Image'
    entry.slug = 'slugy-slug-slug'
    entry.media_type = 'image'
    entry.created = now - datetime.timedelta(days=2)
    entry.save()
    assert MediaEntry.query.filter_by(id=entry_id).first() is not None
    collect_garbage()
    assert MediaEntry.query.filter_by(id=entry_id).first() is None


def test_comments_removed_when_graveyarded(test_app):
    """ Checks comments which are tombstones are removed from collection """
    user = fixture_add_user()
    media = fixture_media_entry(uploader=user.id, expunge=False, fake_upload=False)
    comment = TextComment()
    comment.actor = user.id
    comment.content = 'This is a comment that will be deleted.'
    comment.save()
    link = Comment()
    link.target = media
    link.comment = comment
    link.save()
    assert Comment.query.filter_by(target_id=link.target_id).first() is not None
    comment.delete()
    assert Comment.query.filter_by(target_id=link.target_id).first() is None