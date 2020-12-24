# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/virtualenvs/kd/src/chalk/chalk/tests.py
# Compiled at: 2013-08-19 21:02:57
from django.test import TestCase
from django.core.urlresolvers import reverse
from .models import Article

class ArticleViewTests(TestCase):
    """Test article views."""
    fixtures = [
     'chalk_test_data.json']

    def test_list_view(self):
        """Should only return published articles for non-staff users."""
        published_articles = Article.objects.filter(published=True)
        response = self.client.get(reverse('list_articles'))
        returned_articles = response.context['article_list']
        self.assertItemsEqual(returned_articles, published_articles)

    def test_detail_view(self):
        """Check that article detail view returns correct article."""
        article = Article.objects.filter(published=True)[0]
        response = self.client.get(reverse('view_article', kwargs={'slug': article.slug}))
        returned_article = response.context['article']
        self.assertEqual(article, returned_article)

    def test_detail_view_unpublished(self):
        """Unpublished articles should return 404 for non-staff users."""
        article = Article.objects.filter(published=False)[0]
        response = self.client.get(reverse('view_article', kwargs={'slug': article.slug}))
        self.assertEqual(response.status_code, 404)


class ArticleModelTests(TestCase):
    """Test the Article model."""
    fixtures = [
     'chalk_test_data.json']

    def test_save(self):
        """Saving should populate HTML fields by default."""
        article = Article.objects.get(title='Test Title')
        article.content = 'Some content'
        article.content_html = 'content to be overwritten'
        article.excerpt = 'An excerpt'
        article.excerpt_html = 'excerpt to be overwritten'
        article.save()
        self.assertEqual(article.content_html, '<p>Some content</p>\n')
        self.assertEqual(article.excerpt_html, '<p>An excerpt</p>\n')

    def test_protect_html(self):
        """Article.protect_html should prevent HTML overwrites."""
        article = Article.objects.get(title='Test Title')
        article.protect_html = True
        article.content = 'Content goes here.'
        article.content_html = 'Protected Content'
        article.excerpt = 'A blurb about nothing.'
        article.excerpt_html = 'Protected Excerpt'
        article.save()
        self.assertEqual(article.content_html, 'Protected Content')
        self.assertEqual(article.excerpt_html, 'Protected Excerpt')

    def test_generate_html(self):
        """Articles should generate correct HTML from reST input."""
        excerpt = "Here's a bit of `reStructuredText`_ for *testing* purposes.\n\n.. _reStructuredText: http://docutils.sourceforge.net/rst.html\n"
        expected_html = ('<div class="section" id="glorious-content">\n<h2>Glorious Content</h2>\n<p>What about an internal reference to a <a class="reference internal" href="#section">Section</a>?</p>\n<div class="section" id="section">\n<h3>Section</h3>\n<p>Great.</p>\n</div>\n</div>\n',
                         '<p>Here\'s a bit of <a class="reference external" href="http://docutils.sourceforge.net/rst.html">reStructuredText</a> for <em>testing</em> purposes.</p>\n')
        content = 'Glorious Content\n----------------\n\nWhat about an internal reference to a `Section`_?\n\nSection\n=======\n\nGreat.'
        article = Article.objects.get(title='Test Title')
        article.excerpt = excerpt
        article.content = content
        self.assertEqual(article.generate_html(), expected_html)