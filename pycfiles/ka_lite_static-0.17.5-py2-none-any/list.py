# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/views/generic/list.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import unicode_literals
from django.core.paginator import Paginator, InvalidPage
from django.core.exceptions import ImproperlyConfigured
from django.http import Http404
from django.utils.translation import ugettext as _
from django.views.generic.base import TemplateResponseMixin, ContextMixin, View

class MultipleObjectMixin(ContextMixin):
    """
    A mixin for views manipulating multiple objects.
    """
    allow_empty = True
    queryset = None
    model = None
    paginate_by = None
    context_object_name = None
    paginator_class = Paginator
    page_kwarg = b'page'

    def get_queryset(self):
        """
        Get the list of items for this view. This must be an iterable, and may
        be a queryset (in which qs-specific behavior will be enabled).
        """
        if self.queryset is not None:
            queryset = self.queryset
            if hasattr(queryset, b'_clone'):
                queryset = queryset._clone()
        elif self.model is not None:
            queryset = self.model._default_manager.all()
        else:
            raise ImproperlyConfigured(b"'%s' must define 'queryset' or 'model'" % self.__class__.__name__)
        return queryset

    def paginate_queryset(self, queryset, page_size):
        """
        Paginate the queryset, if needed.
        """
        paginator = self.get_paginator(queryset, page_size, allow_empty_first_page=self.get_allow_empty())
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        try:
            page_number = int(page)
        except ValueError:
            if page == b'last':
                page_number = paginator.num_pages
            else:
                raise Http404(_(b"Page is not 'last', nor can it be converted to an int."))

        try:
            page = paginator.page(page_number)
            return (paginator, page, page.object_list, page.has_other_pages())
        except InvalidPage as e:
            raise Http404(_(b'Invalid page (%(page_number)s): %(message)s') % {b'page_number': page_number, 
               b'message': str(e)})

    def get_paginate_by(self, queryset):
        """
        Get the number of items to paginate by, or ``None`` for no pagination.
        """
        return self.paginate_by

    def get_paginator(self, queryset, per_page, orphans=0, allow_empty_first_page=True):
        """
        Return an instance of the paginator for this view.
        """
        return self.paginator_class(queryset, per_page, orphans=orphans, allow_empty_first_page=allow_empty_first_page)

    def get_allow_empty(self):
        """
        Returns ``True`` if the view should display empty lists, and ``False``
        if a 404 should be raised instead.
        """
        return self.allow_empty

    def get_context_object_name(self, object_list):
        """
        Get the name of the item to be used in the context.
        """
        if self.context_object_name:
            return self.context_object_name
        else:
            if hasattr(object_list, b'model'):
                return b'%s_list' % object_list.model._meta.object_name.lower()
            else:
                return

            return

    def get_context_data(self, **kwargs):
        """
        Get the context for this view.
        """
        queryset = kwargs.pop(b'object_list')
        page_size = self.get_paginate_by(queryset)
        context_object_name = self.get_context_object_name(queryset)
        if page_size:
            paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
            context = {b'paginator': paginator, 
               b'page_obj': page, 
               b'is_paginated': is_paginated, 
               b'object_list': queryset}
        else:
            context = {b'paginator': None, b'page_obj': None, 
               b'is_paginated': False, 
               b'object_list': queryset}
        if context_object_name is not None:
            context[context_object_name] = queryset
        context.update(kwargs)
        return super(MultipleObjectMixin, self).get_context_data(**context)


class BaseListView(MultipleObjectMixin, View):
    """
    A base view for displaying a list of objects.
    """

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        allow_empty = self.get_allow_empty()
        if not allow_empty:
            if self.get_paginate_by(self.object_list) is not None and hasattr(self.object_list, b'exists'):
                is_empty = not self.object_list.exists()
            else:
                is_empty = len(self.object_list) == 0
            if is_empty:
                raise Http404(_(b"Empty list and '%(class_name)s.allow_empty' is False.") % {b'class_name': self.__class__.__name__})
        context = self.get_context_data(object_list=self.object_list)
        return self.render_to_response(context)


class MultipleObjectTemplateResponseMixin(TemplateResponseMixin):
    """
    Mixin for responding with a template and list of objects.
    """
    template_name_suffix = b'_list'

    def get_template_names(self):
        """
        Return a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """
        try:
            names = super(MultipleObjectTemplateResponseMixin, self).get_template_names()
        except ImproperlyConfigured:
            names = []

        if hasattr(self.object_list, b'model'):
            opts = self.object_list.model._meta
            names.append(b'%s/%s%s.html' % (opts.app_label, opts.object_name.lower(), self.template_name_suffix))
        return names


class ListView(MultipleObjectTemplateResponseMixin, BaseListView):
    """
    Render some list of objects, set by `self.model` or `self.queryset`.
    `self.queryset` can actually be any iterable of items, not just a queryset.
    """
    pass