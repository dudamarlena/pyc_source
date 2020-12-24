# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_contenttypes/djinn_contenttypes/views/share.py
# Compiled at: 2015-11-13 09:19:04
from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _
from djinn_contenttypes.views.base import CTMixin, MimeTypeMixin
from djinn_contenttypes.forms.share import ShareForm
from pgtimeline.models import QueuedActivity
from pgevents.events import Events
from pgevents.settings import RETWEET_CONTENTITEM, RETWEET_ACTIVITY

class ShareView(MimeTypeMixin, FormView, CTMixin):
    """Share the given content with other users or groups. This will
    result in a notification to the users/groups. The share form is
    shown in a modal window.
    """
    template_name = 'djinn_contenttypes/snippets/share.html'
    form_class = ShareForm
    success_url = '#'
    notification_type = RETWEET_CONTENTITEM
    content_type = 'text/plain'

    @property
    def page_title(self):
        return _('share %(obj)s with:') % {'obj': self.obj}

    @property
    def share_url(self):
        return self.request.path

    @property
    def recipient_value(self):
        form = self.get_form(self.form_class)
        return form.data.get('recipient')

    def render_recipients(self):
        """ Render the separate radio options of the recipient field """
        form = self.get_form(self.form_class)
        recipient = form.fields['recipient']
        value = form.data.get('recipient')
        options = []
        for opt in recipient.widget.get_renderer('recipient', ''):
            opt.value = value
            options.append(opt)

        return [ option.render(value=value) for option in options ]

    @property
    def obj(self):
        """ Accessor for object, keeping the object in a variable """
        if not hasattr(self, '_obj'):
            self._obj = self.get_object()
        return self._obj

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form), status=202)

    def form_valid(self, form):
        if form.cleaned_data['recipient'] == 'followers':
            Events.send(self.notification_type, user=self.request.user, content_item=self.get_object(), message=form.cleaned_data['message'])
        elif form.cleaned_data['recipient'] == 'group':
            for group in form.cleaned_data['group']:
                Events.send(self.notification_type, user=self.request.user, to_usergroup=group.usergroup, content_item=self.get_object(), message=form.cleaned_data['message'])

        elif form.cleaned_data['recipient'] == 'user':
            for user in form.cleaned_data['user']:
                Events.send(self.notification_type, user=self.request.user, to_user=user.user, content_item=self.get_object(), message=form.cleaned_data['message'])

        return super(ShareView, self).form_valid(form)


class ShareActivityView(ShareView):
    notification_type = RETWEET_ACTIVITY

    @property
    def page_title(self):
        return _('Share this message with:')

    def get_object(self, queryset=None):
        return QueuedActivity.objects.get(pk=self.kwargs['activity_id'])