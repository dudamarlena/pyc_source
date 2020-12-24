# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-odnoklassniki-photos/odnoklassniki_photos/tests.py
# Compiled at: 2015-11-01 17:30:14
from datetime import datetime, date
from django.test import TestCase
from django.utils import timezone
from odnoklassniki_api.api import OdnoklassnikiError
from odnoklassniki_groups.factories import GroupFactory
from odnoklassniki_users.factories import UserFactory
from odnoklassniki_users.models import User
import simplejson as json
from .factories import AlbumFactory, PhotoFactory
from .models import Album, Photo
GROUP_ID = 50415375614101
ALBUM1_ID = 51836162801813
ALBUM2_ID = 51751246299285
ALBUM_BIG_ID = 51324428026005
PHOTO_ID = 544442732181
GROUP_SMALL_ID = 53129767747696
ALBUM_BIG2_ID = 53169390747760
PHOTO1_ID = 585084794224
PHOTO2_ID = 584955983472
DISCUSSION_ID = 62575868474773

class OdnoklassnikiPhotosTest(TestCase):

    def test_album_fetch(self):
        group = GroupFactory(id=GROUP_ID)
        self.assertEqual(Album.objects.count(), 0)
        albums = Album.remote.fetch(group=group, all=True)
        self.assertTrue(len(albums) > 360)
        self.assertEqual(Album.objects.count(), len(albums))
        albums2 = Album.remote.fetch_group_specific(group=group, ids=[ALBUM1_ID, ALBUM2_ID])
        self.assertEqual(len(albums2), 2)
        self.assertTrue(set(albums2).issubset(set(albums)))
        for album in albums2:
            self.assertEqual(album, albums.filter(id=album.id)[0])
            self.assertEqual(album.owner, group)
            self.assertTrue(album.likes_count > 0)
            self.assertTrue(album.last_like_date is not None)
            self.assertTrue(album.created is not None)
            self.assertTrue(len(album.owner_name) > 0)
            self.assertTrue(len(album.title) > 0)

        albums_part = Album.remote.fetch(group=group, count=40)
        self.assertTrue(albums_part.count() < 40)
        self.assertTrue(albums_part.count() > 0)
        self.assertRaises(OdnoklassnikiError, Album.remote.fetch, group=group, count=Album.remote.__class__.fetch_album_limit + 20)
        albums_part2 = Album.remote.fetch(group=group)
        self.assertTrue(albums_part2.count() < Album.remote.__class__.fetch_album_limit)
        albums_all = Album.remote.fetch(group=group, count=90, all=True)
        self.assertTrue(albums_all.count() > 360)
        self.assertRaises(Exception, Album.remote.fetch, all=True)
        self.assertRaises(Exception, Album.remote.fetch, group=11)
        self.assertRaises(Exception, Album.remote.fetch, group='')
        return

    def test_album_fetch_specific(self):
        group = GroupFactory(id=GROUP_ID)
        album1 = Album.remote.fetch_group_specific(group=group, count=1, ids=[ALBUM1_ID, ALBUM2_ID])
        self.assertEqual(album1.count(), 1)
        album1 = Album.remote.fetch_group_specific(group=group, ids=[ALBUM1_ID])
        self.assertEqual(album1.count(), 1)
        albums_not_all = Album.remote.fetch_group_specific(group=group, ids=[ALBUM1_ID, ALBUM2_ID], all=True)
        self.assertEqual(albums_not_all.count(), 2)
        self.assertRaises(Exception, Album.remote.fetch_group_specific, group=11)
        self.assertRaises(Exception, Album.remote.fetch_group_specific, group=group, ids=11)

    def test_album_fetch_photos(self):
        self.assertEqual(Album.objects.count(), 0)
        self.assertEqual(Photo.objects.count(), 0)
        group = GroupFactory(id=GROUP_ID)
        album = AlbumFactory(id=ALBUM_BIG_ID, owner=group)
        photos = album.fetch_photos(count=50)
        self.assertEqual(photos.count(), 50)
        self.assertEqual(photos.count(), Photo.objects.count())
        Photo.objects.all().delete()
        photos = album.fetch_photos(all=True)
        self.assertGreater(photos.count(), 300)
        self.assertEqual(photos.count(), Photo.objects.count())
        album = Album.objects.get(pk=album.pk)
        self.assertNotEqual(album.updated, None)
        return

    def test_album_fetch_photos_after_before(self):
        group = GroupFactory(id=GROUP_ID)
        album = AlbumFactory(id=ALBUM_BIG_ID, owner=group)
        after = datetime(2013, 9, 13, 5, 20, 25).replace(tzinfo=timezone.utc)
        photos_after = album.fetch_photos(all=True, after=after)
        self.assertLess(photos_after.count(), 50)
        self.assertEqual(photos_after.count(), 41)
        self.assertEqual(photos_after.filter(created__lt=after).count(), 0)

    def test_album_parse(self):
        response = '{"albums":\n            [{"photos_count": 335,\n              "created": "2012-09-22",\n              "title": "\\u0414\\u0435\\u043d\\u044c \\u0432 \\u0438\\u0441\\u0442\\u043e\\u0440\\u0438\\u0438",\n              "author_name": "\\u0420\\u0418\\u0410 \\u041d\\u043e\\u0432\\u043e\\u0441\\u0442\\u0438",\n              "like_count": 8555,\n              "attrs": {"flags": "l"},\n              "liked_it": false,\n              "like_summary": {"count": 8555, "like_possible": true, "self": false, "like_id": "nhIyoINYykF3rWr8_88J9A", "unlike_possible": true, "last_like_date_ms": 1399567588656},\n              "aid": "51324428026005",\n              "group_id": "50415375614101",\n              "author_type": "GROUP"\n            }]}\n            '
        instance = Album()
        group = GroupFactory(id=GROUP_ID)
        instance.parse(json.loads(response)['albums'][0])
        instance.save()
        self.assertEqual(instance.id, 51324428026005)
        self.assertEqual(instance.owner_name, 'РИА Новости')
        self.assertEqual(instance.last_like_date, datetime(2014, 5, 8, 16, 46, 28, tzinfo=timezone.utc))
        self.assertEqual(instance.owner, group)
        self.assertIsInstance(instance.created, datetime)

    def test_group_fetch_albums(self):
        group = GroupFactory(id=GROUP_ID)
        albums = group.fetch_albums(all=True)
        self.assertTrue(len(albums) > 360)
        self.assertEqual(Album.objects.count(), len(albums))

    def test_photo_fetch(self):
        group_big = GroupFactory(id=GROUP_ID)
        album = AlbumFactory(id=ALBUM_BIG_ID, owner=group_big)
        group_small = GroupFactory(id=GROUP_SMALL_ID)
        album2 = AlbumFactory(id=ALBUM_BIG2_ID, owner=group_small)
        self.assertEqual(Album.objects.count(), 2)
        self.assertRaises(Exception, Photo.remote.fetch, group=11)
        self.assertRaises(Exception, Photo.remote.fetch, group='')
        photos_all = Photo.remote.fetch(group=group_small, all=True)
        self.assertTrue(len(photos_all) > 0)
        self.assertEqual(Photo.objects.count(), len(photos_all))
        Photo.objects.all().delete()
        self.assertEqual(Photo.objects.count(), 0)
        photos_album_all = Photo.remote.fetch(group=group_big, album=album, all=True)
        self.assertTrue(len(photos_album_all) > 0)
        self.assertEqual(Photo.objects.count(), len(photos_album_all))
        Photo.objects.all().delete()
        photos_album_all2 = Photo.remote.fetch(group=group_big, album=album, count=230, all=True)
        self.assertEqual(len(photos_album_all2), len(photos_album_all))
        self.assertEqual(Photo.objects.count(), len(photos_album_all2))
        Photo.objects.all().delete()
        photos_group_part = Photo.remote.fetch(group=group_small, count=110)
        self.assertEqual(len(photos_group_part), 110)
        self.assertEqual(Photo.objects.count(), len(photos_group_part))
        Photo.objects.all().delete()
        photos = Photo.remote.fetch(group=group_small, count=Photo.remote.__class__.fetch_photo_limit)
        self.assertEqual(len(photos), Photo.remote.__class__.fetch_photo_limit)
        Photo.objects.all().delete()
        photos = Photo.remote.fetch(group=group_small, count=50)
        self.assertEqual(len(photos), 50)
        Photo.objects.all().delete()
        photos_all3 = Photo.remote.fetch(group=group_small)
        self.assertEqual(photos_all3.count(), len(photos_all))
        Photo.objects.all().delete()
        photos_album_all3 = Photo.remote.fetch(group=group_small, album=album2, all=True)
        album_count = len(photos_album_all3)
        Photo.objects.all().delete()
        photos_album_all4 = Photo.remote.fetch(group=group_small, album=album2)
        self.assertEqual(photos_album_all4.count(), album_count)
        Photo.objects.all().delete()
        photos_group_album_part = Photo.remote.fetch(group=group_small, album=album2, count=110)
        self.assertTrue(len(photos_group_album_part) > 0)
        self.assertEqual(Photo.objects.count(), len(photos_group_album_part))
        Photo.objects.all().delete()
        photos = Photo.remote.fetch(group=group_small, album=album2, count=100)
        self.assertEqual(len(photos), 100)
        Photo.objects.all().delete()
        photos = Photo.remote.fetch(group=group_small, album=album2, count=50)
        self.assertEqual(len(photos), 50)
        Photo.objects.all().delete()
        self.assertRaises(Exception, Photo.remote.fetch, group=group_small, album=11)
        self.assertRaises(Exception, Photo.remote.fetch, group=group_small, album='')
        self.assertRaises(Exception, Album.remote.fetch, all=True)

    def test_photo_fetch_group_specific(self):
        group = GroupFactory(id=GROUP_SMALL_ID)
        album = AlbumFactory(id=ALBUM_BIG2_ID, owner=group)
        self.assertEqual(Album.objects.count(), 1)
        self.assertRaises(Exception, Photo.remote.fetch_group_specific, group=11)
        self.assertRaises(Exception, Photo.remote.fetch_group_specific, group='')
        self.assertRaises(Exception, Photo.remote.fetch_group_specific, group=group, ids=[PHOTO1_ID, PHOTO2_ID])
        self.assertRaises(Exception, Photo.remote.fetch_group_specific, group=group, album=11, ids=[PHOTO1_ID, PHOTO2_ID])
        self.assertRaises(Exception, Photo.remote.fetch_group_specific, group=group)
        self.assertRaises(Exception, Photo.remote.fetch_group_specific, group=group, ids=111)
        photos = Photo.remote.fetch_group_specific(group=group, album=album, ids=[PHOTO1_ID, PHOTO2_ID])
        self.assertEqual(len(photos), 2)
        self.assertEqual(Photo.objects.count(), len(photos))

    def test_photo_fetch_likes(self, *kwargs):
        group = GroupFactory(id=GROUP_ID)
        album = AlbumFactory(id=ALBUM_BIG_ID, owner=group)
        photo = Photo.remote.fetch_group_specific(group=group, album=album, ids=[PHOTO_ID])[0]
        self.assertEqual(photo.like_users.count(), 0)
        users = photo.fetch_likes(count=50)
        self.assertEqual(50, len(users))
        self.assertEqual(50, User.objects.count())
        users = photo.fetch_likes(all=True)
        self.assertGreater(users.count(), User.remote.__class__.fetch_users_limit)
        self.assertEqual(users.count(), photo.likes_count - 1)
        self.assertEqual(users.count(), User.objects.count())
        self.assertEqual(users.count(), photo.like_users.count())

    def test_photo_parse(self):
        response = '{"photos":\n            [{"album_id": "51324428026005",\n             "standard_height": 768,\n             "created_ms": 1390456312257,\n             "author_name": "\\u0420\\u0418\\u0410 \\u041d\\u043e\\u0432\\u043e\\u0441\\u0442\\u0438",\n             "like_count": 147,\n             "attrs": {"flags": "l,s"},\n             "pic180min": "http://itd2.mycdn.me/getImage?photoId=544442732181&photoType=13&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "like_summary": {"count": 147, "like_possible": true, "self": false, "like_id": "7QQmgWn6-sgl9skZmB4Rsg07GJziF49kdwtS94a7c3s", "unlike_possible": true, "last_like_date_ms": 1397655462641},\n             "id": "544442732181",\n             "pic50x50": "http://groupava1.mycdn.me/getImage?photoId=544442732181&photoType=4&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "standard_width": 768,\n             "text": "\\u0415\\u0441\\u043b\\u0438 \\u0432\\u044b \\u0434\\u0430\\u0432\\u043d\\u043e \\u043d\\u0435 \\u043f\\u0438\\u0441\\u0430\\u043b\\u0438 \\u043a\\u043e\\u043c\\u0443-\\u043d\\u0438\\u0431\\u0443\\u0434\\u044c \\u0440\\u0443\\u043a\\u043e\\u043f\\u0438\\u0441\\u043d\\u044b\\u0435 \\u043f\\u043e\\u0441\\u043b\\u0430\\u043d\\u0438\\u044f \\u2014 \\u0441\\u0435\\u0433\\u043e\\u0434\\u043d\\u044f \\u0435\\u0441\\u0442\\u044c \\u043f\\u043e\\u0432\\u043e\\u0434: \\u0432 \\u043c\\u0438\\u0440\\u0435 \\u043e\\u0442\\u043c\\u0435\\u0447\\u0430\\u044e\\u0442 \\u0414\\u0435\\u043d\\u044c \\u0440\\u0443\\u0447\\u043d\\u043e\\u0433\\u043e \\u043f\\u0438\\u0441\\u044c\\u043c\\u0430 \\u0438\\u043b\\u0438, \\u043f\\u0440\\u043e\\u0449\\u0435 \\u0433\\u043e\\u0432\\u043e\\u0440\\u044f, \\u043f\\u043e\\u0447\\u0435\\u0440\\u043a\\u0430, \\u043a\\u043e\\u0442\\u043e\\u0440\\u044b\\u0439 \\u0443 \\u043a\\u0430\\u0436\\u0434\\u043e\\u0433\\u043e \\u0447\\u0435\\u043b\\u043e\\u0432\\u0435\\u043a\\u0430 \\u0443\\u043d\\u0438\\u043a\\u0430\\u043b\\u0435\\u043d.",\n             "discussion_summary": {"discussion_type": "GROUP_PHOTO", "comments_count": 4, "discussion_id": "544442732181"},\n             "author_type": "GROUP",\n             "pic640x480": "http://dg52.mycdn.me/getImage?photoId=544442732181&photoType=0&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "pic1024max": "http://dg52.mycdn.me/getImage?photoId=544442732181&photoType=3&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "liked_it": false,\n             "pic320min": "http://itd2.mycdn.me/getImage?photoId=544442732181&photoType=15&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "pic1024x768": "http://dg52.mycdn.me/getImage?photoId=544442732181&photoType=3&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "pic128x128": "http://itd2.mycdn.me/getImage?photoId=544442732181&photoType=23&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "pic240min": "http://itd2.mycdn.me/getImage?photoId=544442732181&photoType=14&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "comments_count": 4,\n             "pic128max": "http://dg52.mycdn.me/getImage?photoId=544442732181&photoType=2&viewToken=zTBy6mruu-TknmDenjXlwg",\n             "group_id": "50415375614101"}]}\n            '
        instance = Photo()
        group = GroupFactory(id=GROUP_ID)
        album = AlbumFactory(id=ALBUM_BIG_ID, owner=group)
        instance.parse(json.loads(response)['photos'][0])
        instance.save()
        self.assertEqual(instance.id, 544442732181)
        self.assertEqual(instance.created, datetime(2014, 1, 23, 5, 51, 52, tzinfo=timezone.utc))
        self.assertEqual(instance.owner_name, 'РИА Новости')
        self.assertEqual(instance.likes_count, 147)
        self.assertEqual(instance.comments_count, 4)
        self.assertEqual(instance.last_like_date, datetime(2014, 4, 16, 13, 37, 42, tzinfo=timezone.utc))
        self.assertEqual(instance.pic1024max, 'http://dg52.mycdn.me/getImage?photoId=544442732181&photoType=3&viewToken=zTBy6mruu-TknmDenjXlwg')
        self.assertEqual(instance.pic1024x768, 'http://dg52.mycdn.me/getImage?photoId=544442732181&photoType=3&viewToken=zTBy6mruu-TknmDenjXlwg')
        self.assertEqual(instance.pic128max, 'http://dg52.mycdn.me/getImage?photoId=544442732181&photoType=2&viewToken=zTBy6mruu-TknmDenjXlwg')
        self.assertEqual(instance.pic128x128, 'http://itd2.mycdn.me/getImage?photoId=544442732181&photoType=23&viewToken=zTBy6mruu-TknmDenjXlwg')
        self.assertEqual(instance.pic180min, 'http://itd2.mycdn.me/getImage?photoId=544442732181&photoType=13&viewToken=zTBy6mruu-TknmDenjXlwg')
        self.assertEqual(instance.pic240min, 'http://itd2.mycdn.me/getImage?photoId=544442732181&photoType=14&viewToken=zTBy6mruu-TknmDenjXlwg')
        self.assertEqual(instance.pic50x50, 'http://groupava1.mycdn.me/getImage?photoId=544442732181&photoType=4&viewToken=zTBy6mruu-TknmDenjXlwg')
        self.assertEqual(instance.pic640x480, 'http://dg52.mycdn.me/getImage?photoId=544442732181&photoType=0&viewToken=zTBy6mruu-TknmDenjXlwg')
        self.assertEqual(instance.standard_height, 768)
        self.assertEqual(instance.standard_width, 768)
        self.assertEqual(instance.text, 'Если вы давно не писали кому-нибудь рукописные послания — сегодня есть повод: в мире отмечают День ручного письма или, проще говоря, почерка, который у каждого человека уникален.')
        self.assertEqual(instance.owner, group)
        self.assertEqual(instance.album, album)