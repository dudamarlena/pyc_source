# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/foundry/tasks.py
# Compiled at: 2015-04-30 10:11:23
import unicodedata, jellyfish
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import get_template_from_string
from django.template import Context
from django.contrib.sites.models import Site
from django.utils.html import strip_tags
from django.utils.encoding import force_unicode
from django.conf import settings
from celery import task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from preferences import preferences
from foundry.models import FoundryComment
TEMPLATE = '\n<html>\n<body>\n\n{% for comment in comments %}\n    <div>\n        {{ comment.comment }}\n        <br />\n        <a href="http://{{ site_domain}}{% url "admin-remove-comment" comment.id %}" target="_">Remove this comment</a>\n        |\n        <a href="http://{{ site_domain}}{% url "admin-allow-comment" comment.id %}" target="_">Allow this comment</a>\n    </div>\n    <br />\n{% endfor %}\n\n</body>\n<html>\n'

@periodic_task(run_every=crontab(hour='*', minute='*/10', day_of_week='*'), ignore_result=True)
def report_naughty_words():

    def flag(text, threshold, words):
        """Very simple check for naughty words"""
        normalized_text = unicodedata.normalize('NFKD', force_unicode(text)).encode('ascii', 'ignore')
        total_weight = 0
        lwords = normalized_text.lower().split()
        for naughty in words:
            for word in lwords:
                score = jellyfish.jaro_distance(word, naughty)
                if score > 0.7:
                    total_weight = total_weight + score * words[naughty]

        return total_weight > threshold

    threshold = preferences.NaughtyWordPreferences.threshold
    words = {}
    entries = preferences.NaughtyWordPreferences.entries
    for entry in entries.split('\n'):
        try:
            k, v = entry.split(',')
            k = k.strip()
            v = int(v.strip())
        except:
            continue

        words[k] = v

    flagged = []
    comments = FoundryComment.objects.filter(moderated=False).order_by('id')
    for comment in comments:
        if comment.content_object:
            if flag(comment.comment, threshold, words):
                flagged.append(comment)
            else:
                comment.moderated = True
                comment.save()

    if flagged:
        site = Site.objects.get(id=settings.SITE_ID)
        template = get_template_from_string(TEMPLATE)
        c = dict(comments=flagged, site_domain=site.domain)
        content = template.render(Context(c))
        msg = EmailMultiAlternatives('Naughty words report on %s' % site.name, strip_tags(content), settings.DEFAULT_FROM_EMAIL, preferences.NaughtyWordPreferences.email_recipients.split())
        msg.attach_alternative(content, 'text/html')
        msg.send()