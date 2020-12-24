# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/opps/feedcrawler/views.py
# Compiled at: 2014-06-23 11:25:49
import random
from django.shortcuts import redirect
from django.utils.text import slugify
from opps.articles.models import Post
from opps.feedcrawler.models import Entry
from opps.channels.models import Channel

def get_tmp_channel(user=None):
    channel, created = Channel.objects.get_or_create(slug='tmp', name='tmp', user=user)
    return channel


def create_post(request, post_id):
    entry = Entry.objects.get(pk=int(post_id))
    post = Post(title=entry.entry_title, slug=slugify(entry.entry_title), content=entry.entry_content, channel=entry.entry_feed.channel or get_tmp_channel(request.user or entry.user), site=entry.site, user=request.user or entry.user, show_on_root_channel=True, published=False, hat=entry.hat)
    try:
        post.save()
    except:
        post.slug = ('{0}-{1}').format(post.slug[:100], random.getrandbits(32))
        post.save()

    entry.post_created = True
    entry.save()
    return redirect(('/admin/articles/post/{}/').format(post.pk))