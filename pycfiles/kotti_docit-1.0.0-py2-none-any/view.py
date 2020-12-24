# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_docit/kotti_docit/views/view.py
# Compiled at: 2016-10-10 16:19:10
"""
Created on 2016-09-20
:author: Oshane Bailey (oshane@alteroo.com)
"""
from pyramid.view import view_config
from pyramid.view import view_defaults
from kotti_docit import _
from kotti_docit.resources import AdminManual
from kotti_docit.fanstatic import css_and_js
from kotti_docit.views import BaseView

@view_defaults(context=AdminManual, permission='manage')
class AdminManualViews(BaseView):
    """ Views for :class:`dpis_help.resources.CustomContent` """

    @view_config(name='view', permission='manage', renderer='kotti:templates/view/document.pt')
    def default_view(self):
        return {}