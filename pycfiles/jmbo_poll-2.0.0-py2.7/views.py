# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/poll/views.py
# Compiled at: 2015-04-21 15:32:20
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.contrib import messages
from poll.models import Poll
from poll.forms import PollVoteForm

def poll_vote(request, poll_id, template):
    poll = get_object_or_404(Poll, id=poll_id)
    if request.method == 'POST':
        form = PollVoteForm(request.POST, request=request, poll=poll)
        if form.is_valid():
            form.save()
            msg = _('Your vote has been saved')
            messages.success(request, msg, fail_silently=True)
        if template == 'poll/poll_widget.html' and not request.is_ajax():
            template = 'poll/poll_detail.html'
    else:
        form = PollVoteForm(request=request, poll=poll)
    extra = dict(form=form, object=poll, view_modifier=None)
    return render_to_response(template, extra, context_instance=RequestContext(request))