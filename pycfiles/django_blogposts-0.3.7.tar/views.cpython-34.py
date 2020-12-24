# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/django_blogposts/django_blogposts/views.py
# Compiled at: 2018-08-06 07:34:20
# Size of source mod 2**32: 3984 bytes
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.http import Http404
from django.shortcuts import render
from django.conf import settings
from django.db.models import Q
from django.views.decorators.cache import cache_page
from .models.blogpost import BlogPost
from .models.categories import Categories
from .models.tags import Tags
__author__ = 'spi4ka'
CACHE_TIMEOUT = 0
if getattr(settings, 'BLOGPOST_CACHE_TIMEOUT', False):
    CACHE_TIMEOUT = settings.BLOGPOST_CACHE_TIMEOUT

def _get_queryset(request, queryset, pk=None):
    if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
        queryset = queryset.prefetch_related('category')
        queryset = queryset.filter(category__is_moderated=True)
        if pk:
            queryset = queryset.filter(category__pk=pk)
        if getattr(settings, 'BLOGPOSTS_USE_TAGS', True):
            queryset = queryset.prefetch_related('tags')
            if request.GET.get('tag'):
                queryset = queryset.filter(tags__is_moderated=True)
                queryset = queryset.filter(tags__slug=request.GET.get('tag'))
            else:
                queryset = queryset.filter(Q(tags__is_moderated=True) | Q(tags=None))
        if request.GET.get('q'):
            if 'django.contrib.postgres' in settings.INSTALLED_APPS:
                from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank
                query = SearchQuery(request.GET.get('q'))
                vector = SearchVector('header')
                queryset = queryset.annotate(search=vector).filter(search=query).annotate(rank=SearchRank(vector, query)).order_by('-rank')
                queryset = queryset.filter(header__search=request.GET.get('q'))
            else:
                queryset = queryset.filter(header__icontains=request.GET.get('q'))
        return queryset.distinct().defer('content', 'meta_title', 'meta_kw', 'meta_desc', 'de')


class PostsListView(ListView):
    queryset = BlogPost.active.all()
    paginate_by = 10
    template_name = 'django_blogposts/list.html'

    def get_queryset(self):
        return _get_queryset(self.request, self.queryset)

    def get_context_data(self, *args, **kw):
        context = super().get_context_data(*args, **kw)
        if self.kwargs.get('pk'):
            if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
                try:
                    context['category'] = Categories.objects.get(pk=self.kwargs.get('pk'))
                except Categories.DoesNotExist:
                    pass

            if getattr(settings, 'BLOGPOSTS_USE_TAGS', True):
                context['tags'] = Tags.objects.filter(is_moderated=True)
        context['active_category'] = self.kwargs.get('pk')
        context['active_tag'] = self.request.GET.get('tag')
        return context

    def get(self, request, *args, **kwargs):
        if 'rest_framework' in settings.INSTALLED_APPS:
            return render(request, template_name=self.template_name)
        else:
            return super().get(request, *args, **kwargs)


class PostsDetailView(DetailView):
    queryset = BlogPost.active.all()
    template_name = 'django_blogposts/detail.html'

    def dispatch(self, *args, **kw):
        return cache_page(CACHE_TIMEOUT)(super().dispatch)(*args, **kw)

    def get_object(self, *args, **kw):
        page = super().get_object(*args, **kw)
        try:
            if getattr(settings, 'BLOGPOSTS_USE_CATEGORIES', True):
                if not page.category.is_moderated:
                    raise Http404
        except:
            raise Http404

        return page