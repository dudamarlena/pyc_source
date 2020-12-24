# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/maluki/blog/django_blog/blog_project/contact/views.py
# Compiled at: 2019-07-25 09:23:44
# Size of source mod 2**32: 333 bytes
from django.views.generic.edit import FormView
from contact.forms import ContactForm

class ContactView(FormView):
    template_name = 'contact/contact.html'
    form_class = ContactForm
    success_url = '/contact'

    def form_valid(self, form):
        form.send_email()
        return super(ContactView, self).form_valid(form)