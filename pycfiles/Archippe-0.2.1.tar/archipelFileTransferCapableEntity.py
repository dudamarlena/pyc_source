# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelcore/archipelFileTransferCapableEntity.py
# Compiled at: 2013-03-20 13:50:16
import xmpp, socket, hashlib
from archipelcore.utils import build_error_iq

class TNFileTransferCapableEntity(object):
    """
    This class allow ArchipelEntity to handle file transfer.
    ** This is work in progress. It's not working for now **
    """

    def __init__(self, jid, xmppclient, permission_center, log):
        """
        Initialize the TNFileTransferCapableEntity.
        @type jid: string
        @param jid: the JID of the current entity
        @type xmppclient: xmpp.Dispatcher
        @param xmppclient: the entity xmpp client
        @type permission_center: TNPermissionCenter
        @param permission_center: the permission center of the entity
        @type log: TNArchipelLog
        @param log: the logger of the entity
        """
        self.xmppclient = xmppclient
        self.permission_center = permission_center
        self.jid = jid
        self.log = log
        self.current_sids = {}

    def check_acp(conn, iq):
        """
        Function that verify if the ACP is valid.
        @type conn: xmpp.Dispatcher
        @param conn: the connection
        @type iq: xmpp.Protocol.Iq
        @param iq: the IQ to check
        @raise Exception: Exception if not implemented
        """
        raise Exception('Subclass of TNFileTransferCapableEntity must implement check_acp.')

    def check_perm(self, conn, stanza, action_name, error_code=-1, prefix=''):
        """
        function that verify if the permissions are granted
        @type conn: xmpp.Dispatcher
        @param conn: the connection
        @type stanza: xmpp.Node
        @param stanza: the stanza containing the action
        @type action_name: string
        @param action_name: the action to check
        @type error_code: int
        @param error_code: the error code to return
        @type prefix: string
        @param prefix: the prefix of the action
        @raise Exception: Exception if not implemented
        """
        raise Exception('Subclass of TNFileTransferCapableEntity must implement check_perm.')

    def init_permissions(self):
        """
        Initialize the tag permissions.
        """
        self.permission_center.create_permission('sendfiles', 'Authorizes users to send files to entity', False)

    def register_handlers(self):
        """
        Initialize the handlers for tags.
        """
        pass

    def unregister_handlers(self):
        """
        Unregister the handlers for tags.
        """
        pass

    def process_disco_request(self, conn, iq):
        """
        This method is invoked when a http://jabber.org/protocol/disco#info IQ is received.
        @type conn: xmpp.Dispatcher
        @param conn: ths instance of the current connection that send the stanza
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        """
        reply = iq.buildReply('result')
        reply.getTag('query').addChild('identity', attrs={'category': 'client', 'type': 'pc'})
        reply.getTag('query').addChild('feature', attrs={'var': 'http://jabber.org/protocol/bytestreams'})
        conn.send(reply)
        raise xmpp.protocol.NodeProcessed

    def process_si_request(self, conn, iq):
        """
        This method is invoked when a http://jabber.org/protocol/si IQ is received.
        @type conn: xmpp.Dispatcher
        @param conn: ths instance of the current connection that send the stanza
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        """
        if not iq.getTag('si').getAttr('profile') == 'http://jabber.org/protocol/si/profile/file-transfer':
            return
        self.check_perm(conn, iq, 'sendfiles', -1)
        file_name = iq.getTag('si').getTag('file').getAttr('name')
        file_size = iq.getTag('si').getTag('file').getAttr('size')
        sender_jid = iq.getFrom()
        sid = iq.getTag('si').getAttr('id')
        self.current_sids[sid] = {'name': file_name, 'size': file_size, 'sender': sender_jid}
        reply = iq.buildReply('result')
        node_feature = reply.getTag('si').addChild('feature', namespace='http://jabber.org/protocol/feature-neg')
        node_x = node_feature.addChild('x', namespace='jabber:x:data', attrs={'type': 'submit'})
        node_field = node_x.addChild('field', attrs={'var': 'stream-method'})
        node_value = node_field.addChild('value')
        node_value.setData('http://jabber.org/protocol/bytestreams')
        self.log.info('file system request from %s: %s (%s bytes)' % (sender_jid, file_name, file_size))
        conn.send(reply)
        raise xmpp.protocol.NodeProcessed

    def process_bytestream_request(self, conn, iq):
        """
        This method is invoked when a http://jabber.org/protocol/bytestreams IQ is received.
        @type conn: xmpp.Dispatcher
        @param conn: ths instance of the current connection that send the stanza
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        """
        remote_host = iq.getTag('query').getTag('streamhost').getAttr('host')
        remote_port = iq.getTag('query').getTag('streamhost').getAttr('port')
        sid = iq.getTag('query').getAttr('sid')
        sock_host = '%s%s%s' % (sid, str(iq.getFrom()), str(iq.getTo()))
        sha1_hash = hashlib.sha1(sock_host).hexdigest()
        print 'HASH %s' % sha1_hash
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((remote_host, int(remote_port)))
        s.send('\x05\x01\x00\x03\x03%s%s\x00\x00' % (chr(len(sha1_hash)), sha1_hash))
        data = s.recv(2)
        resp = iq.buildReply('result')
        resp.getTag('query').addChild('streamhost-used', attrs={'jid': str(iq.getFrom())})
        self.xmppclient.send(resp)
        raise xmpp.protocol.NodeProcessed