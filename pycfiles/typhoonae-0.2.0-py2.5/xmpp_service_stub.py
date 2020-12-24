# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/typhoonae/xmpp/xmpp_service_stub.py
# Compiled at: 2010-12-12 04:36:57
"""XMPP service API stub using ejabberd."""
import google.appengine.api.apiproxy_stub, google.appengine.api.xmpp.xmpp_service_pb, logging, os, xmpp
NO_ERROR = google.appengine.api.xmpp.xmpp_service_pb.XmppMessageResponse.NO_ERROR

class XmppServiceStub(google.appengine.api.apiproxy_stub.APIProxyStub):
    """XMPP service stub."""

    def __init__(self, log=logging.info, host='localhost', service_name='xmpp'):
        """Initializer.

        Args:
            log: A logger, used for dependency injection.
            host: Hostname of the XMPP service.
            service_name: Service name expected for all calls.
        """
        super(XmppServiceStub, self).__init__(service_name)
        self.log = log
        self.host = host

    def do_action(self, action, request):
        """Establishes the xmpp connection and makes an action.

        Args:
            action: A callable with client as first argument.
            request: The request.
        """
        jid = xmpp.protocol.JID(self._GetFrom(request.from_jid()))
        client = xmpp.Client(jid.getDomain(), debug=[])
        client.connect()
        node = jid.getNode()
        client.auth(node, node)
        result = action(client)
        client.disconnect()
        return result

    def _Dynamic_GetPresence(self, request, response):
        """Implementation of XmppService::GetPresence.

        Returns online.

        Args:
            request: A PresenceRequest.
            response: A PresenceResponse.
        """
        response.set_is_available(True)

    def _Dynamic_SendMessage(self, request, response):
        """Implementation of XmppService::SendMessage.

        Args:
            request: An XmppMessageRequest.
            response: An XmppMessageResponse .
        """

        def action(client):
            for to_jid in request.jid_list():
                client.send(xmpp.protocol.Message(to_jid, request.body()))
                response.add_status(NO_ERROR)

        self.do_action(action, request)

    def _Dynamic_SendInvite(self, request, response):
        """Implementation of XmppService::SendInvite.

        Args:
            request: An XmppInviteRequest.
            response: An XmppInviteResponse .
        """

        def action(client):
            roster = client.getRoster()
            roster.Subscribe(request.jid())

        self.do_action(action, request)

    def _GetFrom(self, requested):
        """Validates that the from JID is valid.

        Args:
            requested: The requested from JID.

        Returns:
            string, The from JID.

        Raises:
            xmpp.InvalidJidError if the requested JID is invalid.
        """
        appid = os.environ['APPLICATION_ID']
        return '%s@%s' % (appid, self.host)