# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stein/Projekte/eclipse/django-easy-contact/easy_contact/views.py
# Compiled at: 2014-10-23 09:33:03
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from easy_contact.forms import ContactForm
from django.views.decorators.cache import cache_control
import settings, smtplib
from smtplib import SMTPException
from email.mime.text import MIMEText

@cache_control(private=True)
def contact(request):
    u"""
    View für simples Kontaktformular.
    1. It should be possible to us the contact form by give only the reciver adress
    in the django-contac-formt-setup so the server in settings.py will be used
    for sending.
    2. If a full server setup is given in django-contac-formt-setup than it will
    be used
    3. if Complete server setup is not installed then settings.py is used for
    complete mail host setup.

    Anyway, for best results use a smtp server who allowed to send mails with any
    sender adress.
    """

    def get_mail_data():
        """
        If django-contac-formt-setup is installed than get data set from the app if not
        pull it from settings.py
        Also if there are missig data in spite of no server was specified in
        the app than it will be filled up by our setup.py
        """
        error_message = 'Pleas configure your settings file withthe necessary mailserver settings.'
        d = {}
        send_with_formulars_email_from = False
        if 'easy_contact_setup' in settings.INSTALLED_APPS:
            from easy_contact_setup.models import Setup
            try:
                m = Setup.objects.filter(active=True)[0]
            except IndexError:
                raise IndexError('Create an instance in the easy_contact_setup app a and activate it!')

            d['MAIL_DEFAULT_TO'] = m.mail_to
            d['MAIL_HOST_PASS'] = m.mail_host_pass
            d['MAIL_HOST_USER'] = m.mail_host_user
            d['MAIL_HOST'] = m.mail_host
            if m.mail_host and m.mail_host_pass and m.mail_host_user:
                send_with_formulars_email_from = True
                return (
                 d, send_with_formulars_email_from)
            d['MAIL_FROM'] = settings.DEFAULT_FROM_EMAIL
        else:
            send_with_formulars_email_from = True
            try:
                d['MAIL_DEFAULT_TO'] = settings.DEFAULT_FROM_EMAIL
            except AttributeError:
                raise AttributeError(error_message)

            try:
                d['MAIL_HOST_PASS'] = settings.EMAIL_HOST_PASSWORD
                d['MAIL_HOST_USER'] = settings.EMAIL_HOST_USER
                d['MAIL_HOST'] = settings.EMAIL_HOST
                return (d, send_with_formulars_email_from)
            except AttributeError:
                raise AttributeError(error_message)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sd, swmd = get_mail_data()
            cd = form.cleaned_data
            subject = 'Message from %s on website %s' % (cd['email'], request.META['HTTP_HOST'])
            message = 'Subj: %s\n\n%s' % (cd['subject'], cd['message'])
            mail_from = cd['email']
            mail_recipient_list = [
             sd['MAIL_DEFAULT_TO']]

            def get_mime_text_instance(subj=subject, mail_from=mail_from, mail_to=sd['MAIL_DEFAULT_TO']):
                """Create and configure an mime text instance"""
                inst = MIMEText(message.encode('utf-8'), 'plain', 'UTF-8')
                inst['Subject'] = subj
                inst['From'] = mail_from
                inst['To'] = mail_to
                return inst

            s = smtplib.SMTP(sd['MAIL_HOST'])
            try:
                s.login(sd['MAIL_HOST_USER'], sd['MAIL_HOST_PASS'])
            except SMTPException:
                s.starttls()
                s.ehlo()
                s.login(sd['MAIL_HOST_USER'], sd['MAIL_HOST_PASS'])

            if swmd:
                try:
                    msg = get_mime_text_instance()
                    s.sendmail(msg['From'], mail_recipient_list, msg.as_string())
                except smtplib.SMTPSenderRefused:
                    msg = get_mime_text_instance(mail_from=sd['MAIL_DEFAULT_TO'])
                    s.sendmail(msg['From'], mail_recipient_list, msg.as_string())

            else:
                msg = get_mime_text_instance(mail_from=sd['MAIL_FROM'])
                s.sendmail(msg['From'], mail_recipient_list, msg.as_string())
            s.quit()
            return HttpResponseRedirect('/%s/feedback/success/' % request.LANGUAGE_CODE)
    else:
        form = ContactForm(initial={'message': ''})
    current_dict = {'form': form}
    return render_to_response('easy_contact/contact.html', current_dict, context_instance=RequestContext(request))


def thanks(request):
    return render_to_response('easy_contact/success.html', context_instance=RequestContext(request))