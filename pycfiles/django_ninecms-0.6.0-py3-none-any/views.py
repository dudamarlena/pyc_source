# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /media/dev-p5qc/workspace/python/team_reset/ninecms/views.py
# Compiled at: 2015-04-06 10:06:39
""" View handler definitions for Nine CMS """
__author__ = 'George Karakostas'
__copyright__ = 'Copyright 2015, George Karakostas'
__licence__ = 'BSD-3'
__email__ = 'gkarak@9-dev.com'
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, ListView
from django.template import loader, RequestContext, TemplateDoesNotExist
from django.http import Http404
from django.db.models import Q
from django.conf import settings
from django.core.mail import mail_managers, BadHeaderError
from ninecms.models import Node, PageLayoutElement
from ninecms.signals import block_signal
from ninecms.forms import ContentNodeEditForm, ImageInlineFormset, ContactForm

class ContentView(ListView):
    """ Display a list of nodes under /cms/content """
    template_name = 'ninecms/content.html'
    context_object_name = 'node_list'

    def get_queryset(self):
        """ Return all nodes
        :return: QuerySet
        """
        return Node.objects.all()


class NodeView(View):
    """ Basic page render functions
    Base class for ContentNodeEditView, AliasView, IndexView
    """

    def get_node_by_alias(self, alias, request):
        r""" Get a node given a path alias
        Query from the opposite direction: https://docs.djangoproject.com/en/1.7/topics/db/examples/many_to_one/
        The order -language returns first objects with language not empty and then with language empty (tested utf8)
        Prefetch related terms is not necessary if node.terms.all are not called in template (adds 1 query)
        But if terms are populated in template then this reduces the number of queries to 1 from 2
        Also .prefetch_related('terms__nodes')\ can be added if necessary
        :param alias: a url path alias
        :param request: the request object
        :return: a Node object
        """
        return Node.objects.filter(urlalias__alias=alias).filter(Q(urlalias__language=request.LANGUAGE_CODE) | Q(language='')).prefetch_related('terms').order_by('-language')[0]

    def construct_classes(self, page_name, request):
        """ Construct default body classes for a page
        :param page_name: an individual page type name
        :param request: the request object
        :return: a classes string
        """
        classes = 'page-' + page_name
        classes += ' i18n-' + request.LANGUAGE_CODE
        if request.user.is_authenticated():
            classes += ' logged-in'
        if request.user.is_superuser:
            classes += ' superuser toolbar'
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
        else:
            return default

    def console_add(self, request, msg):
        """ Add a message to the console messages
        :param request: the request object
        :param msg: a list (alert type, the message to add)
        """
        if 'console' in request.session:
            request.session['console'].append(msg)
        else:
            request.session['console'] = (
             msg,)

    def block_render(self, template, region, specific, request, context_name, context_value):
        """ Render a block given a specific template
        Template name priorities: template_region_specific, template_specific, template_region, template
        :param template: block template
        :param region: the region of the block in order to provide specific template, if any
        :param specific: the id of the specific content in order to provide specific template, if any
        :param request: request object
        :param context_name: the name of the context
        :param context_value: the value for the context name
        :return: rendered block string for page render
        """
        specific = str(specific).replace(' ', '_')
        try:
            t = loader.get_template('ninecms/' + ('_').join(filter(None, (template, region, specific))) + '.html')
        except TemplateDoesNotExist:
            try:
                t = loader.get_template('ninecms/' + ('_').join(filter(None, (template, specific))) + '.html')
            except TemplateDoesNotExist:
                try:
                    t = loader.get_template('ninecms/' + ('_').join(filter(None, (template, region))) + '.html')
                except TemplateDoesNotExist:
                    t = loader.get_template('ninecms/' + template + '.html')

        c = RequestContext(request, {context_name: context_value})
        return t.render(c)

    def page_render(self, node, request):
        """ Construct the page context
        Render all blocks in a node page
        :param node: the node requested
        :param request: the request object
        :return: rendered page string for context
        """
        if node.title == settings.SITE_NAME:
            title = node.title
        else:
            title = (' | ').join((node.title, settings.SITE_NAME))
        page = {'title': title, 
           'classes': self.construct_classes(node.page_type.name, request), 
           'node': node, 
           'content': self.block_render('block_content', node.page_type.name, node.id, request, 'node', node), 
           'console': self.session_pop(request, 'console', None)}
        elements = PageLayoutElement.objects.select_related('block').select_related('block__node').select_related('block__menu_item').filter(page_type=node.page_type_id).order_by('region', 'weight')
        for element in elements:
            reg = element.region
            if reg not in page:
                page[reg] = ''
            if element.block.type == 'static':
                node = element.block.node
                if node.language in (request.LANGUAGE_CODE, '') and node.status == 1:
                    page[reg] += self.block_render('block_static', reg, node.id, request, 'node', node)
            elif element.block.type == 'menu':
                menu = element.block.menu_item
                if menu.language in (request.LANGUAGE_CODE, '') and menu.disabled == 0:
                    page[reg] += self.block_render('block_menu', reg, menu.id, request, 'menu', menu.get_children())
            elif element.block.type == 'signal':
                signal = element.block.signal
                responses = block_signal.send(sender=self.__class__, view=signal, request=request)
                responses = list(filter(lambda response: response[1] is not None, responses))
                if responses:
                    page[reg] += self.block_render('block_signal', reg, signal, request, 'content', responses[(-1)][1])
            elif element.block.type == 'contact':
                form = ContactForm(self.session_pop(request, 'contact_form_post', None))
                page[reg] += self.block_render('block_contact', reg, None, request, 'form', form)

        return page


class ContentNodeView(NodeView):
    """ Display a node as invoked by its node id from /cms/content/<node_id>
    If an alias exists then issue redirect to allow a single content page per URL
    """

    def get(self, request, **kwargs):
        """ HTML get for /cms/content/<node_id>
        :param request: the request object
        :param kwargs: contains node_id
        :return: response object
        """
        node = get_object_or_404(Node, id=kwargs['node_id'])
        try:
            alias = node.urlalias_set.filter(Q(language=request.LANGUAGE_CODE) | Q(language='')).order_by('-language')[0]
        except IndexError:
            return render(request, 'ninecms/index.html', self.page_render(node, request))

        return redirect('ninecms:alias', url_alias=alias.alias + '/', permanent=True)


class AliasView(NodeView):
    """ Render content based on Url Alias """

    def get(self, request, **kwargs):
        """ HTML get for /<url_alias>
        :param request: the request object
        :param kwargs: contains url_alias
        :return: response object
        """
        if kwargs['url_alias'][(-1)] == '/':
            alias = kwargs['url_alias'][:-1]
            if alias == '/':
                return redirect('ninecms:index', permanent=True)
            try:
                node = self.get_node_by_alias(alias, request)
            except IndexError:
                raise Http404

            return render(request, 'ninecms/index.html', self.page_render(node, request))
        else:
            return redirect('ninecms:alias', url_alias=kwargs['url_alias'] + '/', permanent=True)


class IndexView(NodeView):
    """ Render index at root / """

    def get(self, request):
        """ HTML get for /
        :param request: the request object
        :return: response object
        """
        try:
            node = self.get_node_by_alias('/', request)
        except IndexError:
            return render(request, 'ninecms/index.html', {'console': (('alert', 'No front page has been created yet.'), )})

        return render(request, 'ninecms/index.html', self.page_render(node, request))


class ContentNodeEditView(NodeView):
    """ Content edit form at /cms/content/<node_id>/edit """
    form_class = ContentNodeEditForm
    image_form_class = ImageInlineFormset

    def get(self, request, **kwargs):
        """ HTML get for /cms/content/<node_id>/edit
        :param request: the request object
        :param kwargs: contains node_id
        :return: response object
        """
        node = get_object_or_404(Node, id=kwargs['node_id'])
        form = self.form_class(instance=node)
        image_formset = self.image_form_class(instance=node, prefix='image')
        classes = self.construct_classes('node-edit-view ninecms', request)
        return render(request, 'ninecms/content_node_edit.html', {'form': form, 
           'image_formset': image_formset, 
           'node': node, 
           'classes': classes})

    def post(self, request, **kwargs):
        """ HTML post for /cms/content/<node_id>/edit
        :param request: the request object
        :param kwargs: contains node_id
        :return: response object
        """
        node = get_object_or_404(Node, id=kwargs['node_id'])
        form = self.form_class(request.POST, instance=node)
        image_formset = self.image_form_class(request.POST, request.FILES, instance=node, prefix='image')
        classes = self.construct_classes('node-edit-view ninecms', request)
        if form.is_valid() and image_formset.is_valid():
            form.save()
            image_formset.save()
            return redirect('ninecms:content')
        return render(request, 'ninecms/content_node_edit.html', {'form': form, 
           'image_formset': image_formset, 
           'node': node, 
           'classes': classes})


class ContentNodeAddView(NodeView):
    """ Content add form at /cms/content/add """
    form_class = ContentNodeEditForm
    image_form_class = ImageInlineFormset

    def get(self, request):
        """ HTML get for /cms/content/<node_id>/add
        :param request: the request object
        :return: response object
        """
        form = self.form_class()
        image_formset = self.image_form_class(prefix='image')
        classes = self.construct_classes('node-add-view ninecms', request)
        return render(request, 'ninecms/content_node_add.html', {'form': form, 
           'image_formset': image_formset, 
           'classes': classes})

    def post(self, request):
        """ HTML post for /cms/content/<node_id>/add
        :param request: the request object
        :return: response object
        """
        form = self.form_class(request.POST)
        image_formset = self.image_form_class(request.POST, request.FILES, prefix='image')
        classes = self.construct_classes('node-edit-view ninecms', request)
        if form.is_valid() and image_formset.is_valid():
            form.save()
            image_formset.save()
            return redirect('ninecms:content')
        return render(request, 'ninecms/content_node_add.html', {'form': form, 
           'image_formset': image_formset, 
           'classes': classes})


class ContactView(NodeView):
    """ Handle contact post request """
    form_class = ContactForm

    def post(self, request):
        """ Handle contact form send
        :param request: the request object
        :return: response object
        """
        form = self.form_class(request.POST)
        if form.is_valid():
            t = loader.get_template('ninecms/mail_contact.txt')
            c = RequestContext(request, {'sender_name': form.cleaned_data['sender_name'], 
               'sender_email': form.cleaned_data['sender_email'], 
               'message': form.cleaned_data['message']})
            try:
                mail_managers(form.cleaned_data['subject'], t.render(c))
            except BadHeaderError:
                self.console_add(request, ('danger', 'Contact form message has NOT been sent. Invalid header found.'))
            else:
                self.console_add(request, ('success', 'A message has been sent to the site using the contact form.'))

            return redirect(form.cleaned_data['redirect'])
        self.console_add(request, ('warning', 'Contact form message has NOT been sent. Please fill in all contact form fields.'))
        request.session['contact_form_post'] = request.POST
        return redirect(form.cleaned_data['redirect'])