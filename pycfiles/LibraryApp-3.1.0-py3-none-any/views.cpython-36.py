# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/Documents/LibraryApp/LibAppDjango/feedback/views.py
# Compiled at: 2019-07-24 10:35:27
# Size of source mod 2**32: 332 bytes
from django.views.generic.edit import FormView
from feedback.forms import FeedbackForm

class FeedbackView(FormView):
    template_name = 'feedback/contact.html'
    form_class = FeedbackForm
    success_url = '/'

    def form_valid(self, form):
        form.send_email()
        return super(FeedbackView, self).form_valid(form)