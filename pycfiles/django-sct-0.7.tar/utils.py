# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/sphblog/utils.py
# Compiled at: 2012-03-17 12:42:14
import re, unicodedata
from htmlentitydefs import name2codepoint
from django.utils.encoding import smart_unicode, force_unicode
from slughifi import slughifi

def slugify(s, entities=True, decimal=True, hexadecimal=True, model=None, slug_field='slug', pk=None):
    s = smart_unicode(s)
    if len(s) > 40:
        s = s[:40]
    s = slughifi(s)
    slug = s
    if model:

        def get_query():
            query = model.objects.filter(**{slug_field: slug})
            if pk:
                query = query.exclude(pk=pk)
            return query

        counter = 2
        while get_query():
            slug = '%s-%s' % (s, counter)
            counter += 1

    return slug