# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-vkontakte-polls/vkontakte_polls/signals.py
# Compiled at: 2016-03-11 13:09:27
import logging, re
from django.db.models.signals import post_save
from django.dispatch import receiver
from vkontakte_api.api import VkontakteError
from vkontakte_wall.models import Post
log = logging.getLogger('vkontakte_polls')

@receiver(post_save, sender=Post)
def fetch_poll_for_post(sender, instance, created, **kwargs):
    from .models import Poll
    try:
        poll_id = None
        if instance.raw_html:
            poll_id = re.findall('<input type="hidden" id="post_poll_(?:raw|id)(?:[^"]+)" value="([^"]+)" />', instance.raw_html)[0]
            if '_' in poll_id:
                poll_id = poll_id.split('_')[1]
                if poll_id:
                    Poll.remote.fetch(poll_id, instance)
        elif instance.raw_json:
            if 'copy_history' in instance.raw_json and len(instance.raw_json['copy_history']) >= 1:
                attachments = instance.raw_json['copy_history'][0].get('attachments', [])
            else:
                attachments = instance.raw_json.get('attachments', [])
            for attachment in attachments:
                if attachment['type'] == 'poll':
                    poll = Poll.remote.parse_response_dict(attachment['poll'], {'post_id': instance.pk})
                    Poll.remote.get_or_create_from_instance(poll)

    except VkontakteError as e:
        log.error("Vkontakte error (code = %s) raised: '%s'" % (e.code, e.description))
    except (IndexError, AssertionError):
        pass

    return