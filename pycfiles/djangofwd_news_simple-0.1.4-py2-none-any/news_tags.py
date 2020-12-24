# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\workspace\apps\news\news\app\news\templatetags\news_tags.py
# Compiled at: 2015-04-16 06:39:37
from django import template
from news.app.news.models import News
register = template.Library()

def latest_news(context, category_slug, count):
    news = News.objects.filter(category__slug=category_slug, published=True).order_by('-created_at')[:count]
    context = {'news': news, 
       'category_slug': category_slug, 
       'request': context['request']}
    return context


register.inclusion_tag('news/templatetags/latest_news.html', takes_context=True)(latest_news)

def highlight_news(context, count):
    news = News.objects.filter(published=True, highlight=True).order_by('-created_at')[:count]
    context = {'news': news, 
       'request': context['request']}
    return context


register.inclusion_tag('news/templatetags/highlight_news.html', takes_context=True)(highlight_news)