# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/leotrubach/development/django-saas-email/venv/lib/python3.7/site-packages/django_saas_email/views.py
# Compiled at: 2018-10-24 06:32:38
# Size of source mod 2**32: 1534 bytes
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView, ListView
from .models import Mail, MailTemplate, Attachment, TemplateAttachment

class MailCreateView(CreateView):
    model = Mail


class MailDeleteView(DeleteView):
    model = Mail


class MailDetailView(DetailView):
    model = Mail


class MailUpdateView(UpdateView):
    model = Mail


class MailListView(ListView):
    model = Mail


class MailTemplateCreateView(CreateView):
    model = MailTemplate


class MailTemplateDeleteView(DeleteView):
    model = MailTemplate


class MailTemplateDetailView(DetailView):
    model = MailTemplate


class MailTemplateUpdateView(UpdateView):
    model = MailTemplate


class MailTemplateListView(ListView):
    model = MailTemplate


class AttachmentCreateView(CreateView):
    model = Attachment


class AttachmentDeleteView(DeleteView):
    model = Attachment


class AttachmentDetailView(DetailView):
    model = Attachment


class AttachmentUpdateView(UpdateView):
    model = Attachment


class AttachmentListView(ListView):
    model = Attachment


class TemplateAttachmentCreateView(CreateView):
    model = TemplateAttachment


class TemplateAttachmentDeleteView(DeleteView):
    model = TemplateAttachment


class TemplateAttachmentDetailView(DetailView):
    model = TemplateAttachment


class TemplateAttachmentUpdateView(UpdateView):
    model = TemplateAttachment


class TemplateAttachmentListView(ListView):
    model = TemplateAttachment