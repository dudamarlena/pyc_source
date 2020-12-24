# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/eetu/envs/cmsplugin-articles-ai/project/cmsplugin_articles_ai/views.py
# Compiled at: 2017-08-31 05:41:42
# Size of source mod 2**32: 4256 bytes
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from publisher.views import PublisherDetailView, PublisherListView
from .models import Article, Category, Tag, TagFilterMode

class ArticleView(PublisherDetailView):
    """ArticleView"""
    model = Article
    template_name = 'cmsplugin_articles_ai/article_detail.html'

    def get_queryset(self):
        articles = super(ArticleView, self).get_queryset()
        return articles.public()

    def get_context_data(self, **kwargs):
        context = super(ArticleView, self).get_context_data(**kwargs)
        article = self.object
        attachments = article.attachments.select_related('attachment_file')
        images = []
        non_images = []
        for attachment in article.attachments.select_related('attachment_file').all():
            (images if attachment.is_image else non_images).append(attachment)

        context.update({'attachments': non_images, 
         'image_attachments': images, 
         'tags': article.tags.select_related()})
        return context


class ArticleListView(PublisherListView):
    """ArticleListView"""
    model = Article
    context_object_name = 'articles'
    paginate_by = getattr(settings, 'ARTICLES_PER_PAGE', 10)
    tag_filter = ''
    template_name = 'cmsplugin_articles_ai/app_index.html'

    def get(self, request, *args, **kwargs):
        self.tag_filter = self.kwargs.get('tag', '')
        self.lang_filter = request.GET.get('lang', '')
        return super(ArticleListView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        articles = super(ArticleListView, self).get_queryset()
        articles = articles.public(language=self.lang_filter)
        if self.tag_filter:
            return articles.filter(tags__slug=self.tag_filter)
        return articles

    def get_context_data(self, **kwargs):
        context = super(ArticleListView, self).get_context_data(**kwargs)
        context.update({'all_tags': Tag.objects.all(), 
         'all_categories': Category.objects.all(), 
         'page_title': self.tag_filter or _('All articles'), 
         'tag_filter': self.tag_filter})
        return context


class CategoryView(ArticleListView):
    """CategoryView"""

    def get(self, request, *args, **kwargs):
        category_slug = self.kwargs.get('category', '')
        self.category = Category.objects.get(slug=category_slug)
        return super(CategoryView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        articles = super(CategoryView, self).get_queryset()
        return articles.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        context.update({'category': self.category, 
         'page_title': self.category.title})
        return context


class TagFilteredArticleView(ArticleListView):
    """TagFilteredArticleView"""

    def get(self, request, *args, **kwargs):
        self.filter_tags = request.GET.get('filter_tags', [])
        if self.filter_tags:
            self.filter_tags = [int(pk, 10) for pk in self.filter_tags.split(',')]
        self.filter_mode = TagFilterMode(int(request.GET.get('filter_mode', TagFilterMode.ALL.value)))
        return super(TagFilteredArticleView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        articles = super(TagFilteredArticleView, self).get_queryset()
        return articles.tag_filter(self.filter_mode, self.filter_tags)