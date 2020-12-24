# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/django_ginger/ginger/templatetags/allauth_tags.py
# Compiled at: 2015-05-19 09:09:08
# Size of source mod 2**32: 842 bytes
from ginger.template.library import ginger_tag
try:
    from allauth.socialaccount import providers
except ImportError:
    pass
else:

    @ginger_tag(takes_context=True)
    def provider_login_url(context, provider_id, **query):
        provider = providers.registry.by_id(provider_id)
        request = context['request']
        if 'next' not in query:
            next = request.REQUEST.get('next')
            if next:
                query['next'] = next
        elif not query['next']:
            del query['next']
        return provider.get_login_url(request, **query)


    @ginger_tag(takes_context=True)
    def provider_media_js(context):
        request = context['request']
        ret = '\n'.join([p.media_js(request) for p in providers.registry.get_list()])
        return ret