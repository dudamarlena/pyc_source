# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture_old/env/src/django-vkontakte-wall/vkontakte_wall/models.py
# Compiled at: 2015-06-17 13:40:16
import logging, re
from django.conf import settings
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.dispatch import Signal
from django.utils.encoding import python_2_unicode_compatible
from vkontakte_api.decorators import fetch_all, atomic
from vkontakte_api.mixins import OwnerableModelMixin, AuthorableModelMixin, RawModelMixin
from vkontakte_api.models import VkontakteTimelineManager, VkontakteIDStrModel, VkontakteCRUDModel, VkontakteCRUDManager
from vkontakte_comments.mixins import CommentableModelMixin
from vkontakte_groups.models import Group, ParseGroupsMixin
from vkontakte_users.models import User, ParseUsersMixin
from .mixins import RepostableModelMixin, LikableModelMixin
from .parser import VkontakteWallParser, VkontakteParseError
log = logging.getLogger('vkontakte_wall')
parsed = Signal(providing_args=['sender', 'instance', 'container'])

class WallRemoteManager(VkontakteTimelineManager, ParseUsersMixin, ParseGroupsMixin):
    response_instances_fieldname = 'wall'
    timeline_force_ordering = True

    def fetch(self, ids=None, *args, **kwargs):
        """
        Retrieve and save object to local DB
        """
        if ids:
            kwargs['posts'] = (',').join(ids)
            kwargs['method'] = 'getById'
        return super(WallRemoteManager, self).fetch(*args, **kwargs)

    def parse_response_dict(self, resource, extra_fields=None):
        if self.response_instances_fieldname in resource:
            self.parse_response_users(resource)
            self.parse_response_groups(resource)
            return super(WallRemoteManager, self).parse_response_list(resource[self.response_instances_fieldname], extra_fields)
        else:
            return super(WallRemoteManager, self).parse_response_dict(resource, extra_fields)

    @atomic
    @fetch_all
    def fetch_wall(self, owner, offset=0, count=100, filter='all', extended=False, before=None, after=None, **kwargs):
        if filter not in ('owner', 'others', 'all'):
            raise ValueError("Attribute 'fiter' has illegal value '%s'" % filter)
        if count > 100:
            raise ValueError("Attribute 'count' can not be more than 100")
        if before and not after:
            raise ValueError('Attribute `before` should be specified with attribute `after`')
        if before and before < after:
            raise ValueError('Attribute `before` should be later, than attribute `after`')
        kwargs['owner_id'] = self.model.get_owner_remote_id(owner)
        kwargs['filter'] = filter
        kwargs['extended'] = int(extended)
        kwargs['offset'] = int(offset)
        kwargs['count'] = count
        kwargs['after'] = after
        kwargs['before'] = before
        log.debug('Fetching posts of owner "%s", offset %d' % (owner, offset))
        return self.fetch(**kwargs)

    @atomic
    def fetch_group_wall_parser(self, group, offset=0, count=None, own=False, after=None):
        """
        Old method via parser
        TODO: `before` parameter not implemented
        """
        post_data = {'al': 1, 
           'offset': offset, 
           'own': int(own), 
           'part': 1}
        log.debug('Fetching post of group "%s", offset %d' % (group, offset))
        parser = VkontakteWallParser().request('/wall-%s' % group.remote_id, data=post_data)
        items = parser.content_bs.findAll('div', {'class': re.compile('^post'), 'id': re.compile('^post-%d' % group.remote_id)})
        current_count = offset + len(items)
        need_cut = count and count < current_count
        if need_cut:
            items = items[:count - offset]
        for item in items:
            try:
                post = parser.parse_post(item, group)
            except VkontakteParseError as e:
                log.error(e)
                continue

            if after and post.date < after:
                need_cut = True
                break
            post.raw_html = unicode(item)
            post.save()
            parsed.send(sender=Post, instance=post, container=item)

        if len(items) == 20 and not need_cut:
            return self.fetch_group_wall(group, offset=current_count, count=count, own=own, after=after)
        else:
            if after:
                return group.wall_posts.filter(date__gte=after)
            return group.wall_posts.all()


@python_2_unicode_compatible
class Post(RawModelMixin, OwnerableModelMixin, AuthorableModelMixin, LikableModelMixin, RepostableModelMixin, CommentableModelMixin, VkontakteIDStrModel, VkontakteCRUDModel):
    slug_prefix = 'wall'
    fields_required_for_update = ['owner_id']
    comments_remote_related_name = 'post_id'
    likes_remote_type = 'post'
    _commit_remote = False
    raw_html = models.TextField()
    date = models.DateTimeField('Время сообщения', db_index=True)
    text = models.TextField('Текст записи')
    attachments = models.TextField()
    media = models.TextField()
    geo = models.TextField()
    signer_id = models.PositiveIntegerField(null=True, help_text='Eсли запись была опубликована от имени группы и подписана пользователем, то в поле содержится идентификатор её автора')
    copy_owner_content_type = models.ForeignKey(ContentType, related_name='vkontakte_wall_copy_posts', null=True)
    copy_owner_id = models.PositiveIntegerField(null=True, db_index=True, help_text='Eсли запись является копией записи с чужой стены, то в поле содержится идентификатор владельца стены у которого была скопирована запись')
    copy_owner = generic.GenericForeignKey('copy_owner_content_type', 'copy_owner_id')
    copy_post = models.ForeignKey('Post', null=True, related_name='wall_reposts', help_text='Если запись является копией записи с чужой стены, то в поле содержится идентфикатор скопированной записи на стене ее владельца')
    copy_text = models.TextField('Комментарий при репосте', help_text='Если запись является копией записи с чужой стены и при её копировании был добавлен комментарий, его текст содержится в данном поле')
    post_source = models.TextField()
    online = models.PositiveSmallIntegerField(null=True)
    reply_count = models.PositiveIntegerField(null=True)
    objects = VkontakteCRUDManager()
    remote = WallRemoteManager(remote_pk=('remote_id', ), version=5.27, methods_namespace='wall', methods={'get': 'get', 
       'getById': 'getById', 
       'create': 'post', 
       'update': 'edit', 
       'delete': 'delete', 
       'restore': 'restore'})

    class Meta:
        verbose_name = 'Сообщение Вконтакте'
        verbose_name_plural = 'Сообщения Вконтакте'

    def __str__(self):
        return '%s: %s' % (unicode(self.owner), self.text)

    def save(self, *args, **kwargs):
        if self.copy_owner_id and not self.copy_owner_content_type:
            ct_model = User if self.copy_owner_id > 0 else Group
            self.copy_owner_content_type = ContentType.objects.get_for_model(ct_model)
            self.copy_owner = ct_model.remote.fetch(ids=[
             abs(self.copy_owner_id)])[0]
        if self.copy_owner:
            self.copy_owner.save()
        return super(Post, self).save(*args, **kwargs)

    def prepare_create_params(self, **kwargs):
        kwargs.update({'owner_id': self.owner_remote_id, 
           'friends_only': kwargs.get('friends_only', 0), 
           'from_group': kwargs.get('from_group', ''), 
           'message': self.text, 
           'attachments': self.attachments, 
           'services': kwargs.get('services', ''), 
           'signed': 1 if self.signer_id else 0, 
           'publish_date': kwargs.get('publish_date', ''), 
           'lat': kwargs.get('lat', ''), 
           'long': kwargs.get('long', ''), 
           'place_id': kwargs.get('place_id', ''), 
           'post_id': kwargs.get('post_id', '')})
        return kwargs

    def prepare_update_params(self, **kwargs):
        return self.prepare_create_params(post_id=self.remote_id_short, **kwargs)

    def prepare_delete_params(self):
        return {'owner_id': self.owner_remote_id, 
           'post_id': self.remote_id_short}

    def parse_remote_id_from_response(self, response):
        if response:
            return '%s_%s' % (self.owner_remote_id, response['post_id'])
        else:
            return

    def parse(self, response):
        super(Post, self).parse(response)
        self.remote_id = '%s_%s' % (self.owner_remote_id, self.remote_id)

    def fetch_statistic(self, *args, **kwargs):
        if 'vkontakte_wall_statistic' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_wall_statistic' not in INSTALLED_APPS")
        from vkontakte_wall_statistic.models import PostStatistic
        return PostStatistic.remote.fetch(post=self, *args, **kwargs)

    def fetch_reach(self, *args, **kwargs):
        if 'vkontakte_wall_statistic' not in settings.INSTALLED_APPS:
            raise ImproperlyConfigured("Application 'vkontakte_wall_statistic' not in INSTALLED_APPS")
        from vkontakte_wall_statistic.models import PostReach
        return PostReach.remote.fetch(post=self, *args, **kwargs)


Group.add_to_class('wall_posts', generic.GenericRelation(Post, content_type_field='owner_content_type', object_id_field='owner_id', related_name='group_wall', verbose_name='Сообщения на стене'))
User.add_to_class('wall_posts', generic.GenericRelation(Post, content_type_field='owner_content_type', object_id_field='owner_id', related_name='user_wall', verbose_name='Сообщения на стене'))
Group.add_to_class('posts', generic.GenericRelation(Post, content_type_field='author_content_type', object_id_field='author_id', related_name='group', verbose_name='Сообщения'))
User.add_to_class('posts', generic.GenericRelation(Post, content_type_field='author_content_type', object_id_field='author_id', related_name='user', verbose_name='Сообщения'))