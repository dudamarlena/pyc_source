# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/news/views.py
# Compiled at: 2014-03-27 09:47:06
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Article
from .forms import ArticleSearchForm

def ArticleList(request):
    """
    This renders the list of articles.
    """
    form = ArticleSearchForm(request.GET)
    if form.is_valid() and request.GET:
        if len(form.cleaned_data['category']) > 0:
            articles = Article.objects.published().filter(category__in=form.cleaned_data['category']).order_by('-publish_on')
        else:
            articles = Article.objects.published().order_by('-publish_on')
        if len(form.cleaned_data['date']) > 0:
            query = reduce(lambda a, b: a | b, [ Q(publish_on__month=d.split('-')[1], publish_on__year=d.split('-')[0]) for d in form.cleaned_data['date'] ])
            articles = articles.filter(query)
    else:
        articles = Article.objects.published().order_by('-publish_on')
    paginator = Paginator(articles, 6)
    page = paginator.page(request.GET.get('page', 1))
    qs = request.GET.copy()
    if qs.has_key('page'):
        qs.pop('page')
    query_string = qs.urlencode()
    return render(request, 'news/article_list.html', {'form': form, 
       'obj_list': articles, 
       'paginator': paginator, 
       'page': page, 
       'query_string': query_string})


def ArticleDetail(request, slug):
    """
    View a single article.
    """
    article = get_object_or_404(Article, slug=slug)
    return render(request, 'news/article_detail.html', {'object': article})