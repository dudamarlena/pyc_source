# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notifier/notifier.py
# Compiled at: 2011-09-22 12:02:05
"""
Created on Tue 16 Aug 2011

@author: leewei
"""
from __future__ import with_statement
import os, json, uuid, smtplib, email.utils
from datetime import datetime, date
from pkg_resources import resource_filename
from trac.core import *
from trac.web import IRequestFilter
from trac.web.chrome import ITemplateProvider, add_stylesheet, add_notice
from trac.ticket import Ticket
from trac.ticket.api import ITicketChangeListener
from trac.prefs import IPreferencePanelProvider
from trac.util.translation import _
from genshi.template import TemplateLoader
from amqpdeliver import send
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
AMQP_HOST = 'localhost'
AMQP_PORT = 5672
AMQP_SERVER = '%s:%s' % (AMQP_HOST, AMQP_PORT)
AMQP_VHOST = 'Trac'
AMQP_USER = 'lshift'
AMQP_PASS = 'lshift'

class NotifyMain(Component):
    """ Central functionality for the Ticket Notification plugin. """
    implements(ITicketChangeListener, IPreferencePanelProvider, IRequestFilter, ITemplateProvider)

    @staticmethod
    def send_email(env, recipient_email, content, subject=None):
        """ Sends an email containing content via localhost SMTP Server. """
        if not isinstance(content, MIMEBase):
            try:
                content = NotifyMain.construct_message(env, recipient_email, content, subject)
            except:
                env.log.error('Error occurred constructing email message.')
                return False

        env.log.debug('sending email to recipient: %s' % recipient_email)
        smtp = smtplib.SMTP('localhost')
        try:
            try:
                smtp.sendmail('trac@lshift.net', [recipient_email], content.as_string())
            except:
                env.log.error('Error occurred sending email message.')
                return False

        finally:
            smtp.quit()
            return True

    @staticmethod
    def construct_message(env, recipient_email, contents, subject):
        """
            Transforms an incoming string into an outgoing email (SMTP) message.
            (for both single email notifications & daily digests)
        """
        env.log.debug('construct_message to: %s' % recipient_email)
        env.log.debug('contents: %s' % contents)
        if isinstance(contents, dict):
            contents = [
             contents]
        else:
            if isinstance(contents, list):
                contents = map(json.loads, contents)
                for item in contents:
                    item['params']['changes'] = map(tuple, item['params']['changes'])

            msg = MIMEMultipart('alternative')
            msg['To'] = email.utils.formataddr(('LShiftee', recipient_email))
            msg['From'] = email.utils.formataddr(('Trac', 'trac@lshift.net'))
            msg['Reply-to'] = email.utils.formataddr(('Do Not Reply', 'no-such-address@lshift.net'))
            msg['Subject'] = '%s [%s]' % (
             subject or 'Untitled Email',
             date.today().strftime('%d/%m/%Y'))
            text = '<text-only version is not available yet>'
            msg.attach(MIMEText(text, 'plain'))
            loader = TemplateLoader([resource_filename(__name__, 'templates')])
            tmpl = loader.load('email.html')
            path_project_logo = os.path.join(env.path, env.config.get('header_logo', 'src').replace('site', 'htdocs'))
            png_file = open(path_project_logo, 'rb')
            png_txt = png_file.read()
            png_img = png_txt.encode('base64')
            base64_project_logo = 'data:image/png;base64,%s' % png_img
            tkt_changes = {}
            for content in contents:
                tkt_id = content['tkt_id']
                ticket = Ticket(env, tkt_id=tkt_id)
                tkt_title = ticket['summary']
                tkt_desc = ticket['description']
                key = (tkt_id, tkt_title, tkt_desc)
                new_changes = []
                new_changes.extend(content['params']['changes'] or [])
                comment = content['params'].get('comment', None)
                if comment:
                    old_value = content['params']['old_values'].get('comment', '')
                    new_changes.append(('comment', old_value, comment))
                tkt_change = {content['params']['author']: new_changes}
                if key in tkt_changes:
                    if content['params']['author'] in tkt_changes[key]:
                        tkt_changes[key][content['params']['author']].extend(new_changes)
                    else:
                        tkt_changes[key][content['params']['author']] = new_changes
                else:
                    tkt_changes[key] = tkt_change

        stream = tmpl.generate(base_url=env.config.get('trac', 'base_url'), tkt_changes=tkt_changes, URL={'project': env.config.get('project', 'url'), 
           'project_logo': base64_project_logo, 
           'prefs_notify': os.path.join(env.config.get('trac', 'base_url'), 'prefs/notifier')})
        html = stream.render()
        msg.attach(MIMEText(html, 'html'))
        return msg

    def __init__(self, *args, **kwargs):
        conf = self.env.config
        conf.set('notification', 'smtp_enabled', False)
        for role in ['owner', 'reporter', 'updater']:
            conf.set('notification', 'always_notify_%s' % role, False)

        conf.save()

    def ticket_created(self, tkt):
        """ Called when a ticket is created. """
        self.env.log.debug('NotifyMain::ticket_created(#%d)' % tkt.id)
        self._notify_handler(tkt, {'title': tkt['summary'], 'description': tkt['description'], 'author': tkt['reporter'], 
           'changes': [('create', '', tkt.id)]}, 'create')

    def ticket_deleted(self, tkt):
        """ Called when a ticket is deleted. """
        self.env.log.debug('NotifyMain::ticket_deleted(#%d)' % tkt.id)
        self._notify_handler(tkt, {'title': tkt['summary'], 'description': tkt['description'], 'author': tkt['reporter'], 
           'changes': [('delete', '', tkt.id)]}, 'delete')

    def ticket_changed(self, tkt, comment, author, old_values):
        """ Called when a ticket is modified. """
        self.env.log.debug('NotifyMain::ticket_changed(#%d)' % tkt.id)
        changes = [ (item, old_values[item], tkt[item]) for item in old_values.keys() ]
        self._notify_handler(tkt, {'comment': comment, 'author': author, 'old_values': old_values, 'title': tkt['summary'], 
           'description': tkt['description'], 'changes': changes}, 'update')

    def _prettify_message(self, msg):
        """
            Accepts as input a message as a dictionary and returns
            its equivalent pretty printed string representation.
        """
        return json.dumps(msg)

    def _notify_handler(self, tkt, params, tix_type):
        """ Common handler for ticket-{created, changed, deleted} events. """
        self.env.log.debug('notify_handler: ticket id - #%d' % tkt.id)
        ticket_users = {'owner': {'name': tkt['owner'], 'email': None}, 'reporter': {'name': tkt['reporter'], 'email': None}, 'cc': {'name': tkt['cc'], 'email': None}, 'old_owner': {'name': None, 'email': None}, 'author': {'name': None, 'email': None}}
        if tix_type == 'update':
            ticket_users['old_owner']['name'] = params['old_values'].get('owner', None)
            ticket_users['author']['name'] = params.get('author', None)
        cursor = self.env.get_read_db().cursor()
        for role, name_email in ticket_users.iteritems():
            username = name_email['name']
            cursor.execute("\n                SELECT DISTINCT(value)\n                FROM session_attribute\n                WHERE name='email' AND sid=%s\n            ", (username,))
            row = cursor.fetchone()
            if row:
                name_email['email'] = row[0]

        self.env.log.debug('Ticket users: %s' % ticket_users)
        msg = {'tkt_id': tkt.id, 'params': params, 'type': tix_type, 'timestamp': str(datetime.now())}
        sent = []
        for role in ['old_owner', 'owner']:
            name_email = ticket_users[role]
            exchange = name_email['email']
            if exchange and exchange not in sent:
                tag = uuid.uuid4()
                self.env.log.debug('[NOW] %s to email' % tag)
                msg.update({'role': role, 
                   'username': name_email['name'], 
                   'id': str(tag)})
                self.env.log.debug("To: '%s'..." % exchange)
                self.env.log.debug('Body: %s' % msg)
                NotifyMain.send_email(self.env, exchange, msg, '[NOW] Trac email')
                sent.append(exchange)

        for role, name_email in ticket_users.iteritems():
            exchange = name_email['email']
            if exchange and exchange not in sent:
                tag = uuid.uuid4()
                self.env.log.debug('[LATER] %s to exchange' % tag)
                msg.update({'role': role, 
                   'username': name_email['name'], 
                   'id': str(tag)})
                self.env.log.debug("To: '%s'..." % exchange)
                self.env.log.debug('Body: %s' % msg)
                send.send(AMQP_SERVER, exchange, self._prettify_message(msg), virtual_host=AMQP_VHOST, userid=AMQP_USER, password=AMQP_PASS)
                sent.append(exchange)

        return

    __PANEL_ID = 'notifier'

    def get_preference_panels(self, req):
        if req.session.authenticated:
            yield (
             self.__PANEL_ID, _('Ticket Notification'))

    def render_preference_panel(self, req, panel):
        if req.method == 'POST' and req.args['panel_id'] == self.__PANEL_ID:
            for option in ['opt_notify_limit', 'opt_custom_textarea']:
                req.session[option] = req.args.get(option, None)

            opt_notify = req.args.get('opt_notify', [])
            if not isinstance(opt_notify, list):
                opt_notify = [
                 opt_notify]
            req.session['opt_notify'] = json.dumps({item:1 for item in opt_notify})
            if req.args['action'] == 'save':
                add_notice(req, _('Your ticket mail notification preference settings have' + ' been saved successfully.'))
            req.redirect(req.href.prefs(panel or None))
        data = {}
        for option in ['opt_notify_limit', 'opt_custom_textarea']:
            data.update({option: req.session.get(option, None)})

        data.update({'opt_notify': json.loads(req.session.get('opt_notify', '{}'))})
        return (
         'prefs_notifier.html', data)

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, data, content_type):
        if req.path_info[1:] == 'prefs/notifier':
            add_stylesheet(req, 'notifier/css/notifier.css')
        return (
         template, data, content_type)

    def get_htdocs_dirs(self):
        """
            Return a list of directories with static resources (such as style
            sheets, images, etc.)

            Each item in the list must be a `(prefix, abspath)` tuple. The
            `prefix` part defines the path in the URL that requests to these
            resources are prefixed with.

            The `abspath` is the absolute path to the directory containing the
            resources on the local file system.
        """
        return [
         (
          'notifier', resource_filename(__name__, 'htdocs'))]

    def get_templates_dirs(self):
        """
            Return a list of directories containing the provided template
            files.
        """
        return [
         resource_filename(__name__, 'templates')]