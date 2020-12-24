# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/scripts/sender.py
# Compiled at: 2008-06-20 03:40:59
__doc__ = 'sender.py - script that sends messages in the outbox thru kannel\n\nAUTHOR: Emanuel Gardaya Calso\n\n'
import time, re
from datetime import datetime
import urllib
from emantools import create_daemon
from emantools.daemon import Daemon
from base import *
import message_filter
INTERVAL = 10
OUTBOX = 3
SENT = 4

class SendMsg(object):
    interval = INTERVAL

    def __init__(self, msg, log=None):
        self.entry = msg
        self.log = log
        self.message = urllib.quote(msg.message)
        self.recipient = urllib.quote_plus(msg.recipient)

    def send(self):
        num = self.recipient
        msg = self.message
        url = 'http://127.0.0.1:13013/cgi-bin/sendsms?username=smsuser&password=111111&to=%s&text=%s'
        print 'Sending %s to %s' % (msg, num)
        site = urllib.FancyURLopener().open(url % (num, msg))
        status = site.read()
        if not re.match('^0', status) and not re.match('^4', status):
            print 'Cannot send message: %s' % status
            return False
        self.entry.folder = SENT
        self.entry.created = datetime.now()
        self.entry.modified = datetime.now()
        model.Session.update(self.entry)
        model.Session.commit()
        print 'Sent %s to %s' % (msg, num)
        self.entry = message_filter.go_thru_filters(self.entry)
        return status


class Sender(Daemon):
    interval = INTERVAL
    pid_file = '/tmp/sender.pid'
    log_file = '/tmp/pycrud-sender.log'

    def __init__(self):
        self.main()

    def run(self):
        now = datetime.now()
        query = model.list(model.Message).filter_by(folder=OUTBOX)
        query = query.order_by(model.Message.created)
        query = query.filter(model.Message.created <= now)
        for msg in query:
            sendmsg = SendMsg(msg, log=self.log)
            sendmsg.send()
            time.sleep(self.interval)

    def start(self):
        print 'Starting Daemon ...'
        if self.get_status():
            print 'Daemon already started.'
            return False
        create_daemon.createDaemon()
        self.write_pid()
        while True:
            self.run()
            time.sleep(self.interval)

        return True


def setup(filename=SERVER_CONF):
    global model
    conf = appconfig('config:' + filename)
    load_environment(conf.global_conf, conf.local_conf)
    paste.deploy.CONFIG.push_process_config({'app_conf': conf.local_conf, 'global_conf': conf.global_conf})
    from pycrud import model


def main():
    from sys import argv
    try:
        conf_file = argv[2]
    except IndexError:
        conf_file = SERVER_CONF

    setup(conf_file)
    message_filter.model = model
    Sender()


if __name__ == '__main__':
    main()