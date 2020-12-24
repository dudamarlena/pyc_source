# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-polls/vkontakte_polls/models.py
# Compiled at: 2016-03-11 12:46:53
import logging
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from vkontakte_api.api import api_call
from vkontakte_api.models import VkontakteManager, VkontakteModel
from vkontakte_api.parser import VkontakteParser
from vkontakte_api.decorators import fetch_all
from vkontakte_groups.models import Group
from vkontakte_users.models import User, USER_FIELDS, ParseUsersMixin
from vkontakte_wall.models import Post
from . import signals
log = logging.getLogger('vkontakte_polls')

class PollsRemoteManager(VkontakteManager):
    methods_namespace = 'polls'
    version = 5.5


class PollRemoteManager(PollsRemoteManager):

    def fetch(self, poll_id, post, **kwargs):
        owner = post.copy_owner or post.owner
        kwargs['extra_fields'] = {'post_id': post.id}
        kwargs['poll_id'] = poll_id
        kwargs['owner_id'] = owner.remote_id
        if isinstance(owner, Group):
            kwargs['owner_id'] *= -1
        return super(PollRemoteManager, self).fetch(**kwargs)


class AnswerRemoteManager(PollsRemoteManager, ParseUsersMixin):

    @fetch_all(always_all=True)
    def fetch_voters(self, answer, offset=0, count=100):
        """
        Update and save fields:
            * votes_count - count of likes
        Update relations:
            * voters - users, who vote for this answer
        """
        params = {'owner_id': answer.poll.post.remote_id.split('_')[0], 
           'poll_id': answer.poll.pk, 
           'answer_ids': answer.pk, 
           'offset': offset, 
           'count': count, 
           'fields': USER_FIELDS}
        result = self.api_call('voters', **params)[0]
        if offset == 0:
            try:
                answer.votes_count = int(result['users']['count'])
                pp = Poll.remote.fetch(answer.poll.pk, answer.poll.post)
                if pp and pp.votes_count:
                    answer.rate = float(answer.votes_count) / pp.votes_count * 100
                else:
                    answer.rate = 0
                answer.save()
            except Exception as err:
                log.warning('Answer fetching error with message: %s' % err)

            answer.voters.clear()
        users = self.parse_response_users(result['users'], items_field='items')
        for user in users:
            answer.voters.add(user)

        return users


class PollsAbstractModel(VkontakteModel):
    remote_id = models.BigIntegerField('ID', help_text='Уникальный идентификатор', primary_key=True)

    class Meta:
        abstract = True


@python_2_unicode_compatible
class Poll(PollsAbstractModel):
    _answers = []
    owner_content_type = models.ForeignKey(ContentType, related_name='vkontakte_polls_polls')
    owner_id = models.PositiveIntegerField(db_index=True)
    owner = generic.GenericForeignKey('owner_content_type', 'owner_id')
    post = models.OneToOneField(Post, verbose_name='Сообщение, в котором опрос', related_name='poll')
    created = models.DateTimeField('Дата создания', db_index=True)
    question = models.TextField('Вопрос')
    votes_count = models.PositiveIntegerField('Голосов', help_text='Общее количество ответивших пользователей', db_index=True)
    answer_id = models.PositiveIntegerField('Ответ', help_text='идентификатор ответа текущего пользователя')
    objects = models.Manager()
    remote = PollRemoteManager(remote_pk=('remote_id', ), methods={'get': 'getById'})

    class Meta:
        verbose_name = 'Опрос Вконтакте'
        verbose_name_plural = 'Опросы Вконтакте'

    @property
    def slug(self):
        return '%s?w=poll-%s' % (self.owner.screen_name, self.post.remote_id)

    def __str__(self):
        return self.question

    def parse(self, response):
        response['votes_count'] = response.pop('votes')
        self._answers = [ Answer.remote.parse_response(answer) for answer in response.pop('answers') ]
        owner_id = int(response.pop('owner_id'))
        ct_model = User if owner_id > 0 else Group
        self.owner_content_type = ContentType.objects.get_for_model(ct_model)
        try:
            self.owner_id = self.owner_content_type.get_object_for_this_type(remote_id=abs(owner_id)).pk
        except ObjectDoesNotExist:
            raise ValueError('Impossible to parse poll with unexisted owner %s, remote_id=%s' % (
             self.owner_content_type.model, owner_id))

        return super(Poll, self).parse(response)

    def save(self, *args, **kwargs):
        duplicate_qs = Poll.objects.filter(post_id=self.post_id)
        if duplicate_qs.count() > 0:
            duplicate_qs.delete()
        result = super(Poll, self).save(*args, **kwargs)
        for answer in self._answers:
            answer.poll = self
            answer.save()

        self._answers = []
        return result


@python_2_unicode_compatible
class Answer(PollsAbstractModel):
    poll = models.ForeignKey(Poll, verbose_name='Опрос', related_name='answers')
    text = models.TextField('Текст ответа')
    votes_count = models.PositiveIntegerField('Голосов', help_text='Количество пользователей, проголосовавших за ответ', db_index=True)
    rate = models.FloatField('Рейтинг', help_text='Рейтинг ответа, в %')
    voters = models.ManyToManyField(User, verbose_name='Голосующие', blank=True, related_name='poll_answers')
    objects = models.Manager()
    remote = AnswerRemoteManager(methods={'voters': 'getVoters'})

    class Meta:
        verbose_name = 'Ответ опроса Вконтакте'
        verbose_name_plural = 'Ответы опросов Вконтакте'

    def __str__(self):
        return self.text

    def parse(self, response):
        response['votes_count'] = response.pop('votes')
        super(Answer, self).parse(response)

    def fetch_voters(self, source='api', **kwargs):
        if source == 'api':
            return self.fetch_voters_by_api(**kwargs)
        return self.fetch_voters_by_parser(**kwargs)

    def fetch_voters_by_parser(self, offset=0):
        """
        Update and save fields:
            * votes_count - count of likes
        Update relations:
            * voters - users, who vote for this answer
        """
        post_data = {'act': 'poll_voters', 
           'al': 1, 
           'opt_id': self.pk, 
           'post_raw': self.poll.post.remote_id}
        number_on_page = 40
        if offset != 0:
            post_data['offset'] = '%d,0,0,0,0,0,0,0,0' % offset
        log.debug('Fetching votes of answer ID="%s" of poll %s of post %s of group "%s", offset %d' % (
         self.pk, self.poll.pk, self.poll.post, self.poll.owner, offset))
        parser = VkontakteParser().request('/al_wall.php', data=post_data)
        if offset == 0:
            try:
                self.votes_count = int(parser.content_bs.find('span', {'id': 'wk_poll_row_count0'}).text)
                self.rate = float(parser.content_bs.find('b', {'id': 'wk_poll_row_percent0'}).text.replace('%', ''))
                self.save()
            except:
                log.warning('Strange markup of first page votes response: "%s"' % parser.content)

            self.voters.clear()
        items = parser.add_users(users=('div', {'class': 'wk_poll_voter inl_bl'}), user_link=(
         'a', {'class': 'wk_poll_voter_lnk'}), user_photo=(
         'img', {'class': 'wk_poll_voter_img'}), user_add=lambda user: self.voters.add(user))
        if len(items) == number_on_page:
            return self.fetch_voters(offset=offset + number_on_page)
        else:
            return self.voters.all()

    def fetch_voters_by_api(self, **kwargs):
        return Answer.remote.fetch_voters(answer=self, **kwargs)