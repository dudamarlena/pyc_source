# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/archipelagentvirtualmachinesnapshoting/snapshoting.py
# Compiled at: 2013-03-20 13:50:16
import libvirt, xmpp
from archipelcore.archipelPlugin import TNArchipelPlugin
from archipel.archipelVirtualMachine import ARCHIPEL_ERROR_CODE_VM_MIGRATING
from archipelcore.utils import build_error_iq
from archipel.archipelLibvirtEntity import ARCHIPEL_NS_LIBVIRT_GENERIC_ERROR
ARCHIPEL_NS_SNAPSHOTING = 'archipel:virtualmachine:snapshoting'
ARCHIPEL_ERROR_CODE_SNAPSHOT_TAKE = -2001
ARCHIPEL_ERROR_CODE_SNAPSHOT_GET = -2002
ARCHIPEL_ERROR_CODE_SNAPSHOT_CURRENT = -2003
ARCHIPEL_ERROR_CODE_SNAPSHOT_DELETE = -2004
ARCHIPEL_ERROR_CODE_SNAPSHOT_REVERT = -2005
ARCHIPEL_ERROR_CODE_SNAPSHOT_NO_DRIVE = -2006

class TNSnapshoting(TNArchipelPlugin):

    def __init__(self, configuration, entity, entry_point_group):
        """
        Initialize the plugin.
        @type configuration: Configuration object
        @param configuration: the configuration
        @type entity: L{TNArchipelEntity}
        @param entity: the entity that owns the plugin
        @type entry_point_group: string
        @param entry_point_group: the group name of plugin entry_point
        """
        TNArchipelPlugin.__init__(self, configuration=configuration, entity=entity, entry_point_group=entry_point_group)
        self.entity.permission_center.create_permission('snapshot_take', 'Authorizes user to get take a snapshot', False)
        self.entity.permission_center.create_permission('snapshot_delete', 'Authorizes user to delete a snapshot', False)
        self.entity.permission_center.create_permission('snapshot_get', 'Authorizes user to get all snapshots', False)
        self.entity.permission_center.create_permission('snapshot_current', 'Authorizes user to get current used snapshot', False)
        self.entity.permission_center.create_permission('snapshot_revert', 'Authorizes user to revert to a snapshot', False)

    def register_handlers(self):
        """
        This method will be called by the plugin user when it will be
        necessary to register module for listening to stanza.
        """
        self.entity.xmppclient.RegisterHandler('iq', self.process_iq, ns=ARCHIPEL_NS_SNAPSHOTING)

    def unregister_handlers(self):
        """
        Unregister the handlers.
        """
        self.entity.xmppclient.UnregisterHandler('iq', self.process_iq, ns=ARCHIPEL_NS_SNAPSHOTING)

    @staticmethod
    def plugin_info():
        """
        Return informations about the plugin.
        @rtype: dict
        @return: dictionary contaning plugin informations
        """
        plugin_friendly_name = 'Virtual Machine Snapshoting'
        plugin_identifier = 'snapshoting'
        plugin_configuration_section = None
        plugin_configuration_tokens = None
        return {'common-name': plugin_friendly_name, 'identifier': plugin_identifier, 
           'configuration-section': plugin_configuration_section, 
           'configuration-tokens': plugin_configuration_tokens}

    def process_iq(self, conn, iq):
        """
        This method is invoked when a ARCHIPEL_NS_SNAPSHOTING IQ is received.
        It understands IQ of type:
            - take
            - delete
            - get
            - current
            - revert
        @type conn: xmpp.Dispatcher
        @param conn: ths instance of the current connection that send the stanza
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        """
        reply = None
        action = self.entity.check_acp(conn, iq)
        self.entity.check_perm(conn, iq, action, -1, prefix='snapshot_')
        if not self.entity.domain:
            raise xmpp.protocol.NodeProcessed
        if self.entity.is_migrating and action not in ('current', 'get'):
            reply = build_error_iq(self, "Virtual machine is migrating. Can't perform any snapshoting operation.", iq, ARCHIPEL_ERROR_CODE_VM_MIGRATING)
        elif action == 'take':
            reply = self.iq_take(iq)
        elif action == 'delete':
            reply = self.iq_delete(iq)
        elif action == 'get':
            reply = self.iq_get(iq)
        elif action == 'current':
            reply = self.iq_getcurrent(iq)
        elif action == 'revert':
            reply = self.iq_revert(iq)
        if reply:
            conn.send(reply)
            raise xmpp.protocol.NodeProcessed
        return

    def iq_take(self, iq):
        """
        Creating a snapshot.
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        @rtype: xmpp.Protocol.Iq
        @return: a ready to send IQ containing the result of the action
        """
        reply = iq.buildReply('result')
        try:
            xmlDesc = iq.getTag('query').getTag('archipel').getTag('domainsnapshot')
            name = xmlDesc.getTag('name').getData()
            old_status = self.entity.xmppstatus
            old_show = self.entity.xmppstatusshow
            try:
                devices_node = self.entity.definition.getTag('devices')
                disk_nodes = devices_node.getTags('disk', attrs={'type': 'file'})
                if not disk_nodes:
                    raise
            except:
                return build_error_iq(self, Exception("Virtual machine hasn't any drive to snapshot."), iq, code=ARCHIPEL_ERROR_CODE_SNAPSHOT_NO_DRIVE)

            self.entity.log.info('Creating snapshot with name %s desc :%s' % (name, xmlDesc))
            self.entity.change_presence(presence_show='dnd', presence_status='Snapshoting...')
            self.entity.domain.snapshotCreateXML(str(xmlDesc), 0)
            self.entity.change_presence(presence_show=old_show, presence_status=old_status)
            self.entity.log.info('Snapshot with name %s created' % name)
            self.entity.push_change('snapshoting', 'taken')
            self.entity.shout('Snapshot', "I've created a snapshot named %s as asked by %s" % (name, iq.getFrom()))
        except libvirt.libvirtError, ex:
            self.entity.change_presence(presence_show=old_show, presence_status='Error while snapshoting')
            reply = build_error_iq(self, ex, iq, ex.get_error_code(), ns=ARCHIPEL_NS_LIBVIRT_GENERIC_ERROR)
            try:
                snapshotObject = self.entity.domain.snapshotLookupByName(name, 0)
                snapshotObject.delete(libvirt.VIR_DOMAIN_SNAPSHOT_DELETE_CHILDREN)
            except:
                pass

        except Exception, ex:
            self.entity.change_presence(presence_show=old_show, presence_status='Error while snapshoting')
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_SNAPSHOT_TAKE)
            try:
                snapshotObject = self.entity.domain.snapshotLookupByName(name, 0)
                snapshotObject.delete(libvirt.VIR_DOMAIN_SNAPSHOT_DELETE_CHILDREN)
            except:
                pass

        return reply

    def iq_get(self, iq):
        """
        List all snapshots.
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        @rtype: xmpp.Protocol.Iq
        @return: a ready to send IQ containing the result of the action
        """
        try:
            reply = iq.buildReply('result')
            nodes = []
            if self.entity.domain.hasCurrentSnapshot(0):
                snapshot_names = self.entity.domain.snapshotListNames(0)
                for snapshot_name in snapshot_names:
                    snapshotObject = self.entity.domain.snapshotLookupByName(snapshot_name, 0)
                    desc = snapshotObject.getXMLDesc(0)
                    n = xmpp.simplexml.NodeBuilder(data=desc).getDom()
                    nodes.append(n)

            reply.setQueryPayload(nodes)
        except libvirt.libvirtError, ex:
            reply = build_error_iq(self, ex, iq, ex.get_error_code(), ns=ARCHIPEL_NS_LIBVIRT_GENERIC_ERROR)
        except Exception, ex:
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_SNAPSHOT_GET)

        return reply

    def iq_getcurrent(self, iq):
        """
        Return current snapshot.
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        @rtype: xmpp.Protocol.Iq
        @return: a ready to send IQ containing the result of the action
        """
        try:
            reply = iq.buildReply('result')
            if self.entity.domain.hasCurrentSnapshot(0):
                snapshotObject = self.entity.domain.snapshotCurrent(0)
                desc = snapshotObject.getXMLDesc(0)
                n = xmpp.simplexml.NodeBuilder(data=desc).getDom()
                reply.setQueryPayload([n])
        except libvirt.libvirtError, ex:
            if ex.get_error_code() == libvirt.VIR_ERR_NO_DOMAIN_SNAPSHOT:
                reply = iq.buildReply('result')
            else:
                reply = build_error_iq(self, ex, iq, ex.get_error_code(), ns=ARCHIPEL_NS_LIBVIRT_GENERIC_ERROR)
        except Exception, ex:
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_SNAPSHOT_CURRENT)

        return reply

    def iq_delete(self, iq):
        """
        Delete snapshot.
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        @rtype: xmpp.Protocol.Iq
        @return: a ready to send IQ containing the result of the action
        """
        try:
            reply = iq.buildReply('result')
            name = iq.getTag('query').getTag('archipel').getAttr('name')
            old_status = self.entity.xmppstatus
            old_show = self.entity.xmppstatusshow
            self.entity.log.info('Deleting snapshot with name %s' % name)
            self.entity.change_presence(presence_show='dnd', presence_status='Removing snapshot...')
            snapshotObject = self.entity.domain.snapshotLookupByName(name, 0)
            snapshotObject.delete(libvirt.VIR_DOMAIN_SNAPSHOT_DELETE_CHILDREN)
            self.entity.change_presence(presence_show=old_show, presence_status=old_status)
            self.entity.log.info('Snapshot with name %s deleted.' % name)
            self.entity.push_change('snapshoting', 'deleted')
            self.entity.shout('Snapshot', "I've deleted the snapshot named %s as asked by %s" % (name, iq.getFrom()))
        except libvirt.libvirtError, ex:
            self.entity.change_presence(presence_show=old_show, presence_status='Error while deleting snapshot.')
            reply = build_error_iq(self, ex, iq, ex.get_error_code(), ns=ARCHIPEL_NS_LIBVIRT_GENERIC_ERROR)
        except Exception, ex:
            self.entity.change_presence(presence_show=old_show, presence_status='Error while deleting snapshot.')
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_SNAPSHOT_DELETE)

        return reply

    def iq_revert(self, iq):
        """
        Restore from a snapshot.
        @type iq: xmpp.Protocol.Iq
        @param iq: the received IQ
        @rtype: xmpp.Protocol.Iq
        @return: a ready to send IQ containing the result of the action
        """
        try:
            reply = iq.buildReply('result')
            name = iq.getTag('query').getTag('archipel').getAttr('name')
            old_show = self.entity.xmppstatusshow
            old_status = self.entity.xmppstatus
            self.entity.log.info('Restoring snapshot with name %s' % name)
            self.entity.change_presence(presence_show='dnd', presence_status='Restoring snapshot...')
            snapshotObject = self.entity.domain.snapshotLookupByName(name, 0)
            self.entity.domain.revertToSnapshot(snapshotObject, 0)
            self.entity.change_presence(presence_show=old_show, presence_status=old_status)
            self.entity.log.info('Reverted to snapshot with name %s ' % name)
            self.entity.push_change('snapshoting', 'restored')
            self.entity.shout('Snapshot', "I've been reverted to the snapshot named %s as asked by %s" % (name, iq.getFrom()))
        except libvirt.libvirtError, ex:
            self.entity.change_presence(presence_show=old_show, presence_status='Error while reverting.')
            reply = build_error_iq(self, ex, iq, ex.get_error_code(), ns=ARCHIPEL_NS_LIBVIRT_GENERIC_ERROR)
        except Exception, ex:
            self.entity.change_presence(presence_show=old_show, presence_status='Error while reverting.')
            reply = build_error_iq(self, ex, iq, ARCHIPEL_ERROR_CODE_SNAPSHOT_REVERT)

        return reply