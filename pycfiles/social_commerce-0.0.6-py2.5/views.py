# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/apps/tag_app/views.py
# Compiled at: 2009-10-31 23:19:40
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from blog.models import Post
from tagging.models import Tag, TaggedItem
from photos.models import Image
from bookmarks.models import BookmarkInstance
from wiki.models import Article as WikiArticle

def tags(request, tag, template_name='tags/index.html'):
    tag = get_object_or_404(Tag, name=tag)
    alltags = TaggedItem.objects.get_by_model(Post, tag).filter(status=2)
    phototags = TaggedItem.objects.get_by_model(Image, tag)
    bookmarktags = TaggedItem.objects.get_by_model(BookmarkInstance, tag)
    wiki_article_tags = TaggedItem.objects.get_by_model(WikiArticle, tag)
    return render_to_response(template_name, {'tag': tag, 
       'alltags': alltags, 
       'phototags': phototags, 
       'bookmarktags': bookmarktags, 
       'project_tags': project_tags, 
       'wiki_article_tags': wiki_article_tags}, context_instance=RequestContext(request))