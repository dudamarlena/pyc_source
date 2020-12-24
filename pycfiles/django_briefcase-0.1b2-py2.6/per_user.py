# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\briefcase\views\per_user.py
# Compiled at: 2010-10-21 09:15:29
"""
Per-user document views, for example "my documents" etc.
"""
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from briefcase.views import document_list
from briefcase.models import Document

@login_required
def my_documents(request, **kwargs):
    """
    Renders a list of all documents added by current user.
    
    We need a User here, not an AnonymousUser, so the view is wrapped with
    login_required decorator.
    """
    queryset = Document.objects.filter(added_by=request.user)
    return document_list(request, queryset, 'briefcase/my_documents.html', **kwargs)


def documents_for_user(request, username=None, user_id=None, **kwargs):
    """
    Renders a list of documents added by a specific user.
    
    The user can be identified by his username or user_id. If both are 
    specified, username takes precedence.
    """
    if username is not None:
        queryset = Document.objects.filter(added_by__username=username)
    elif user_id is not None:
        queryset = Document.objects.filter(added_by_id=user_id)
    else:
        raise AttributeError(_('documents_for_user requires either username or user_id.'))
    return document_list(request, queryset, 'briefcase/documents_for_user.html', **kwargs)