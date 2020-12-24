# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/botlib/testing/smtpsrv.py
# Compiled at: 2008-08-09 12:39:34
"""An smtpd-based RFC 2821-compliant mail server."""
import os, re, sys, email, smtpd, signal, socket, mailbox, asyncore, optparse
COMMASPACE = ', '

class Channel(smtpd.SMTPChannel):

    def __init__(self, server, conn, addr):
        smtpd.SMTPChannel.__init__(self, server, conn, addr)
        self._server = server

    def send(self, data):
        try:
            return smtpd.SMTPChannel.send(self, data)
        except socket.error:
            pass


class Server(smtpd.SMTPServer):

    def __init__(self, host, port, maildir):
        smtpd.SMTPServer.__init__(self, (host, port), None)
        self._mailbox = mailbox.Maildir(maildir, email.message_from_file)
        return

    def handle_accept(self):
        (conn, addr) = self.accept()
        channel = Channel(self, conn, addr)

    def process_message(self, peer, mailfrom, rcpttos, data):
        msg = email.message_from_string(data)
        msg['X-Peer'] = str(peer)
        msg['X-RCPT-To'] = COMMASPACE.join(rcpttos)
        msg['Return-Path'] = mailfrom
        self._mailbox.add(msg)


def parseargs():
    parser = optparse.OptionParser()
    parser.add_option('--host', default='localhost', action='store')
    parser.add_option('--port', type='int')
    parser.add_option('--mbox', action='store')
    (options, arguments) = parser.parse_args()
    parser.options = options
    parser.arguments = arguments
    return parser


def signal_handler(*ignore):
    asyncore.socket_map.clear()


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    parser = parseargs()
    server = Server(parser.options.host, parser.options.port, parser.options.mbox)
    asyncore.loop()
    asyncore.close_all()