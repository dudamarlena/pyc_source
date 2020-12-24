# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/inviteme/views.py
# Compiled at: 2012-05-20 01:08:31
from django.conf import settings
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import render_to_response
from django.template import loader, Context, RequestContext
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_GET, require_POST
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from inviteme import signals, signed
from inviteme.utils import send_mail
from inviteme.models import ContactMail
from inviteme.forms import ContactMailForm
DEFAULT_FROM_EMAIL = getattr(settings, 'DEFAULT_FROM_EMAIL')
INVITEME_SALT = getattr(settings, 'INVITEME_SALT', '')

class ContactMailPostBadRequest(HttpResponseBadRequest):
    """
    Response returned when a post is invalid. If ``DEBUG`` is on a
    nice-ish error message will be displayed (for debugging purposes), but in
    production mode a simple opaque 400 page will be displayed.
    """

    def __init__(self, why):
        super(ContactMailPostBadRequest, self).__init__()
        if settings.DEBUG:
            self.content = render_to_string('inviteme/400-debug.html', {'why': why})


def send_confirmation_email(data, key, text_template='inviteme/confirmation_email.txt', html_template='inviteme/confirmation_email.html'):
    """
    Render message and send contact_mail confirmation email
    """
    site = Site.objects.get_current()
    subject = '[%s] %s' % (site.name, _('confirm invitation request'))
    confirmation_url = reverse('inviteme-confirm-mail', args=[key])
    message_context = Context({'data': data, 'confirmation_url': confirmation_url, 
       'support_email': DEFAULT_FROM_EMAIL, 
       'site': site})
    text_message_template = loader.get_template(text_template)
    text_message = text_message_template.render(message_context)
    html_message_template = loader.get_template(html_template)
    html_message = html_message_template.render(message_context)
    send_mail(subject, text_message, DEFAULT_FROM_EMAIL, [data['email']], html=html_message)


def send_request_received_email(contact_mail, template='inviteme/request_received_email.txt'):
    site = Site.objects.get_current()
    subject = '[%s] %s' % (site.name, _('new invitation request'))
    message_template = loader.get_template(template)
    message_context = Context({'contact_mail': contact_mail, 'site': site})
    message = message_template.render(message_context)
    if getattr(settings, 'INVITEME_NOTIFY_TO', False):
        if len(settings.INVITEME_NOTIFY_TO.split(',')) > 0:
            notify_to = settings.INVITEME_NOTIFY_TO.split(',')
        else:
            notify_to = [
             settings.INVITEME_NOTIFY_TO]
    else:
        notify_to = [ '%s <%s>' % (name, email) for (name, email) in settings.ADMINS
                    ]
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, notify_to)


@require_GET
def get_form(request, next=None, template='inviteme/inviteme.html'):
    return render_to_response(template, {'next': next}, RequestContext(request))


@csrf_protect
@require_POST
def post_form(request, next=None, template_preview='inviteme/preview.html', template_discarded='inviteme/discarded.html', template_post='inviteme/confirmation_sent.html'):
    """
    Post the mail form.

    HTTP POST is required. If ``POST['submit'] == "preview"`` or if there are
    errors a preview template, ``comments/preview.html``, will be rendered.
    """
    data = request.POST.copy()
    next = data.get('next', next)
    form = ContactMailForm(data=data)
    if form.security_errors():
        return ContactMailPostBadRequest('The contact message form failed security verification: %s' % escape(str(form.security_errors())))
    else:
        if form.errors:
            return render_to_response(template_preview, {'form': form, 'next': next}, RequestContext(request, {}))
        contact_mail_data = form.get_instance_data()
        responses = signals.confirmation_will_be_requested.send(sender=form.__class__, data=contact_mail_data, request=request)
        for (receiver, response) in responses:
            if response == False:
                return render_to_response(template_discarded, {'data': contact_mail_data}, context_instance=RequestContext(request))

        key = signed.dumps(contact_mail_data, compress=True, extra_key=INVITEME_SALT)
        send_confirmation_email(contact_mail_data, key)
        signals.confirmation_requested.send(sender=form.__class__, data=contact_mail_data, request=request)
        if next is not None:
            return HttpResponseRedirect(next)
        return render_to_response(template_post, context_instance=RequestContext(request))


def confirm_mail(request, key, template_accepted='inviteme/accepted.html', template_discarded='inviteme/discarded.html'):
    try:
        data = signed.loads(key, extra_key=INVITEME_SALT)
    except (ValueError, signed.BadSignature):
        raise Http404

    exists = ContactMail.objects.filter(email=data['email'], submit_date=data['submit_date']).count() > 0
    if exists:
        raise Http404
    responses = signals.confirmation_received.send(sender=ContactMail, data=data, request=request)
    for (receiver, response) in responses:
        if response == False:
            return render_to_response(template_discarded, {'data': data}, context_instance=RequestContext(request))

    contact_mail = ContactMail.objects.create(site_id=settings.SITE_ID, email=data['email'], submit_date=data['submit_date'])
    contact_mail.ip_address = request.META.get('REMOTE_ADDR', None)
    contact_mail.save()
    send_request_received_email(contact_mail)
    return render_to_response(template_accepted, {'data': data}, context_instance=RequestContext(request))