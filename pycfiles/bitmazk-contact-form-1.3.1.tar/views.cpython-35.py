# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/views.py
# Compiled at: 2016-04-11 03:10:24
# Size of source mod 2**32: 926 bytes
"""Views for bitmazk-contact-form application."""
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView
from .forms import AntiSpamContactForm

class ContactFormView(FormView):
    __doc__ = 'View class for the ``contact_form.ContactForm`` Form.'
    form_class = AntiSpamContactForm
    template_name = 'contact_form/contact_form.html'

    def form_valid(self, form):
        form.save()
        success_message = getattr(settings, 'CONTACT_FORM_SUCCESS_MESSAGE', _('Your request has been successfully submitted. We will get back to you as soon as posisble.'))
        messages.add_message(self.request, messages.SUCCESS, success_message)
        return self.render_to_response(self.get_context_data(form=form, success=True))