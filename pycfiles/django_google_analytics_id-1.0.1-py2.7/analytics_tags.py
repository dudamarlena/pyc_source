# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\analytics\templatetags\analytics_tags.py
# Compiled at: 2017-04-02 21:01:37
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
register = template.Library()

@register.simple_tag()
def google_analytics(google_analytics_id=None):
    """ Generate google analytics code ready for including to a template """
    is_disabled = getattr(settings, 'DISABLE_GOOGLE_ANALYTICS', None)
    if is_disabled:
        return ''
    else:
        if google_analytics_id is None:
            google_analytics_id = getattr(settings, 'GOOGLE_ANALYTICS_ID')
        else:
            google_analytics_id = getattr(settings, google_analytics_id, google_analytics_id)
        return mark_safe("<script>\n      (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){\n      (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),\n      m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)\n      })(window,document,'script','https://www.google-analytics.com/analytics.js','ga');\n\n      ga('create', '%s', 'auto');\n      ga('send', 'pageview');\n\n    </script>\n" % google_analytics_id)