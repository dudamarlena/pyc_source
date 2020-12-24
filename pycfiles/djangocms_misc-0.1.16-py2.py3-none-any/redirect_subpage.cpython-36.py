# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/benzkji/Development/open/djangocms-misc/djangocms_misc/basic/middleware/redirect_subpage.py
# Compiled at: 2018-07-27 08:00:56
# Size of source mod 2**32: 1271 bytes
from django.shortcuts import redirect

class RedirectFirstSubpageMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if getattr(request, 'current_page', None):
            the_page = request.current_page
            the_redirect = the_page.get_redirect()
            if view_func.__name__ == 'details':
                if 'slug' in view_kwargs:
                    if the_redirect == '/firstchild':
                        if getattr(request.current_page, 'get_child_pages', None):
                            subpages = request.current_page.get_child_pages()
                        else:
                            subpages = request.current_page.children.all()
                        if len(subpages):
                            return redirect((subpages[0].get_absolute_url()), permanent=True)