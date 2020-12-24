# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/mail/message.py
# Compiled at: 2019-06-12 01:17:17
"""E-mail message composition and sending."""
from __future__ import unicode_literals
import logging
from email.utils import parseaddr
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import six
from django.utils.datastructures import MultiValueDict
from djblets.mail.dmarc import is_email_allowed_by_dmarc
from djblets.mail.utils import build_email_address_via_service
logger = logging.getLogger(__name__)

class EmailMessage(EmailMultiAlternatives):
    """An EmailMesssage subclass with improved header and message ID support.

    This class knows about several headers (standard and variations), including
    :mailheader:`Sender`/:mailheader:`X-Sender`,
    :mailheader:`In-Reply-To`/:mailheader:`References``, and
    :mailheader:`Reply-To`.

    The generated :mailheader:`Message-ID` header from the e-mail can be
    accessed via the :py:attr:`message_id` attribute after the e-mail has been
    sent.

    In order to prevent issues when sending on behalf of users whose e-mail
    domains are controlled by DMARC, callers can specify
    ``from_spoofing`` (or set ``settings.DJBLETS_EMAIL_FROM_SPOOFING``). When
    set, the e-mail address used for the :mailheader:`From` header will only be
    used if there aren't any DMARC rules that may prevent the e-mail from being
    sent/received.

    .. note::

       Releases prior to Djblets 1.0.10 required using
       ``enable_smart_spoofing`` or ``settings.EMAIL_ENABLE_SMART_SPOOFING``,
       which didn't allow From spoofing to be completely disabled.)

    In the event that a DMARC rule would prevent sending on behalf of that
    user, the ``sender`` address will be used instead, with the full name
    appearing as the value in ``from_email`` with "via <Service Name>" tacked
    onto it.

    Callers wishing to use this should also set
    ``settings.EMAIL_DEFAULT_SENDER_SERVICE_NAME`` to the desired service name.
    Otherwise, the domain on the sender e-mail will be used instead.

    This class also supports repeated headers.

    Version Changed:
        1.0.10:
        Added the ``from_spoofing`` parameter and
        ``settings.DJBLETS_EMAIL_FROM_SPOOFING`` to replace
        ``enable_smart_spoofing`` and ``settings.EMAIL_ENABLE_SMART_SPOOFING``.
    """
    FROM_SPOOFING_ALWAYS = b'always'
    FROM_SPOOFING_SMART = b'smart'
    FROM_SPOOFING_NEVER = b'never'

    def __init__(self, subject=b'', text_body=b'', html_body=b'', from_email=None, to=None, cc=None, bcc=None, sender=None, in_reply_to=None, headers=None, auto_generated=False, prevent_auto_responses=False, from_spoofing=None, enable_smart_spoofing=None):
        """Create a new EmailMessage.

        Args:
            subject (unicode, optional):
                The subject of the message. Defaults to being blank (which
                MTAs might replace with "no subject".)

            text_body (unicode, optional):
                The body of the e-mail as plain text. Defaults to an empty
                string (allowing HTML-only e-mails to be sent).

            html_body (unicode, optional):
                The body of the e-mail as HTML. Defaults to an empty string
                (allowing text-only e-mails to be sent).

            from_email (unicode, optional):
                The from address for the e-mail. Defaults to
                :django:setting:`DEFAULT_FROM_EMAIL`.

            to (list, optional):
                A list of e-mail addresses as :py:class:`unicode` objects that
                are to receive the e-mail. Defaults to an empty list of
                addresses (allowing using CC/BCC only).

            cc (list, optional):
                A list of e-mail addresses as :py:class:`unicode` objects that
                are to receive a carbon copy of the e-mail, or ``None`` if
                there are no CC recipients.

            bcc (list, optional):
                A list of e-mail addresses as :py:class:`unicode` objects that
                are to receive a blind carbon copy of the e-mail, or ``None``
                if there are not BCC recipients.

            sender (unicode, optional):
                The actual e-mail address sending this e-mail, for use in
                the :mailheader:`Sender` header. If this differs from
                ``from_email``, it will be left out of the header as per
                :rfc:`2822`.

                This will default to :django:setting:`DEFAULT_FROM_EMAIL`
                if unspecified.

            in_reply_to (unicode, optional):
                An optional message ID (which will be used as the value for the
                :mailheader:`In-Reply-To` and :mailheader:`References`
                headers). This will be generated if not provided and will be
                available as the :py:attr:`message_id` attribute after the
                e-mail has been sent.

            headers (django.utils.datastructures.MultiValueDict, optional):
                Extra headers to provide with the e-mail.

            auto_generated (bool, optional):
                If ``True``, the e-mail will contain headers that mark it as
                an auto-generated message (as per :rfc:`3834`) to avoid auto
                replies.

            prevent_auto_responses (bool, optional):
                If ``True``, the e-mail will contain headers to prevent auto
                replies for delivery reports, read receipts, out of office
                e-mails, and other auto-generated e-mails from Exchange.

            from_spoofing (int, optional):
                Whether to spoof the :mailheader:`From` header for the user.
                This can be one of :py:attr:`FROM_SPOOFING_ALWAYS`,
                :py:attr:`FROM_SPOOFING_SMART`, or
                :py:attr:`FROM_SPOOFING_NEVER`.

                This defaults to ``None``, in which case the
                ``enable_smart_spoofing`` will be checked (for legacy reasons),
                falling back to ``settings.DJBLETS_EMAIL_FROM_SPOOFING`` (which
                defaults to :py:attr:`FROM_SPOOFING_ALWAYS`, also for legacy
                reasons).

            enable_smart_spoofing (bool, optional):
                Whether to enable smart spoofing of any e-mail addresses for
                the :mailheader:`From` header (if ``from_spoofing`` is
                ``None``). This defaults to
                ``settings.EMAIL_ENABLE_SMART_SPOOFING``.

                This is deprecated in favor of ``from_spoofing``.
        """
        headers = headers or MultiValueDict()
        if isinstance(headers, dict) and not isinstance(headers, MultiValueDict):
            headers = MultiValueDict(dict((key, [value]) for key, value in six.iteritems(headers)))
        if in_reply_to:
            headers[b'In-Reply-To'] = in_reply_to
            headers[b'References'] = in_reply_to
        headers[b'Reply-To'] = from_email
        if from_spoofing is None:
            if enable_smart_spoofing is None:
                enable_smart_spoofing = getattr(settings, b'EMAIL_ENABLE_SMART_SPOOFING', None)
            if enable_smart_spoofing is not None:
                if enable_smart_spoofing:
                    from_spoofing = self.FROM_SPOOFING_SMART
                else:
                    from_spoofing = self.FROM_SPOOFING_ALWAYS
            if from_spoofing is None:
                from_spoofing = getattr(settings, b'DJBLETS_EMAIL_FROM_SPOOFING', self.FROM_SPOOFING_ALWAYS)
        if not sender:
            sender = settings.DEFAULT_FROM_EMAIL
        if sender == from_email:
            sender = None
        elif from_spoofing != self.FROM_SPOOFING_ALWAYS:
            parsed_from_name, parsed_from_email = parseaddr(from_email)
            parsed_sender_name, parsed_sender_email = parseaddr(sender)
            if not parsed_from_email:
                logger.warning(b'EmailMessage: Unable to parse From address "%s"', from_email)
            if not parsed_sender_email:
                logger.warning(b'EmailMessage: Unable to parse Sender address "%s"', sender)
            if from_spoofing == self.FROM_SPOOFING_NEVER or parsed_from_email != parsed_sender_email and not is_email_allowed_by_dmarc(parsed_from_email):
                from_email = build_email_address_via_service(full_name=parsed_from_name, email=parsed_from_email, sender_email=parsed_sender_email)
        if sender:
            headers[b'Sender'] = sender
            headers[b'X-Sender'] = sender
        if auto_generated:
            headers[b'Auto-Submitted'] = b'auto-generated'
        if prevent_auto_responses:
            headers[b'X-Auto-Response-Suppress'] = b'DR, RN, OOF, AutoReply'
        super(EmailMessage, self).__init__(subject=subject, body=text_body, from_email=settings.DEFAULT_FROM_EMAIL, to=to, cc=cc, bcc=bcc, headers={b'From': from_email})
        self.message_id = None
        self._headers = headers
        if html_body:
            self.attach_alternative(html_body, b'text/html')
        return

    def message(self):
        """Construct an outgoing message for the e-mail.

        This will construct a message based on the data provided to the
        constructor. This represents the e-mail that will later be sent using
        :py:meth:`send`.

        After calling this method, the message's ID will be stored in the
        :py:attr:`message_id` attribute for later reference.

        This does not need to be called manually. It's called by
        :py:meth:`send`.

        Returns:
            django.core.mail.message.SafeMIMEText:
            The resulting message.
        """
        msg = super(EmailMessage, self).message()
        self.message_id = msg[b'Message-ID']
        for name, value_list in six.iterlists(self._headers):
            for value in value_list:
                msg.add_header(six.binary_type(name), value)

        return msg

    def recipients(self):
        """Return a list of all recipients of the e-mail.

        Returns:
            list:
            A list of all recipients included on the To, CC, and BCC lists.
        """
        return self.to + self.bcc + self.cc