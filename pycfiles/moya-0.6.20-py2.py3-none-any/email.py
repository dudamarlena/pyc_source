# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/tags/email.py
# Compiled at: 2016-02-28 13:01:55
from __future__ import unicode_literals
from __future__ import absolute_import
from ..elements.elementbase import Attribute, LogicElement
from ..tags.content import ContentElementMixin
from .. import logic
from .. import namespaces
from ..render import render_object
from ..template.rendercontainer import RenderContainer
from ..mail import Email
import logging
log = logging.getLogger(b'moya.email')

class EmailElement(LogicElement):
    """Define an email."""
    xmlns = namespaces.email

    class Meta:
        tag_name = b'email'

    class Help:
        synopsis = b'define an email'

    from_ = Attribute(b'From email', required=False, default=None, name=b'from')
    to = Attribute(b'To email address', type=b'commalist', required=False, default=None)
    cc = Attribute(b'CC email address', type=b'commalist', required=False, default=None)
    bcc = Attribute(b'BCC email address', type=b'commalist', required=False, default=None)
    replyto = Attribute(b'Reply to email address', required=False, default=None)
    subject = Attribute(b'Email subjects', default=None)


class Text(LogicElement, ContentElementMixin):
    """Add text template to an email."""
    xmlns = namespaces.email

    class Help:
        synopsis = b'add text to an email'

    template = Attribute(b'Template path', type=b'template', required=False)
    content = Attribute(b'Content Element', required=False, type=b'elementref')

    def logic(self, context):
        template, content = self.get_parameters(context, b'template', b'content')
        app = self.get_app(context)
        email = context[b'email']
        if template:
            template = app.resolve_template(template)
            render_container = RenderContainer.create(app, template=template)
            render_container.update(email.data)
            text = render_object(render_container, self.archive, context, b'text')
        else:
            for defer in self.generate_content(context, content, app, td=email.data):
                yield defer

            content = context[b'.content']
            text = render_object(content, self.archive, context, b'text')
        email.text = text


class HTML(LogicElement, ContentElementMixin):
    """Add an HTML template to an email."""
    xmlns = namespaces.email

    class Help:
        synopsis = b'add HTML to an email'

    class Meta:
        one_of = [
         ('template', 'content')]

    template = Attribute(b'Template path', type=b'template', required=False)
    content = Attribute(b'Content element', required=False, type=b'elementref')

    def logic(self, context):
        template, content = self.get_parameters(context, b'template', b'content')
        app = self.get_app(context)
        email = context[b'email']
        if template:
            template = app.resolve_template(template)
            render_container = RenderContainer.create(app, template=template)
            render_container.update(email.data)
            html = render_object(render_container, self.archive, context, b'html')
        else:
            for defer in self.generate_content(context, content, app, td=email.data):
                yield defer

            content = context[b'_content']
            html = render_object(content, self.archive, context, b'html')
        email.html = html


class Get(LogicElement):
    """Get an previously defined email object."""
    xmlns = namespaces.email

    class Help:
        synopsis = b'get an email object'

    dst = Attribute(b'Destination to store exception object', type=b'reference', required=True)
    email = Attribute(b'Reference to email tag', type=b'elementref')
    subject = Attribute(b'Email subject', default=None)
    data = Attribute(b'Template / content data', type=b'expression', default=None)
    from_ = Attribute(b'From email', required=False, default=None, name=b'from', map_to=b'from')
    to = Attribute(b'To email address', type=b'commalist', required=False, default=None)
    cc = Attribute(b'CC email address', type=b'commalist', required=False, default=None)
    bcc = Attribute(b'BCC email address', type=b'commalist', required=False, default=None)
    replyto = Attribute(b'Reply to email address', required=False, default=None)

    def get_email(self, context):
        dst, data, email_ref, subject, from_ = self.get_parameters(context, b'dst', b'data', b'email', b'subject', b'from')
        if data is None:
            data = {}
        data.update(self.get_let_map(context))
        with context.data_scope(data):
            app = self.get_app(context)
            email_app, email_element = self.get_element(email_ref, app)
            subject = email_element.subject(context) or subject or b''
            from_ = email_element.get_parameter(context, b'from') or from_ or b''
            emails = email_element.get_parameters_map(context, b'from', b'to', b'cc', b'bcc', b'replyto')
            for k, v in self.get_parameters_map(context, b'from', b'to', b'cc', b'bcc', b'replyto').items():
                if v is not None:
                    emails[k] = v

            email = Email(data=data)
            email.app = email_app
            email.email_element = email_element
            email.subject = subject
            email.set_from(from_)
            for addr in emails[b'to'] or []:
                email.add_to(addr)

            for addr in emails[b'cc'] or []:
                email.add_to(addr)

            for addr in emails[b'bcc'] or []:
                email.add_to(addr)

            email.replyto = emails[b'replyto']
            return email
        return

    def logic(self, context):
        email = context[self.dst(context)] = self.get_email(context)
        email_app, email_element = self.get_element(self.email(context), self.get_app(context))
        with self.call(context, app=email_app, email=email):
            yield logic.DeferNodeContents(email_element)


class Send(Get):
    """Send an email."""

    class Help:
        synopsis = b'send an email'

    xmlns = namespaces.email
    dst = Attribute(b'Destination to store exception object', type=b'reference', required=False)
    src = Attribute(b'Source email', type=b'index', default=None)
    smtp = Attribute(b'SMTP server', default=b'')
    failsilently = Attribute(b'Should mail exceptions be ignored?', type=b'boolean', default=True)

    def logic(self, context):
        fail_silently = self.failsilently(context)
        _email = self.src(context)
        if _email is None:
            email = self.get_email(context)
            with self.call(context, app=email.app, email=email):
                yield logic.DeferNodeContents(email.email_element)
        dst = self.dst(context)
        if dst is not None:
            context[self.dst(context)] = email
        if context.get(b'.debug', False):
            context[b'.console'].obj(context, email)
        mail_server = self.archive.get_mailserver(self.smtp(context))
        try:
            mail_server.send(email)
            log.info((b'sent email to "{}", subject "{}"').format(email.to_text, email.subject or b''))
        except Exception as e:
            log.error(b'failed to send email to "%s", with subject "%s" (%s)', email.to_text, email.subject or b'', e)
            if not fail_silently:
                self.throw(b'email.send-failed', (b"Moya was unable to send email '{}' ({})").format(_email, e), diagnosis=b'Check the [smtp:] section in settings, and that the mail server is running.', info={b'email': _email, b'pyerror': e})

        return