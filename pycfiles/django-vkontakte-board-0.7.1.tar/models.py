# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-board/vkontakte_board/models.py
# Compiled at: 2016-03-02 13:24:29
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from vkontakte_api.models import VkontakteTimelineManager, VkontakteModel, VkontakteContentError, VkontakteError
from vkontakte_api.decorators import fetch_all
from vkontakte_groups.models import Group
from vkontakte_users.models import User, ParseUsersMixin
from vkontakte_api.decorators import atomic
import logging
log = logging.getLogger('vkontakte_board')

class CommentManager(models.Manager):
    pass


class TopicManager(models.Manager):
    pass


class BoardRemoteManager(VkontakteTimelineManager, ParseUsersMixin):

    def parse_response(self, response, *args, **kwargs):
        self.parse_response_users(response)
        return super(BoardRemoteManager, self).parse_response(response, *args, **kwargs)


class TopicRemoteManager(BoardRemoteManager):

    @atomic
    @fetch_all(default_count=100)
    def fetch(self, group, ids=None, extended=False, order=None, offset=0, count=100, preview=0, preview_length=90, **kwargs):
        kwargs['group_id'] = group.remote_id
        if ids and isinstance(ids, (list, tuple)):
            kwargs['topic_ids'] = (',').join(map(lambda i: str(i), ids))
        kwargs['extended'] = int(extended)
        if order:
            kwargs['order'] = int(order)
        kwargs['offset'] = int(offset)
        kwargs['count'] = int(count)
        kwargs['preview'] = int(preview)
        kwargs['preview_length'] = int(preview_length)
        kwargs['extra_fields'] = {'group_id': group.pk}
        return super(TopicRemoteManager, self).fetch(**kwargs)


class CommentRemoteManager(BoardRemoteManager):

    @atomic
    @fetch_all(default_count=100)
    def fetch(self, topic, extended=False, offset=0, count=100, sort='asc', need_likes=True, before=None, after=None, **kwargs):
        if count > 100:
            raise ValueError("Attribute 'count' can not be more than 100")
        if sort not in ('asc', 'desc'):
            raise ValueError("Attribute 'sort' should be equal to 'asc' or 'desc'")
        if sort == 'asc' and after:
            raise ValueError("Attribute `sort` should be equal to 'desc' with defined `after` attribute")
        if before and not after:
            raise ValueError('Attribute `before` should be specified with attribute `after`')
        if before and before < after:
            raise ValueError('Attribute `before` should be later, than attribute `after`')
        kwargs['group_id'] = topic.group.remote_id
        kwargs['topic_id'] = topic.remote_id.split('_')[1]
        kwargs['extended'] = int(extended)
        kwargs['offset'] = int(offset)
        kwargs['sort'] = sort
        kwargs['count'] = int(count)
        kwargs['need_likes'] = int(need_likes)
        kwargs['after'] = after
        kwargs['before'] = before
        kwargs['extra_fields'] = {'topic_id': topic.pk}
        try:
            return super(CommentRemoteManager, self).fetch(**kwargs)
        except VkontakteError as e:
            if e.code == 100 and 'invalid tid' in e.description:
                log.error('Impossible to fetch comments for unexisted topic ID=%s' % topic.remote_id)
                return self.model.objects.none()
            raise e


class BoardAbstractModel(VkontakteModel):
    methods_namespace = 'board'
    slug_prefix = 'topic'
    remote_id = models.CharField('ID', max_length='50', help_text='Уникальный идентификатор', unique=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Topic(BoardAbstractModel):
    group = models.ForeignKey(Group, verbose_name='Группа', related_name='topics')
    title = models.CharField('Заголовок', max_length=500)
    created = models.DateTimeField('Дата создания', db_index=True)
    updated = models.DateTimeField('Дата последнего сообщения', null=True, db_index=True)
    created_by = models.ForeignKey(User, related_name='topics_created', verbose_name='Пользователь, создавший тему')
    updated_by = models.ForeignKey(User, related_name='topics_updated', verbose_name='Пользователь, оставивший последнее сообщение')
    is_closed = models.BooleanField('Закрыта?', default=False, help_text='Тема является закрытой (в ней нельзя оставлять сообщения)')
    is_fixed = models.BooleanField('Прикреплена?', default=False, help_text='Тема является прилепленной (находится в начале списка тем)')
    comments_count = models.PositiveIntegerField('Число сообщений в теме', default=0, db_index=True)
    first_comment = models.TextField('Текст первого сообщения')
    last_comment = models.TextField('Текст последнего сообщения')
    objects = TopicManager()
    remote = TopicRemoteManager(remote_pk=('remote_id', ), version=5.8, methods={'get': 'getTopics'})

    class Meta:
        verbose_name = 'Дискуссия групп Вконтакте'
        verbose_name_plural = 'Дискуссии групп Вконтакте'

    def __str__(self):
        return self.title

    @property
    def slug(self):
        return self.slug_prefix + str(self.remote_id)

    def parse(self, response):
        self.created_by = User.objects.get_or_create(remote_id=response.pop('created_by'))[0]
        self.updated_by = User.objects.get_or_create(remote_id=response.pop('updated_by'))[0]
        if 'comments' in response:
            response['comments_count'] = response.pop('comments')
        super(Topic, self).parse(response)
        if '_' not in str(self.remote_id):
            self.remote_id = '-%s_%s' % (self.group.remote_id, self.remote_id)

    @atomic
    def fetch_comments(self, *args, **kwargs):
        return Comment.remote.fetch(topic=self, *args, **kwargs)


class Comment(BoardAbstractModel):
    topic = models.ForeignKey(Topic, verbose_name='Тема', related_name='comments')
    author = models.ForeignKey(User, related_name='topics_comments', verbose_name='Aвтор комментария')
    date = models.DateTimeField(help_text='Дата создания', db_index=True)
    text = models.TextField('Текст сообщения')
    objects = CommentManager()
    remote = CommentRemoteManager(remote_pk=('remote_id', ), version=5.8, methods={'get': 'getComments'})

    class Meta:
        verbose_name = 'Коммментарий дискуссии групп Вконтакте'
        verbose_name_plural = 'Коммментарии дискуссий групп Вконтакте'

    def save(self, *args, **kwargs):
        try:
            self.text.encode('utf-16').decode('utf-16')
        except UnicodeDecodeError:
            self.text = ''

        return super(Comment, self).save(*args, **kwargs)

    @property
    def slug(self):
        return self.slug_prefix + str(self.topic.remote_id) + '?post=' + self.remote_id.split('_')[2]

    def parse(self, response):
        self.author = User.objects.get_or_create(remote_id=response.pop('from_id'))[0]
        if 'attachments' in response:
            response.pop('attachments')
        if 'poll' in response:
            response.pop('poll')
        super(Comment, self).parse(response)
        if '_' not in str(self.remote_id):
            self.remote_id = '%s_%s' % (self.topic.remote_id, self.remote_id)