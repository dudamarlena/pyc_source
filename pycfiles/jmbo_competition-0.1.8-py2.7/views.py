# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/competition/views.py
# Compiled at: 2013-10-10 08:50:08
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from competition.models import Competition, CompetitionPreferences
from competition.forms import CompetitionBaseEntryForm, SingleAnswerEntryForm, MultichoiceEntryForm, FileUploadEntryForm

def competition_terms(request, slug):
    competition = get_object_or_404(Competition.permitted, slug=slug)
    extra = {'title': _('Competition terms'), 'competition': competition}
    preferences = CompetitionPreferences.objects.all()
    if preferences:
        preferences = preferences[0]
        extra['preferences'] = preferences
    return render_to_response('competition/competition_terms.html', extra, context_instance=RequestContext(request))


def competition_detail(request, slug):
    competition = get_object_or_404(Competition.permitted, slug=slug)
    if competition.question and competition.answer_type:
        if competition.answer_type == 'free_text_input':
            form_class = SingleAnswerEntryForm
        elif competition.answer_type == 'multiple_choice_selection':
            form_class = MultichoiceEntryForm
        else:
            form_class = FileUploadEntryForm
    else:
        form_class = CompetitionBaseEntryForm
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, request=request, competition=competition)
        if form.is_valid():
            form.save()
            msg = _('You have entered the competition')
            messages.success(request, msg, fail_silently=True)
    else:
        form = form_class(request=request, competition=competition)
    extra = {'competition_entry_form': form, 'object': competition}
    return render_to_response('competition/competition_detail.html', extra, context_instance=RequestContext(request))