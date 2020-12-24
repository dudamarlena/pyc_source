# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shuyucms/utils/urls.py
# Compiled at: 2016-06-02 20:19:56
from __future__ import unicode_literals
import re, unicodedata
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import resolve, reverse, get_script_prefix
from django.shortcuts import redirect
from future.builtins import str
try:
    from django.utils.encoding import smart_text
except ImportError:
    from django.utils.encoding import smart_unicode as smart_text

from django.utils.http import is_safe_url
from shuyucms.conf import settings
from shuyucms.utils.importing import import_dotted_path

def admin_url(model, url, object_id=None):
    """
    Returns the URL for the given model and admin url name.
    """
    opts = model._meta
    url = b'admin:%s_%s_%s' % (opts.app_label, opts.object_name.lower(), url)
    args = ()
    if object_id is not None:
        args = (
         object_id,)
    return reverse(url, args=args)


def home_slug():
    """
    Returns the slug arg defined for the ``home`` urlpattern, which
    is the definitive source of the ``url`` field defined for an
    editable homepage object.
    """
    prefix = get_script_prefix()
    slug = reverse(b'home')
    if slug.startswith(prefix):
        slug = b'/' + slug[len(prefix):]
    try:
        return resolve(slug).kwargs[b'slug']
    except KeyError:
        return slug


def slugify(s):
    """
    Loads the callable defined by the ``SLUGIFY`` setting, which defaults
    to the ``slugify_unicode`` function.
    """
    return import_dotted_path(settings.SLUGIFY)(s)


def slugify_unicode(s):
    """
    Replacement for Django's slugify which allows unicode chars in
    slugs, for URLs in Chinese, Russian, etc.
    Adopted from https://github.com/mozilla/unicode-slugify/
    """
    chars = []
    for char in str(smart_text(s)):
        cat = unicodedata.category(char)[0]
        if cat in b'LN' or char in b'-_~':
            chars.append(char)
        elif cat == b'Z':
            chars.append(b' ')

    return re.sub(b'[-\\s]+', b'-', (b'').join(chars).strip()).lower()


def unique_slug(queryset, slug_field, slug):
    """
    Ensures a slug is unique for the given queryset, appending
    an integer to its end until the slug is unique.
    """
    i = 0
    while True:
        if i > 0:
            if i > 1:
                slug = slug.rsplit(b'-', 1)[0]
            slug = b'%s-%s' % (slug, i)
        try:
            queryset.get(**{slug_field: slug})
        except ObjectDoesNotExist:
            break

        i += 1

    return slug


def next_url(request):
    """
    Returns URL to redirect to from the ``next`` param in the request.
    """
    next = request.REQUEST.get(b'next', b'')
    host = request.get_host()
    if next and is_safe_url(next, host=host):
        return next
    else:
        return


def login_redirect(request):
    """
    Returns the redirect response for login/signup. Favors:
    - next param
    - homepage
    """
    next = next_url(request) or b''
    if next in ('', ):
        next = b'/'
    return redirect(next)