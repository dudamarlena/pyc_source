# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/comments/views/comments.py
# Compiled at: 2018-07-11 18:15:30
from __future__ import absolute_import
from django import http
from django.conf import settings
from django.contrib import comments
from django.contrib.comments import signals
from django.contrib.comments.views.utils import next_redirect, confirmation_view
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.html import escape
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST

class CommentPostBadRequest(http.HttpResponseBadRequest):
    """
    Response returned when a comment post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """

    def __init__(self, why):
        super(CommentPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string('comments/400-debug.html', {'why': why})


@csrf_protect
@require_POST
def post_comment(request, next=None, using=None):
    """
    Post a comment.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    data = request.POST.copy()
    if request.user.is_authenticated():
        if not data.get('name', ''):
            data['name'] = request.user.get_full_name() or request.user.get_username()
        if not data.get('email', ''):
            data['email'] = request.user.email
    ctype = data.get('content_type')
    object_pk = data.get('object_pk')
    if ctype is None or object_pk is None:
        return CommentPostBadRequest('Missing content_type or object_pk field.')
    else:
        try:
            model = models.get_model(*ctype.split('.', 1))
            target = model._default_manager.using(using).get(pk=object_pk)
        except TypeError:
            return CommentPostBadRequest('Invalid content_type value: %r' % escape(ctype))
        except AttributeError:
            return CommentPostBadRequest('The given content-type %r does not resolve to a valid model.' % escape(ctype))
        except ObjectDoesNotExist:
            return CommentPostBadRequest('No object matching content-type %r and object PK %r exists.' % (
             escape(ctype), escape(object_pk)))
        except (ValueError, ValidationError) as e:
            return CommentPostBadRequest('Attempting go get content-type %r and object PK %r exists raised %s' % (
             escape(ctype), escape(object_pk), e.__class__.__name__))

        preview = 'preview' in data
        form = comments.get_form()(target, data=data)
        if form.security_errors():
            return CommentPostBadRequest('The comment form failed security verification: %s' % escape(str(form.security_errors())))
        if form.errors or preview:
            template_list = [
             'comments/%s_%s_preview.html' % (model._meta.app_label, model._meta.module_name),
             'comments/%s_preview.html' % model._meta.app_label,
             'comments/%s/%s/preview.html' % (model._meta.app_label, model._meta.module_name),
             'comments/%s/preview.html' % model._meta.app_label,
             'comments/preview.html']
            return render_to_response(template_list, {'comment': form.data.get('comment', ''), 
               'form': form, 
               'next': data.get('next', next)}, RequestContext(request, {}))
        comment = form.get_comment_object()
        comment.ip_address = request.META.get('REMOTE_ADDR', None)
        if request.user.is_authenticated():
            comment.user = request.user
        responses = signals.comment_will_be_posted.send(sender=comment.__class__, comment=comment, request=request)
        for receiver, response in responses:
            if response == False:
                return CommentPostBadRequest('comment_will_be_posted receiver %r killed the comment' % receiver.__name__)

        comment.save()
        signals.comment_was_posted.send(sender=comment.__class__, comment=comment, request=request)
        return next_redirect(request, fallback=next or 'comments-comment-done', c=comment._get_pk_val())


comment_done = confirmation_view(template='comments/posted.html', doc='Display a "comment was posted" success page.')