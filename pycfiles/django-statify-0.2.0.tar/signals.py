# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chschw/Workspace/django/lab/django-cms/site/statify/signals.py
# Compiled at: 2013-04-24 07:28:53
from django.db.models.signals import post_save, post_delete
from django.contrib.sites.models import Site
from models import URL
from utils import url_is_valid
import settings as statify_settings
EXCLUDED_MODELS = ('Session', 'Group', 'User', 'LogEntry', 'Release', 'DeploymentHost',
                   'URL', 'ExternalURL')

def save_handler(sender, **kwargs):
    """
    Example class methods:

    Use the following example method for multiple urls:
    def statify_urls(self):
        url_list = list()
        url_list.append('/%s/' % self.locale)

        return url_list

    Use the following example method for a single url:
    def statify_url(self):
        return u'/%s/' % self.locale
    """
    current_site = Site.objects.get_current()
    model = sender.__name__
    if statify_settings.STATIFY_USE_CMS and model is 'Title':
        instance = kwargs.get('instance')
        if not instance.page.is_home():
            absolute_url = '/%s/%s/' % (instance.language, instance.path)
        else:
            absolute_url = '/%s/' % instance.language
        if url_is_valid('http://%s%s' % (current_site, absolute_url)):
            try:
                URL(url=absolute_url).save()
            except:
                pass

    if model not in EXCLUDED_MODELS:
        try:
            urls = kwargs.get('instance').statify_urls()
            for url in urls:
                try:
                    URL(url=url).save()
                except:
                    pass

        except:
            pass

        try:
            url = kwargs.get('instance').statify_url()
            URL(url=url).save()
        except:
            pass


post_save.connect(save_handler)

def delete_handler(sender, **kwargs):
    model = sender.__name__
    if statify_settings.STATIFY_USE_CMS and model is 'Title':
        instance = kwargs.get('instance')
        if instance.path:
            absolute_url = '/%s/%s/' % (instance.language, instance.path)
        else:
            absolute_url = '/%s/' % instance.language
        try:
            URL.objects.get(url=absolute_url).delete()
        except:
            pass

    if model not in EXCLUDED_MODELS:
        try:
            urls = kwargs.get('instance').statify_urls()
            for url in urls:
                try:
                    URL.objects.get(url=url).delete()
                except:
                    pass

        except:
            pass

        try:
            url = kwargs.get('instance').statify_url()
            URL.objects.get(url=url).delete()
        except:
            pass


post_delete.connect(delete_handler)