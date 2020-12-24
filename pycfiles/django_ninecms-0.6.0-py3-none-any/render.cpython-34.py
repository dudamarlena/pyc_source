# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gkarak/workspace/python/django-ninecms/ninecms/utils/render.py
# Compiled at: 2016-04-06 03:40:49
# Size of source mod 2**32: 6536 bytes
""" Node render utility functions """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.conf import settings
from django.views.generic import View
from django.db.models import Q
from django.http import HttpResponse
from django.template import loader
from django.utils.text import slugify
from ninecms.models import Node
from ninecms.signals import block_signal
from ninecms.forms import ContactForm, LoginForm, SearchForm

class NodeView(View):
    __doc__ = ' Basic page render functions\n    Base class for ContentNodeEditView, AliasView, IndexView\n    '

    def get_node_by_alias(self, alias, request):
        r""" Get a node given a path alias
        Query from the opposite direction: https://docs.djangoproject.com/en/1.7/topics/db/examples/many_to_one/
        The order -language returns first objects with language not empty and then with language empty (tested utf8)
        Prefetch related terms is not necessary if node.terms.all are not called in template (adds 1 query)
        But if terms are populated in template then this reduces the number of queries to 1 from 2
        Also .prefetch_related('terms__nodes')\ can be added if necessary
        Requires url alias in db without slashes
        :param alias: a url path alias
        :param request: the request object
        :return: a Node object
        """
        return Node.objects.filter(alias=alias).filter(language__in=(
         request.LANGUAGE_CODE, '')).select_related('page_type').order_by('-language', 'id')[0]

    def construct_classes(self, type_classes, request):
        """ Construct default body classes for a page
        :param type_classes: an individual page type name
        :param request: the request object
        :return: a classes string
        """
        classes = ' '.join(list('page-' + slugify(c) for c in type_classes))
        classes += ' i18n-' + request.LANGUAGE_CODE
        if request.user.is_authenticated():
            classes += ' logged-in'
        if request.user.is_superuser:
            classes += ' superuser'
        return classes

    def session_pop(self, request, key, default):
        """ Return the value of a session key if exists and pop it; otherwise return default
        :param request: request object
        :param key: the session key to pop if exists
        :param default: a default value if key not exists
        :return: session key or default value
        """
        if key in request.session:
            return request.session.pop(key)
        return default

    def construct_context(self, node, request):
        """ Construct the page context
        Render all blocks in a node page
        :param node: the node requested
        :param request: the request object
        :return: context dictionary
        """
        title = node.title if node.title == settings.SITE_NAME else ' | '.join((node.title, settings.SITE_NAME))
        status = 'published' if node.status else 'unpublished'
        page = {'title': title, 
         'classes': self.construct_classes((node.page_type.name, 'content', status), request), 
         'node': node, 
         'author': settings.SITE_AUTHOR, 
         'keywords': settings.SITE_KEYWORDS}
        for block in node.page_type.blocks.all():
            reg = slugify(block.name).replace('-', '_')
            if block.type == 'static':
                if block.node.language in (request.LANGUAGE_CODE, ''):
                    if block.node.status == 1:
                        page[reg] = block.node
            elif block.type == 'menu':
                if block.menu_item.language in (request.LANGUAGE_CODE, ''):
                    if block.menu_item.disabled == 0:
                        page[reg] = block.menu_item.get_descendants()
            elif block.type == 'signal':
                responses = block_signal.send(sender=self.__class__, view=block.signal, node=node, request=request)
                responses = list(filter(lambda response: response[1] is not None, responses))
                if responses:
                    page[reg] = responses[(-1)][1]
            elif block.type == 'contact':
                page[reg] = ContactForm(self.session_pop(request, 'contact_form_post', None), initial=request.GET)
            elif block.type == 'language':
                page[reg] = settings.LANGUAGE_MENU_LABELS
            elif block.type == 'login':
                page[reg] = LoginForm(self.session_pop(request, 'login_form_post', None))
            elif block.type == 'user-menu':
                page[reg] = True
            elif block.type == 'search':
                page[reg] = SearchForm(request.GET)
            elif block.type == 'search-results':
                form = SearchForm(request.GET)
                form.is_valid()
                results = None
                if 'q' in form.cleaned_data:
                    q = form.cleaned_data['q']
                    results = Node.objects.filter(Q(title__icontains=q) | Q(body__icontains=q) | Q(summary__icontains=q) | Q(highlight__icontains=q))
                    results = {'q': q,  'nodes': results}
                page[reg] = results
                continue

        return page

    def render(self, node, request):
        """
        Render shortcut function
        Select the proper template based on page type and construct context
        :param node: the node requested
        :param request: the request object
        :return: rendered http response
        """
        page_type_name = slugify(node.page_type.name).replace('-', '_')
        t = loader.select_template((
         'ninecms/page_%s.html' % page_type_name,
         'ninecms/%s.html' % page_type_name,
         'ninecms/index.html'))
        return HttpResponse(t.render(self.construct_context(node, request), request))