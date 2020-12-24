# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hedley/django/instances/foundry/src/jmbo-twitter/jmbo_twitter/templatetags/jmbo_twitter_tags.py
# Compiled at: 2013-09-27 03:42:28
import re
from django import template
from django.utils.html import urlize
register = template.Library()

@register.filter(name='tweetify')
def tweetify(value):
    s = urlize(value)
    s = re.sub('(@[\\w]+)', '<a href="http://twitter.com/\\g<1>">\\g<1></a>', s)
    return s