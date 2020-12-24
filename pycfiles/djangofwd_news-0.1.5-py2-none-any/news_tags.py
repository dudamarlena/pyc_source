# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\workspace\apps\testin\testnews-env\lib\site-packages\news\templatetags\news_tags.py
# Compiled at: 2015-04-21 16:13:55
from django import template
from django.db.models import Q
from django.utils.translation import get_language, get_language_from_path
import pdb
from news.models import News, Category
register = template.Library()

def latest_news(context, count=3):
    news = News.objects.filter(published=True).order_by('-created_at')[:count]
    context = {'news': news, 
       'request': context['request']}
    return context


register.inclusion_tag('news/templatetags/latest_news.html', takes_context=True)(latest_news)

def highlight_news(context, count):
    news = News.objects.filter(published=True, highlight=True).order_by('-created_at')[:count]
    context = {'news': news, 
       'request': context['request']}
    return context


register.inclusion_tag('news/templatetags/highlight_news.html', takes_context=True)(highlight_news)

def latest_news_category(context, category_id, count=3):
    news = News.objects.filter(category__id=category_id, published=True, category__published=True).order_by('-created_at')[:count]
    category = Category.objects.filter(id=category_id, published=True)
    context = {'news': news, 
       'category_id': category_id, 
       'request': context['request']}
    return context


register.inclusion_tag('news/templatetags/latest_news_category.html', takes_context=True)(latest_news_category)