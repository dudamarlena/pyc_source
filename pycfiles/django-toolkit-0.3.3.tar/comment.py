# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/forms/comment.py
# Compiled at: 2013-12-12 20:55:32
from django import forms
from django.contrib.comments.models import COMMENT_MAX_LENGTH, Comment
from django.contrib.comments.signals import comment_was_posted
from django.utils import timezone
from django.conf import settings

class AddCommentFormMixin(forms.Form):
    """
    Adds a 'add_comment' field to the form with a helper to save the comment.
    
    The form must hav ea 
    """
    add_comment = forms.CharField(widget=forms.Textarea, max_length=COMMENT_MAX_LENGTH, help_text='Add a comment.', required=False)

    def __init__(self, *args, **kwargs):
        if 'request' not in kwargs:
            raise AttributeError('AddCommentFormMixin.__init__() expects request to be in kwargs.')
        self.request = kwargs.get('request')
        del kwargs['request']
        super(AddCommentFormMixin, self).__init__(*args, **kwargs)

    def save_comment(self, object):
        if 'add_comment' in self.cleaned_data and len(self.cleaned_data['add_comment']) > 0:
            comment = Comment.objects.create(user=self.request.user, content_object=object, comment=self.cleaned_data['add_comment'], submit_date=timezone.now(), site_id=settings.SITE_ID, is_public=True, ip_address=self.request.META.get('REMOTE_ADDR', None), is_removed=False)
            comment_was_posted.send(sender=comment.__class__, comment=comment, request=self.request)
        return