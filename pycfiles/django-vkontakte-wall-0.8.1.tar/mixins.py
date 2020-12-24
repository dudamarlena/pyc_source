# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-wall/vkontakte_wall/mixins.py
# Compiled at: 2015-06-02 11:53:26
from datetime import datetime
import logging, re
from django.db import models
from django.utils import timezone
from m2m_history.fields import ManyToManyHistoryField
from vkontakte_api.api import api_call
from vkontakte_api.decorators import fetch_all, atomic
from vkontakte_api.mixins import LikableModelMixin as LikableModelMixinBase
from vkontakte_api.models import MASTER_DATABASE
from vkontakte_users.models import User
from .parser import VkontakteWallParser
log = logging.getLogger('vkontakte_wall')

class LikableModelMixin(LikableModelMixinBase):

    class Meta:
        abstract = True

    @atomic
    def fetch_likes(self, source='api', *args, **kwargs):
        if source == 'api':
            return super(LikableModelMixin, self).fetch_likes(*args, **kwargs)
        else:
            return self.fetch_likes_parser(*args, **kwargs)

    @atomic
    def fetch_likes_parser(self, offset=0):
        """
        Update and save fields:
            * likes - count of likes
        Update relations:
            * likes_users - users, who likes this post
        """
        post_data = {'act': 'show', 
           'al': 1, 
           'w': 'likes/wall%s' % self.remote_id}
        if offset == 0:
            number_on_page = 120
            post_data['loc'] = ('wall%s' % self.remote_id,)
        else:
            number_on_page = 60
            post_data['offset'] = offset
        log.debug('Fetching likes of post "%s" of owner "%s", offset %d' % (
         self.remote_id, self.owner, offset))
        parser = VkontakteWallParser().request('/wkview.php', data=post_data)
        if offset == 0:
            try:
                self.likes_count = int(parser.content_bs.find('a', {'id': 'wk_likes_tablikes'}).find('nobr').text.split()[0])
                self.save()
            except ValueError:
                return
            except:
                log.warning('Strange markup of first page likes response: "%s"' % parser.content)

            self.likes_users.clear()
        items = parser.add_users(users=('div', {'class': re.compile('^wk_likes_liker_row')}), user_link=(
         'a', {'class': 'wk_likes_liker_lnk'}), user_photo=(
         'img', {'class': 'wk_likes_liker_img'}), user_add=lambda user: self.likes_users.add(user))
        if len(items) == number_on_page:
            self.fetch_likes_parser(offset=offset + number_on_page)
        else:
            return self.likes_users.all()


class RepostableModelMixin(models.Model):
    reposts_users = ManyToManyHistoryField(User, related_name='reposts_%(class)ss')
    reposts_count = models.PositiveIntegerField('Кол-во репостов', null=True, db_index=True)

    class Meta:
        abstract = True

    def parse(self, response):
        if 'reposts' in response:
            value = response.pop('reposts')
            if isinstance(value, int):
                response['reposts_count'] = value
            elif isinstance(value, dict) and 'count' in value:
                response['reposts_count'] = value['count']
        super(RepostableModelMixin, self).parse(response)

    @property
    def reposters(self):
        return [ repost.author for repost in self.wall_reposts.all() ]

    def fetch_reposts(self, source='api', *args, **kwargs):
        if source == 'api':
            return self.fetch_reposts_api(*args, **kwargs)
        else:
            return self.fetch_reposts_parser(*args, **kwargs)

    def fetch_reposts_api(self, *args, **kwargs):
        self.fetch_instance_reposts(*args, **kwargs)
        reposts_count = self.reposts_users.get_query_set(only_pk=True).count()
        if reposts_count < self.reposts_count:
            log.warning('Fetched ammount of repost users less, than attribute `reposts` of post "%s": %d < %d' % (
             self.remote_id, reposts_count, self.reposts_count))
        elif reposts_count > self.reposts_count:
            self.reposts_count = reposts_count
            self.save()
        return self.reposts_users.all()

    @atomic
    def fetch_instance_reposts(self, *args, **kwargs):
        resources = self.fetch_reposts_items(*args, **kwargs)
        if not resources:
            return self.__class__.objects.none()
        else:
            timestamps = dict([ (post['from_id'], post['date']) for post in resources if post['from_id'] > 0 ])
            ids_new = timestamps.keys()
            ids_current = self.reposts_users.get_query_set(only_pk=True).using(MASTER_DATABASE).exclude(time_from=None)
            ids_current_left = self.reposts_users.get_query_set_through().using(MASTER_DATABASE).exclude(time_to=None).values_list('user_id', flat=True)
            ids_add = set(ids_new).difference(set(ids_current))
            ids_remove = set(ids_current).difference(set(ids_new))
            ids_unleft = set(ids_add).intersection(set(ids_current_left))
            ids_add = ids_add.difference(ids_unleft)
            User.remote.fetch(ids=ids_add, only_expired=True)
            self.reposts_users.get_query_set_through().filter(time_from=None).delete()
            self.reposts_users.get_query_set_through().exclude(time_to=None).filter(user_id__in=ids_unleft).update(time_to=None)
            get_repost_date = lambda id: datetime.utcfromtimestamp(timestamps[id]).replace(tzinfo=timezone.utc) if id in timestamps else self.date
            m2m_model = self.reposts_users.through
            m2m_model.objects.bulk_create([ m2m_model(**{'user_id': id, 'post_id': self.pk, 'time_from': get_repost_date(id)}) for id in ids_add ])
            self.reposts_users.get_query_set_through().filter(user_id__in=ids_remove).update(time_to=timezone.now())
            return

    @fetch_all(max_extra_calls=3)
    def fetch_reposts_items(self, offset=0, count=1000, *args, **kwargs):
        if count > 1000:
            raise ValueError("Parameter 'count' can not be more than 1000")
        kwargs['owner_id'] = self.owner_remote_id
        kwargs['post_id'] = self.remote_id_short
        kwargs['offset'] = int(offset)
        kwargs['count'] = int(count)
        response = api_call('wall.getReposts', **kwargs)
        log.debug('Fetching reposts for post %s: %d returned, offset %d, count %d' % (
         self.remote_id, len(response['items']), offset, count))
        return response['items']

    @atomic
    def fetch_reposts_parser(self, offset=0):
        """
        OLD method via parser, may works incorrect
        Update and save fields:
            * reposts - count of reposts
        Update relations
            * reposts_users - users, who repost this post
        """
        post_data = {'act': 'show', 
           'al': 1, 
           'w': 'shares/wall%s' % self.remote_id}
        if offset == 0:
            number_on_page = 40
            post_data['loc'] = ('wall%s' % self.remote_id,)
        else:
            number_on_page = 20
            post_data['offset'] = offset
        log.debug('Fetching reposts of post "%s" of owner "%s", offset %d' % (self.remote_id, self.owner, offset))
        parser = VkontakteWallParser().request('/wkview.php', data=post_data)
        if offset == 0:
            try:
                self.reposts_count = int(parser.content_bs.find('a', {'id': 'wk_likes_tabshares'}).find('nobr').text.split()[0])
                self.save()
            except ValueError:
                return
            except:
                log.warning('Strange markup of first page shares response: "%s"' % parser.content)

            self.reposts_users.clear()
        items = parser.add_users(users=('div', {'id': re.compile('^post\\d'), 'class': re.compile('^post ')}), user_link=(
         'a', {'class': 'author'}), user_photo=lambda item: item.find('a', {'class': 'post_image'}).find('img'), user_add=lambda user: self.reposts_users.add(user))
        if len(items) == number_on_page:
            self.fetch_reposts(offset=offset + number_on_page)
        else:
            return self.reposts_users.all()