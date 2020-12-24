# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-ads/vkontakte_ads/models.py
# Compiled at: 2015-02-03 11:42:33
import logging, os, time
from datetime import datetime
import requests, simplejson as json
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.query import QuerySet
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _
from smart_selects.db_fields import ChainedForeignKey
from vkontakte import VKError
from vkontakte_api import fields
from vkontakte_api.models import VkontakteContentError, VkontakteCRUDManager, VkontakteCRUDModel, VkontakteManager, VkontakteModel, VkontaktePKModel
COMMIT_REMOTE = getattr(settings, 'VKONTAKTE_ADS_COMMIT_REMOTE', True)
log = logging.getLogger('vkontakte_ads')
ERROR_CODES = (
 (
  1, _('Unknown error occurred.')),
 (
  4, _('Incorrect signature.')),
 (
  5, _('User authorization failed.')),
 (
  6, _('Too many requests per second.')),
 (
  7, _('Permission to perform this action is denied by user.')),
 (
  10, _('Internal server error')),
 (
  100, _('One of the parameters specified was missing or invalid.')),
 (
  600, _('Permission denied. You have no access to operations specified with given object(s).')),
 (
  603, _('Specific error.')))
ACCOUNT_ACCESS_ROLE_CHOICES = (
 ('admin', 'главный администратор'),
 ('manager', 'администратор'),
 ('reports', 'наблюдатель'))
TARGETING_GROUP_TYPES_CHOICES = [
 [
  32, 'R&B'],
 [
  33, 'Rap & Hip-Hop'],
 [
  92, 'Автомобили'],
 [
  93, 'Автоспорт'],
 [
  58, 'Азартные игры'],
 [
  81, 'Академические группы'],
 [
  47, 'Баскетбол'],
 [
  76, 'Бизнес'],
 [
  79, 'Благотворительность'],
 [
  26, 'Блюз'],
 [
  55, 'Боевые искусства'],
 [
  15, 'ВКонтакте'],
 [
  49, 'Велосипеды'],
 [
  54, 'Водный спорт'],
 [
  86, 'Города'],
 [
  82, 'Группы выпускников'],
 [
  89, 'Дачи'],
 [
  27, 'Джаз'],
 [
  90, 'Дискуссионные клубы'],
 [
  12, 'Домашние животные'],
 [
  1, 'Друзья'],
 [
  64, 'Железо'],
 [
  10, 'Здоровье'],
 [
  52, 'Зимние виды спорта'],
 [
  13, 'Знаки зодиака'],
 [
  39, 'Знакомства'],
 [
  61, 'Игры'],
 [
  28, 'Инди'],
 [
  6, 'История'],
 [
  18, 'Кино'],
 [
  29, 'Классика'],
 [
  30, 'Латина'],
 [
  53, 'Легкая атлетика'],
 [
  17, 'Литература'],
 [
  88, 'Места отдыха'],
 [
  31, 'Металл'],
 [
  65, 'Мобильные технологии'],
 [
  77, 'Молодежные движения'],
 [
  94, 'Мотоспорт'],
 [
  75, 'Музыкальные движения'],
 [
  63, 'Мультимедиа'],
 [
  95, 'Настольные игры'],
 [
  9, 'Наука'],
 [
  3, 'Новости'],
 [
  24, 'Обмен музыкой'],
 [
  83, 'Общежития'],
 [
  85, 'Общества и клубы'],
 [
  80, 'Общества и клубы'],
 [
  5, 'Общество'],
 [
  14, 'Однофамильцы и тезки'],
 [
  40, 'Отношения полов'],
 [
  4, 'Политика'],
 [
  67, 'Программирование'],
 [
  96, 'Работа'],
 [
  23, 'Радио и Интернет-радио'],
 [
  34, 'Регги'],
 [
  8, 'Религия'],
 [
  35, 'Рок'],
 [
  51, 'Ролики'],
 [
  66, 'Сайты'],
 [
  62, 'Софт'],
 [
  56, 'Спортивные игры'],
 [
  78, 'Спортивные организации'],
 [
  87, 'Страны'],
 [
  84, 'Студенческие советы'],
 [
  36, 'Танцевальная'],
 [
  50, 'Танцы'],
 [
  16, 'Творчество'],
 [
  19, 'Театр'],
 [
  25, 'Тексты и аккорды'],
 [
  22, 'Телевидение'],
 [
  46, 'Теннис'],
 [
  41, 'Технические вопросы'],
 [
  11, 'Туризм и путешествия'],
 [
  60, 'Университетский спорт'],
 [
  57, 'Упражнения и фитнес'],
 [
  91, 'Фан-клубы'],
 [
  7, 'Философия'],
 [
  37, 'Фолк'],
 [
  20, 'Фотография и живопись'],
 [
  45, 'Футбол'],
 [
  48, 'Хоккей'],
 [
  59, 'Экстремальный спорт'],
 [
  38, 'Электронная'],
 [
  21, 'Юмор'],
 [
  2, 'Языки']]
TARGETING_RELIGIONS_CHOICES = [[102, 'Православие'],
 [
  103, 'Православный'],
 [
  104, 'Православная'],
 [
  105, 'Orthodox'],
 [
  101, 'Католицизм'],
 [
  99, 'Католик'],
 [
  98, 'Католичка'],
 [
  97, 'Catholic'],
 [
  96, 'catholicism'],
 [
  107, 'Протестантизм'],
 [
  108, 'Протестант'],
 [
  167, 'Иудаизм'],
 [
  168, 'Иудей'],
 [
  169, 'Иудейка'],
 [
  170, 'Jewish'],
 [
  171, 'Judaism'],
 [
  122, 'Islam'],
 [
  123, 'Muslim'],
 [
  124, 'Ислам'],
 [
  125, 'Мусульманин'],
 [
  126, 'Мусульманка'],
 [
  129, 'Буддизм'],
 [
  130, 'Буддист'],
 [
  131, 'Buddhism'],
 [
  139, 'Конфуцианство'],
 [
  138, 'Даосизм'],
 [
  200, 'Светский гуманизм'],
 [
  201, 'Христианство'],
 [
  202, 'Христианин'],
 [
  203, 'Христианство'],
 [
  204, 'Christian'],
 [
  205, 'Атеизм'],
 [
  206, 'Атеист'],
 [
  207, 'Атеистка']]
TARGETING_SEX_CHOICES = ((0, 'любой'), (1, 'женский'), (2, 'мужской'))
TARGETING_STATUS_CHOICES = ((1, 'Не женат/Не замужем'),
 (2, 'Есть подруга/Есть друг'),
 (3, 'Полмолвлен(а)'),
 (4, 'Женат/Замужем'),
 (5, 'Все сложно'),
 (6, 'В активном поиске'))

class VkontakteAdsMixin:
    methods_namespace = 'ads'
    methods_access_tag = 'ads'


class VkontakteAdsModel(VkontakteAdsMixin, VkontakteModel):

    class Meta:
        abstract = True


class VkontakteAdsIDModel(VkontakteAdsMixin, VkontaktePKModel):

    class Meta:
        abstract = True

    def fetch_ads(self, model=None, ids=None):
        """
        Get all ads|ad_targetings|ad_layouts of campaign
        """
        if not ids:
            ids = 'null'
        else:
            if not isinstance(ids, list):
                raise ValueError('Argument ids must be list or tuple')
            kwargs = {'account_id': self.account.remote_id, 
               'campaign_ids': [
                              int(self.remote_id)], 
               'ad_ids': ids}
            if self.client:
                kwargs.update({'client_id': self.client.remote_id})
            instances = model.remote.get(**kwargs)
            instances_saved = []
            for instance in instances:
                instance.campaign = self
                instance.fetched = datetime.now()
                instance._commit_remote = False
                instances_saved += [model.remote.get_or_create_from_instance(instance)]

        return instances_saved

    def fetch_campaigns(self, account, client=None, ids=None):
        """
        Get all campaigns of account
        """
        if not ids:
            ids = 'null'
        else:
            if not isinstance(ids, list):
                raise ValueError('Argument ids must be list or tuple')
            kwargs = {'account_id': account.remote_id, 
               'campaign_ids': ids}
            if client:
                kwargs.update({'client_id': client.remote_id})
            try:
                instances = Campaign.remote.get(**kwargs)
            except VKError as e:
                if e.code == 100:
                    return []
                raise e

            instances_saved = []
            for instance in instances:
                instance.account = account
                instance.fetched = datetime.now()
                instance._commit_remote = False
                if client:
                    instance.client = client
                instances_saved += [Campaign.remote.get_or_create_from_instance(instance)]

        return instances_saved

    def fetch_statistics(self, **kwargs):
        """
        Get statistics of content object
        """
        return Statistic.remote.fetch(objects=[self], **kwargs)


@python_2_unicode_compatible
class VkontakteAdsIDContentModel(VkontakteCRUDModel, VkontakteAdsIDModel):
    """
    Model with remote_id and CRUD remote methods
    """

    class Meta:
        abstract = True

    def __str__(self):
        return ('(архив) ' if self.archived else '') + self.name

    def parse_remote_id_from_response(self, response):
        """
        Handle response errors
        # http://vk.com/developers.php?oid=-1&p=ads.createAds
        # http://vk.com/developers.php?oid=-1&p=ads.updateAds
        If id in response == 0 -> raise error, otherwise log error and return it for saving to local DB
        """
        error_message = "Error while saving %s. Code %s, description: '%s'" % (
         self._meta.object_name, response[0].get('error_desc'), response[0].get('error_desc'))
        if response[0]['id']:
            if 'error_code' in response[0]:
                log.error(error_message)
            return response[0]['id']
        log.error(error_message)
        raise VkontakteContentError(error_message)

    def prepare_create_params(self, **kwargs):
        return {'account_id': self.account.remote_id, 
           'data': [
                  self.fields_for_create()]}

    def prepare_update_params(self, **kwargs):
        return self.fields_for_update()

    def prepare_update_params_distinct(self, **kwargs):
        return {'account_id': self.account.remote_id, 
           'data': [
                  super(VkontakteAdsIDContentModel, self).prepare_update_params_distinct()]}

    def prepare_delete_params(self, **kwargs):
        return {'account_id': self.account.remote_id, 
           'ids': [
                 self.remote_id]}

    def save(self, *args, **kwargs):
        """
        Update remote version of object before saving if data is different
        """
        if not self.account:
            raise ValueError('You must specify ad campaign field')
        super(VkontakteAdsIDContentModel, self).save(*args, **kwargs)

    @property
    def refresh_kwargs(self):
        return {'include_deleted': 1}

    def check_remote_existance(self, *args, **kwargs):
        if self.remote_id < 10000:
            self.archive(commit_remote=False)
            return False
        super(VkontakteAdsIDContentModel, self).check_remote_existance(*args, **kwargs)


@python_2_unicode_compatible
class Account(VkontakteAdsIDModel):
    remote_pk_field = 'account_id'
    name = models.CharField('Название', blank=True, max_length=100)
    account_status = models.BooleanField(help_text='Cтатус рекламного кабинета. активен / неактивен.')
    access_role = models.CharField(choices=ACCOUNT_ACCESS_ROLE_CHOICES, max_length=10, help_text='права пользователя в рекламном кабинете.')
    remote = VkontakteManager(remote_pk=('remote_id', ), methods={'get': 'getAccounts'})
    statistics = generic.GenericRelation('Statistic', verbose_name='Статистика')

    class Meta:
        verbose_name = 'Рекламный кабинет Вконтакте'
        verbose_name_plural = 'Рекламные кабинеты Вконтакте'

    def __str__(self):
        return self.name or 'Account #%s' % self.remote_id

    def _substitute(self, old_instance):
        super(Account, self)._substitute(old_instance)
        self.name = old_instance.name

    def fetch_clients(self):
        """
        Get all clients of account
        """
        try:
            instances = Client.remote.get(account_id=self.remote_id)
        except VKError as e:
            if e.code == 100:
                return []
            raise e

        instances_saved = []
        for instance in instances:
            instance.account = self
            instance.fetched = datetime.now()
            instance._commit_remote = False
            instances_saved += [Client.remote.get_or_create_from_instance(instance)]

        return instances_saved

    def fetch_campaigns(self, ids=None):
        """
        Get all campaigns of account
        """
        return super(Account, self).fetch_campaigns(account=self, ids=ids)

    def fetch_budget(self):
        """
        Get budget of account
        """
        instance = Budget.remote.get(account_id=self.remote_id)
        instance.account = self
        instance = Budget.remote.get_or_create_from_instance(instance)
        return instance


@python_2_unicode_compatible
class Client(VkontakteAdsIDContentModel):
    fields_required_for_update = [
     'client_id']
    account = models.ForeignKey(Account, verbose_name='Аккаунт', related_name='clients', help_text='Номер рекламного кабинета, в котором должны создаваться кампании.')
    name = models.CharField('Название', max_length=60)
    day_limit = models.IntegerField('Дневной лимит', null=True, help_text='Целое число рублей.')
    all_limit = models.IntegerField('Общий лимит', null=True, help_text='Целое число рублей.')
    statistics = generic.GenericRelation('Statistic', verbose_name='Статистика')
    objects = VkontakteCRUDManager()
    remote = VkontakteManager(remote_pk=('remote_id', ), methods={'get': 'getClients', 
       'create': 'createClients', 
       'update': 'updateClients', 
       'delete': 'deleteClients'})

    class Meta:
        verbose_name = 'Рекламный клиент Вконтакте'
        verbose_name_plural = 'Рекламные клиенты Вконтакте'

    def __str__(self):
        return self.name

    def fields_for_update(self):
        fields = self.fields_for_create()
        fields.update(client_id=self.remote_id)
        return fields

    def fields_for_create(self):
        fields = dict(name=self.name)
        if self.day_limit:
            fields.update(day_limit=self.day_limit)
        if self.all_limit:
            fields.update(all_limit=self.all_limit)
        return fields

    def fetch_campaigns(self, ids=None):
        """
        Get all campaigns of account
        """
        return super(Client, self).fetch_campaigns(account=self.account, client=self, ids=ids)


class Campaign(VkontakteAdsIDContentModel):
    account = models.ForeignKey(Account, verbose_name='Аккаунт', related_name='campaigns', help_text='Номер рекламного кабинета, в котором должны создаваться кампании.')
    client = ChainedForeignKey(Client, verbose_name='Клиент', chained_field='account', chained_model_field='account', show_all=False, auto_choose=True, related_name='campaigns', null=True, blank=True, help_text='Только для рекламных агентств. id клиента, в рекламном кабинете которого будет создаваться кампания.')
    name = fields.CharRangeLengthField('Название', min_length=3, max_length=60, help_text='Название рекламной кампании - строка длиной от 3 до 60 символов.')
    day_limit = models.IntegerField('Дневной лимит', null=True, help_text='Целое число рублей.')
    all_limit = models.IntegerField('Общий лимит', null=True, help_text='Целое число рублей.')
    start_time = models.DateTimeField('Время запуска', null=True, blank=True, help_text='Время запуска кампании в unixtime формате.')
    stop_time = models.DateTimeField('Время остановки', null=True, blank=True, help_text='Время остановки кампании в unixtime формате.')
    status = models.BooleanField('Статус', help_text='Статус рекламной кампании: остановлена / запущена.')
    statistics = generic.GenericRelation('Statistic', verbose_name='Статистика')
    objects = VkontakteCRUDManager()
    remote = VkontakteManager(remote_pk=('remote_id', ), methods={'get': 'getCampaigns', 
       'create': 'createCampaigns', 
       'update': 'updateCampaigns', 
       'delete': 'deleteCampaigns'})

    class Meta:
        verbose_name = 'Рекламная кампания Вконтакте'
        verbose_name_plural = 'Рекламные кампании Вконтакте'

    def _substitute(self, old_instance):
        super(Campaign, self)._substitute(old_instance)
        self.account = old_instance.account
        self.client = old_instance.client

    @property
    def refresh_kwargs(self):
        kwargs = super(Campaign, self).retresh_kwargs
        kwargs['account_id'] = self.account.remote_id
        kwargs['campaign_ids'] = [self.remote_id]
        if self.client:
            kwargs['client_id'] = self.client.remote_id
        return kwargs

    def check_remote_existance(self, *args, **kwargs):
        existance = super(Campaign, self).check_remote_existance(**kwargs)
        if not existance:
            for ad in self.ads.all():
                ad.archived = True
                ad.save(commit_remote=False)

        return existance

    fields_required_for_update = [
     'campaign_id']

    def fields_for_update(self):
        """
        TODO: add dropping start_time, stop_time http://vk.com/developers.php?oid=-1&p=ads.updateCampaigns
        """
        fields = self.fields_for_create()
        if 'client_id' in fields:
            fields.pop('client_id')
        fields.update(campaign_id=self.remote_id)
        return fields

    def fields_for_create(self):
        fields = dict(name=self.name, status=int(self.status))
        if self.client:
            fields.update(client_id=self.client.remote_id)
        if self.day_limit:
            fields.update(day_limit=self.day_limit)
        if self.all_limit:
            fields.update(all_limit=self.all_limit)
        if self.start_time:
            fields.update(start_time=int(time.mktime(self.start_time.timetuple())))
        if self.stop_time:
            fields.update(stop_time=int(time.mktime(self.stop_time.timetuple())))
        return fields

    def parse(self, response):
        if response['status'] == 2:
            response['status'] = 0
            self.archived = True
        super(Campaign, self).parse(response)

    def fetch_ads(self, ids=None):
        """
        Get all ads of campaign
        """
        return super(Campaign, self).fetch_ads(model=Ad, ids=ids)

    def fetch_ads_targeting(self, ids=None):
        """
        Get all ad targetings of campaign
        """
        return super(Campaign, self).fetch_ads(model=Targeting, ids=ids)

    def fetch_ads_layout(self, ids=None):
        """
        Get all ad layouts of campaign
        """
        return super(Campaign, self).fetch_ads(model=Layout, ids=ids)


class AdAbstract(VkontakteAdsIDContentModel):
    """
    Abstract model of vkontakte ads with all fields for some special needs
    """
    account = models.ForeignKey(Account, verbose_name='Аккаунт', related_name='ads', help_text='Номер рекламного кабинета, в котором создается объявление.')
    campaign = ChainedForeignKey(Campaign, verbose_name='Кампания', chained_field='account', chained_model_field='account', show_all=False, auto_choose=True, related_name='ads', help_text='Кампания, в которой будет создаваться объявление.')
    name = fields.CharRangeLengthField('Название', min_length=3, max_length=100, help_text='Название объявления (для использования в рекламном кабинете) - строка длиной от 3 до 60 символов.')
    all_limit = models.PositiveIntegerField('Общий лимит', null=True, help_text='Целое число рублей.')
    cost_type = models.PositiveSmallIntegerField('Тип оплаты', choices=(
     (0, 'оплата за переходы'), (1, 'оплата за показы')), help_text='Флаг, описывающий тип оплаты')
    cpc = fields.IntegerRangeField('Цена за переход', min_value=50, null=True, blank=True, help_text='Если оплата за переходы, цена за переход в копейках, минимум 50 коп.')
    cpm = models.PositiveIntegerField('Цена за показы', null=True, blank=True, help_text='Если оплата за показы, цена за 1000 показов в копейках')
    status = models.BooleanField('Статус', help_text='Статус рекламного объявления: остановлено / запущено.')
    disclaimer = models.BooleanField('Противопоказания', help_text='Укажите, если имеются противопоказания (только для рекламы медицинских товаров и услуг).')
    approved = models.BooleanField('Одобрено')
    statistics = generic.GenericRelation('Statistic', verbose_name='Статистика')
    objects = VkontakteCRUDManager()
    remote = VkontakteManager(remote_pk=('remote_id', ), methods={'get': 'getAds', 
       'create': 'createAds', 
       'update': 'updateAds', 
       'delete': 'deleteAds'})

    class Meta:
        abstract = True


class Ad(AdAbstract):
    """
    Model of vkontakte ads
    """

    class Meta:
        verbose_name = 'Рекламное объявление Вконтакте'
        verbose_name_plural = 'Рекламные объявления Вконтакте'

    def __init__(self, *args, **kwargs):
        targeting_defaults = dict([ (k.replace('targeting__', ''), kwargs.pop(k)) for k in kwargs.keys() if k[:11] == 'targeting__'
                                  ])
        layout_defaults = dict([ (k.replace('layout__', ''), kwargs.pop(k)) for k in kwargs.keys() if k[:8] == 'layout__'
                               ])
        image = kwargs.pop('image', None)
        super(Ad, self).__init__(*args, **kwargs)
        self._targeting = Targeting(ad=self, campaign_id=self.campaign_id, **targeting_defaults)
        self._layout = Layout(ad=self, campaign_id=self.campaign_id, **layout_defaults)
        if image:
            self._image = image
            self._image.ad = self
        else:
            self._image = Image(ad=self)
        return

    def _substitute(self, old_instance):
        super(Ad, self)._substitute(old_instance)
        self.account = old_instance.account
        self.campaign = old_instance.campaign
        self.layout = old_instance.layout
        self.targeting = old_instance.targeting
        self.image = old_instance.image

    @property
    def refresh_kwargs(self):
        kwargs = super(Ad, self).refresh_kwargs
        kwargs['ad_ids'] = [self.remote_id]
        kwargs['account_id'] = self.account.remote_id
        kwargs['campaign_ids'] = [self.campaign.remote_id]
        if self.campaign.client:
            kwargs['client_id'] = self.campaign.client.remote_id
        return kwargs

    fields_required_for_update = [
     'ad_id']

    def fields_for_update(self):
        fields = self.fields_for_create()
        for field in ['campaign_id', 'cost_type']:
            if field in fields:
                fields.pop(field)

        fields.update(ad_id=int(self.remote_id))
        return fields

    def fields_for_create(self):
        fields = dict(campaign_id=int(self.campaign.remote_id), cost_type=self.cost_type, title=self.layout.title, link_url=self.layout.link_url, status=int(self.status))
        if self.image:
            if not self.image.hash:
                self.image.upload()
            fields.update(hash=self.image.hash, photo_hash=self.image.photo_hash, photo=self.image.photo, server=self.image.server)
        if self.cost_type == 0:
            fields.update(cpc=float(self.cpc) / 100 if self.cpc else 0)
        else:
            if self.cost_type == 1:
                fields.update(cpm=float(self.cpm) / 100 if self.cpm else 0)
            if self.name:
                fields.update(name=self.name)
            if self.all_limit:
                fields.update(all_limit=self.all_limit)
            if self.layout.description:
                fields.update(description=self.layout.description)
            if self.layout.link_domain:
                fields.update(link_domain=self.layout.link_domain)
            fields.update(sex=self.targeting.sex, age_from=self.targeting.age_from, age_to=self.targeting.age_to, country=self.targeting.country, school_from=self.targeting.school_from, school_to=self.targeting.school_to, uni_from=self.targeting.uni_from, uni_to=self.targeting.uni_to, travellers=int(self.targeting.travellers == 'on'))
            if self.targeting.tags:
                fields.update(tags=self.targeting.tags)
            if self.targeting.birthday:
                fields.update(birthday=self.targeting.birthday)
            for field in ['cities', 'cities_not', 'statuses', 'group_types', 'groups', 'districts', 'stations', 'streets', 'schools', 'positions', 'religions', 'interests', 'browsers']:
                if getattr(self.targeting, field):
                    fields[field] = getattr(self.targeting, field)

        return fields

    def parse(self, response):
        if response['status'] == 2:
            response['status'] = 0
            self.archived = True
        super(Ad, self).parse(response)

    def save(self, *args, **kwargs):
        try:
            self.account = self.campaign.account
        except ObjectDoesNotExist:
            pass

        if self.cost_type is None:
            if self.cpc is not None:
                self.cost_type = 0
            elif self.cpm is not None:
                self.cost_type = 1
            else:
                raise ValueError('Properties cost_type or cpc and cpm must be specified before saving')
        super(Ad, self).save(*args, **kwargs)
        try:
            self.targeting
        except:
            self._targeting.save()

        try:
            self.layout
        except:
            self._layout.save()

        try:
            self.image
        except:
            self._image.save()

        return


class Targeting(VkontakteAdsMixin, VkontakteModel):
    remote_pk_local_field = 'ad'
    ad = models.OneToOneField(Ad, verbose_name='Объявление', primary_key=True, related_name='targeting')
    campaign = models.ForeignKey(Campaign, verbose_name='Кампания')
    sex = models.PositiveSmallIntegerField('Пол', choices=TARGETING_SEX_CHOICES, default=0)
    age_from = models.PositiveSmallIntegerField('Возраст с', default=0)
    age_to = models.PositiveSmallIntegerField('Возраст до', default=0)
    birthday = models.CommaSeparatedIntegerField('День рождения', max_length=100, choices=[
     ('', 'Неважно'), (1, 'Сегодня'), (2, 'Завтра'), (3, 'Сегодня или завтра')], blank=True)
    country = models.PositiveIntegerField('Страна', default=0)
    cities = models.CommaSeparatedIntegerField('Города', max_length=500, blank=True)
    cities_not = models.CommaSeparatedIntegerField('Города исключить', max_length=500, blank=True)
    statuses = models.CommaSeparatedIntegerField('Семейное положение', max_length=500, blank=True)
    group_types = models.CommaSeparatedIntegerField('Категории групп', max_length=500, blank=True)
    groups = models.CommaSeparatedIntegerField('Группы', max_length=500, blank=True)
    religions = models.CommaSeparatedIntegerField('Религиозные взгляды', max_length=500, blank=True)
    interests = fields.CommaSeparatedCharField('Интересы', max_length=500, blank=True, help_text='Последовательность слов, разделенных запятой.')
    travellers = models.BooleanField('Путешественники')
    districts = models.CommaSeparatedIntegerField('Районы', max_length=500, blank=True)
    stations = models.CommaSeparatedIntegerField('Станции метро', max_length=500, blank=True)
    streets = models.CommaSeparatedIntegerField('Улицы', max_length=500, blank=True)
    schools = models.CommaSeparatedIntegerField('Учебные заведения', max_length=500, blank=True)
    positions = models.CommaSeparatedIntegerField('Должности', max_length=500, blank=True)
    school_from = models.PositiveSmallIntegerField('Окончание школы после', default=0)
    school_to = models.PositiveSmallIntegerField('Окончание школы дое', default=0)
    uni_from = models.PositiveSmallIntegerField('Окончание ВУЗа после', default=0)
    uni_to = models.PositiveSmallIntegerField('Окончание ВУЗа до', default=0)
    browsers = models.CommaSeparatedIntegerField('Браузеры и устройства', max_length=500, blank=True)
    tags = fields.CommaSeparatedCharField('Ключевые слова', max_length=200, blank=True, help_text='Набор строк, разделенных запятой.')
    approved = models.BooleanField('Одобрено')
    count = models.PositiveIntegerField(null=True, blank=True, help_text='')
    operators = models.CommaSeparatedIntegerField('Операторы', max_length=500, blank=True, help_text='')
    remote = VkontakteManager(remote_pk=('ad_id', ), methods={'get': 'getAdsTargeting'})

    class Meta:
        verbose_name = 'Таргетинг объявления Вконтакте'
        verbose_name_plural = 'Таргетинг объявления Вконтакте'


class Layout(VkontakteAdsMixin, VkontakteModel):
    remote_pk_local_field = 'ad'
    ad = models.OneToOneField(Ad, verbose_name='Объявление', primary_key=True, related_name='layout')
    campaign = models.ForeignKey(Campaign, verbose_name='Кампания', help_text='Кампания объявления.')
    title = fields.CharRangeLengthField('Заголовок', min_length=3, max_length=50, help_text='Заголовок объявления - строка длиной от 3 до 25 символов')
    description = fields.CharRangeLengthField('Описание', min_length=3, max_length=100, help_text='Описание объявления - строка длиной от 3 до 60 символов - обязательно при выборе типа "оплата за переходы"')
    link_url = models.URLField('Ссылка', max_length=500, help_text='Ссылка на рекламируемый объект в формате http://yoursite.com или ВКонтакте API. Если в ссылке содержатся строки "{ad_id}" или "{campaign_id}", то они заменяются соответственно на ID объявления и ID кампании в момент перехода пользователя по такой ссылке.')
    link_domain = models.CharField('Домен', blank=True, max_length=50, help_text='Домен рекламируемого объекта в формате yoursite.com')
    preview_link = models.CharField('Превью', blank=True, max_length=200)
    preview = models.TextField()
    remote = VkontakteManager(remote_pk=('ad_id', ), methods={'get': 'getAdsLayout'})

    class Meta:
        verbose_name = 'Контент объявления Вконтакте'
        verbose_name_plural = 'Контент объявления Вконтакте'

    def save(self, *args, **kwargs):
        self.set_preview()
        super(Layout, self).save(*args, **kwargs)

    def set_preview(self):
        if self.preview_link:
            response = requests.get(self.preview_link)
            self.preview = response.content.decode('windows-1251', 'ignore')


class Image(VkontakteAdsMixin, VkontakteModel):
    """
    Model of vkontakte image
    """

    def _get_upload_to(self, filename=None):
        return 'images/%f.jpg' % time.time()

    ad = models.OneToOneField(Ad, verbose_name='Объявление', primary_key=True, related_name='image')
    hash = models.CharField(max_length=50, blank=True, help_text='Значение, полученное в результате загрузки фотографии на сервер')
    photo_hash = models.CharField(max_length=50, blank=True, help_text='Значение, полученное в результате загрузки фотографии на сервер')
    photo = models.CharField(max_length=200, blank=True, help_text='Значение, полученное в результате загрузки фотографии на сервер')
    server = models.PositiveIntegerField(blank=True, null=True, help_text='Значение, полученное в результате загрузки фотографии на сервер')
    size = models.CharField(max_length=1, blank=True)
    aid = models.PositiveIntegerField(null=True, blank=True)
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    file = models.ImageField('Картинка', upload_to=_get_upload_to, blank=True)
    post_url = models.CharField(max_length=200, blank=True, help_text='Адрес загрузки картинки на сервер')
    remote = VkontakteManager(methods={'get_post_url': 'getUploadURL'})

    class Meta:
        verbose_name = 'Картинка объявления Вконтакте'
        verbose_name_plural = 'Картинка объявления Вконтакте'

    def get_post_url(self):
        self.post_url = Image.remote.api_call(method='get_post_url', cost_type=self.ad.cost_type)
        return self.post_url

    def upload(self):
        if self.file:
            if not self.file._committed:
                self.file.field.pre_save(self, True)
            url = self.post_url or self.get_post_url()
            files = {'file': (
                      self.file.name.split('/')[(-1)], open(os.path.join(settings.MEDIA_ROOT, self.file.name), 'rb'))}
            response = requests.post(url, files=files)
            response = json.loads(response.content)
            if 'errcode' in response:
                raise VkontakteContentError('Error with code %d while uploading image %s' % (
                 response['errcode'], self.file))
            self.parse(response)


class VkontakteTargetingStatsManager(VkontakteManager):

    def api_call(self, method='get', **kwargs):
        ad = kwargs.pop('ad')
        kwargs['link_url'] = ad.layout.link_url
        kwargs['link_domain'] = ad.layout.link_domain
        kwargs['account_id'] = ad.account.remote_id
        if ad.remote_id:
            kwargs['ad_id'] = ad.remote_id
        else:
            kwargs['criteria'] = dict([ (k, v) for k, v in ad.targeting.__dict__.items() if k[0] != '_' ])
            for field_name in ['campaign_id', 'approved']:
                del kwargs['criteria'][field_name]

        return super(VkontakteTargetingStatsManager, self).api_call('get', **kwargs)

    def parse_response_list(self, response_list, extra_fields=None):
        return super(VkontakteTargetingStatsManager, self).parse_response_list([response_list], extra_fields)

    def fetch(self):
        raise Exception('Impossible to fetch targeting stats, use get() method')


class TargetingStats(VkontakteAdsModel):
    audience_count = models.PositiveIntegerField(help_text='Размер целевой аудитории')
    recommended_cpc = models.FloatField(help_text='Рекомендованная цена для объявлений за клики, указана в рублях с копейкам в дробной части')
    recommended_cpm = models.FloatField(help_text='Рекомендованная цена для объявлений за показы, указана в рублях с копейкам в дробной части')
    remote = VkontakteTargetingStatsManager(methods={'get': 'getTargetingStats'})

    class Meta:
        verbose_name = 'Размер целевой аудитории Вконтакте'
        verbose_name_plural = 'Размеры целевой аудитории Вконтакте'

    def parse(self, response):
        """
        Additionally convert values from rubles to kopeyki :)
        """
        super(TargetingStats, self).parse(response)
        self.recommended_cpc *= 100
        self.recommended_cpm *= 100
        self.fetched = datetime.now()


class VkontakteStatisticManager(VkontakteManager):

    def _get_types(self):
        return (
         (
          ContentType.objects.get_for_model(Ad), 'ad'),
         (
          ContentType.objects.get_for_model(Campaign), 'campaign'),
         (
          ContentType.objects.get_for_model(Client), 'client'),
         (
          ContentType.objects.get_for_model(Account), 'office'))

    def parse_response_list(self, response_list, extra_fields=None):
        """
        Parse retrieved objects from remote server
        """
        types = dict([ (v, k) for k, v in self._get_types() ])
        instances = []
        for resource in response_list:
            if isinstance(resource, list) and len(resource):
                resource = resource[0]
            try:
                resource = dict(resource)
            except ValueError as e:
                log.error('Impossible to handle response of api call %s with parameters: %s' % (
                 self.methods['get'], kwargs))
                raise e

            for stat in resource['stats']:
                instance = self.model()
                try:
                    instance.content_type = types[resource['type']]
                    model = instance.content_type.model_class()
                except KeyError:
                    raise ValueError('Could not find type of object for statistic %s' % resource['type'])

                try:
                    instance.object_id = model.objects.get(remote_id=resource['id']).pk
                except model.DoesNotExist:
                    raise ValueError('Could not find object %s for statistic with id %s' % (model, resource['id']))

                if extra_fields:
                    instance.__dict__.update(extra_fields)
                instance.parse(stat)
                instances += [instance]

        return instances

    def fetch(self, objects, period='overall', date_from=0, date_to=0):
        """
        Retrieve and save object to local DB
        """
        if isinstance(objects, QuerySet):
            ids = [ str(id) for id in objects.values_list('remote_id', flat=True) ]
        else:
            if isinstance(objects, (list, tuple)):
                ids = [ str(campaign.remote_id) for campaign in objects ]
            else:
                raise ValueError('Argument objects must be list or QuerySet')
            if not ids:
                return []
            if period not in ('day', 'month', 'overall'):
                raise ValueError("Period argument must be 'day','month' or 'overall'.")
            try:
                types = dict(self._get_types())
                ids_type = types[ContentType.objects.get_for_model(objects[0])]
                if ids_type == 'ad':
                    account_id = objects[0].campaign.account.remote_id
                elif ids_type in ('campaign', 'client'):
                    account_id = objects[0].account.remote_id
                elif ids_type == 'office' and len(objects) == 1:
                    account_id = objects[0].remote_id
                else:
                    raise ValueError('Could not define account_id for multiple objects %s' % objects)
            except KeyError:
                raise ValueError('Could not recognize ids_type for object %s' % objects[0])

        kwargs = {'account_id': account_id, 'ids_type': ids_type, 
           'ids': (',').join(ids), 
           'period': period, 
           'date_from': date_from, 
           'date_to': date_to}
        instances = super(VkontakteStatisticManager, self).fetch(**kwargs)
        return instances

    def fetch_for_all_campaigns(self, **kwargs):
        stats = []
        for account in Account.objects.all():
            stats += self.fetch(account.campaigns.all(), **kwargs)

        return stats

    def fetch_for_all_ads(self, **kwargs):
        stats = []
        for account in Account.objects.all():
            stats += self.fetch(Ad.objects.filter(campaign__account=account), **kwargs)

        return stats

    def fetch_for_all_clients(self, **kwargs):
        stats = []
        for account in Account.objects.all():
            stats += self.fetch(account.clients.all(), **kwargs)

        return stats

    def fetch_for_all_accounts(self, **kwargs):
        stats = []
        for account in Account.objects.all():
            stats += self.fetch([account], **kwargs)

        return stats


class StatisticAbstract(VkontakteAdsModel):
    """
    Abstract model of vkontakte statistic with stat fields for some special needs
    """
    clicks = models.PositiveIntegerField('Клики', default=0)
    impressions = models.PositiveIntegerField('Просмотры', default=0)
    reach = models.PositiveIntegerField('Охват', default=0)
    spent = models.FloatField('Потраченные средства', default=0)
    video_views = models.PositiveIntegerField('Просмотры видеозаписи (для видеорекламы)', null=True)
    join_rate = models.FloatField(null=True, help_text='Вступления в группу, событие, подписки на публичную страницу или установки приложения (только если в объявлении указана прямая ссылка на соответствующую страницу ВКонтакте)')
    ctr = models.FloatField(null=True)
    cpc = models.FloatField(null=True)
    cpm = models.FloatField(null=True)

    class Meta:
        abstract = True

    def set_auto_values(self):
        if not self.ctr:
            self.ctr = float('%.3f' % (100 * float(self.clicks) / self.impressions)) if self.impressions else None
        if not self.cpc:
            self.cpc = float('%.2f' % (self.spent / self.clicks)) if self.clicks else None
        if not self.cpm:
            self.cpm = float('%.2f' % (100 * self.spent / self.impressions)) if self.impressions else None
        return

    def save(self, *args, **kwargs):
        self.set_auto_values()
        return super(StatisticAbstract, self).save(*args, **kwargs)


class Statistic(StatisticAbstract):
    content_type = models.ForeignKey(ContentType, limit_choices_to=models.Q(app_label='vkontakte_ads', model='account') | models.Q(app_label='vkontakte_ads', model='campaign') | models.Q(app_label='vkontakte_ads', model='ad') | models.Q(app_label='vkontakte_ads', model='client'))
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    day = models.DateField('День', null=True)
    month = models.CharField('Месяц', max_length=7)
    overall = models.BooleanField('За все время?')
    objects = models.Manager()
    remote = VkontakteStatisticManager(remote_pk=('content_type', 'object_id', 'day',
                                                  'month', 'overall'), methods={'get': 'getStatistics'})

    class Meta:
        verbose_name = 'Рекламная статистика Вконтакте'
        verbose_name_plural = 'Рекламная статистика Вконтакте'
        unique_together = ('content_type', 'object_id', 'day', 'month', 'overall')


class Budget(VkontakteAdsModel):
    account = models.ForeignKey(Account, primary_key=True, help_text='Номер рекламного кабинета, бюджет которого запрашивается.')
    budget = models.DecimalField(max_digits=10, decimal_places=2, help_text='Оставшийся бюджет в указанном рекламном кабинете.')
    remote = VkontakteManager(remote_pk=('account', ), methods={'get': 'getBudget'})

    class Meta:
        verbose_name = 'Бюджет личного кабинета Вконтакте'
        verbose_name_plural = 'Бюджеты личных кабинетов Вконтакте'