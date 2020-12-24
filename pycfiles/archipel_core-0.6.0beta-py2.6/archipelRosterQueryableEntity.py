# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelcore/archipelRosterQueryableEntity.py
# Compiled at: 2013-03-20 13:50:16
import xmpp
from archipelcore.utils import build_error_iq
ARCHIPEL_ERROR_CODE_GET_ROSTER = -450001
ARCHIPEL_NS_ROSTER = 'archipel:roster'

class TNRosterQueryableEntity(object):
    """
    TODO ADD description here
    """

    def __init__(self, configuration, permission_center, xmppclient, log):
        """
        Initialize the TNRosterQueryableEntity.
        @type configuration: configuration object
        @param configuration: the configuration
        @type permission_center: TNPermissionCenter
        @param permission_center: the permission center of the entity
        @type xmppclient: xmpp.Dispatcher
        @param xmppclient: the entity xmpp client
        @type log: TNArchipelLog
        @param log: the logger of the entity
        """
        self.configuration = configuration
        self.permission_center = permission_center
        self.xmppclient = xmppclient
        self.log = log

    def check_acp(conn, iq):
        """
        Function that verify if the ACP is valid.
        @type conn: xmpp.Dispatcher
        @param conn: the connection
        @type iq: xmpp.Protocol.Iq
        @param iq: the IQ to check
        @raise Exception: Exception if not implemented
        """
        raise Exception('Subclass of TNRosterQueryableEntity must implement check_acp.')

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
        raise Exception('Subclass of TNRosterQueryableEntity must implement check_perm')

    def init_vocabulary(self):
        """
        Initialize the vocabulary.
        """
        item = {'commands': ['roster', 'users'], 'parameters': [], 'permissions': [
                         'roster'], 
           'method': self.message_roster, 
           'description': "I'll give you the content of my roster"}
        self.add_message_registrar_item(item)

    def init_permissions(self):
        """
        Initialize the permissions.
        """
        self.permission_center.create_permission('roster', 'Authorizes users to get the content of my roster', False)

    def register_handlers(self):
        """
        initialize the avatar handlers
        """
        self.xmppclient.RegisterHandler('iq', self.process_roster_iq, ns=ARCHIPEL_NS_ROSTER)

    def unregister_handlers(self):
        """
        initialize the avatar handlers
        """
        self.xmppclient.UnregisterHandler('iq', self.process_roster_iq, ns=ARCHIPEL_NS_ROSTER)

    def process_roster_iq(self, conn, iq):
        """
        This method is invoked when a ARCHIPEL_NS_ROSTER IQ is received.
        It understands IQ of type:
            - getroster
        @type conn: xmpp.Dispatcher
        @param conn: ths instance of the current connection that send the stanza
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        """
        reply = None
        action = self.check_acp(conn, iq)
        self.check_perm(conn, iq, action, -1)
        if action == 'getroster':
            reply = self.iq_get_roster(iq)
        if reply:
            conn.send(reply)
            raise xmpp.protocol.NodeProcessed
        return

    def iq_get_roster(self, iq):
        """
        Return the content of the roster.
        @type iq: xmpp.Protocol.Iq
        @param iq: the IQ containing the request
        """
        try:
            reply = iq.buildReply('result')
        except Exception, ex:
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_GET_ROSTER)

        return reply

    def message_roster(self, msg):
        """
        Handle roster asking message.
        @type msg: xmpp.Protocol.Message
        @param msg: the received message
        @rtype: xmpp.Protocol.Message
        @return: a ready to send Message containing the result of the action
        """
        ret = 'Here is the content of my roster : \n'
        for barejid in self.roster.getItems():
            if self.jid.getStripped() == barejid:
                continue
            ret = '%s    - %s\n' % (ret, barejid)

        return ret