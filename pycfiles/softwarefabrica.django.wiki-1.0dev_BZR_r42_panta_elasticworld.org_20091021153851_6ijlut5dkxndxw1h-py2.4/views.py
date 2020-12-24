# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/wiki/views.py
# Compiled at: 2009-01-08 09:11:51
from django.shortcuts import get_object_or_404
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django import forms
from softwarefabrica.django.forms import extended
from django.utils.translation import ugettext_lazy as _
from softwarefabrica.django.utils.viewshelpers import render_to_response
from softwarefabrica.django.wiki.models import *

class PageForm(extended.ModelForm):
    __module__ = __name__

    class Meta:
        __module__ = __name__
        model = Page


class PageContentForm(extended.ModelForm):
    __module__ = __name__
    text = forms.CharField(widget=forms.widgets.Textarea(attrs={'class': 'page-text', 'cols': 72, 'rows': 30}))

    class Meta:
        __module__ = __name__
        model = PageContent
        exclude = ('page', 'rev')


def v_wikipage(request, wikiname=None, pagename=None, template_name='wiki/page_detail.html'):
    """WikiPage view."""
    wiki = get_object_or_404(Wiki, fullname_url_cache=wikiname)
    try:
        instance = Page.objects.get(wiki=wiki, name=pagename)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('wiki-page-create-named', kwargs={'wikiname': wikiname, 'pagename': pagename}))

    rev = request.GET.get('rev', None)
    context = {'wiki': wiki, 'page': instance, 'content': instance.get_content(rev=rev), 'name': instance and instance.name or pagename, 'has_nav': instance.prev or instance.up or instance.next}
    if request.GET.has_key('format'):
        format = request.GET['format']
        if format == 'text':
            return render_to_response(request, 'wiki/page_detail_txt.txt', context, mimetype='text/plain')
        elif format == 'html':
            return render_to_response(request, 'wiki/page_detail_html.html', context, mimetype='text/plain')
    return render_to_response(request, template_name, context)


def v_wikipage_edit(request, wikiname=None, page_id=None, pagename=None, create=False, template_name='wiki/page_edit.html'):
    """WikiPage create/update."""
    assert page_id or pagename or create
    wiki = get_object_or_404(Wiki, fullname_url_cache=wikiname)
    instance = None
    if create:
        if pagename:
            try:
                instance = Page.objects.get(wiki=wiki, name=pagename)
            except ObjectDoesNotExist:
                pass

    elif page_id is not None:
        instance = get_object_or_404(Page, pk=page_id)
    elif pagename:
        instance = get_object_or_404(Page, wiki=wiki, name=pagename)
    content = None
    content_form = None
    if instance:
        content = instance.get_content()
    content_form = PageContentForm(request.POST or None, request.FILES or None, instance=content)
    initial = None
    if create:
        initial = {'wiki': wiki.uuid, 'name': pagename}
    form = PageForm(request.POST or None, request.FILES or None, initial=initial, instance=instance)
    if request.method == 'POST' and form.is_valid():
        instance = form.save()
        if content_form and content_form.is_valid():
            old_content = content and content.uuid and PageContent.objects.get(uuid=content.uuid)
            content = content_form.save(commit=False)
            content.page = instance
            if old_content:
                content.uuid = None
                content.created = None
                content.rev = old_content.rev + 1
            if old_content is None or not content.same_content(old_content):
                content.save()
        return HttpResponseRedirect(instance.get_absolute_url())
    return render_to_response(request, template_name, {'wiki': wiki, 'page': instance, 'content': content, 'name': instance and instance.name or pagename, 'form': form, 'content_form': content_form, 'create': create and not instance, 'change': not create and instance})


def v_search(request, template_name='wiki/search_results.html'):
    from softwarefabrica.django.utils import usearch
    query_string = ''
    found_wikis = None
    found_pages = None
    found_pagecontents = None
    if 'q' in request.GET and request.GET['q'].strip():
        query_string = request.GET['q']
        wiki_query = usearch.get_query(query_string, ['name', 'desc', 'long_desc'])
        page_query = usearch.get_query(query_string, ['name', 'desc'])
        pagecontent_query = usearch.get_query(query_string, ['title', 'text', 'page__name', 'page__desc'])
        found_wikis = Wiki.objects.filter(wiki_query).order_by('-created')
        found_pages = Page.objects.filter(page_query).order_by('-wiki', '-created')
        found_pagecontents = PageContent.objects.filter(pagecontent_query).order_by('-page', '-created', '-rev')
    return render_to_response(request, template_name, {'query_string': query_string, 'wikis': found_wikis, 'pages': found_pages, 'pagecontents': found_pagecontents})