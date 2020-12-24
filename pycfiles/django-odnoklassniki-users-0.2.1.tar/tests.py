# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-odnoklassniki-users/odnoklassniki_users/tests.py
# Compiled at: 2015-03-06 07:16:55
from datetime import datetime, timedelta
from django.test import TestCase
from django.utils import timezone
import mock, simplejson as json
from .factories import UserFactory
from .models import User, USER_INFO_TIMEOUT_DAYS
USER1_ID = 561348705024
USER1_NAME = 'Евгений Дуров'
USER2_ID = 578592731938
USER_SLUG_ID = 31073078859

def user_fetch_mock(**kwargs):
    ids = kwargs.get('uids').split(',')
    users = [ User.objects.get(id=id) if User.objects.filter(id=id).count() == 1 else UserFactory(id=id) for id in ids ]
    ids = [ user.pk for user in users ]
    return User.objects.filter(pk__in=ids)


class OdnoklassnikiUsersTest(TestCase):

    def test_get_by_url(self):
        user = UserFactory(id=USER_SLUG_ID)
        self.assertEqual(User.objects.count(), 1)
        urls = ('http://ok.ru/ivanov/', 'http://ok.ru/ivanov', 'http://odnoklassniki.ru/ivanov',
                'http://www.odnoklassniki.ru/ivanov', 'http://www.odnoklassniki.ru/profile/31073078859')
        for url in urls:
            instance = User.remote.get_by_url(url)
            self.assertEqual(instance.id, USER_SLUG_ID)

    def test_refresh_user(self):
        instance = User.remote.fetch(ids=[USER1_ID])[0]
        self.assertEqual(instance.name, USER1_NAME)
        instance.name = 'temp'
        instance.save()
        self.assertEqual(instance.name, 'temp')
        instance.refresh()
        self.assertEqual(instance.name, USER1_NAME)

    def test_fetch_user(self):
        self.assertEqual(User.objects.count(), 0)
        users = User.remote.fetch(ids=[USER1_ID, USER2_ID])
        self.assertEqual(len(users), 2)
        self.assertEqual(User.objects.count(), 2)
        instance = users.get(id=USER1_ID)
        self.assertEqual(instance.id, USER1_ID)
        self.assertEqual(instance.name, USER1_NAME)
        self.assertTrue(isinstance(instance.registered_date, datetime))

    @mock.patch('odnoklassniki_api.models.OdnoklassnikiManager.fetch', side_effect=user_fetch_mock)
    def test_fetch_users_more_than_100(self, fetch):
        users = User.remote.fetch(ids=range(0, 150))
        self.assertEqual(len(users), 150)
        self.assertEqual(User.objects.count(), 150)
        self.assertEqual(len(fetch.mock_calls[0].call_list()[0][2]['uids'].split(',')), 100)
        self.assertEqual(len(fetch.mock_calls[1].call_list()[0][2]['uids'].split(',')), 50)

    @mock.patch('odnoklassniki_api.models.OdnoklassnikiManager.fetch', side_effect=user_fetch_mock)
    def test_fetching_expired_users(self, fetch):
        users = User.remote.fetch(ids=range(0, 50))
        User.objects.all().update(fetched=timezone.now())
        User.objects.filter(pk__lt=10).update(fetched=timezone.now() - timedelta(USER_INFO_TIMEOUT_DAYS + 1))
        users_new = User.remote.fetch(ids=range(0, 50), only_expired=True)
        self.assertEqual(len(fetch.mock_calls[0].call_list()[0][2]['uids'].split(',')), 50)
        self.assertEqual(len(fetch.mock_calls[1].call_list()[0][2]['uids'].split(',')), 10)
        self.assertEqual(users.count(), 50)
        self.assertEqual(users.count(), users_new.count())

    def test_parse_user(self):
        response = '[{\n              "allows_anonym_access": true,\n              "birthday": "05-11",\n              "current_status": "собщество генерал шермон",\n              "current_status_date": "2013-11-12 03:45:01",\n              "current_status_id": "62725470887936",\n              "first_name": "Евгений",\n              "gender": "male",\n              "has_email": false,\n              "has_service_invisible": false,\n              "last_name": "Дуров",\n              "last_online": "2014-04-09 02:35:10",\n              "locale": "r",\n              "location": {"city": "Кемерово",\n               "country": "RUSSIAN_FEDERATION",\n               "countryCode": "RU"},\n              "name": "Евгений Дуров",\n              "photo_id": "508669228288",\n              "pic1024x768": "http://uld1.mycdn.me/getImage?photoId=508669228288&photoType=3&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic128max": "http://usd1.mycdn.me/getImage?photoId=508669228288&photoType=2&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic128x128": "http://umd1.mycdn.me/getImage?photoId=508669228288&photoType=6&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic180min": "http://itd0.mycdn.me/getImage?photoId=508669228288&photoType=13&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic190x190": "http://i500.mycdn.me/getImage?photoId=508669228288&photoType=5&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic240min": "http://itd0.mycdn.me/getImage?photoId=508669228288&photoType=14&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic320min": "http://itd0.mycdn.me/getImage?photoId=508669228288&photoType=15&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic50x50": "http://i500.mycdn.me/getImage?photoId=508669228288&photoType=4&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic640x480": "http://uld1.mycdn.me/getImage?photoId=508669228288&photoType=0&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic_1": "http://i500.mycdn.me/getImage?photoId=508669228288&photoType=4&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic_2": "http://usd1.mycdn.me/getImage?photoId=508669228288&photoType=2&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic_3": "http://i500.mycdn.me/getImage?photoId=508669228288&photoType=5&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic_4": "http://uld1.mycdn.me/getImage?photoId=508669228288&photoType=0&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "pic_5": "http://umd1.mycdn.me/getImage?photoId=508669228288&photoType=6&viewToken=1gbG-ihJLgI5L_XujVV_6A",\n              "private": false,\n              "registered_date": "2012-11-05 14:13:53",\n              "uid": "561348705024",\n              "url_profile": "http://www.odnoklassniki.ru/profile/561348705024",\n              "url_profile_mobile": "http://www.odnoklassniki.ru/profile/?st.application_key=CBAEBGLBEBABABABA&st.signature=d9867421a0017d9a08c17a206edf2730&st.reference_id=561348705024"}]'
        instance = User()
        instance.parse(json.loads(response)[0])
        instance.save()
        self.assertEqual(instance.id, 561348705024)
        self.assertEqual(instance.name, 'Евгений Дуров')
        self.assertEqual(instance.allows_anonym_access, True)
        self.assertEqual(instance.birthday, '05-11')
        self.assertEqual(instance.current_status, 'собщество генерал шермон')
        self.assertEqual(instance.current_status_id, 62725470887936)
        self.assertEqual(instance.first_name, 'Евгений')
        self.assertEqual(instance.gender, 2)
        self.assertEqual(instance.has_email, False)
        self.assertEqual(instance.has_service_invisible, False)
        self.assertEqual(instance.last_name, 'Дуров')
        self.assertIsInstance(instance.current_status_date, datetime)
        self.assertIsInstance(instance.last_online, datetime)
        self.assertEqual(instance.locale, 'r')
        self.assertEqual(instance.city, 'Кемерово')
        self.assertEqual(instance.country, 'RUSSIAN_FEDERATION')
        self.assertEqual(instance.country_code, 'RU')
        self.assertEqual(instance.name, 'Евгений Дуров')
        self.assertEqual(instance.photo_id, 508669228288)
        self.assertEqual(instance.pic1024x768, 'http://uld1.mycdn.me/getImage?photoId=508669228288&photoType=3&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.pic128max, 'http://usd1.mycdn.me/getImage?photoId=508669228288&photoType=2&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.pic128x128, 'http://umd1.mycdn.me/getImage?photoId=508669228288&photoType=6&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.pic180min, 'http://itd0.mycdn.me/getImage?photoId=508669228288&photoType=13&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.pic190x190, 'http://i500.mycdn.me/getImage?photoId=508669228288&photoType=5&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.pic240min, 'http://itd0.mycdn.me/getImage?photoId=508669228288&photoType=14&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.pic320min, 'http://itd0.mycdn.me/getImage?photoId=508669228288&photoType=15&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.pic50x50, 'http://i500.mycdn.me/getImage?photoId=508669228288&photoType=4&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.pic640x480, 'http://uld1.mycdn.me/getImage?photoId=508669228288&photoType=0&viewToken=1gbG-ihJLgI5L_XujVV_6A')
        self.assertEqual(instance.private, False)
        self.assertIsInstance(instance.registered_date, datetime)
        self.assertEqual(instance.url_profile, 'http://www.odnoklassniki.ru/profile/561348705024')
        self.assertEqual(instance.url_profile_mobile, 'http://www.odnoklassniki.ru/profile/?st.application_key=CBAEBGLBEBABABABA&st.signature=d9867421a0017d9a08c17a206edf2730&st.reference_id=561348705024')