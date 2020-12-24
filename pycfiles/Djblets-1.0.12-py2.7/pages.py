# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/configforms/pages.py
# Compiled at: 2019-06-12 01:17:17
"""Base support for configuration pages."""
from __future__ import unicode_literals
from django.template.context import RequestContext
from djblets.util.compat.django.template.loader import render_to_string

class ConfigPage(object):
    """Base class for a page of configuration forms.

    Each ConfigPage is represented in the main page by an entry in the
    navigation sidebar. When the user has navigated to that page, all visible
    :py:class:`djblets.configforms.forms.ConfigPageForm` subclasses owned by
    the ConfigPage will be displayed.
    """
    page_id = None
    page_title = None
    form_classes = None
    template_name = b'configforms/config_page.html'

    def __init__(self, config_view, request, user):
        """Initialize the page.

        Args:
            config_view (ConfigPagesView):
                The view that manages this ConfigPage.

            request (HttpRequest):
                The HTTP request from the client.

            user (User):
                The user who is viewing the page.
        """
        self.config_view = config_view
        self.request = request
        self.forms = [ form for form in (form_cls(self, request, user) for form_cls in self.form_classes) if form.is_visible()
                     ]

    def is_visible(self):
        """Return whether the page should be visible.

        Visible pages are shown in the sidebar and can be navigated to.

        By default, a page is visible if at least one of its forms are
        also visible.

        Returns:
            bool:
                ``True`` if the page will be rendered, or ``False`` otherwise.
        """
        for form in self.forms:
            if form.is_visible():
                return True

        return False

    def render(self):
        """Render the page to a string.

        :py:attr:`template_name` will be used to render the page. The
        template will be passed ``page`` (this page's instance) and
        ``forms`` (the list of :py:class:`ConfigPageForm` instances to
        render).

        Subclasses can override this to provide additional rendering logic.

        Returns:
            unicode: The rendered page as HTML.
        """
        return render_to_string(template_name=self.template_name, context={b'page': self, 
           b'forms': self.forms}, request=self.request)