# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/kyle/git/flask-xxl/flask_xxl/apps/page/views.py
# Compiled at: 2018-06-20 18:52:33
from flask_xxl.baseviews import BaseView, ModelAPIView
import flask
from . import page
from .forms import TestForm, ContactUsForm
from .models import Page

class ContactFormView(BaseView):
    _template = 'contact.html'
    _form = ContactUsForm
    _context = {}

    def get(self):
        return self.render()

    def post(self):
        return self.render()


class PageSlugView(BaseView):
    _template = 'page.html'
    _context = {}

    def get(self, slug):
        file_name = None
        if slug.endswith('.html'):
            if slug in page.jinja_loader.list_templates():
                file_name = slug
            else:
                slug = slug.split('.html')[0]
                try:
                    url = flask.url_for('page.' + slug)
                    return self.redirect(url)
                except:
                    pass

        test = TestForm()
        content = ''
        page_name = ''
        if '.html' in slug:
            slug = slug.split('.html')[0]
        page = Page._session.query(Page).filter(Page.slug == slug).all()
        if page is not None:
            if type(page) == list and len(page) != 0:
                page = page[0]
            content = page.body_content
            template_file = page.template_file if getattr(page, 'template_file', False) and os.path.exists(page.template_file) else page.DEFAULT_TEMPLATE
            page_name = page.name
            title = page.title
            meta_title = page.meta_title
        elif file_name is not None:
            template_file = file_name
            title = slug
            meta_title = slug
        else:
            template_file = slug + '.html'
            title = slug
            meta_title = slug
        self._template = template_file
        self._context['content'] = content
        self._context['page_title'] = title
        self._context['page_name'] = page_name
        self._context['test'] = test
        return self.render()


class AddPageView(BaseView):
    pass


class PagesView(BaseView):
    pass