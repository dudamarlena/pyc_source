# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelagenthypervisorgeolocalization/geoloc.py
# Compiled at: 2013-03-20 13:50:16
import httplib, xmpp
from archipelcore.archipelPlugin import TNArchipelPlugin
from archipelcore.utils import build_error_iq
ARCHIPEL_NS_HYPERVISOR_GEOLOC = 'archipel:hypervisor:geolocalization'
ARCHIPEL_ERROR_CODE_LOCALIZATION_GET = -9001

class TNHypervisorGeolocalization(TNArchipelPlugin):
    """
    This plugin allow to geolocalize the hypervisor.
    """

    def __init__(self, configuration, entity, entry_point_group):
        """
        Initialize the module.
        @type configuration: Configuration object
        @param configuration: the configuration
        @type entity: L{TNArchipelEntity}
        @param entity: the entity that owns the plugin
        @type entry_point_group: string
        @param entry_point_group: the group name of plugin entry_point
        """
        TNArchipelPlugin.__init__(self, configuration=configuration, entity=entity, entry_point_group=entry_point_group)
        self.plugin_deactivated = False
        try:
            mode = self.configuration.get('GEOLOCALIZATION', 'localization_mode')
            lat = ''
            lon = ''
            if mode == 'auto':
                service = self.configuration.get('GEOLOCALIZATION', 'localization_service_url')
                request = self.configuration.get('GEOLOCALIZATION', 'localization_service_request')
                method = self.configuration.get('GEOLOCALIZATION', 'localization_service_method')
                conn = httplib.HTTPConnection(service)
                conn.request(method, request)
                data_node = xmpp.simplexml.NodeBuilder(data=str(conn.getresponse().read())).getDom()
                lat = data_node.getTagData('Latitude')
                lon = data_node.getTagData('Longitude')
            else:
                lat = self.configuration.getfloat('GEOLOCALIZATION', 'localization_latitude')
                lon = self.configuration.getfloat('GEOLOCALIZATION', 'localization_longitude')
            string = '<gelocalization><Latitude>' + str(lat) + '</Latitude>\n<Longitude>' + str(lon) + '</Longitude></gelocalization>'
            self.localization_information = xmpp.simplexml.NodeBuilder(data=string).getDom()
            registrar_item = {'commands': ['where are you', 'localize'], 'parameters': {}, 'method': self.message_get, 
               'permissions': [
                             'geolocalization_get'], 
               'description': 'give my the latitude and longitude.'}
            self.entity.add_message_registrar_item(registrar_item)
            self.entity.permission_center.create_permission('geolocalization_get', 'Authorizes user to get the entity location coordinates', False)
        except Exception, ex:
            self.plugin_deactivated = True
            self.entity.log.error('Cannot initialize geolocalization. plugin deactivated. Exception: %s' % str(ex))

    def register_handlers(self):
        """
        This method will be called by the plugin user when it will be
        necessary to register module for listening to stanza.
        """
        if self.plugin_deactivated:
            return
        self.entity.xmppclient.RegisterHandler('iq', self.process_iq, ns=ARCHIPEL_NS_HYPERVISOR_GEOLOC)

    def unregister_handlers(self):
        """
        Unregister the handlers.
        """
        if self.plugin_deactivated:
            return
        self.entity.xmppclient.UnregisterHandler('iq', self.process_iq, ns=ARCHIPEL_NS_HYPERVISOR_GEOLOC)

    @staticmethod
    def plugin_info():
        """
        Return informations about the plugin.
        @rtype: dict
        @return: dictionary contaning plugin informations
        """
        plugin_friendly_name = 'Hypervisor Geolocalization'
        plugin_identifier = 'geolocalization'
        plugin_configuration_section = 'GEOLOCALIZATION'
        plugin_configuration_tokens = ['localization_mode',
         'localization_latitude',
         'localization_longitude',
         'localization_service_url',
         'localization_service_request',
         'localization_service_method',
         'localization_service_response_root_node']
        return {'common-name': plugin_friendly_name, 'identifier': plugin_identifier, 
           'configuration-section': plugin_configuration_section, 
           'configuration-tokens': plugin_configuration_tokens}

    def process_iq(self, conn, iq):
        """
        This method is invoked when a ARCHIPEL_NS_HYPERVISOR_GEOLOC IQ is received.
        It understands IQ of type:
            - get
        @type conn: xmpp.Dispatcher
        @param conn: ths instance of the current connection that send the stanza
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        """
        reply = None
        action = self.entity.check_acp(conn, iq)
        self.entity.check_perm(conn, iq, action, -1, prefix='geolocalization_')
        if action == 'get':
            reply = self.iq_get(iq)
        if reply:
            conn.send(reply)
            raise xmpp.protocol.NodeProcessed
        return

    def iq_get(self, iq):
        """
        Return the geolocalization information.
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        """
        reply = iq.buildReply('result')
        try:
            reply.setQueryPayload([self.localization_information])
        except Exception, ex:
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_LOCALIZATION_GET)

        return reply

    def message_get(self, msg):
        """
        Return the geolocalization information asked by message.
        @type msg: xmpp.Protocol.Message
        @param msg: the received message
        @rtype: string
        @return: string containing the answer to send
        """
        lat = self.localization_information.getTagData('Latitude')
        lon = self.localization_information.getTagData('Longitude')
        return "I'm localized at longitude: %s latitude: %s" % (lon, lat)