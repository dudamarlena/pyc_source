# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/utils/sendgrid.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 4297 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import base64, mimetypes, os, sendgrid
from sendgrid.helpers.mail import Attachment, Content, Email, Mail, Personalization, CustomArg, Category
from airflow.utils.email import get_email_address_list
from airflow.utils.log.logging_mixin import LoggingMixin

def send_email(to, subject, html_content, files=None, dryrun=False, cc=None, bcc=None, mime_subtype='mixed', **kwargs):
    """
    Send an email with html content using sendgrid.

    To use this plugin:
    0. include sendgrid subpackage as part of your Airflow installation, e.g.,
    pip install 'apache-airflow[sendgrid]'
    1. update [email] backend in airflow.cfg, i.e.,
    [email]
    email_backend = airflow.contrib.utils.sendgrid.send_email
    2. configure Sendgrid specific environment variables at all Airflow instances:
    SENDGRID_MAIL_FROM={your-mail-from}
    SENDGRID_API_KEY={your-sendgrid-api-key}.
    """
    mail = Mail()
    from_email = kwargs.get('from_email') or os.environ.get('SENDGRID_MAIL_FROM')
    from_name = kwargs.get('from_name') or os.environ.get('SENDGRID_MAIL_SENDER')
    mail.from_email = Email(from_email, from_name)
    mail.subject = subject
    personalization = Personalization()
    to = get_email_address_list(to)
    for to_address in to:
        personalization.add_to(Email(to_address))

    if cc:
        cc = get_email_address_list(cc)
        for cc_address in cc:
            personalization.add_cc(Email(cc_address))

    if bcc:
        bcc = get_email_address_list(bcc)
        for bcc_address in bcc:
            personalization.add_bcc(Email(bcc_address))

    pers_custom_args = kwargs.get('personalization_custom_args', None)
    if isinstance(pers_custom_args, dict):
        for key in pers_custom_args.keys():
            personalization.add_custom_arg(CustomArg(key, pers_custom_args[key]))

    mail.add_personalization(personalization)
    mail.add_content(Content('text/html', html_content))
    categories = kwargs.get('categories', [])
    for cat in categories:
        mail.add_category(Category(cat))

    for fname in files or []:
        basename = os.path.basename(fname)
        attachment = Attachment()
        with open(fname, 'rb') as (f):
            attachment.content = str(base64.b64encode(f.read()), 'utf-8')
            attachment.type = mimetypes.guess_type(basename)[0]
            attachment.filename = basename
            attachment.disposition = 'attachment'
            attachment.content_id = '<%s>' % basename
        mail.add_attachment(attachment)

    _post_sendgrid_mail(mail.get())


def _post_sendgrid_mail(mail_data):
    log = LoggingMixin().log
    sg = sendgrid.SendGridAPIClient(apikey=(os.environ.get('SENDGRID_API_KEY')))
    response = sg.client.mail.send.post(request_body=mail_data)
    if response.status_code >= 200:
        if response.status_code < 300:
            log.info('Email with subject %s is successfully sent to recipients: %s' % (
             mail_data['subject'], mail_data['personalizations']))
    else:
        log.warning('Failed to send out email with subject %s, status code: %s' % (
         mail_data['subject'], response.status_code))