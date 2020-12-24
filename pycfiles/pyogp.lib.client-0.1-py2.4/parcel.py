# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/parcel.py
# Compiled at: 2010-02-09 00:00:15
"""
Contributors can be viewed at:
http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt 

$LicenseInfo:firstyear=2008&license=apachev2$

Copyright 2009, Linden Research, Inc.

Licensed under the Apache License, Version 2.0.
You may obtain a copy of the License at:
    http://www.apache.org/licenses/LICENSE-2.0
or in 
    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt

$/LicenseInfo$
"""
from logging import getLogger
from eventlet import api
from pyogp.lib.base.datatypes import UUID
from pyogp.lib.client.exc import NotImplemented
from pyogp.lib.client.datamanager import DataManager
from pyogp.lib.base.message.message import Message, Block
from pyogp.lib.base.message.message_handler import MessageHandler
from pyogp.lib.base.helpers import Helpers
logger = getLogger('pyogp.lib.client.parcel')

class ParcelManager(DataManager):
    """ a parcel manager, generally used as an attribute of a region """
    __module__ = __name__

    def __init__(self, agent=None, region=None, settings=None, message_handler=None, events_handler=None):
        """ initialize the parcel manager """
        super(ParcelManager, self).__init__(agent, settings)
        self.region = region
        self.message_handler = message_handler
        self.helpers = Helpers()
        self.parcels = []
        self.parcel_overlay = {}
        self.parcel_map = [ [ 0 for _ in range(64) ] for _ in range(64) ]
        self.parcel_map_full = False
        if self.settings.LOG_VERBOSE:
            logger.debug('Initializing the parcel manager in region %s.' % self.region.SimName)

    def enable_callbacks(self):
        """enable the callback handlers for this ParcelManager"""
        if self.message_handler == None:
            self.message_handler = MessageHandler()
        self.onParcelOverlay_received = self.message_handler.register('ParcelOverlay')
        self.onParcelOverlay_received.subscribe(self.onParcelOverlay)
        self.onParcelProperties_received = self.message_handler.register('ParcelProperties')
        self.onParcelProperties_received.subscribe(self.onParcelProperties)
        self.onParcelPropertiesUpdate_received = self.message_handler.register('ParcelPropertiesUpdate')
        self.onParcelPropertiesUpdate_received.subscribe(self.onParcelPropertiesUpdate)
        self.onParcelInfoReply_received = self.message_handler.register('ParcelInfoReply')
        self.onParcelInfoReply_received.subscribe(self.onParcelInfoReply)
        return

    def onParcelOverlay(self, packet):
        """ parse and handle an incoming ParcelOverlay packet

        Currently, we store this data in the ParcelManager.packet_overlay dictionary
        as parcel_overlay[sequence_id] = data (unparsed binary)
        """
        sequence_id = packet['ParcelData'][0]['SequenceID']
        data = packet['ParcelData'][0]['Data']
        self.parcel_overlay[sequence_id] = data

    def onParcelProperties(self, packet):
        """ parse and handle an incoming ParcelProperties packet. Parse and serialize the info into a Parcel() representation, then store it (or replace the stored version) """
        parcel_info = {}
        parcel_info['RequestResult'] = packet['ParcelData'][0]['RequestResult']
        parcel_info['SequenceID'] = packet['ParcelData'][0]['SequenceID']
        parcel_info['SnapSelection'] = packet['ParcelData'][0]['SnapSelection']
        parcel_info['SelfCount'] = packet['ParcelData'][0]['SelfCount']
        parcel_info['OtherCount'] = packet['ParcelData'][0]['OtherCount']
        parcel_info['PublicCount'] = packet['ParcelData'][0]['PublicCount']
        parcel_info['LocalID'] = packet['ParcelData'][0]['LocalID']
        parcel_info['OwnerID'] = packet['ParcelData'][0]['OwnerID']
        parcel_info['IsGroupOwned'] = packet['ParcelData'][0]['IsGroupOwned']
        parcel_info['AuctionID'] = packet['ParcelData'][0]['AuctionID']
        parcel_info['ClaimDate'] = packet['ParcelData'][0]['ClaimDate']
        parcel_info['ClaimPrice'] = packet['ParcelData'][0]['ClaimPrice']
        parcel_info['RentPrice'] = packet['ParcelData'][0]['RentPrice']
        parcel_info['AABBMin'] = packet['ParcelData'][0]['AABBMin']
        parcel_info['AABBMax'] = packet['ParcelData'][0]['AABBMax']
        parcel_info['Bitmap'] = packet['ParcelData'][0]['Bitmap']
        parcel_info['Area'] = packet['ParcelData'][0]['Area']
        parcel_info['Status'] = packet['ParcelData'][0]['Status']
        parcel_info['SimWideMaxPrims'] = packet['ParcelData'][0]['SimWideMaxPrims']
        parcel_info['SimWideTotalPrims'] = packet['ParcelData'][0]['SimWideTotalPrims']
        parcel_info['MaxPrims'] = packet['ParcelData'][0]['MaxPrims']
        parcel_info['TotalPrims'] = packet['ParcelData'][0]['TotalPrims']
        parcel_info['OwnerPrims'] = packet['ParcelData'][0]['OwnerPrims']
        parcel_info['GroupPrims'] = packet['ParcelData'][0]['GroupPrims']
        parcel_info['OtherPrims'] = packet['ParcelData'][0]['OtherPrims']
        parcel_info['SelectedPrims'] = packet['ParcelData'][0]['SelectedPrims']
        parcel_info['ParcelPrimBonus'] = packet['ParcelData'][0]['ParcelPrimBonus']
        parcel_info['OtherCleanTime'] = packet['ParcelData'][0]['OtherCleanTime']
        parcel_info['ParcelFlags'] = packet['ParcelData'][0]['ParcelFlags']
        parcel_info['SalePrice'] = packet['ParcelData'][0]['SalePrice']
        parcel_info['Name'] = packet['ParcelData'][0]['Name']
        parcel_info['Desc'] = packet['ParcelData'][0]['Desc']
        parcel_info['MusicURL'] = packet['ParcelData'][0]['MusicURL']
        parcel_info['MediaURL'] = packet['ParcelData'][0]['MediaURL']
        parcel_info['MediaID'] = packet['ParcelData'][0]['MediaID']
        parcel_info['MediaAutoScale'] = packet['ParcelData'][0]['MediaAutoScale']
        parcel_info['GroupID'] = packet['ParcelData'][0]['GroupID']
        parcel_info['PassPrice'] = packet['ParcelData'][0]['PassPrice']
        parcel_info['PassHours'] = packet['ParcelData'][0]['PassHours']
        parcel_info['Category'] = packet['ParcelData'][0]['Category']
        parcel_info['AuthBuyerID'] = packet['ParcelData'][0]['AuthBuyerID']
        parcel_info['SnapshotID'] = packet['ParcelData'][0]['SnapshotID']
        parcel_info['UserLocation'] = packet['ParcelData'][0]['UserLocation']
        parcel_info['UserLookAt'] = packet['ParcelData'][0]['UserLookAt']
        parcel_info['LandingType'] = packet['ParcelData'][0]['LandingType']
        parcel_info['RegionPushOverride'] = packet['ParcelData'][0]['RegionPushOverride']
        parcel_info['RegionDenyAnonymous'] = packet['ParcelData'][0]['RegionDenyAnonymous']
        parcel_info['RegionDenyIdentified'] = packet['ParcelData'][0]['RegionDenyIdentified']
        parcel_info['RegionDenyTransacted'] = packet['ParcelData'][0]['RegionDenyTransacted']
        parcel_info['RegionDenyAgeUnverified'] = packet['AgeVerificationBlock'][0]['RegionDenyAgeUnverified']
        self._store_parcel_properties(parcel_info)

    def onParcelPropertiesUpdate(self, packet):
        """ parse and handle an incoming ParcelPropertiesUpdate packet. parse the data into a dictionary and pass the blob to the Parcel() instance for self handling """
        parcel_update = {}
        parcel_update['LocalID'] = packet['ParcelData'][0]['LocalID']
        parcel_update['Flags'] = packet['ParcelData'][0]['Flags']
        parcel_update['ParcelFlags'] = packet['ParcelData'][0]['ParcelFlags']
        parcel_update['SalePrice'] = packet['ParcelData'][0]['SalePrice']
        parcel_update['Name'] = packet['ParcelData'][0]['Name']
        parcel_update['Desc'] = packet['ParcelData'][0]['Desc']
        parcel_update['MusicURL'] = packet['ParcelData'][0]['MusicURL']
        parcel_update['MediaURL'] = packet['ParcelData'][0]['MediaURL']
        parcel_update['MediaID'] = packet['ParcelData'][0]['MediaID']
        parcel_update['MediaAutoScale'] = packet['ParcelData'][0]['MediaAutoScale']
        parcel_update['GroupID'] = packet['ParcelData'][0]['GroupID']
        parcel_update['PassPrice'] = packet['ParcelData'][0]['PassPrice']
        parcel_update['PassHours'] = packet['ParcelData'][0]['PassHours']
        parcel_update['Category'] = packet['ParcelData'][0]['Category']
        parcel_update['AuthBuyerID'] = packet['ParcelData'][0]['AuthBuyerID']
        parcel_update['SnapshotID'] = packet['ParcelData'][0]['SnapshotID']
        parcel_update['UserLocation'] = packet['ParcelData'][0]['UserLocation']
        parcel_update['UserLookAt'] = packet['ParcelData'][0]['UserLookAt']
        parcel_update['LandingType'] = packet['ParcelData'][0]['LandingType']
        self._update_parcel_properties(parcel_update)

    def _store_parcel_properties(self, parcel_info):
        """ store a representation of a parcel """
        index = [ self.parcels.index(parcel) for parcel in self.parcels if parcel.LocalID == parcel_info['LocalID'] ]
        if index != []:
            self._update_parcel_properties(parcel_info)
            if self.settings.LOG_VERBOSE:
                logger.debug("Updating a stored parcel: %s in region '%s'" % (parcel_info['LocalID'], self.region.SimName))
        else:
            new_parcel = Parcel(self.region, self.agent, RequestResult=parcel_info['RequestResult'], SequenceID=parcel_info['SequenceID'], SnapSelection=parcel_info['SnapSelection'], SelfCount=parcel_info['SelfCount'], OtherCount=parcel_info['OtherCount'], PublicCount=parcel_info['PublicCount'], LocalID=parcel_info['LocalID'], OwnerID=parcel_info['OwnerID'], IsGroupOwned=parcel_info['IsGroupOwned'], AuctionID=parcel_info['AuctionID'], ClaimDate=parcel_info['ClaimDate'], ClaimPrice=parcel_info['ClaimPrice'], RentPrice=parcel_info['RentPrice'], AABBMin=parcel_info['AABBMin'], AABBMax=parcel_info['AABBMax'], Bitmap=parcel_info['Bitmap'], Area=parcel_info['Area'], Status=parcel_info['Status'], SimWideMaxPrims=parcel_info['SimWideMaxPrims'], SimWideTotalPrims=parcel_info['SimWideTotalPrims'], MaxPrims=parcel_info['MaxPrims'], TotalPrims=parcel_info['TotalPrims'], OwnerPrims=parcel_info['OwnerPrims'], GroupPrims=parcel_info['GroupPrims'], OtherPrims=parcel_info['OtherPrims'], SelectedPrims=parcel_info['SelectedPrims'], ParcelPrimBonus=parcel_info['ParcelPrimBonus'], OtherCleanTime=parcel_info['OtherCleanTime'], ParcelFlags=parcel_info['ParcelFlags'], SalePrice=parcel_info['SalePrice'], Name=parcel_info['Name'], Desc=parcel_info['Desc'], MusicURL=parcel_info['MusicURL'], MediaURL=parcel_info['MediaURL'], MediaID=parcel_info['MediaID'], MediaAutoScale=parcel_info['MediaAutoScale'], GroupID=parcel_info['GroupID'], PassPrice=parcel_info['PassPrice'], PassHours=parcel_info['PassHours'], Category=parcel_info['Category'], AuthBuyerID=parcel_info['AuthBuyerID'], SnapshotID=parcel_info['SnapshotID'], UserLocation=parcel_info['UserLocation'], UserLookAt=parcel_info['UserLookAt'], LandingType=parcel_info['LandingType'], RegionPushOverride=parcel_info['RegionPushOverride'], RegionDenyAnonymous=parcel_info['RegionDenyAnonymous'], RegionDenyIdentified=parcel_info['RegionDenyIdentified'], RegionDenyTransacted=parcel_info['RegionDenyTransacted'], RegionDenyAgeUnverified=parcel_info['RegionDenyAgeUnverified'], settings=self.settings)
            self.parcels.append(new_parcel)
            self._update_parcel_map(new_parcel)
            if self.settings.LOG_VERBOSE:
                logger.debug("Stored a new parcel: %s in region '%s'" % (new_parcel.LocalID, self.region.SimName))

    def _update_parcel_properties(self, parcel_properties):
        """ update a stored parcel's properties. finds the stored parcel and passes it a dictionary to process """
        parcels_found = []
        if parcel_properties.has_key('LocalID'):
            LocalID = parcel_properties['LocalID']
            parcels_found = [ parcel for parcel in self.parcels if str(parcel.LocalID) == str(LocalID) ]
            if len(parcels_found) == 0:
                logger.info('Received ParcelPropertiesUpdate for parcel we do not know about yet. Storing a partial representation.')
                new_parcel = Parcel(self.region, self.agent, LocalID=parcel_properties['LocalID'], Flags=parcel_properties['Flags'], ParcelFlags=parcel_properties['ParcelFlags'], SalePrice=parcel_properties['SalePrice'], Name=parcel_properties['Name'], Desc=parcel_properties['Desc'], MusicURL=parcel_properties['MusicURL'], MediaURL=parcel_properties['MediaURL'], MediaID=parcel_properties['MediaID'], MediaAutoScale=parcel_properties['MediaAutoScale'], GroupID=parcel_properties['GroupID'], PassPrice=parcel_properties['PassPrice'], PassHours=parcel_properties['PassHours'], Category=parcel_properties['Category'], AuthBuyerID=parcel_properties['AuthBuyerID'], SnapshotID=parcel_properties['SnapshotID'], UserLocation=parcel_properties['UserLocation'], UserLookAt=parcel_properties['UserLookAt'], LandingType=parcel_properties['LandingType'], settings=self.settings)
                self._store_parcel(new_parcel)
            elif len(parcels_found) == 1:
                parcel = parcels_found[0]
                parcel._update_properties(parcel_properties)
        elif parcel_properties.has_key('ParcelID'):
            ParcelID = parcel_properties['ParcelID']
            parcels_found = [ parcel for parcel in self.parcels if str(parcel.ParcelID) == str(ParcelID) ]
            if len(parcels_found) == 0:
                logger.info('Received ParcelPropertiesUpdate for parcel we do not know about yet. Storing a partial representation.')
                new_parcel = Parcel(self.region, self.agent, LocalID=parcel_properties['LocalID'], Flags=parcel_properties['Flags'], ParcelFlags=parcel_properties['ParcelFlags'], SalePrice=parcel_properties['SalePrice'], Name=parcel_properties['Name'], Desc=parcel_properties['Desc'], MusicURL=parcel_properties['MusicURL'], MediaURL=parcel_properties['MediaURL'], MediaID=parcel_properties['MediaID'], MediaAutoScale=parcel_properties['MediaAutoScale'], GroupID=parcel_properties['GroupID'], PassPrice=parcel_properties['PassPrice'], PassHours=parcel_properties['PassHours'], Category=parcel_properties['Category'], AuthBuyerID=parcel_properties['AuthBuyerID'], SnapshotID=parcel_properties['SnapshotID'], UserLocation=parcel_properties['UserLocation'], UserLookAt=parcel_properties['UserLookAt'], LandingType=parcel_properties['LandingType'], settings=self.settings)
                self._store_parcel(new_parcel)
            elif len(parcels_found) == 1:
                parcel = parcels_found[0]
                parcel._update_properties(parcel_properties)

    def _update_parcel_map(self, parcel):
        """Use the parcel's bitmap to update the manager's (x,y) to LocalID mapping"""
        full = True
        for x in range(64):
            for y in range(64):
                index = x + 64 * y
                byte = index >> 3
                mask = 1 << index % 8
                if ord(parcel.Bitmap[byte]) & mask:
                    self.parcel_map[x][y] = parcel.LocalID
                full = full and self.parcel_map[x][y] != 0

        self.parcel_map_full = full

    def get_parcel_by_id(self, local_id):
        """Returns a parcel if info has been received, None otherwise."""
        for parcel in self.parcels:
            if parcel.LocalID == local_id:
                return parcel

        return

    def get_parcel_id_by_location(self, local_x, local_y):
        """Returns a parcel's local id if info has been received, 0 otherwise."""
        return self.parcel_map[(int(local_x) / 4)][(int(local_y) / 4)]

    def get_parcel_by_location(self, local_x, local_y):
        """Returns a parcel if info has been received, None otherwise."""
        return self.get_parcel_by_id(self.get_parcel_id_by_location(local_x, local_y))

    def get_current_parcel(self):
        """Returns the agent's current parcel if info has been received, None otherwise."""
        return self.get_parcel_by_location(self.agent.Position.X, self.agent.Position.Y)

    def request_estate_covenant(self):
        """ request the estate covenant (for the current estate)"""
        self.onEstateCovenantReply_received = self.message_handler.register('EstateCovenantReply')
        self.onEstateCovenantReply_received.subscribe(self.onEstateCovenantReply)
        self.sendEstateCovenantRequest(self.agent.agent_id, self.agent.session_id)

    def sendEstateCovenantRequest(self, agent_id, session_id):
        """ send an EstateCovenantRequest message to the host simulator """
        packet = Message('EstateCovenantRequest', Block('AgentData', AgentID=agent_id, SessionID=session_id))
        self.region.enqueue_message(packet)

    def onEstateCovenantReply(self, packet):
        """ parse and handle an EstateCovenantReply packet """
        try:
            self.onEstateCovenantReply_received.unsubscribe(self.onEstateCovenantReply)
        except AttributeError:
            pass

        CovenantID = packet['Data'][0]['CovenantID']
        CovenantTimestamp = packet['Data'][0]['CovenantTimestamp']
        EstateName = packet['Data'][0]['EstateName']
        EstateOwnerID = packet['Data'][0]['EstateOwnerID']
        logger.info('Received EstateCovenantReply for estate name %s with a CovenantID of %s.' % (EstateName, CovenantID))
        self.estatecovenantreply = {'CovenantID': CovenantID, 'CovenantTimestamp': CovenantTimestamp, 'EstateName': EstateName, 'EstateOwnerID': EstateOwnerID}

    def sendParcelPropertiesRequest(self, agent_id, session_id, SequenceID, West, South, East, North, SnapSelection):
        """ sends a ParcelPropertiesRequest message to the host simulator """
        packet = Message('ParcelPropertiesRequest', Block('AgentData', AgentID=agent_id, SessionID=session_id), Block('ParcelData', SequenceID=SequenceID, West=West, South=South, East=East, North=North, SnapSelection=SnapSelection))
        self.region.enqueue_message(packet)

    def sendParcelPropertiesRequestByID(self, agent_id, session_id, SequenceID, LocalID):
        """ sends a ParcelPropertiesRequestByID packet """
        packet = Message('ParcelPropertiesRequestByID', Block('AgentData', AgentID=agent_id, SessionID=session_id), Block('ParcelData', SequenceID=SequenceID, LocalID=LocalID))
        self.region.enqueue_message(packet)

    def request_parcel_info(self, parcel_id):
        """ request information for a parcel by id """
        if type(parcel_id) == str:
            try:
                parcel_id = UUID(parcel_id)
            except ValueError:
                logger.warning('Parcel_id passed to request_parcel_info must but a valid UUID or string representation of a uuid. %s was passed in' % parcel_id)
                return

        elif not isinstance(parcel_id, UUID):
            logger.warning('Parcel_id passed to request_parcel_info must but a valid UUID or string representation of a uuid. %s was passed in' % parcel_id)
            return
        self.sendParcelInfoRequest(self.agent.agent_id, self.agent.session_id, parcel_id)

    def sendParcelInfoRequest(self, agent_id, session_id, parcel_id):
        """ send a ParcelInfoRequest packet for the specified parcel_id """
        packet = Message('ParcelInfoRequest', Block('AgentData', AgentID=agent_id, SessionID=session_id), Block('Data', ParcelID=parcel_id))
        self.region.enqueue_message(packet)

    def onParcelInfoReply(self, packet):
        """ parse and handle a ParcelInfoReply packet """
        parcel_info = {}
        parcel_info['ParcelID'] = packet['Data'][0]['ParcelID']
        parcel_info['OwnerID'] = packet['Data'][0]['OwnerID']
        parcel_info['Name'] = packet['Data'][0]['Name']
        parcel_info['Desc'] = packet['Data'][0]['Desc']
        parcel_info['ActualArea'] = packet['Data'][0]['ActualArea']
        parcel_info['BillableArea'] = packet['Data'][0]['BillableArea']
        parcel_info['Flags'] = packet['Data'][0]['Flags']
        parcel_info['GlobalX'] = packet['Data'][0]['GlobalX']
        parcel_info['GlobalY'] = packet['Data'][0]['GlobalY']
        parcel_info['GlobalZ'] = packet['Data'][0]['GlobalZ']
        parcel_info['SimName'] = packet['Data'][0]['SimName']
        parcel_info['SnapshotID'] = packet['Data'][0]['SnapshotID']
        parcel_info['Dwell'] = packet['Data'][0]['Dwell']
        parcel_info['SalePrice'] = packet['Data'][0]['SalePrice']
        parcel_info['AuctionID'] = packet['Data'][0]['AuctionID']
        self._update_parcel_properties(parcel_info)

    def request_current_parcel_properties(self, refresh=False):
        """ request the properties of the parcel the agent currently inhabits """
        x = self.agent.Position.X
        y = self.agent.Position.Y
        if refresh or self.get_parcel_id_by_location(x, y) == 0:
            self.sendParcelPropertiesRequest(self.agent.agent_id, self.agent.session_id, -50000, x, y, x, y, False)

    def request_all_parcel_properties(self, delay=0.5, refresh=False):
        """ request the properties of all of the parcels on the current region. The delay parameter is a sleep between the send of each packet request; if refresh, current data will be discarded before requesting. If refresh is not True, data will not be re-requested for region locations already queried. """
        api.spawn(self.__request_all_parcel_properties, delay, refresh)

    def __request_all_parcel_properties(self, delay=1, refresh=False):
        """ request the properties of all of the parcels on the current region """
        if refresh:
            self.parcel_map = [ [ 0 for _ in range(64) ] for _ in range(64) ]
            self.parcel_map_full = False
        for y in range(64):
            for x in range(64):
                if self.parcel_map[x][y] == 0:
                    tx = x * 4 + 2
                    ty = y * 4 + 2
                    self.sendParcelPropertiesRequest(self.agent.agent_id, self.agent.session_id, -50000, tx, ty, tx, ty, False)
                    api.sleep(delay)

    def return_parcel_objects(self):
        """ return the specified objects for the specified parcel """
        pass

    def disable_objects(self):
        """ set objects nonphysical and disable scripts for the specified parcel """
        pass

    def sendParcelDisableObjects(self):
        """ send a ParcelDisableObjects packet """
        pass

    def join_parcels(self):
        """ joins the specified parcels """
        pass

    def sendParcelJoin(self):
        """ send a ParcelJoin packet """
        pass

    def divide_parcel(self):
        """ divide the selection into a new parcel """
        pass

    def sendParcelDivide(self):
        """ send a ParcelDivide packet """
        pass

    def request_parcel_access_list(self, LocalID, Flags):
        """ request an access list for the specified parcel, while enabling a callback handler for the response """
        self.onParcelAccessListReply_received = self.message_handler.register('ParcelAccessListReply')
        self.onParcelAccessListReply_received.subscribe(self.onParcelAccessListReply, LocalID=LocalID)
        self.sendParcelAccessListRequest(self.agent.agent_id, self.agent.session_id, LocalID, Flags)

    def sendParcelAccessListRequest(self, agent_id, session_id, LocalID, Flags, SequenceID=-5150):
        """ send a ParcelAccessListRequest packet to the host simulator """
        packet = Message('ParcelAccessListRequest', Block('AgentData', AgentID=agent_id, SessionID=session_id), Block('Data', SequenceID=SequenceID, Flags=Flags, LocalID=LocalID))
        self.region.enqueue_message(packet)

    def onParcelAccessListReply(self, packet):
        """ parse and handle a ParcelAccessListReply packet """
        raise NotImplemented('sendFetchInventoryDescendentsRequest')

    def request_parcel_dwell(self, LocalID):
        """ request dwell for the specified parcel, while enabling a callback handler for the response """
        self.onParcelDwellReply_received = self.message_handler.register('ParcelDwellReply')
        self.onParcelDwellReply_received.subscribe(self.onParcelDwellReply, LocalID=LocalID)
        self.sendParcelDwellRequest(self.agent.agent_id, self.agent.session_id, LocalID)

    def sendParcelDwellRequest(self, agent_id, session_id, LocalID):
        """ send a ParcelDwellRequest packet """
        packet = Message('ParcelDwellRequest', Block('AgentData', AgentID=agent_id, SessionID=session_id), Block('Data', LocalID=LocalID, ParcelID=UUID()))
        self.region.enqueue_message(packet, True)

    def onParcelDwellReply(self, packet, LocalID=None):
        """ parse and handle a ParcelDwellReply packet"""
        AgentID = packet['AgentData'][0]['AgentID']
        if str(AgentID) != str(self.agent.agent_id):
            logger.warning('%s received a packet for the wrong agent_id. Expected: %s Received: %s' % (self.agent.Name(), self.agent.agent_id, AgentID))
        parcel_info = {}
        parcel_info['LocalID'] = packet['Data'][0]['LocalID']
        parcel_info['ParcelID'] = packet['Data'][0]['ParcelID']
        parcel_info['Dwell'] = packet['Data'][0]['Dwell']
        if LocalID == parcel_info['LocalID']:
            self.onParcelDwellReply_received.unsubscribe(self.onParcelDwellReply, LocalID=LocalID)
        self._update_parcel_properties(parcel_info)


class Parcel(object):
    """ a representation of a parcel """
    __module__ = __name__

    def __init__(self, region, agent, RequestResult=None, SequenceID=None, SnapSelection=None, SelfCount=None, OtherCount=None, PublicCount=None, LocalID=None, OwnerID=None, IsGroupOwned=None, AuctionID=None, ClaimDate=None, ClaimPrice=None, RentPrice=None, AABBMin=None, AABBMax=None, Bitmap=None, Area=None, Status=None, SimWideMaxPrims=None, SimWideTotalPrims=None, MaxPrims=None, TotalPrims=None, OwnerPrims=None, GroupPrims=None, OtherPrims=None, SelectedPrims=None, ParcelPrimBonus=None, OtherCleanTime=None, ParcelFlags=None, SalePrice=None, Name=None, Desc=None, MusicURL=None, MediaURL=None, MediaID=None, MediaAutoScale=None, GroupID=None, PassPrice=None, PassHours=None, Category=None, AuthBuyerID=None, SnapshotID=None, UserLocation=None, UserLookAt=None, LandingType=None, RegionPushOverride=None, RegionDenyAnonymous=None, RegionDenyIdentified=None, RegionDenyTransacted=None, RegionDenyAgeUnverified=None, ParcelID=None, ActualArea=None, BillableArea=None, Flags=None, GlobalX=None, GlobalY=None, GlobalZ=None, SimName=None, Dwell=None, settings=None):
        """ initialize a representation of a parcel. the data is currently being populated directly from the ParcelProperties message """
        if settings != None:
            self.settings = settings
        else:
            from pyogp.lib.client.settings import Settings
            self.settings = Settings()
        self.region = region
        self.agent = agent
        self.ParcelID = ParcelID
        self.OwnerID = OwnerID
        self.ActualArea = ActualArea
        self.BillableArea = BillableArea
        self.Flags = Flags
        self.GlobalX = GlobalX
        self.GlobalY = GlobalY
        self.GlobalZ = GlobalZ
        self.SimName = SimName
        self.Dwell = Dwell
        self.AuctionID = AuctionID
        self.RequestResult = RequestResult
        self.SequenceID = SequenceID
        self.SnapSelection = SnapSelection
        self.SelfCount = SelfCount
        self.OtherCount = OtherCount
        self.PublicCount = PublicCount
        self.LocalID = LocalID
        self.OwnerID = OwnerID
        self.IsGroupOwned = IsGroupOwned
        self.AuctionID = AuctionID
        self.ClaimDate = ClaimDate
        self.ClaimPrice = ClaimPrice
        self.RentPrice = RentPrice
        self.AABBMin = AABBMin
        self.AABBMax = AABBMax
        self.Bitmap = Bitmap
        self.Area = Area
        self.Status = Status
        self.SimWideMaxPrims = SimWideMaxPrims
        self.SimWideTotalPrims = SimWideTotalPrims
        self.MaxPrims = MaxPrims
        self.TotalPrims = TotalPrims
        self.OwnerPrims = OwnerPrims
        self.GroupPrims = GroupPrims
        self.OtherPrims = OtherPrims
        self.SelectedPrims = SelectedPrims
        self.ParcelPrimBonus = ParcelPrimBonus
        self.OtherCleanTime = OtherCleanTime
        self.ParcelFlags = ParcelFlags
        self.SalePrice = SalePrice
        self.Name = Name
        self.Desc = Desc
        self.MusicURL = MusicURL
        self.MediaURL = MediaURL
        self.MediaID = MediaID
        self.MediaAutoScale = MediaAutoScale
        self.GroupID = GroupID
        self.PassPrice = PassPrice
        self.PassHours = PassHours
        self.Category = Category
        self.AuthBuyerID = AuthBuyerID
        self.SnapshotID = SnapshotID
        self.UserLocation = UserLocation
        self.UserLookAt = UserLookAt
        self.LandingType = LandingType
        self.RegionPushOverride = RegionPushOverride
        self.RegionDenyAnonymous = RegionDenyAnonymous
        self.RegionDenyIdentified = RegionDenyIdentified
        self.RegionDenyTransacted = RegionDenyTransacted
        self.RegionDenyAgeUnverified = RegionDenyAgeUnverified
        return

    def _update_properties(self, parcel_properties):
        """ update a parcel's properties via a dictionary """
        for attribute in parcel_properties:
            setattr(self, attribute, parcel_properties[attribute])

    def return_objects(self):
        """ return the specified objects for this parcel """
        pass

    def set_other_clean_time(self):
        """ sends a SetOtherCleanTime packet for this parcel """
        pass

    def disable_objects(self):
        """ set objects nonphysical and disable scripts for this parcel """
        pass

    def select_objects(self):
        """ selects the specified objects for this parcel """
        pass

    def deed_to_group(self):
        """ deed this parcel to a group """
        pass

    def reclaim(self):
        """ reclaim this parcel"""
        pass

    def claim(self):
        """ change the owner of a parcel """
        pass

    def release(self):
        """ release this parcel to the public """
        pass

    def buy(self):
        """ buy this parcel """
        pass

    def godforce_owner(self):
        """ god force own this parcel """
        pass