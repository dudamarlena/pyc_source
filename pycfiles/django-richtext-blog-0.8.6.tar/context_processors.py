# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/projects/wholebaked-site/venv/lib/python2.7/site-packages/richtext_blog/context_processors.py
# Compiled at: 2012-04-15 00:30:08
from datetime import datetime
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from models import Post, Tag
from views import PostListView

def blog_global(request):
    """
    Pass up global context objects
    """
    current_site = Site.objects.get_current()
    dates = Post.objects.dates('created', 'month')
    now = datetime.now()
    archive_links = []
    seen_years = {}
    for date in dates:
        if date.year < now.year:
            if date.year not in seen_years:
                archive_links.append({'link': reverse('posts_yearly', kwargs={'year': date.year}), 
                   'link_text': date.year})
                seen_years[date.year] = None
        else:
            archive_links.append({'link': reverse('posts_monthly', kwargs={'year': date.year, 'month': date.strftime('%m')}), 
               'link_text': date.strftime('%B %Y')})

    tag_counts = [ {'slug': t.slug, 'count': t.tag_posts.count(), 'name': t.name} for t in Tag.objects.all()
                 ]
    recent_post_links = [ {'title': p.title, 'link': p.get_absolute_url(), 'date': p.created.strftime('%A %B %d, %Y')} for p in Post.objects.all().order_by('-created')[:5]
                        ]
    return {'SITE': current_site, 
       'BLOG_ARCHIVE_LINKS': sorted(archive_links, reverse=True), 
       'BLOG_TAG_COUNTS': sorted(tag_counts, key=lambda tag: tag['count'], reverse=True), 
       'BLOG_RECENT_POSTS': recent_post_links}