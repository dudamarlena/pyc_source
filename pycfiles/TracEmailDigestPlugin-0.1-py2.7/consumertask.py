# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notifier/consumertask.py
# Compiled at: 2011-09-22 11:28:07
"""
Created on Tue 16 Aug 2011

@author: leewei
"""
from __future__ import with_statement
from contextlib import closing
import socket, json
from trac.core import *
from traccron.api import ICronTask
from traccron.core import CronConfig
from amqplib import client_0_8 as amqp
from notifier import NotifyMain
DEFAULT_SERVER = 'localhost'
DEFAULT_USERID = 'lshift'
DEFAULT_PASSWORD = 'lshift'
DEFAULT_VIRTUAL_HOST = 'Trac'

class ConsumerTask(Component, ICronTask):
    """
        This consumer polls the AMQP Queues at regular intervals
        (as per specified) to generate & send daily digest emails.
    """
    implements(ICronTask)

    def _get_preferences(self, username):
        """
            Retrieves user's preferences regarding ticket email notifications.
        """
        result = []
        with closing(self.env.get_read_db()) as (db):
            with closing(db.cursor()) as (cursor):
                for attr in ['opt_notify_limit', 'opt_notify', 'opt_custom_textarea']:
                    result.append(self._get_db_attr(cursor, attr, username))

        return result

    def _get_db_attr(self, cursor, attr, username):
        cursor.execute('\n            SELECT DISTINCT(value) FROM session_attribute\n            WHERE name=%s AND sid=%s\n        ', (attr, username))
        row = cursor.fetchone()
        if row:
            return row[0]
        return ''

    def wake_up(self, *args):
        isFlush = False
        if len(args) == 1:
            isFlush = args[0].lower() == 'true'
        self.env.log.debug('ConsumerTask::wake_up() - isFlush = %s' % isFlush)
        logger = self.env.log
        chan = self._amqp_setup_channel()
        for exchange in self._get_all_user_emails():
            queue = '%s-%s' % (socket.gethostname(), exchange)
            self._amqp_setup_queue(chan, exchange, queue)
            qname, qmsg, qconsumer = chan.queue_declare(queue=queue, passive=True)
            logger.debug("Queue '%s': %d messages (for %d consumer(s))" % (
             qname, qmsg, qconsumer))
            if qmsg > 0:
                msg = chan.basic_get(queue)
                username = json.loads(msg.body)['username']
                opt_notify_limit, opt_notify, opt_custom_textarea = self._get_preferences(username)
                opt_notify_limit = int(opt_notify_limit or 20)
                opt_notify = json.loads(opt_notify)
                if qmsg >= opt_notify_limit or isFlush:
                    logger.debug('Sending daily digest to %s...' % exchange)
                    self._generate_daily_digest(chan, queue, exchange, msg)

    def getId(self):
        return 'amqp_consumer'

    def getDescription(self):
        return self.__doc__

    def _generate_daily_digest(self, chan, queue, recipient_email, msg):
        dtags = [
         msg.delivery_tag]
        digest_body = [msg.body]
        while True:
            msg = chan.basic_get(queue)
            if msg is not None:
                digest_body.append(msg.body)
                dtags.append(msg.delivery_tag)
            else:
                break

        isEmailSent = NotifyMain.send_email(self.env, recipient_email, digest_body, '[LATER] Trac daily digest')
        if isEmailSent:
            chan.basic_ack(max(dtags), multiple=True)
            self.env.log.debug('ACK msg delivery tags up to #%d' % max(dtags))
            self.env.log.debug('...daily digest email send completed')
        else:
            self.env.log.debug('...error occurred sending daily digest email')
        return

    def _amqp_setup_channel(self):
        conn = amqp.Connection(host=DEFAULT_SERVER, userid=DEFAULT_USERID, password=DEFAULT_PASSWORD, virtual_host=DEFAULT_VIRTUAL_HOST, insist=False)
        chan = conn.channel()
        return chan

    def _amqp_setup_queue(self, chan, exchange, queue):
        chan.exchange_declare(exchange=exchange, type='direct', durable=True, auto_delete=False)
        chan.queue_declare(queue=queue, durable=True, exclusive=False, auto_delete=False)
        chan.queue_bind(queue=queue, exchange=exchange)

    def _get_all_user_emails(self):
        emails = []
        with closing(self.env.get_db_cnx()) as (db):
            with closing(db.cursor()) as (cursor):
                cursor.execute("\n                    SELECT DISTINCT(value) FROM session_attribute\n                    WHERE name = 'email'\n                ")
                emails = [ row[0] for row in cursor.fetchall() ]
        return emails