# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/Envs/djangoplus/lib/python3.7/site-packages/djangoplus/ui/components/navigation/breadcrumbs.py
# Compiled at: 2019-04-14 09:38:41
# Size of source mod 2**32: 1663 bytes
from djangoplus.ui.components import Component
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from djangoplus.utils.http import httprr

class Breadcrumbs(Component):
    __doc__ = 'Used in the dashboard to show the sequence of pages the user has visited'

    def __init__(self, request, view_title):
        super(Breadcrumbs, self).__init__('breadcrumbs', request)
        self.referrer = None
        if view_title:
            path = request.get_full_path()
            is_popup = 'popup=1' in path
            is_csv = 'export=csv' in path
            is_static = path.startswith('/static/')
            is_media = path.startswith('/media/')
            if not (is_popup or is_csv):
                if not is_static:
                    if not is_media:
                        if 'stack' not in request.session:
                            request.session['stack'] = []
                        else:
                            stack = request.session['stack']
                            count = 0
                            index = len(stack)
                            while index:
                                index -= 1
                                title, url = stack[index]
                                if view_title == title:
                                    count = len(stack) - index
                                    break

                            while count:
                                stack.pop()
                                count -= 1

                            if stack:
                                title, url = stack[(-1)]
                                request.REFERRER = url
                            else:
                                request.REFERRER = path
                        stack.append((view_title, path))
                        request.session.save()
                        self.referrer = len(stack) > 1 and stack[(-2)][1]