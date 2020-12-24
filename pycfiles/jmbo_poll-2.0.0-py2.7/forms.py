# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/poll/forms.py
# Compiled at: 2015-04-21 15:32:20
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.dispatch import Signal
from secretballot.views import vote
from jmbo.forms import as_div
from poll.models import PollOption
from poll.widgets import RadioSelect
poll_voted = Signal(providing_args=['poll_option', 'request'])

class PollVoteForm(forms.Form):
    poll_option = forms.ChoiceField(choices=[], required=True, widget=RadioSelect)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.poll = kwargs.pop('poll')
        super(PollVoteForm, self).__init__(*args, **kwargs)
        self.fields['poll_option'].label = ''
        self.fields['poll_option'].choices = [ (o.id, o.title) for o in self.poll.polloption_set.all() ]

    def clean(self):
        if not self.poll.can_vote(self.request):
            raise forms.ValidationError(_('You are not allowed to vote on this poll.'))
        return super(PollVoteForm, self).clean()

    def save(self):
        poll_option = self.cleaned_data['poll_option']
        content_type = ContentType.objects.get(app_label='poll', model='polloption')
        vote(self.request, content_type, poll_option, 1)
        poll_voted.send(sender=self.__class__, poll_option=poll_option, request=self.request)

    as_div = as_div