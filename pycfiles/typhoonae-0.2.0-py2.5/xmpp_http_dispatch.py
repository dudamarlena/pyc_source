# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/xmpp/xmpp_http_dispatch.py
# Compiled at: 2010-12-12 04:36:57
"""Simple XMPP/HTTP dispatcher implementation."""
import logging, mimetools, optparse, sys, time, urllib2, xmpp
DESCRIPTION = 'XMPP/HTTP dispatcher.'
USAGE = 'usage: %prog [options]'

def post_multipart(url, fields):
    """Posts multipart form data fields.

    Args:
        url: Post multipart form data to this URL.
        fields: A list of tuples of the form [(fieldname, value), ...].
    """
    (content_type, body) = encode_multipart_formdata(fields)
    headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}
    req = urllib2.Request(url, str(body.encode('utf-8')), headers)
    try:
        res = urllib2.urlopen(req)
    except urllib2.URLError, err_obj:
        reason = getattr(err_obj, 'reason', err_obj)
        logging.error('failed message %s' % reason)
        return

    return res.read()


def encode_multipart_formdata(fields):
    """Encodes multipart form data.

    Returns content type and body.
    """
    BOUNDARY = mimetools.choose_boundary()
    CRLF = '\r\n'
    buffer = []
    for (key, value) in fields:
        buffer.append('--%s' % BOUNDARY)
        buffer.append('Content-Disposition: form-data; name="%s"' % key)
        buffer.append('')
        buffer.append(value.decode('utf-8'))

    buffer.append('--%s--' % BOUNDARY)
    buffer.append('')
    body = CRLF.join(buffer)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return (
     content_type, body)


class Dispatcher(object):
    """The XMPP/HTTP dispatcher class."""

    def __init__(self, address):
        """Initializes the dispatcher."""
        self.address = address

    def __call__(self, conn, message):
        """The dispatcher function."""
        post_multipart('http://%s/_ah/xmpp/message/chat/' % self.address, [
         (
          'body', unicode(message.getBody()).encode('utf-8')),
         (
          'from', unicode(message.getFrom())),
         (
          'stanza', unicode(message).encode('utf-8')),
         (
          'to', unicode(message.getTo()))])


def loop(conn):
    """The main loop."""

    def process():
        try:
            conn.Process(1)
        except KeyboardInterrupt:
            return 0

        return 1

    while process():
        pass


def main():
    """The main function."""
    op = optparse.OptionParser(description=DESCRIPTION, usage=USAGE)
    op.add_option('-a', '--address', dest='address', metavar='HOST:PORT', help='the application host and port', default='localhost:8770')
    op.add_option('-j', '--jid', dest='jid', metavar='JID', help='use this Jabber ID', default='demo@localhost')
    op.add_option('-p', '--password', dest='password', metavar='PASSWORD', help='use this password', default='demo')
    (options, args) = op.parse_args()
    logging.basicConfig(format='%(levelname)-8s %(asctime)s %(filename)s:%(lineno)s] %(message)s', level=logging.DEBUG)
    jid = xmpp.JID(options.jid)
    user, server, password = jid.getNode(), jid.getDomain(), options.password
    client = xmpp.Client(server, debug=[])
    for i in range(5):
        conn = client.connect()
        if conn:
            break
        logging.warning("Retrying to connect to server '%s'" % server)
        time.sleep(5)

    if not conn:
        logging.error("Unable to connect to server '%s'" % server)
        sys.exit(2)
    if conn != 'tls':
        logging.warning('Unable to estabilish secure connection - TLS failed')
    auth = client.auth(user, password)
    if not auth:
        logging.error('Authentication on %s failed' % server)
        sys.exit(1)
    if auth != 'sasl':
        logging.warning('SASL authentication on %s failed' % server)
    client.RegisterHandler('message', Dispatcher(options.address))
    client.sendInitPresence()
    loop(client)


if __name__ == '__main__':
    main()