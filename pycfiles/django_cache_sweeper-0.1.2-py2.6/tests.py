# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/cachesweeper/tests.py
# Compiled at: 2011-01-26 07:35:04
from django.test import TestCase, Client
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.utils.hashcompat import md5_constructor
from django.core.management import call_command
from cachesweeper.utils import cache_token_key_for_record, generate_fragment_cache_key_for_record
from cachesweeper.test_models import Comment, Article, TestMixinModel, TestAttributeModel

class FragmentCacheInvalidation(TestCase):
    fixtures = [
     'test_auth_data', 'test_cachesweeper_data']

    def __init__(self, *args, **kwargs):
        call_command('syncdb')
        super(FragmentCacheInvalidation, self).__init__(*args, **kwargs)

    def setUp(self):
        cache.clear()

    def tearDown(self):
        pass

    def test_version_at_creation(self):
        comment = Comment.objects.latest()
        comment.like_it()
        version_cache_key = cache_token_key_for_record(comment)
        self.assertEquals(cache.get(version_cache_key), 0)

    def test_version_after_save(self):
        comment = Comment.objects.latest()
        version_cache_key = cache_token_key_for_record(comment)
        original_version = cache.get(version_cache_key, None)
        comment.like_it()
        new_version = cache.get(version_cache_key)
        self.assertNotEquals(original_version, new_version)
        return

    def test_fragment_cache_miss(self):
        comment = Comment.objects.latest()
        from django.template import Context, Template
        template = Template('\n        {% load cachesweeper_tags %}\n        {% cachesweeper comment 500 "comment.xml" %}\n        <p>\n            <strong>{{comment.user}}</strong> said at {{comment.created_at}}:<br/>\n            {{comment.content}}\n            <br/>\n        </p>\n        {% endcachesweeper %}\n        ')
        template.render(Context({'comment': comment}))
        cache_key = generate_fragment_cache_key_for_record(comment, 'comment.xml')
        self.assertTrue(cache.get(cache_key))
        comment.like_it()
        new_cache_key = generate_fragment_cache_key_for_record(comment, 'comment.xml')
        self.assertNotEquals(cache_key, new_cache_key)
        self.assertFalse(cache.get(new_cache_key))

    def test_modelsweeper_mixin(self):
        tmm = TestMixinModel(text='testing text')
        tmm.save()
        self.assertEquals(tmm.cachesweeper_version_key, 'cachesweeper.test_models:TestMixinModel:%s' % tmm.pk)
        self.assertEquals(tmm.cachesweeper_version, 0)
        tmm.save()
        self.assertEquals(tmm.cachesweeper_version, 1)

    def test_default_version_zero(self):
        tmm = TestMixinModel(text='testing text')
        tmm.save()
        cache.delete(tmm.cachesweeper_version_key)
        self.assertEquals(tmm.cachesweeper_version, 0)
        tmm.save()
        self.assertEquals(tmm.cachesweeper_version, 1)