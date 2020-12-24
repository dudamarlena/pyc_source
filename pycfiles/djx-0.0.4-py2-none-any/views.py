# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/syndication/views.py
# Compiled at: 2019-02-14 00:35:17
from __future__ import unicode_literals
from calendar import timegm
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.template import TemplateDoesNotExist, loader
from django.utils import feedgenerator, six
from django.utils.encoding import force_text, iri_to_uri
from django.utils.html import escape
from django.utils.http import http_date
from django.utils.timezone import get_default_timezone, is_naive, make_aware

def add_domain(domain, url, secure=False):
    protocol = b'https' if secure else b'http'
    if url.startswith(b'//'):
        url = b'%s:%s' % (protocol, url)
    elif not url.startswith(('http://', 'https://', 'mailto:')):
        url = iri_to_uri(b'%s://%s%s' % (protocol, domain, url))
    return url


class FeedDoesNotExist(ObjectDoesNotExist):
    pass


class Feed(object):
    feed_type = feedgenerator.DefaultFeed
    title_template = None
    description_template = None

    def __call__(self, request, *args, **kwargs):
        try:
            obj = self.get_object(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404(b'Feed object does not exist.')

        feedgen = self.get_feed(obj, request)
        response = HttpResponse(content_type=feedgen.content_type)
        if hasattr(self, b'item_pubdate') or hasattr(self, b'item_updateddate'):
            response[b'Last-Modified'] = http_date(timegm(feedgen.latest_post_date().utctimetuple()))
        feedgen.write(response, b'utf-8')
        return response

    def item_title(self, item):
        return escape(force_text(item))

    def item_description(self, item):
        return force_text(item)

    def item_link(self, item):
        try:
            return item.get_absolute_url()
        except AttributeError:
            raise ImproperlyConfigured(b'Give your %s class a get_absolute_url() method, or define an item_link() method in your Feed class.' % item.__class__.__name__)

    def item_enclosures(self, item):
        enc_url = self._get_dynamic_attr(b'item_enclosure_url', item)
        if enc_url:
            enc = feedgenerator.Enclosure(url=force_text(enc_url), length=force_text(self._get_dynamic_attr(b'item_enclosure_length', item)), mime_type=force_text(self._get_dynamic_attr(b'item_enclosure_mime_type', item)))
            return [
             enc]
        return []

    def _get_dynamic_attr(self, attname, obj, default=None):
        try:
            attr = getattr(self, attname)
        except AttributeError:
            return default

        if callable(attr):
            try:
                code = six.get_function_code(attr)
            except AttributeError:
                code = six.get_function_code(attr.__call__)

            if code.co_argcount == 2:
                return attr(obj)
            return attr()
        return attr

    def feed_extra_kwargs(self, obj):
        """
        Returns an extra keyword arguments dictionary that is used when
        initializing the feed generator.
        """
        return {}

    def item_extra_kwargs(self, item):
        """
        Returns an extra keyword arguments dictionary that is used with
        the `add_item` call of the feed generator.
        """
        return {}

    def get_object(self, request, *args, **kwargs):
        return

    def get_context_data(self, **kwargs):
        """
        Returns a dictionary to use as extra context if either
        ``self.description_template`` or ``self.item_template`` are used.

        Default implementation preserves the old behavior
        of using {'obj': item, 'site': current_site} as the context.
        """
        return {b'obj': kwargs.get(b'item'), b'site': kwargs.get(b'site')}

    def get_feed(self, obj, request):
        """
        Returns a feedgenerator.DefaultFeed object, fully populated, for
        this feed. Raises FeedDoesNotExist for invalid parameters.
        """
        current_site = get_current_site(request)
        link = self._get_dynamic_attr(b'link', obj)
        link = add_domain(current_site.domain, link, request.is_secure())
        feed = self.feed_type(title=self._get_dynamic_attr(b'title', obj), subtitle=self._get_dynamic_attr(b'subtitle', obj), link=link, description=self._get_dynamic_attr(b'description', obj), language=settings.LANGUAGE_CODE, feed_url=add_domain(current_site.domain, self._get_dynamic_attr(b'feed_url', obj) or request.path, request.is_secure()), author_name=self._get_dynamic_attr(b'author_name', obj), author_link=self._get_dynamic_attr(b'author_link', obj), author_email=self._get_dynamic_attr(b'author_email', obj), categories=self._get_dynamic_attr(b'categories', obj), feed_copyright=self._get_dynamic_attr(b'feed_copyright', obj), feed_guid=self._get_dynamic_attr(b'feed_guid', obj), ttl=self._get_dynamic_attr(b'ttl', obj), **self.feed_extra_kwargs(obj))
        title_tmp = None
        if self.title_template is not None:
            try:
                title_tmp = loader.get_template(self.title_template)
            except TemplateDoesNotExist:
                pass

        description_tmp = None
        if self.description_template is not None:
            try:
                description_tmp = loader.get_template(self.description_template)
            except TemplateDoesNotExist:
                pass

        for item in self._get_dynamic_attr(b'items', obj):
            context = self.get_context_data(item=item, site=current_site, obj=obj, request=request)
            if title_tmp is not None:
                title = title_tmp.render(context, request)
            else:
                title = self._get_dynamic_attr(b'item_title', item)
            if description_tmp is not None:
                description = description_tmp.render(context, request)
            else:
                description = self._get_dynamic_attr(b'item_description', item)
            link = add_domain(current_site.domain, self._get_dynamic_attr(b'item_link', item), request.is_secure())
            enclosures = self._get_dynamic_attr(b'item_enclosures', item)
            author_name = self._get_dynamic_attr(b'item_author_name', item)
            if author_name is not None:
                author_email = self._get_dynamic_attr(b'item_author_email', item)
                author_link = self._get_dynamic_attr(b'item_author_link', item)
            else:
                author_email = author_link = None
            tz = get_default_timezone()
            pubdate = self._get_dynamic_attr(b'item_pubdate', item)
            if pubdate and is_naive(pubdate):
                pubdate = make_aware(pubdate, tz)
            updateddate = self._get_dynamic_attr(b'item_updateddate', item)
            if updateddate and is_naive(updateddate):
                updateddate = make_aware(updateddate, tz)
            feed.add_item(title=title, link=link, description=description, unique_id=self._get_dynamic_attr(b'item_guid', item, link), unique_id_is_permalink=self._get_dynamic_attr(b'item_guid_is_permalink', item), enclosures=enclosures, pubdate=pubdate, updateddate=updateddate, author_name=author_name, author_email=author_email, author_link=author_link, categories=self._get_dynamic_attr(b'item_categories', item), item_copyright=self._get_dynamic_attr(b'item_copyright', item), **self.item_extra_kwargs(item))

        return feed