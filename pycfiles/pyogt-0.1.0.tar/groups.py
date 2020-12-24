# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/groups.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from logging import getLogger
import re
from eventlet import api
from pyogp.lib.base.datatypes import UUID, Vector3
from pyogp.lib.client.exc import DataParsingError
from pyogp.lib.base.helpers import Wait
from pyogp.lib.client.datamanager import DataManager
from pyogp.lib.base.message.message import Message, Block
from pyogp.lib.client.enums import ImprovedIMDialogue
logger = getLogger('pyogp.lib.client.groups')

class GroupManager(DataManager):
    """ a storage bin for groups

    also, a functional area for group creation operations
    """
    __module__ = __name__

    def __init__(self, agent, settings=None):
        """ initialize the group manager """
        super(GroupManager, self).__init__(agent, settings)
        self.group_store = []
        if self.settings.LOG_VERBOSE:
            logger.debug('Initialized the Group Manager')

    def enable_callbacks(self):
        """enables the callback handlers for this GroupManager"""
        onAgentGroupDataUpdate_received = self.agent.region.message_handler.register('AgentGroupDataUpdate')
        onAgentGroupDataUpdate_received.subscribe(self.onAgentGroupDataUpdate)
        onChatterBoxInvitation_received = self.agent.region.message_handler.register('ChatterBoxInvitation')
        onChatterBoxInvitation_received.subscribe(self.onChatterBoxInvitation_Message)
        onChatterBoxSessionEventReply_received = self.agent.region.message_handler.register('ChatterBoxSessionEventReply')
        onChatterBoxSessionEventReply_received.subscribe(self.onChatterBoxSessionEventReply)
        onChatterBoxSessionAgentListUpdates_received = self.agent.region.message_handler.register('ChatterBoxSessionAgentListUpdates')
        onChatterBoxSessionAgentListUpdates_received.subscribe(self.onChatterBoxSessionAgentListUpdates)
        onChatterBoxSessionStartReply_received = self.agent.region.message_handler.register('ChatterBoxSessionStartReply')
        onChatterBoxSessionStartReply_received.subscribe(self.onChatterBoxSessionStartReply)

    def handle_group_chat(self, message):
        """ process a ChatterBoxInvitation_Message instance"""
        group = [ group for group in self.group_store if str(message['Message_Data'][0]['session_id']) == str(group.GroupID) ]
        if group != []:
            group[0].handle_inbound_chat(message)
        else:
            logger.warning('Received group chat message from unknown group. Group: %s. Agent: %s. Message: %s' % (message['Message_Data'][0]['session_name'], message['Message_Data'][0]['from_name'], message['Message_Data'][0]['instantmessage']['message_params']['message']))

    def store_group(self, _group):
        """ append to or replace a group in self.group_store """
        try:
            index = [ self.group_store.index(_group_) for _group_ in self.group_store if _group_.ID == _group.GroupID ]
            self.group_store[index[0]] = _group
            if self.settings.LOG_VERBOSE:
                logger.debug("Replacing a stored group: '%s'" % _group.GroupID)
        except:
            self.group_store.append(_group)
            if self.settings.LOG_VERBOSE:
                logger.debug("Stored a new group: '%s'" % _group.GroupID)

    def update_group(self, group_data):
        """ accepts a dictionary of group data and creates/updates a group """
        group = [ group for group in self.group_store if str(group_data['GroupID']) == str(group.GroupID) ]
        if group != []:
            group[0].update_properties(group_data)
            if self.settings.LOG_VERBOSE:
                logger.debug("Updating a stored group: '%s'" % group[0].GroupID)
        else:
            group = Group(GroupID=group_data['GroupID'], GroupPowers=group_data['GroupPowers'], AcceptNotices=group_data['AcceptNotices'], GroupInsigniaID=group_data['GroupInsigniaID'], Contribution=group_data['Contribution'], GroupName=group_data['GroupName'], agent=self.agent)
            self.store_group(group)

    def update_group_by_name(self, group_data, name):
        """ accepts a dictionary of group data and creates/updates a group """
        pattern = re.compile(name)
        group = [ group for group in self.group_store if pattern.match(group.GroupName) ]
        if group != []:
            group[0].update_properties(group_data)
            if self.settings.LOG_VERBOSE:
                logger.debug("Updating a stored group: '%s'" % group[0].GroupName)
        else:
            logger.info('Received an update for an unknown group for name: %s' % name)

    def update_group_by_session_id(self, group_data):
        """ accepts a dictionary of group data and creates/updates a group """
        group = [ group for group in self.group_store if str(group.session_id) == str(group_data['session_id']) ]
        if group != []:
            group[0].update_properties(group_data)
            if self.settings.LOG_VERBOSE:
                logger.debug("Updating a stored group: '%s'" % group[0].GroupName)
        else:
            logger.info('Received an update for an unknown group with a session id of: %s' % str(group_data['session_id']))

    def create_group(self, AgentID=None, SessionID=None, Name=None, Charter='', ShowInList=True, InsigniaID=UUID(), MembershipFee=0, OpenEnrollment=False, AllowPublish=False, MaturePublish=False):
        """ sends a message to the agent's current region requesting to create a group

        enables a callback (which should be unsubscribed from once we get a response)
        """
        if Name != None:
            logger.info("Sending a request to create group with a name of '%s'" % Name)
            if AgentID == None:
                AgentID = self.agent.agent_id
            if SessionID == None:
                SessionID = self.agent.session_id
            packet = Message('CreateGroupRequest', Block('AgentData', AgentID=AgentID, SessionID=SessionID), Block('GroupData', Name=Name, Charter=Charter, ShowInList=ShowInList, InsigniaID=InsigniaID, MembershipFee=MembershipFee, OpenEnrollment=OpenEnrollment, AllowPublish=AllowPublish, MaturePublish=MaturePublish))
            self.agent.region.enqueue_message(packet, True)
            self.onCreateGroupReply_received = self.agent.region.message_handler.register('CreateGroupReply')
            self.onCreateGroupReply_received.subscribe(self.onCreateGroupReply)
        else:
            raise DataParsingError('Failed to create a group, please specify a name')
        return

    def get_group(self, GroupID=None):
        """ searches the store and returns group if stored, None otherwise """
        group = [ group for group in self.group_store if str(group.GroupID) == str(GroupID) ]
        if group == []:
            return
        else:
            return group[0]
        return

    def get_group_by_name(self, GroupName=None):
        """ searches the store and returns group if stored, None otherwise """
        group = [ group for group in self.group_store if str(group.GroupName) == str(GroupName) ]
        if group == []:
            return
        else:
            return group[0]
        return

    def join_group(self, group_id):
        """ sends a JoinGroupRequest packet for the specified uuid """
        self.onJoinGroupReply_received = self.agent.message_handler.register('JoinGroupReply')
        self.onJoinGroupReply_received.subscribe(self.onJoinGroupReply)
        self.send_JoinGroupRequest(self.agent.agent_id, self.agent.session_id, group_id)

    def send_JoinGroupRequest(self, agent_id, session_id, group_id):
        """ sends a JoinGroupRequest message to the hsot simulator """
        packet = Message('JoinGroupRequest', Block('AgentData', AgentID=AgentID, SessionID=SessionID), Block('GroupData', GroupID=group_id))
        self.agent.region.enqueue_message(packet, True)

    def activate_group(self, group_id):
        """ set a particular group as active """
        self.send_ActivateGroup(self.agent.agent_id, self.agent.session_id, group_id)

    def send_ActivateGroup(self, agent_id, session_id, group_id):
        """ sends an ActivateGroup message to the host simulator """
        packet = Message('ActivateGroup', Block('AgentData', AgentID=agent_id, SessionID=session_id, GroupID=group_id))
        self.agent.region.enqueue_message(packet)

    def onCreateGroupReply(self, packet):
        """ when we get a CreateGroupReply packet, log Success, and if True, request the group details. remove the callback in any case """
        self.onCreateGroupReply_received.unsubscribe(self.onCreateGroupReply)
        AgentID = packet['AgentData'][0]['AgentID']
        GroupID = packet['ReplyData'][0]['GroupID']
        Success = packet['ReplyData'][0]['Success']
        _Message = packet['ReplyData'][0]['Message']
        if Success:
            logger.info('Created group %s. Message data is: %s' % (GroupID, _Message))
            logger.warning('We now need to request the group data...')
        else:
            logger.warning('Failed to create group due to: %s' % _Message)

    def onJoinGroupReply(self, packet):
        """ the simulator tells us if joining a group was a success. """
        self.onJoinGroupReply_received.unsubscribe(self.onJoinGroupReply)
        AgentID = packet['AgentData'][0]['AgentID']
        GroupID = packet['GroupData'][0]['GroupID']
        Success = packet['GroupData'][0]['Success']
        if Success:
            logger.info('Joined group %s' % GroupID)
        else:
            logger.warning('Failed to join group %s' % GroupID)

    def onAgentGroupDataUpdate(self, packet):
        """ deal with the data that comes in over the event queue """
        group_data = {}
        AgentID = packet['AgentData'][0]['AgentID']
        for GroupData_block in packet['GroupData']:
            group_data['GroupID'] = GroupData_block['GroupID']
            group_data['GroupPowers'] = GroupData_block['GroupPowers']
            group_data['AcceptNotices'] = GroupData_block['AcceptNotices']
            group_data['GroupInsigniaID'] = GroupData_block['GroupInsigniaID']
            group_data['Contribution'] = GroupData_block['Contribution']
            group_data['GroupName'] = GroupData_block['GroupName']
            group_data['GroupPowers'] = [ ord(x) for x in group_data['GroupPowers'] ]
            group_data['GroupPowers'] = ('').join([ str(x) for x in group_data['GroupPowers'] ])
            self.update_group(group_data)

    def onChatterBoxInvitation_Message(self, message):
        """ handle a group chat message from the event queue """
        self.handle_group_chat(message)

    def onChatterBoxSessionEventReply(self, message):
        """ handle a response from the simulator re: a message we sent to a group chat """
        self.agent.helpers.log_event_queue_data(message, self)

    def onChatterBoxSessionAgentListUpdates(self, message):
        """ parse teh response to a request to join a group chat and propagate data out """
        data = {}
        data['session_id'] = message['Message_Data'][0]['session_id']
        data['agent_updates'] = message['Message_Data'][0]['agent_updates']
        self.update_group_by_session_id(data)

    def onChatterBoxSessionStartReply(self, message):
        data = {}
        data['temp_session_id'] = message['Message_Data'][0]['temp_session_id']
        data['success'] = message['Message_Data'][0]['success']
        data['session_id'] = message['Message_Data'][0]['session_id']
        data['session_info'] = message['Message_Data'][0]['session_info']
        self.update_group_by_name(data, data['session_info']['session_name'])


class Group(object):
    """ representation of a group """
    __module__ = __name__

    def __init__(self, AcceptNotices=None, GroupPowers=None, GroupID=None, GroupName=None, ListInProfile=None, Contribution=None, GroupInsigniaID=None, agent=None):
        self.AcceptNotices = AcceptNotices
        self.GroupPowers = GroupPowers
        self.GroupID = UUID(str(GroupID))
        self.GroupName = GroupName
        self.ListInProfile = ListInProfile
        self.Contribution = Contribution
        self.GroupInsigniaID = UUID(str(GroupInsigniaID))
        self.agent = agent
        self.chat_history = []
        self.session_id = None
        return

    def activate_group(self):
        """ set this group as active """
        self.send_ActivateGroup(self.agent.agent_id, self.agent.session_id, self.GroupID)

    def send_ActivateGroup(self, agent_id, session_id, group_id):
        """ send an ActivateGroup message to the host simulator """
        packet = Message('ActivateGroup', Block('AgentData', AgentID=agent_id, SessionID=session_id, GroupID=group_id))
        self.agent.region.enqueue_message(packet)

    def update_properties(self, properties):
        """ takes a dictionary of attribute:value and makes it so """
        for attribute in properties:
            setattr(self, attribute, properties[attribute])

    def request_join_group_chat(self):
        """ sends an ImprovedInstantMessage packet with the atributes necessary to join a group chat """
        logger.info("Requesting to join group chat session for '%s'" % self.GroupName)
        _AgentID = self.agent.agent_id
        _SessionID = self.agent.session_id
        _FromGroup = False
        _ToAgentID = self.GroupID
        _ParentEstateID = 0
        _RegionID = UUID()
        _Position = Vector3()
        _Offline = 0
        _Dialog = ImprovedIMDialogue.SessionGroupStart
        _ID = self.GroupID
        _Timestamp = 0
        _FromAgentName = self.agent.Name()
        _Message = 'Message'
        _BinaryBucket = ''
        self.agent.send_ImprovedInstantMessage(_AgentID, _SessionID, _FromGroup, _ToAgentID, _ParentEstateID, _RegionID, _Position, _Offline, _Dialog, _ID, _Timestamp, _FromAgentName, _Message, _BinaryBucket)

    def chat(self, Message=None):
        """ sends an instant message to another avatar

        wraps send_ImprovedInstantMessage with some handy defaults """
        if self.session_id == None:
            self.request_join_group_chat()
            Wait(5)
        if self.session_id == None:
            logger.warning('Failed to start chat session with group %s. Please try again later.' % self.GroupName)
            return
        if Message != None:
            _ID = self.GroupID
            _AgentID = self.agent.agent_id
            _SessionID = self.agent.session_id
            _FromGroup = False
            _ToAgentID = self.GroupID
            _ParentEstateID = 0
            _RegionID = UUID()
            _Position = Vector3()
            _Offline = 0
            _Dialog = ImprovedIMDialogue.SessionSend
            _ID = self.GroupID
            _Timestamp = 0
            _FromAgentName = self.agent.Name() + '\x00'
            _Message = Message + '\x00'
            _BinaryBucket = '\x00'
            self.agent.send_ImprovedInstantMessage(_AgentID, _SessionID, _FromGroup, _ToAgentID, _ParentEstateID, _RegionID, _Position, _Offline, _Dialog, _ID, _Timestamp, _FromAgentName, _Message, _BinaryBucket)
        return

    def handle_inbound_chat(self, message):
        """ parses an incoming chat message from a group """
        session_id = message['Message_Data'][0]['session_id']
        session_name = message['Message_Data'][0]['session_name']
        from_name = message['Message_Data'][0]['from_name']
        _message = message['Message_Data'][0]['instantmessage']['message_params']['message']
        self.chat_history.append(message)
        logger.info('Group chat received. Group: %s From: %s Message: %s' % (session_name, from_name, _message))