# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/global_untranslated_placeholder/signals.py
# Compiled at: 2018-03-27 09:45:07
from __future__ import unicode_literals
from django.conf import settings
from django.dispatch import receiver
from cms.constants import PUBLISHER_STATE_DIRTY
from cms.signals import post_placeholder_operation, post_publish
from djangocms_misc.global_untranslated_placeholder.utils import get_untranslated_default_language
if b'djangocms_misc.autopublisher' not in settings.INSTALLED_APPS:

    @receiver(post_publish, dispatch_uid=b'cms_global_untranslated_placeholder_post_publish')
    def post_publish_handler(**kwargs):
        page_instance = kwargs.get(b'instance', None)
        if not page_instance:
            return
        else:
            published_language = kwargs.get(b'language', settings.LANGUAGE_CODE)
            default_language = get_untranslated_default_language()
            if not published_language == default_language:
                page_instance.publish(default_language)
            return


    @receiver(post_placeholder_operation, dispatch_uid=b'cms_global_untranslated_placeholder_post_placeholder_operation')
    def post_ph_operation_handler(sender, operation, request, language, token, origin, **kwargs):
        plugin = None
        if operation == b'change_plugin':
            plugin = kwargs.get(b'new_plugin', None)
        if not plugin:
            plugin = kwargs.get(b'plugin', None)
        if not plugin:
            plugin = kwargs.get(b'plugins', [None])[0]
        if plugin:
            placeholder = plugin.placeholder
            if not plugin.language == language:
                if placeholder.page:
                    title = placeholder.page.get_title_obj(language)
                    title.publisher_state = PUBLISHER_STATE_DIRTY
                    title.save()
        return