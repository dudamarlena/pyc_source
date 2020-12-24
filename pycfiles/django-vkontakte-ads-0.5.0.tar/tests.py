# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-ads/vkontakte_ads/tests.py
# Compiled at: 2015-02-03 11:46:10
from datetime import date, datetime
from os import path
import mock, simplejson as json
from django.conf import settings
from django.core.files import File
from django.test import TestCase
from django.utils import timezone
from oauth_tokens.models import AccessToken
from .factories import AccountFactory, AdFactory, CampaignFactory, ClientFactory
from .models import Account, Ad, Budget, Campaign, Client, Image, Layout, Statistic, Targeting, TargetingStats
IMAGE_PATH = path.join(path.dirname(__file__), 'static/vkontakte_ads/img/test.gif')
IMAGE_INITIAL_FIELDS = {'hash': '3620036d2588f91bc51829dd55754181', 'photo_hash': '32c9a0192c', 'photo': 'size:s|server:6167|owner_id:16982350|photo_hash:32c9a0192c|name:32c9a0192cx|width:90|height:65|kid:6e953128d1c79f28513aa976a69e92b8|hash:3620036d2588f91bc51829dd55754181', 
   'server': 6167}
ACCOUNT_ID = 1900000934
CLIENT_ID = 1600599323
CAMPAIGN_ID = 1000967943
CAMPAIGN_WITH_MANY_ADS_ID = 1000787419
AD_ID = 3129375

class VkontakteAdsTest(TestCase):

    def setUp(self):
        self.objects_to_delete = []

    def tearDown(self):
        for object in self.objects_to_delete:
            object.delete()

    def test_fetch_accounts(self):
        self.assertEqual(Account.objects.count(), 0)
        Account.remote.fetch()
        count = Account.objects.count()
        self.assertTrue(count > 0)
        Account.remote.fetch()
        self.assertEqual(Account.objects.count(), count)

    def commentedtest_fetch_account_budget(self):
        """
        Commented - only owner of account have permission to do API call
        """
        account = AccountFactory(remote_id=ACCOUNT_ID)
        self.assertEqual(Budget.objects.count(), 0)
        account.fetch_budget()
        self.assertEqual(Budget.objects.count(), 1)
        account.fetch_budget()
        self.assertEqual(Budget.objects.count(), 1)

    def test_fetch_campaigns(self):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        self.assertEqual(Campaign.objects.count(), 0)
        client.fetch_campaigns()
        campaigns_count = Campaign.objects.count()
        self.assertNotEqual(campaigns_count, 0)
        client.fetch_campaigns()
        self.assertEqual(Campaign.objects.count(), campaigns_count)
        ids = [ int(id) for id in Campaign.objects.values_list('remote_id', flat=True)[:1] ]
        Campaign.objects.all().delete()
        self.assertEqual(Campaign.objects.count(), 0)
        client.fetch_campaigns(ids)
        self.assertEqual(Campaign.objects.count(), 1)

    def test_fetch_campaign_statisics(self):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        campaign = CampaignFactory(remote_id=CAMPAIGN_WITH_MANY_ADS_ID, account=account, client=client)
        self.assertEqual(Statistic.objects.count(), 0)
        start_time = timezone.now()
        campaign.fetch_statistics()
        self.assertEqual(Statistic.objects.count(), 1)
        stat = Statistic.objects.all()[0]
        self.assertEqual(stat.content_object, campaign)
        self.assertEqual(stat.overall, True)
        self.assertTrue(stat.fetched > start_time)
        fetched_time = stat.fetched
        campaign.fetch_statistics()
        self.assertEqual(Statistic.objects.count(), 1)
        stat = Statistic.objects.all()[0]
        self.assertTrue(stat.fetched > fetched_time)
        campaign.fetch_statistics(period='month')
        self.assertTrue(Statistic.objects.count() > 1)

    def test_refresh_ad(self):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        campaign = CampaignFactory(remote_id=CAMPAIGN_ID, account=account, client=client)
        campaign.fetch_ads()
        ad = campaign.ads.all()[0]
        cost = ad.cost_type
        ad.name = ad.name + '###'
        ad.save(commit_remote=False)
        ad.refresh()
        self.assertTrue('#' not in ad.name)
        self.assertEqual(ad.cost_type, cost)
        self.assertEqual(ad.campaign, campaign)
        self.assertEqual(ad.account, account)
        self.assertNotEqual(ad.fetched, None)
        ad = Ad.objects.get(pk=ad.pk)
        self.assertTrue('#' not in ad.name)
        return

    def test_fetch_ads(self):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        campaign = CampaignFactory(remote_id=CAMPAIGN_WITH_MANY_ADS_ID, account=account, client=client)
        self.assertEqual(Ad.objects.count(), 0)
        campaign.fetch_ads()
        ads_count = Ad.objects.count()
        self.assertNotEqual(ads_count, 0)
        campaign.fetch_ads()
        self.assertEqual(Ad.objects.count(), ads_count)
        ids = [ int(id) for id in Ad.objects.values_list('pk', flat=True)[:1] ]
        Ad.objects.all().delete()
        self.assertEqual(Ad.objects.count(), 0)
        campaign.fetch_ads(ids)
        self.assertEqual(Ad.objects.count(), 1)

    @mock.patch('vkontakte_ads.models.Ad.objects.get', side_effect=lambda pk: AdFactory(remote_id=pk, account=Account.objects.all()[0], campaign=Campaign.objects.all()[0]))
    def test_fetch_cities_for_ad(self, *args, **kwargs):
        if 'vkontakte_places' in settings.INSTALLED_APPS:
            from vkontakte_places.models import City
            account = AccountFactory(remote_id=ACCOUNT_ID)
            client = ClientFactory(remote_id=CLIENT_ID, account=account)
            campaign = CampaignFactory(remote_id=CAMPAIGN_ID, account=account, client=client)
            self.assertEqual(Targeting.objects.count(), 0)
            self.assertEqual(City.objects.count(), 0)
            campaign.fetch_ads_targeting([AD_ID])
            self.assertEqual(Targeting.objects.count(), 1)
            self.assertTrue(len(Targeting.objects.all()[0].cities.split(',')), 2)
            self.assertEqual(City.objects.count(), 2)

    @mock.patch('vkontakte_ads.models.Ad.objects.get', side_effect=lambda pk: AdFactory(remote_id=pk, account=Account.objects.all()[0], campaign=Campaign.objects.all()[0]))
    def test_fetch_ads_targeting(self, *args, **kwargs):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        campaign = CampaignFactory(remote_id=CAMPAIGN_WITH_MANY_ADS_ID, account=account, client=client)
        self.assertEqual(Targeting.objects.count(), 0)
        campaign.fetch_ads_targeting()
        ads_count = Targeting.objects.count()
        self.assertNotEqual(ads_count, 0)
        campaign.fetch_ads_targeting()
        self.assertEqual(Targeting.objects.count(), ads_count)
        ids = [ int(id) for id in Targeting.objects.values_list('pk', flat=True)[:1] ]
        Targeting.objects.all().delete()
        self.assertEqual(Targeting.objects.count(), 0)
        campaign.fetch_ads_targeting(ids)
        self.assertEqual(Targeting.objects.count(), 1)

    @mock.patch('vkontakte_ads.models.Ad.objects.get', side_effect=lambda pk: AdFactory(remote_id=pk, account=Account.objects.all()[0], campaign=Campaign.objects.all()[0]))
    def test_fetch_ads_layout(self, *args, **kwargs):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        campaign = CampaignFactory(remote_id=CAMPAIGN_WITH_MANY_ADS_ID, account=account, client=client)
        self.assertEqual(Layout.objects.count(), 0)
        campaign.fetch_ads_layout()
        ads_count = Layout.objects.count()
        self.assertNotEqual(ads_count, 0)
        campaign.fetch_ads_layout()
        self.assertEqual(Layout.objects.count(), ads_count)
        ids = [ int(id) for id in Layout.objects.values_list('pk', flat=True)[:1] ]
        Layout.objects.all().delete()
        self.assertEqual(Layout.objects.count(), 0)
        campaign.fetch_ads_layout(ids)
        self.assertEqual(Layout.objects.count(), 1)

    def test_parse_account(self):
        response = '\n            {"response":[{"account_id":"1600001217","account_status":1,"access_role":"admin"}]}\n            '
        instance = Account()
        instance.parse(json.loads(response)['response'][0])
        instance.save()
        self.assertEqual(instance.remote_id, 1600001217)
        self.assertEqual(instance.account_status, True)
        self.assertEqual(instance.access_role, 'admin')
        instance.delete()
        response = '\n            {"response":[{"account_id":"1600001217","account_status":0,"access_role":"admin"}]}\n            '
        instance = Account()
        instance.parse(json.loads(response)['response'][0])
        instance.save()
        self.assertEqual(instance.account_status, False)

    def test_parse_client(self):
        response = '\n            {"response":[{"id":"107111","name":"Ford","day_limit":170,"all_limit":3000}]}\n            '
        account = AccountFactory(remote_id=1)
        instance = Client(account=account, fetched=timezone.now())
        instance.parse(json.loads(response)['response'][0])
        instance.save(commit_remote=False)
        self.assertEqual(instance.account, account)
        self.assertEqual(instance.remote_id, 107111)
        self.assertEqual(instance.name, 'Ford')
        self.assertEqual(instance.day_limit, 170)
        self.assertEqual(instance.all_limit, 3000)

    def test_parse_campaign(self):
        response = '\n            {"response":[\n                {"id":"111","name":"Campaign1","status":0,"day_limit":2000,"all_limit":1000000,"start_time":"0","stop_time":"0"},\n                {"id":"222","name":"Campaign2","status":1,"day_limit":6000,"all_limit":9000000,"start_time":"1298365200","stop_time":"1298451600"}\n            ]}\n            '
        account = AccountFactory(remote_id=1)
        instance = Campaign(account=account, fetched=timezone.now())
        instance.parse(json.loads(response)['response'][0])
        instance.save(commit_remote=False)
        self.assertEqual(instance.remote_id, 111)
        self.assertEqual(instance.name, 'Campaign1')
        self.assertEqual(instance.status, False)
        self.assertEqual(instance.day_limit, 2000)
        self.assertEqual(instance.all_limit, 1000000)
        self.assertEqual(instance.start_time, None)
        self.assertEqual(instance.stop_time, None)
        instance = Campaign(account=account, fetched=timezone.now())
        instance.parse(json.loads(response)['response'][1])
        instance.save(commit_remote=False)
        self.assertTrue(isinstance(instance.account, Account))
        self.assertEqual(instance.account.remote_id, 1)
        self.assertEqual(instance.remote_id, 222)
        self.assertEqual(instance.name, 'Campaign2')
        self.assertEqual(instance.status, True)
        self.assertEqual(instance.day_limit, 6000)
        self.assertEqual(instance.all_limit, 9000000)
        self.assertEqual(instance.start_time, datetime(2011, 2, 22, 9, 0, 0, tzinfo=timezone.utc))
        self.assertEqual(instance.stop_time, datetime(2011, 2, 23, 9, 0, 0, tzinfo=timezone.utc))
        return

    def test_parse_ad(self):
        response = '\n            {"response":[\n                {"id":"607256","campaign_id":"123","name":"Ad1","status":0,"approved":0,"all_limit":0,"cost_type":0,"cpm":118},\n                {"id":"664868","campaign_id":"123","name":"Ad2","status":1,"approved":1,"all_limit":100,"cost_type":1,"cpc":488}\n            ]}\n            '
        account = AccountFactory(remote_id=1)
        campaign = CampaignFactory(account=account, remote_id=1)
        instance = Ad(campaign=campaign, fetched=timezone.now())
        instance.parse(json.loads(response)['response'][0])
        instance.save(commit_remote=False)
        self.assertTrue(isinstance(instance.campaign, Campaign))
        self.assertEqual(instance.campaign.remote_id, 1)
        self.assertEqual(instance.remote_id, 607256)
        self.assertEqual(instance.name, 'Ad1')
        self.assertEqual(instance.status, False)
        self.assertEqual(instance.approved, False)
        self.assertEqual(instance.all_limit, 0)
        self.assertEqual(instance.cpm, 118)
        instance = Ad(campaign=campaign, fetched=timezone.now())
        instance.parse(json.loads(response)['response'][1])
        instance.save(commit_remote=False)
        self.assertEqual(instance.remote_id, 664868)
        self.assertEqual(instance.name, 'Ad2')
        self.assertEqual(instance.status, True)
        self.assertEqual(instance.approved, True)
        self.assertEqual(instance.all_limit, 100)
        self.assertEqual(instance.cpc, 488)

    def test_parse_layout(self):
        response = '\n            {"response":[\n                {"id":"111","campaign_id":"123","title":"Title","description":"Description","link_url":"http://vkontakte.ru","link_domain":"vkontakte.ru","preview_link":"http://vkontakte.ru/ads.php?act=preview_ad&mid=83813&id=111&t=1298281862&hash=71964c09f15a0f44bf"}\n            ]}\n            '
        account = AccountFactory(remote_id=1)
        campaign = CampaignFactory(account=account, remote_id=123)
        ad = AdFactory(campaign=campaign, remote_id=111, cost_type=0, cpc=100)
        instance = ad.layout
        instance.parse(json.loads(response)['response'][0])
        instance.save()
        self.assertEqual(ad.layout, instance)
        self.assertTrue(isinstance(instance.campaign, Campaign))
        self.assertEqual(instance.campaign.remote_id, 123)
        self.assertEqual(instance.ad_id, 111)
        self.assertEqual(instance.title, 'Title')
        self.assertEqual(instance.description, 'Description')
        self.assertEqual(instance.link_url, 'http://vkontakte.ru')
        self.assertEqual(instance.link_domain, 'vkontakte.ru')
        self.assertEqual(instance.preview_link, 'http://vkontakte.ru/ads.php?act=preview_ad&mid=83813&id=111&t=1298281862&hash=71964c09f15a0f44bf')

    def test_parse_targeting(self):
        response = '\n            {"response":[{"id":"111","campaign_id":"123","sex":"0","age_from":"0","age_to":"0","country":"1","cities":"2","count":"523","group_types":"","groups":"","interests":"232116,369651","districts":"125,126","stations":"","streets":"","schools":"1","positions":"","religions":"","statuses":"2,5","school_from":"0","school_to":"2010","uni_from":"0","uni_to":"2013","operators":"","tags":"SPbSU, Programming"}]}\n            '
        account = AccountFactory(remote_id=1)
        campaign = CampaignFactory(account=account, remote_id=123)
        ad = AdFactory(campaign=campaign, remote_id=111, cost_type=0, cpc=100)
        instance = ad.targeting
        instance.parse(json.loads(response)['response'][0])
        instance.save()
        self.assertEqual(ad.targeting, instance)
        self.assertTrue(isinstance(instance.campaign, Campaign))
        self.assertEqual(instance.campaign.remote_id, 123)
        self.assertEqual(instance.ad_id, 111)
        self.assertEqual(instance.sex, 0)
        self.assertEqual(instance.age_from, 0)
        self.assertEqual(instance.age_to, 0)
        self.assertEqual(instance.country, 1)
        self.assertEqual(instance.cities, '2')
        self.assertEqual(instance.count, 523)
        self.assertEqual(instance.group_types, '')
        self.assertEqual(instance.groups, '')
        self.assertEqual(instance.interests, '232116,369651')
        self.assertEqual(instance.districts, '125,126')
        self.assertEqual(instance.stations, '')
        self.assertEqual(instance.streets, '')
        self.assertEqual(instance.schools, '1')
        self.assertEqual(instance.positions, '')
        self.assertEqual(instance.religions, '')
        self.assertEqual(instance.statuses, '2,5')
        self.assertEqual(instance.school_from, 0)
        self.assertEqual(instance.school_to, 2010)
        self.assertEqual(instance.uni_from, 0)
        self.assertEqual(instance.uni_to, 2013)
        self.assertEqual(instance.operators, '')
        self.assertEqual(instance.tags, 'SPbSU, Programming')

    def test_update_campaign(self):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        client.fetch_campaigns(ids=[CAMPAIGN_ID])
        self.assertEqual(Campaign.objects.count(), 1)
        campaign = Campaign.objects.all()[0]
        old_name = campaign.name
        campaign.name += ' _'
        campaign.save()
        client.fetch_campaigns(ids=[CAMPAIGN_ID])
        campaign = Campaign.objects.all()[0]
        self.assertNotEqual(campaign.name, old_name)
        self.assertEqual(campaign.name, old_name + ' _')
        campaign.name = old_name
        campaign.save()

    def test_crud_campaign(self):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        campaign = Campaign.remote.create(account=account, client=client, name='Test_campaign1', day_limit=1000, all_limit=2000)
        self.objects_to_delete += [campaign]
        self.assertTrue(campaign.remote_id > 0)
        self.assertEqual(campaign.day_limit, 1000)
        self.assertEqual(campaign.all_limit, 2000)
        campaign.name = 'Test_campaign2'
        campaign.save()
        client.fetch_campaigns(ids=[campaign.remote_id])
        campaign1 = Campaign.objects.get(remote_id=campaign.remote_id)
        self.assertEqual(campaign1.name, campaign.name)
        self.assertEqual(campaign1.day_limit, 1000)
        self.assertEqual(campaign1.all_limit, 2000)
        campaign1.delete()
        self.assertEqual(Campaign.objects.filter(remote_id=campaign.remote_id)[0].archived, True)
        client.fetch_campaigns(ids=[campaign.remote_id])
        self.assertEqual(Campaign.objects.filter(remote_id=campaign.remote_id)[0].archived, True)
        self.objects_to_delete = []

    def test_crud_ad(self):
        account = AccountFactory(remote_id=ACCOUNT_ID)
        client = ClientFactory(remote_id=CLIENT_ID, account=account)
        campaign = Campaign.remote.create(account=account, client=client, name='Test_campaign1', day_limit=1000, all_limit=2000)
        image = Image(**IMAGE_INITIAL_FIELDS)
        self.objects_to_delete += [campaign]
        self.assertTrue(campaign.remote_id > 0)
        ad = Ad(campaign=campaign, name='Test_ad1', status=False, cost_type=0, image=image, cpc=100, layout__title='111', layout__link_url='http://ya.ru', layout__description='q' * 50)
        ad.save()
        self.objects_to_delete += [ad]
        image.id = None
        ad = Ad.remote.create(campaign=campaign, name='Test_ad2', status=False, cost_type=0, image=image, cpc=100, layout__title='111', layout__link_url='http://ya.ru', layout__description='q' * 50)
        self.objects_to_delete += [ad]
        self.assertTrue(ad.remote_id > 0)
        self.assertEqual(ad.name, 'Test_ad2')
        self.assertEqual(ad.status, False)
        self.assertEqual(ad.cost_type, 0)
        self.assertEqual(ad.cpc, 100)
        ad.name = 'Test_ad3'
        ad.save()
        campaign.fetch_ads(ids=[ad.remote_id])
        ad1 = Ad.objects.get(remote_id=ad.remote_id)
        self.assertTrue(ad1.name == ad.name == 'Test_ad3')
        self.assertEqual(ad1.cpc, 100)
        ad1.delete()
        self.assertEqual(Ad.objects.filter(remote_id=ad.remote_id)[0].archived, True)
        campaign.fetch_ads(ids=[ad.remote_id])
        self.assertEqual(Ad.objects.filter(remote_id=ad.remote_id)[0].archived, True)
        campaign.delete()
        self.objects_to_delete = []
        return

    def test_upload_ad_image(self):
        image = Image(file=File(open(IMAGE_PATH)))
        ad = Ad(cost_type=0, cpc=100, image=image, campaign=Campaign(account=Account(remote_id=1), remote_id=1))
        url = ad.image.get_post_url()
        self.assertTrue('vk.com/upload.php?' in url)
        ad.image.upload()
        self.assertTrue(len(ad.image.hash) > 0)
        self.assertTrue(ad.image.width > 0)
        self.assertTrue(ad.image.height > 0)

    def test_update_fields(self):
        """
        Test for generating update request with only changed fields
        """
        Campaign.remote.api_call = mock.Mock()
        Campaign.remote.api_call.return_value = [{'id': 1}]
        Ad.remote.api_call = mock.Mock()
        Ad.remote.api_call.return_value = [{'id': 1}]
        account = AccountFactory(remote_id=ACCOUNT_ID)
        campaign = Campaign.remote.create(account=account, name='Test_campaign1', day_limit=1000, all_limit=2000)
        Campaign.remote.api_call.assert_called_with(data=[{'status': 0, 'all_limit': 2000, 'name': 'Test_campaign1', 'day_limit': 1000}], account_id=ACCOUNT_ID, method='create')
        campaign.name = 'Test_campaign2'
        campaign.save()
        Campaign.remote.api_call.assert_called_with(data=[{'name': 'Test_campaign2', 'campaign_id': 1}], account_id=ACCOUNT_ID, method='update')
        ad = Ad.remote.create(campaign=campaign, name='Test_ad1', status=False, cost_type=0, image=Image(), cpc=100)
        Ad.remote.api_call.assert_called_with(data=[
         {'status': 0, 'school_from': 0, 'hash': '', 'photo_hash': '', 'title': '', 'photo': '', 'link_url': '', 'cpc': 1.0, 'campaign_id': 1, 'server': None, 'cost_type': 0, 
            'age_to': 0, 'travellers': 0, 'country': 0, 'age_from': 0, 'sex': 0, 'uni_to': 0, 'school_to': 0, 'uni_from': 0, 'name': 'Test_ad1'}], account_id=ACCOUNT_ID, method='create')
        ad.name = 'Test_ad2'
        ad.save()
        Ad.remote.api_call.assert_called_with(data=[{'name': 'Test_ad2', 'ad_id': 1}], account_id=ACCOUNT_ID, method='update')
        return

    def test_targeting_stats(self):
        stat = TargetingStats.remote.get(ad=Ad(account=AccountFactory(remote_id=ACCOUNT_ID), layout__link_domain='www.ford.com', layout__link_url='http://www.ford.com/trucks/ranger/', targeting__sex=2, targeting__age_from=20, targeting__age_to=30))
        self.assertTrue(stat.audience_count > 0)
        self.assertTrue(stat.recommended_cpc > 0)
        self.assertTrue(stat.recommended_cpm > 0)