# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enrico/pyenv/titschendorf.de/django_clear_memcache/admin.py
# Compiled at: 2017-04-17 10:14:37
from django.conf.urls import url
from django.contrib import admin
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.translation import ugettext_lazy as _
from django_clear_memcache.clear import ClearMemcacheController, ClearMemcacheNoCacheFoundError
from django_clear_memcache.models import ClearMemcache
import json

class ClearMemcacheAdmin(admin.ModelAdmin):
    model = ClearMemcache
    change_list_template = 'admin/clear_memcache.html'

    def get_queryset(self, request):
        """Override queryset to return a simple empty queryset
           as we do not really have a real model anyway"""
        return ClearMemcache.objects.none()

    queryset = get_queryset

    def has_add_permission(self, request):
        """A fake model should not be added"""
        return False

    def has_delete_permission(self, request, obj=None):
        """A fake model should not be added"""
        return False

    def get_urls(self):
        urls = admin.ModelAdmin.get_urls(self)
        my_urls = [
         url('^clear/$', self.admin_site.admin_view(self.clear), name='clear_cache'),
         url('^list/$', self.admin_site.admin_view(self.list_cache_items), name='cache_list_keys')]
        return my_urls + urls

    def clear(self, request):
        use_prefix = 'clear_prefix' in request.POST
        clear_cache_controller = ClearMemcacheController()
        clear_cache_controller.clear_cache(use_prefix=use_prefix)
        self.message_user(request, _('Cache has been cleared'), fail_silently=True)
        changelist_url = self._admin_url('changelist')
        return HttpResponseRedirect(changelist_url)

    def list_cache_items(self, request):
        clear_cache_controller = ClearMemcacheController()
        cache_keys_prefix = clear_cache_controller.keys(use_prefix=True)
        json_ = json.dumps(cache_keys_prefix)
        print 'hallo'
        return HttpResponse(json_, content_type='application/json')

    def _admin_url(self, target_url):
        opts = self.model._meta
        url_ = 'admin:%s_%s_%s' % (opts.app_label, opts.object_name.lower(), target_url)
        return reverse(url_)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or dict()
        extra_context['title'] = _('Clear Memcache')
        try:
            clear_cache_controller = ClearMemcacheController()
            cache_keys_prefix = clear_cache_controller.keys(use_prefix=True)
            cache_keys = clear_cache_controller.keys(use_prefix=False)
        except ClearMemcacheNoCacheFoundError:
            extra_context['no_cache_found'] = True
        else:
            extra_context['cache_keys_prefix_count'] = len(cache_keys_prefix)
            extra_context['cache_key_count'] = len(cache_keys)
            extra_context['cache_key_prefix'] = cache.key_prefix
            extra_context['cl'] = cache_keys

        response = admin.ModelAdmin.changelist_view(self, request, extra_context=extra_context)
        return response


admin.site.register(ClearMemcache, ClearMemcacheAdmin)