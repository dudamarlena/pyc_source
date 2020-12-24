# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/theme/context_processors.py
# Compiled at: 2020-02-26 14:47:58
# Size of source mod 2**32: 2052 bytes
from warnings import warn
from django.conf import settings
from tendenci.apps.theme.utils import get_active_theme, get_theme, is_builtin_theme, get_builtin_theme_dir, get_theme_info

def theme(request):
    context = {}
    if 'theme' in request.GET and request.user.profile.is_superuser:
        theme = request.GET.get('theme')
        if theme:
            request.session['theme'] = theme
    elif 'theme' in request.session:
        del request.session['theme']
    else:
        context['ACTIVE_THEME'] = get_active_theme()
        context['THEME'] = theme = get_theme(context['ACTIVE_THEME'])
        context['THEME_INFO'] = get_theme_info(theme)

        def warn_theme_urls(value):
            warn("{{ THEME_URL }}media/<path> is deprecated, use {% static '<path>' %} instead", DeprecationWarning)
            return value

        if is_builtin_theme(theme):
            theme_url = '%sthemes/%s/' % (settings.STATIC_URL, get_builtin_theme_dir(theme))

            def warn_theme_url(value=theme_url):
                return warn_theme_urls(value)

            context['THEME_URL'] = warn_theme_url
        else:
            if settings.USE_S3_STORAGE:
                theme_url = '%s/%s/%s/themes/%s/' % (
                 settings.S3_ROOT_URL, settings.AWS_STORAGE_BUCKET_NAME, settings.AWS_LOCATION, theme)

                def warn_theme_url(value=theme_url):
                    return warn_theme_urls(value)

                context['THEME_URL'] = warn_theme_url
            else:
                theme_url = '/themes/' + theme + '/'

        def warn_theme_url(value=theme_url):
            return warn_theme_urls(value)

        context['THEME_URL'] = warn_theme_url
    local_theme_url = '/themes/' + theme + '/'

    def warn_local_theme_url(value=local_theme_url):
        warn("{{ LOCAL_THEME_URL }}media/<path> is deprecated, use {% local_static '<path>' %} instead", DeprecationWarning)
        return value

    context['LOCAL_THEME_URL'] = warn_local_theme_url
    return context