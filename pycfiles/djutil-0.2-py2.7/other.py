# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\other.py
# Compiled at: 2013-08-27 09:33:54
from __future__ import unicode_literals
import logging
from copy import copy
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class UserQuerysetLimitMixin(object):

    def get_queryset(self):
        return super(UserQuerysetLimitMixin, self).get_queryset().filter(user=self.request.user)


class UserObjectCreateMixin(object):

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(UserObjectCreateMixin, self).form_valid(form)


class PassUserToFormKwargsMixin(object):

    def get_form_kwargs(self):
        kwargs = super(PassUserToFormKwargsMixin, self).get_form_kwargs()
        kwargs[b'user'] = self.request.user
        return kwargs


class MultiFormMixin(object):
    """
    Adds handling of multiple/related forms
    """
    extra_form_classes = None

    def get_extra_form_classes(self):
        if self.extra_form_classes is None:
            return {}
        else:
            return copy(self.extra_form_classes)

    def get_extra_forms(self):
        if not hasattr(self, b'extra_forms'):
            self.extra_forms = {}
            for name, form_class in self.get_extra_form_classes().items():
                self.extra_forms[name] = form_class(prefix=name, **self.get_form_kwargs())

        return self.extra_forms

    def validate_forms(self, forms):
        """Invoke validation of all forms and then check validation status"""
        return all([ form.is_valid() for form in forms ])

    def get_context_data(self, **kwargs):
        ctx = super(MultiFormMixin, self).get_context_data(**kwargs)
        for name, form in self.get_extra_forms().items():
            ctx[(b'{}_form').format(name)] = form

        return ctx

    def post(self, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        extra_forms = self.get_extra_forms()
        extra_forms_valid = self.validate_forms(extra_forms.values())
        if form.is_valid() and extra_forms_valid:
            return self.form_valid(form, extra_forms)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, extra_forms):
        return super(MultiFormMixin, self).form_valid(form)


class EmailMixin(object):
    email_subject_template = None
    email_message_template = None

    def mail_managers(self, context, from_email=None, fail_silently=False, connection=None):
        if not settings.MANAGERS:
            return
        to = [ a[1] for a in settings.MANAGERS ]
        return self._send_email(to, context, from_email=from_email, fail_silently=fail_silently, connection=connection)

    def mail_support(self, context, from_email=None, fail_silently=False, connection=None):
        if not settings.SUPPORT_EMAILS:
            return
        to = settings.SUPPORT_EMAILS
        return self._send_email(to, context, from_email=from_email, fail_silently=fail_silently, connection=connection)

    def _send_email(self, to, context, from_email=None, fail_silently=False, connection=None):
        subject = render_to_string(self.email_subject_template, context)
        subject = (b'').join(subject.splitlines())
        message = render_to_string(self.email_message_template, context)
        from_email = from_email if from_email else settings.SERVER_EMAIL
        mail = EmailMultiAlternatives(b'%s%s' % (settings.EMAIL_SUBJECT_PREFIX, subject), message, from_email, to, connection=connection)
        try:
            mail.send(fail_silently=fail_silently)
        except Exception as e:
            logging.getLogger(b'app.mixins.email').exception(b'Email sending failed', extra={b'extra': self.request})


from django.db.models import Q

def normalize_search_term(term):
    if term:
        return (b' ').join(term.strip().lower().split())
    return b''


def search_terms_to_query(search_terms, search_fields):
    """
    Naive search

    :type search_terms: str, unicode
    :param search_terms: query
    :param list search_fields: search_fields = ["name", "body"]
    """
    search_terms = normalize_search_term(search_terms)
    conditions = Q()
    parts = search_terms.split()
    for part in parts:
        condition = Q()
        for search_field in search_fields:
            condition |= Q(**{search_field + b'__icontains': part})

        conditions &= condition

    return conditions


def get_week_date_range(day):
    """
    :type day: datetime.datetime

    For given date and time returns week boundaries:
      - start date is monday 0:00
      - end date is monday 0:00 of next week

    >>> import pytz
    >>> from django.utils.timezone import localtime

    >>> time = datetime.datetime(2013, 07, 03, 11, 15, 33, tzinfo=pytz.utc)
    >>> get_week_date_range(time)
    (datetime.datetime(2013, 7, 1, 0, 0, tzinfo=<UTC>), datetime.datetime(2013, 7, 8, 0, 0, tzinfo=<UTC>))

    >>> time = localtime(datetime.datetime(2013, 07, 03, 11, 15, 33, tzinfo=pytz.utc), timezone=pytz.timezone("Europe/Zurich"))
    >>> get_week_date_range(time)
    (datetime.datetime(2013, 7, 1, 0, 0, tzinfo=<DstTzInfo 'Europe/Zurich' CEST+2:00:00 DST>), datetime.datetime(2013, 7, 8, 0, 0, tzinfo=<DstTzInfo 'Europe/Zurich' CEST+2:00:00 DST>))
    """
    monday = day - datetime.timedelta(days=day.isoweekday() - 1)
    next_monday = monday + datetime.timedelta(days=7)
    return (monday.replace(hour=0, minute=0, second=0, microsecond=0),
     next_monday.replace(hour=0, minute=0, second=0, microsecond=0))


def calendar_days_count(start_date, end_date):
    return (end_date.date() - start_date.date()).days + 1


def get_rel_calendar_day(start_date, n):
    return start_date + datetime.timedelta(days=n - 1)