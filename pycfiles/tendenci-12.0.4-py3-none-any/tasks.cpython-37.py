# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/wp_importer/tasks.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 2163 bytes
from celery.task import Task
from celery.registry import tasks
from bs4 import BeautifulStoneSoup
from tendenci.apps.wp_importer.utils import get_media, get_posts, get_pages
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from tendenci.apps.site_settings.utils import get_setting

class WPImportTask(Task):

    def run(self, file_name, user, **kwargs):
        """
        Parse the given xml file using BeautifulSoup. Save all Article, Redirect and Page objects.
        """
        f = open(file_name, 'r')
        xml = f.read()
        f.close()
        soup = BeautifulStoneSoup(xml)
        items = soup.find_all('item')
        for item in items:
            post_type = item.find('wp:post_type').string
            post_status = item.find('wp:status').string
            if post_type == 'attachment':
                get_media(item, user)
            elif post_type == 'post':
                if post_status == 'publish':
                    get_posts(item, user)
            if post_type == 'page' and post_status == 'publish':
                get_pages(item, user)

        if user.email:
            context = {'SITE_GLOBAL_SITEDISPLAYNAME':get_setting('site', 'global', 'sitedisplayname'),  'SITE_GLOBAL_SITEURL':get_setting('site', 'global', 'siteurl')}
            subject = ''.join(render_to_string(template_name='notification/wp_import/short.txt', context=context).splitlines())
            body = render_to_string(template_name='notification/wp_import/full.html', context=context)
            email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
            email.content_subtype = 'html'
            email.send(fail_silently=True)


tasks.register(WPImportTask)