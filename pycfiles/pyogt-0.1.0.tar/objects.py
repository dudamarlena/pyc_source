# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/objects.py
# Compiled at: 2010-02-09 00:00:15
__doc__ = '\nContributors can be viewed at:\nhttp://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/trunk/CONTRIBUTORS.txt \n\n$LicenseInfo:firstyear=2008&license=apachev2$\n\nCopyright 2009, Linden Research, Inc.\n\nLicensed under the Apache License, Version 2.0.\nYou may obtain a copy of the License at:\n    http://www.apache.org/licenses/LICENSE-2.0\nor in \n    http://svn.secondlife.com/svn/linden/projects/2008/pyogp/lib/base/LICENSE.txt\n\n$/LicenseInfo$\n'
from logging import getLogger
import uuid, re, struct, math
from pyogp.lib.client.datamanager import DataManager
from pyogp.lib.client.permissions import PermissionsTarget, PermissionsMask
from pyogp.lib.base.datatypes import UUID, Vector3, Quaternion
from pyogp.lib.client.event_system import AppEvent
from pyogp.lib.client.namevalue import NameValueList
from pyogp.lib.base.message.message_handler import MessageHandler
from pyogp.lib.base.message.message import Message, Block
from pyogp.lib.base.helpers import Helpers
from pyogp.lib.client.enums import PCodeEnum, CompressedUpdateFlags, Permissions, AssetType
logger = getLogger('pyogp.lib.client.objects')

class ObjectManager(DataManager):
    """ is an Object Manager

    Initialize the event queue client class
    >>> objects = ObjectManager()

    Sample implementations: region.py
    Tests: tests/test_objects.py
    """
    __module__ = __name__

    def __init__(self, agent=None, region=None, settings=None, message_handler=None, events_handler=None):
        """ set up the object manager """
        super(ObjectManager, self).__init__(agent, settings)
        self.region = region
        self.object_store = []
        self.avatar_store = []
        self.helpers = Helpers()
        self.message_handler = message_handler
        if self.settings.LOG_VERBOSE:
            logger.info('Initializing object storage')

    def enable_callbacks(self):
        """enables the callback handlers for this ObjectManager"""
        onObjectUpdate_received = self.message_handler.register('ObjectUpdate')
        onObjectUpdate_received.subscribe(self.onObjectUpdate)
        onObjectUpdateCached_received = self.message_handler.register('ObjectUpdateCached')
        onObjectUpdateCached_received.subscribe(self.onObjectUpdateCached)
        onObjectUpdateCompressed_received = self.message_handler.register('ObjectUpdateCompressed')
        onObjectUpdateCompressed_received.subscribe(self.onObjectUpdateCompressed)
        onImprovedTerseObjectUpdate_received = self.message_handler.register('ImprovedTerseObjectUpdate')
        onImprovedTerseObjectUpdate_received.subscribe(self.onImprovedTerseObjectUpdate)
        onObjectProperties_received = self.message_handler.register('ObjectProperties')
        onObjectProperties_received.subscribe(self.onObjectProperties)
        onKillObject_received = self.message_handler.register('KillObject')
        onKillObject_received.subscribe(self.onKillObject)

    def store_object(self, _object):
        """ store a representation of an object that has been transformed from data off the wire """
        index = [ self.object_store.index(_object_) for _object_ in self.object_store if _object_.LocalID == _object.LocalID ]
        if index != []:
            self.object_store[index[0]] = _object
        else:
            self.object_store.append(_object)

    def store_avatar(self, _objectdata):
        """ store a representation of an avatar (Object() instance) that has been transformed from data off the wire  """
        if str(_objectdata.FullID) == str(self.agent.agent_id) or _objectdata.LocalID == self.agent.local_id:
            if _objectdata.Position:
                self.agent.Position = _objectdata.Position
            if _objectdata.FootCollisionPlane:
                self.agent.FootCollisionPlane = _objectdata.FootCollisionPlane
            if _objectdata.Velocity:
                self.agent.Velocity = _objectdata.Velocity
            if _objectdata.Acceleration:
                self.agent.Acceleration = _objectdata.Acceleration
            if _objectdata.Rotation:
                self.agent.Rotation = _objectdata.Rotation
            if _objectdata.AngularVelocity:
                self.agent.AngularVelocity = _objectdata.AngularVelocity
            if _objectdata.LocalID:
                self.agent.local_id = _objectdata.LocalID
            if self.settings.ENABLE_APPEARANCE_MANAGEMENT:
                self.agent.appearance.TextureEntry = _objectdata.TextureEntry
            self.agent.sendDynamicsUpdate()
        index = [ self.avatar_store.index(_avatar_) for _avatar_ in self.avatar_store if _avatar_.LocalID == _objectdata.LocalID ]
        if index != []:
            self.avatar_store[index[0]] = _objectdata
        else:
            self.avatar_store.append(_objectdata)
        self.agent.events_handler.handle(AppEvent('AvatarUpdate', payload={'object': _objectdata, 'region': self.region}))

    def get_object_from_store(self, LocalID=None, FullID=None):
        """ searches the store and returns object if stored, None otherwise """
        _object = []
        if LocalID != None:
            _object = [ _object for _object in self.object_store if _object.LocalID == LocalID ]
        elif FullID != None:
            _object = [ _object for _object in self.object_store if str(_object.FullID) == str(FullID) ]
        if _object == []:
            return
        else:
            return _object[0]
        return

    def get_avatar_from_store(self, LocalID=None, FullID=None):
        """ searches the store and returns object if stored, None otherwise """
        if LocalID != None:
            _avatar = [ _avatar for _avatar in self.avatar_store if _avatar.LocalID == LocalID ]
        elif FullID != None:
            _avatar = [ _avatar for _avatar in self.avatar_store if _avatar.FullID == FullID ]
        if _avatar == []:
            return
        else:
            return _avatar[0]
        return

    def my_objects(self):
        """ returns a list of known objects where the calling client is the owner """
        matches = [ _object for _object in self.object_store if str(_object.OwnerID) == str(self.agent.agent_id) ]
        return matches

    def find_objects_by_name(self, Name):
        """ searches the store for known objects by name 

        returns a list of all such known objects
        """
        pattern = re.compile(Name)
        matches = [ _object for _object in self.object_store if pattern.match(_object.Name) ]
        return matches

    def find_objects_within_radius(self, radius):
        """ returns objects nearby. returns a list of objects """
        if type(radius) != float:
            radius = float(radius)
        objects_nearby = []
        for item in self.object_store:
            if item.Position == None:
                continue
            if math.sqrt(math.pow(item.Position.X - self.agent.Position.X, 2) + math.pow(item.Position.Y - self.agent.Position.Y, 2) + math.pow(item.Position.Z - self.agent.Position.Z, 2)) <= radius:
                objects_nearby.append(item)

        return objects_nearby

    def remove_object_from_store(self, ID=None):
        """ handles removing a stored object representation """
        victim = self.get_object_from_store(LocalID=ID)
        if victim == None:
            victim = self.get_avatar_from_store(LocalID=ID)
        if victim == None or victim == []:
            return
        if victim.PCode == PCodeEnum.Avatar:
            self.kill_stored_avatar(ID)
        elif victim.PCode == PCodeEnum.Primitive:
            self.kill_stored_object(ID)
        elif self.settings.LOG_VERBOSE and self.settings.ENABLE_OBJECT_LOGGING:
            logger.debug('Not processing kill of unstored object type %s' % PCodeEnum(victim.PCode))
        return

    def kill_stored_avatar(self, ID):
        """ removes a stored avatar (Object() instance) from our list """
        index = [ self.avatar_store.index(_avatar_) for _avatar_ in self.avatar_store if _avatar_.LocalID == ID ]
        if index != []:
            self.agent.events_handler.handle(AppEvent('KillAvatar', payload={'object': self.avatar_store[index[0]], 'region': self.region}))
            del self.avatar_store[index[0]]
            if self.settings.LOG_VERBOSE and self.settings.ENABLE_OBJECT_LOGGING:
                logger.debug('Kill on object data for avatar tracked as local id %s' % ID)

    def kill_stored_object(self, ID):
        index = [ self.object_store.index(_object_) for _object_ in self.object_store if _object_.LocalID == ID ]
        if index != []:
            del self.object_store[index[0]]
            if self.settings.LOG_VERBOSE and self.settings.ENABLE_OBJECT_LOGGING:
                logger.debug('Kill on object data for object tracked as local id %s' % ID)

    def update_multiple_objects_properties(self, object_list):
        """ update the attributes of objects """
        for object_properties in object_list:
            self.update_object_properties(object_properties)

    def update_object_properties(self, object_properties):
        """ update the attributes of an object

        If the object is known, we update the properties. 
        If not, we create a new object
        """
        if object_properties.has_key('PCode'):
            if object_properties['PCode'] == PCodeEnum.Avatar:
                _object = Object()
                _object._update_properties(object_properties)
                self.store_avatar(_object)
            else:
                self.update_prim_properties(object_properties)
        else:
            self.update_prim_properties(object_properties)

    def update_prim_properties(self, prim_properties):
        """ handles an object update and updates or adds to internal representation """
        _object = self.get_object_from_store(FullID=prim_properties['FullID'])
        if _object == None:
            _object = Object()
            _object._update_properties(prim_properties)
            self.store_object(_object)
        else:
            _object._update_properties(prim_properties)
        if _object.UpdateFlags & 2 != 0 and self.agent != None:
            self.agent.events_handler.handle(AppEvent('ObjectSelected', payload={'object': _object}))
        return

    def request_object_update(self, AgentID, SessionID, ID_CacheMissType_list=None):
        """ requests object updates from the simulator

        accepts a list of (ID, CacheMissType)
        """
        packet = Message('RequestMultipleObjects', Block('AgentData', AgentID=AgentID, SessionID=SessionID), *[ Block('ObjectData', CacheMissType=ID_CacheMissType[1], ID=ID_CacheMissType[0]) for ID_CacheMissType in ID_CacheMissType_list ])
        self.region.enqueue_message(packet, True)

    def create_default_box(self, GroupID=UUID(), relative_position=(1, 0, 0)):
        """ creates the default box, defaulting as 1m to the east, with an option GroupID to set the prim to"""
        location_to_rez_x = self.agent.Position.X + relative_position[0]
        location_to_rez_y = self.agent.Position.Y + relative_position[1]
        location_to_rez_z = self.agent.Position.Z + relative_position[2]
        location_to_rez = (
         location_to_rez_x, location_to_rez_y, location_to_rez_z)
        RayTargetID = UUID()
        self.object_add(self.agent.agent_id, self.agent.session_id, GroupID=GroupID, PCode=PCodeEnum.Primitive, Material=3, AddFlags=2, PathCurve=16, ProfileCurve=1, PathBegin=0, PathEnd=0, PathScaleX=100, PathScaleY=100, PathShearX=0, PathShearY=0, PathTwist=0, PathTwistBegin=0, PathRadiusOffset=0, PathTaperX=0, PathTaperY=0, PathRevolutions=0, PathSkew=0, ProfileBegin=0, ProfileEnd=0, ProfileHollow=0, BypassRaycast=1, RayStart=location_to_rez, RayEnd=location_to_rez, RayTargetID=RayTargetID, RayEndIsIntersection=0, Scale=(0.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.5,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0.5), Rotation=(0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  0,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  1), State=0)

    def object_add(self, AgentID, SessionID, PCode, Material, AddFlags, PathCurve, ProfileCurve, PathBegin, PathEnd, PathScaleX, PathScaleY, PathShearX, PathShearY, PathTwist, PathTwistBegin, PathRadiusOffset, PathTaperX, PathTaperY, PathRevolutions, PathSkew, ProfileBegin, ProfileEnd, ProfileHollow, BypassRaycast, RayStart, RayEnd, RayTargetID, RayEndIsIntersection, Scale, Rotation, State, GroupID=UUID()):
        """
        ObjectAdd - create new object in the world
        Simulator will assign ID and send message back to signal
        object actually created.

        AddFlags (see also ObjectUpdate)
        0x01 - use physics
        0x02 - create selected

        GroupID defaults to (No group active)
        """
        packet = Message('ObjectAdd', Block('AgentData', AgentID=AgentID, SessionID=SessionID, GroupID=GroupID), Block('ObjectData', PCode=PCode, Material=Material, AddFlags=AddFlags, PathCurve=PathCurve, ProfileCurve=ProfileCurve, PathBegin=PathBegin, PathEnd=PathEnd, PathScaleX=PathScaleX, PathScaleY=PathScaleY, PathShearX=PathShearX, PathShearY=PathShearY, PathTwist=PathTwist, PathTwistBegin=PathTwistBegin, PathRadiusOffset=PathRadiusOffset, PathTaperX=PathTaperX, PathTaperY=PathTaperY, PathRevolutions=PathRevolutions, PathSkew=PathSkew, ProfileBegin=ProfileBegin, ProfileEnd=ProfileEnd, ProfileHollow=ProfileHollow, BypassRaycast=BypassRaycast, RayStart=RayStart, RayEnd=RayEnd, RayTargetID=RayTargetID, RayEndIsIntersection=RayEndIsIntersection, Scale=Scale, Rotation=Rotation, State=State))
        self.region.enqueue_message(packet, True)

    def onObjectUpdate(self, packet):
        """ populates an Object instance and adds it to the ObjectManager() store """
        REGION_SIZE = 256.0
        MIN_HEIGHT = -REGION_SIZE
        MAX_HEIGHT = 4096.0
        object_list = []
        _RegionHandle = packet['RegionData'][0]['RegionHandle']
        _TimeDilation = packet['RegionData'][0]['TimeDilation']
        for ObjectData_block in packet['ObjectData']:
            object_properties = {}
            object_properties['LocalID'] = ObjectData_block['ID']
            object_properties['State'] = ObjectData_block['State']
            object_properties['FullID'] = ObjectData_block['FullID']
            object_properties['CRC'] = ObjectData_block['CRC']
            object_properties['PCode'] = ObjectData_block['PCode']
            object_properties['Material'] = ObjectData_block['Material']
            object_properties['ClickAction'] = ObjectData_block['ClickAction']
            object_properties['Scale'] = ObjectData_block['Scale']
            object_properties['ObjectData'] = ObjectData_block['ObjectData']
            object_properties['ParentID'] = ObjectData_block['ParentID']
            object_properties['UpdateFlags'] = ObjectData_block['UpdateFlags']
            object_properties['PathCurve'] = ObjectData_block['PathCurve']
            object_properties['ProfileCurve'] = ObjectData_block['ProfileCurve']
            object_properties['PathBegin'] = ObjectData_block['PathBegin']
            object_properties['PathEnd'] = ObjectData_block['PathEnd']
            object_properties['PathScaleX'] = ObjectData_block['PathScaleX']
            object_properties['PathScaleY'] = ObjectData_block['PathScaleY']
            object_properties['PathShearX'] = ObjectData_block['PathShearX']
            object_properties['PathShearY'] = ObjectData_block['PathShearY']
            object_properties['PathTwist'] = ObjectData_block['PathTwist']
            object_properties['PathTwistBegin'] = ObjectData_block['PathTwistBegin']
            object_properties['PathRadiusOffset'] = ObjectData_block['PathRadiusOffset']
            object_properties['PathTaperX'] = ObjectData_block['PathTaperX']
            object_properties['PathTaperY'] = ObjectData_block['PathTaperY']
            object_properties['PathRevolutions'] = ObjectData_block['PathRevolutions']
            object_properties['PathSkew'] = ObjectData_block['PathSkew']
            object_properties['ProfileBegin'] = ObjectData_block['ProfileBegin']
            object_properties['ProfileEnd'] = ObjectData_block['ProfileEnd']
            object_properties['ProfileHollow'] = ObjectData_block['ProfileHollow']
            object_properties['TextureEntry'] = ObjectData_block['TextureEntry']
            object_properties['TextureAnim'] = ObjectData_block['TextureAnim']
            object_properties['Data'] = ObjectData_block['Data']
            object_properties['Text'] = ObjectData_block['Text']
            object_properties['TextColor'] = ObjectData_block['TextColor']
            object_properties['MediaURL'] = ObjectData_block['MediaURL']
            object_properties['PSBlock'] = ObjectData_block['PSBlock']
            object_properties['ExtraParams'] = ObjectData_block['ExtraParams']
            object_properties['Sound'] = ObjectData_block['Sound']
            object_properties['OwnerID'] = ObjectData_block['OwnerID']
            object_properties['Gain'] = ObjectData_block['Gain']
            object_properties['Flags'] = ObjectData_block['Flags']
            object_properties['Radius'] = ObjectData_block['Radius']
            object_properties['JointType'] = ObjectData_block['JointType']
            object_properties['JointPivot'] = ObjectData_block['JointPivot']
            object_properties['JointAxisOrAnchor'] = ObjectData_block['JointAxisOrAnchor']
            namevalues = ObjectData_block['NameValue']
            object_properties['NameValue'] = NameValueList(namevalues)
            object_properties['FootCollisionPlane'] = None
            object_properties['Position'] = None
            object_properties['Velocity'] = None
            object_properties['Acceleration'] = None
            object_properties['Rotation'] = None
            object_properties['AngularVelocity'] = None
            objdata = object_properties['ObjectData']
            if len(objdata) == 76 or len(objdata) == 60:
                pos = 0
                if len(objdata) == 76:
                    object_properties['FootCollisionPlane'] = Quaternion(objdata, pos)
                    pos += 16
                object_properties['Position'] = Vector3(objdata, pos + 0)
                object_properties['Velocity'] = Vector3(objdata, pos + 12)
                object_properties['Acceleration'] = Vector3(objdata, pos + 24)
                object_properties['Rotation'] = Quaternion(objdata, pos + 36, 3)
                object_properties['AngularVelocity'] = Vector3(objdata, pos + 48)
            elif len(objdata) == 48 or len(objdata) == 32:
                pos = 0
                if len(objdata) == 48:
                    object_properties['FootCollisionPlane'] = Quaternion(objdata, pos)
                    pos += 16
                object_properties['Position'] = Vector3(X=Helpers.packed_u16_to_float(objdata, pos + 0, -0.5 * REGION_SIZE, 1.5 * REGION_SIZE), Y=Helpers.packed_u16_to_float(objdata, pos + 2, -0.5 * REGION_SIZE, 1.5 * REGION_SIZE), Z=Helpers.packed_u16_to_float(objdata, pos + 4, MIN_HEIGHT, MAX_HEIGHT))
                object_properties['Velocity'] = Vector3(X=Helpers.packed_u16_to_float(objdata, pos + 6, -REGION_SIZE, REGION_SIZE), Y=Helpers.packed_u16_to_float(objdata, pos + 8, -REGION_SIZE, REGION_SIZE), Z=Helpers.packed_u16_to_float(objdata, pos + 10, -REGION_SIZE, REGION_SIZE))
                object_properties['Acceleration'] = Vector3(X=Helpers.packed_u16_to_float(objdata, pos + 12, -REGION_SIZE, REGION_SIZE), Y=Helpers.packed_u16_to_float(objdata, pos + 14, -REGION_SIZE, REGION_SIZE), Z=Helpers.packed_u16_to_float(objdata, pos + 16, -REGION_SIZE, REGION_SIZE))
                object_properties['Rotation'] = Quaternion(X=Helpers.packed_u16_to_float(objdata, pos + 18, -1.0, 1.0), Y=Helpers.packed_u16_to_float(objdata, pos + 20, -1.0, 1.0), Z=Helpers.packed_u16_to_float(objdata, pos + 22, -1.0, 1.0), W=Helpers.packed_u16_to_float(objdata, pos + 24, -1.0, 1.0))
                object_properties['AngularVelocity'] = Vector3(X=Helpers.packed_u16_to_float(objdata, pos + 26, -REGION_SIZE, REGION_SIZE), Y=Helpers.packed_u16_to_float(objdata, pos + 28, -REGION_SIZE, REGION_SIZE), Z=Helpers.packed_u16_to_float(objdata, pos + 30, -REGION_SIZE, REGION_SIZE))
            elif len(objdata) == 16:
                object_properties['Position'] = Vector3(X=Helpers.packed_u8_to_float(objdata, 0, -0.5 * REGION_SIZE, 1.5 * REGION_SIZE), Y=Helpers.packed_u8_to_float(objdata, 1, -0.5 * REGION_SIZE, 1.5 * REGION_SIZE), Z=Helpers.packed_u8_to_float(objdata, 2, MIN_HEIGHT, MAX_HEIGHT))
                object_properties['Velocity'] = Vector3(X=Helpers.packed_u8_to_float(objdata, 3, -REGION_SIZE, REGION_SIZE), Y=Helpers.packed_u8_to_float(objdata, 4, -REGION_SIZE, REGION_SIZE), Z=Helpers.packed_u8_to_float(objdata, 5, -REGION_SIZE, REGION_SIZE))
                object_properties['Acceleration'] = Vector3(X=Helpers.packed_u8_to_float(objdata, 6, -REGION_SIZE, REGION_SIZE), Y=Helpers.packed_u8_to_float(objdata, 7, -REGION_SIZE, REGION_SIZE), Z=Helpers.packed_u8_to_float(objdata, 8, -REGION_SIZE, REGION_SIZE))
                object_properties['Rotation'] = Quaternion(X=Helpers.packed_u8_to_float(objdata, 9, -1.0, 1.0), Y=Helpers.packed_u8_to_float(objdata, 10, -1.0, 1.0), Z=Helpers.packed_u8_to_float(objdata, 11, -1.0, 1.0), W=Helpers.packed_u8_to_float(objdata, 12, -1.0, 1.0))
                object_properties['AngularVelocity'] = Vector3(X=Helpers.packed_u8_to_float(objdata, 13, -REGION_SIZE, REGION_SIZE), Y=Helpers.packed_u8_to_float(objdata, 14, -REGION_SIZE, REGION_SIZE), Z=Helpers.packed_u8_to_float(objdata, 15, -REGION_SIZE, REGION_SIZE))
            object_list.append(object_properties)

        self.update_multiple_objects_properties(object_list)
        return

    def onObjectUpdateCached(self, packet):
        """ borrowing from libomv, we'll request object data for all data coming in via ObjectUpdateCached"""
        _RegionHandle = packet['RegionData'][0]['RegionHandle']
        _TimeDilation = packet['RegionData'][0]['TimeDilation']
        _request_list = []
        for ObjectData_block in packet['ObjectData']:
            LocalID = ObjectData_block['ID']
            _CRC = ObjectData_block['CRC']
            _UpdateFlags = ObjectData_block['UpdateFlags']
            _object = self.get_object_from_store(LocalID=LocalID)
            if _object == None or _object == []:
                CacheMissType = 1
            else:
                CacheMissType = 0
            _request_list.append((LocalID, CacheMissType))

        self.request_object_update(self.agent.agent_id, self.agent.session_id, ID_CacheMissType_list=_request_list)
        return

    def onObjectUpdateCompressed(self, packet):
        """ handles an ObjectUpdateCompressed message from a simulator """
        object_list = []
        _RegionHandle = packet['RegionData'][0]['RegionHandle']
        _TimeDilation = packet['RegionData'][0]['TimeDilation']
        for ObjectData_block in packet['ObjectData']:
            object_properties = {}
            object_properties['UpdateFlags'] = ObjectData_block['UpdateFlags']
            object_properties['Data'] = ObjectData_block['Data']
            _Data = object_properties['Data']
            pos = 0
            object_properties['FullID'] = UUID(bytes=_Data, offset=0)
            pos += 16
            object_properties['LocalID'] = struct.unpack('<I', _Data[pos:pos + 4])[0]
            pos += 4
            object_properties['PCode'] = struct.unpack('>B', _Data[pos:pos + 1])[0]
            pos += 1
            if object_properties['PCode'] != PCodeEnum.Primitive:
                logger.warning('Fix Me!! Skipping parsing of ObjectUpdateCompressed packet when it is not a prim.')
                continue
            object_properties['State'] = struct.unpack('>B', _Data[pos:pos + 1])[0]
            pos += 1
            object_properties['CRC'] = struct.unpack('<I', _Data[pos:pos + 4])[0]
            pos += 4
            object_properties['Material'] = struct.unpack('>B', _Data[pos:pos + 1])[0]
            pos += 1
            object_properties['ClickAction'] = struct.unpack('>B', _Data[pos:pos + 1])[0]
            pos += 1
            object_properties['Scale'] = Vector3(_Data, pos)
            pos += 12
            object_properties['Position'] = Vector3(_Data, pos)
            pos += 12
            object_properties['Rotation'] = Vector3(_Data, pos)
            pos += 12
            object_properties['Flags'] = struct.unpack('>B', _Data[pos:pos + 1])[0]
            pos += 1
            object_properties['OwnerID'] = UUID(bytes=_Data, offset=pos)
            pos += 16
            object_properties['AngularVelocity'] = Vector3()
            object_properties['ParentID'] = UUID()
            object_properties['Text'] = ''
            object_properties['TextColor'] = None
            object_properties['MediaURL'] = ''
            object_properties['Sound'] = UUID()
            object_properties['Gain'] = 0
            object_properties['Flags'] = 0
            object_properties['Radius'] = 0
            object_properties['NameValue'] = NameValueList(None)
            object_properties['ExtraParams'] = None
            if object_properties['Flags'] != 0:
                logger.warning('FixMe! Quiting parsing an ObjectUpdateCompressed packet with flags due to incomplete implemention. Storing a partial representation of an object with uuid of %s' % object_properties['FullID'])
                object_properties['PathCurve'] = None
                object_properties['PathBegin'] = None
                object_properties['PathEnd'] = None
                object_properties['PathScaleX'] = None
                object_properties['PathScaleY'] = None
                object_properties['PathShearX'] = None
                object_properties['PathShearY'] = None
                object_properties['PathTwist'] = None
                object_properties['PathTwistBegin'] = None
                object_properties['PathRadiusOffset'] = None
                object_properties['PathTaperX'] = None
                object_properties['PathTaperY'] = None
                object_properties['PathRevolutions'] = None
                object_properties['PathSkew'] = None
                object_properties['ProfileCurve'] = None
                object_properties['ProfileBegin'] = None
                object_properties['ProfileEnd'] = None
                object_properties['ProfileHollow'] = None
                object_properties['TextureEntry'] = None
                object_properties['TextureAnim'] = None
            else:
                properties = [
                 ('PathCurve', '>B'), ('PathBegin', '<H'), ('PathEnd', '<H'), ('PathScaleX', '>B'), ('PathScaleY', '>B'), ('PathShearX', '>B'), ('PathShearY', '>B'), ('PathTwist', '>B'), ('PathTwistBegin', '>B'), ('PathRadiusOffset', '>B'), ('PathTaperX', '>B'), ('PathTaperY', '>B'), ('PathRevolutions', '>B'), ('PathSkew', '>B'), ('ProfileCurve', '>B'), ('ProfileBegin', '>B'), ('ProfileEnd', '>B'), ('ProfileHollow', '>B')]
                for (prop, pack) in properties:
                    packsize = struct.calcsize(pack)
                    object_properties[prop] = struct.unpack(pack, _Data[pos:pos + packsize])[0]
                    pos += packsize

                size = struct.unpack('<H', _Data[pos:pos + 2])[0]
                pos += 2
                object_properties['TextureEntry'] = _Data[pos:pos + size]
                pos += size
                if object_properties['Flags'] & CompressedUpdateFlags.TextureAnim != 0:
                    object_properties['TextureAnim'] = struct.unpack('<H', _Data[pos:pos + 2])[0]
                    pos += 2
                else:
                    object_properties['TextureAnim'] = None
            object_list.append(object_properties)

        self.update_multiple_objects_properties(object_list)
        return

    def onImprovedTerseObjectUpdate(self, packet):
        """ handles ImprovedTerseObjectUpdate messages from the simulator """
        try:
            _RegionHandle = packet['RegionData'][0]['RegionHandle']
            _TimeDilation = packet['RegionData'][0]['TimeDilation']
            object_list = []
            for ObjectData_block in packet['ObjectData']:
                object_properties = {}
                object_properties['Data'] = ObjectData_block['Data']
                _Data = object_properties['Data']
                pos = 0
                object_properties['LocalID'] = struct.unpack('<I', _Data[pos:pos + 4])[0]
                pos += 4
                object_properties['State'] = struct.unpack('>B', _Data[pos:pos + 1])[0]
                pos += 1
                is_avatar = struct.unpack('>B', _Data[pos:pos + 1])
                pos += 1
                if is_avatar:
                    object_properties['PCode'] = PCodeEnum.Avatar
                    object_properties['FootCollisionPlane'] = Quaternion(_Data, pos)
                    pos += 16
                else:
                    object_properties['PCode'] = PCodeEnum.Primitive
                object_properties['Position'] = Vector3(_Data, pos + 0)
                pos += 12
                object_properties['Velocity'] = Vector3(X=Helpers().packed_u16_to_float(_Data, pos, -128.0, 128.0), Y=Helpers().packed_u16_to_float(_Data, pos + 2, -128.0, 128.0), Z=Helpers().packed_u16_to_float(_Data, pos + 4, -128.0, 128.0))
                pos += 6
                object_properties['Acceleration'] = Vector3(X=Helpers().packed_u16_to_float(_Data, pos, -64.0, 64.0), Y=Helpers().packed_u16_to_float(_Data, pos + 2, -64.0, 64.0), Z=Helpers().packed_u16_to_float(_Data, pos + 4, -64.0, 64.0))
                pos += 6
                object_properties['Rotation'] = Quaternion(X=Helpers().packed_u16_to_float(_Data, pos, -1.0, 1.0), Y=Helpers().packed_u16_to_float(_Data, pos + 2, -1.0, 1.0), Z=Helpers().packed_u16_to_float(_Data, pos + 4, -1.0, 1.0), W=Helpers().packed_u16_to_float(_Data, pos + 6, -1.0, 1.0))
                pos += 8
                object_properties['AngularVelocity'] = Vector3(X=Helpers().packed_u16_to_float(_Data, pos, -64.0, 64.0), Y=Helpers().packed_u16_to_float(_Data, pos + 2, -64.0, 64.0), Z=Helpers().packed_u16_to_float(_Data, pos + 4, -64.0, 64.0))
                pos += 6
                object_properties['TextureEntry'] = ObjectData_block['TextureEntry']
                object_list.append(object_properties)

            self.update_multiple_objects_properties(object_list)
        except:
            pass

    def onKillObject(self, packet):
        _KillID = packet['ObjectData'][0]['ID']
        self.remove_object_from_store(_KillID)

    def onObjectProperties(self, packet):
        object_list = []
        for ObjectData_block in packet['ObjectData']:
            object_properties = {}
            object_properties['FullID'] = ObjectData_block['ObjectID']
            object_properties['CreatorID'] = ObjectData_block['CreatorID']
            object_properties['OwnerID'] = ObjectData_block['OwnerID']
            object_properties['GroupID'] = ObjectData_block['GroupID']
            object_properties['CreationDate'] = ObjectData_block['CreationDate']
            object_properties['BaseMask'] = ObjectData_block['BaseMask']
            object_properties['OwnerMask'] = ObjectData_block['OwnerMask']
            object_properties['GroupMask'] = ObjectData_block['GroupMask']
            object_properties['EveryoneMask'] = ObjectData_block['EveryoneMask']
            object_properties['NextOwnerMask'] = ObjectData_block['NextOwnerMask']
            object_properties['OwnershipCost'] = ObjectData_block['OwnershipCost']
            object_properties['SaleType'] = ObjectData_block['SaleType']
            object_properties['SalePrice'] = ObjectData_block['SalePrice']
            object_properties['AggregatePerms'] = ObjectData_block['AggregatePerms']
            object_properties['AggregatePermTextures'] = ObjectData_block['AggregatePermTextures']
            object_properties['AggregatePermTexturesOwner'] = ObjectData_block['AggregatePermTexturesOwner']
            object_properties['Category'] = ObjectData_block['Category']
            object_properties['InventorySerial'] = ObjectData_block['InventorySerial']
            object_properties['ItemID'] = ObjectData_block['ItemID']
            object_properties['FolderID'] = ObjectData_block['FolderID']
            object_properties['FromTaskID'] = ObjectData_block['FromTaskID']
            object_properties['LastOwnerID'] = ObjectData_block['LastOwnerID']
            object_properties['Name'] = ObjectData_block['Name']
            object_properties['Description'] = ObjectData_block['Description']
            object_properties['TouchName'] = ObjectData_block['TouchName']
            object_properties['SitName'] = ObjectData_block['SitName']
            object_properties['TextureID'] = ObjectData_block['TextureID']
            object_list.append(object_properties)

        self.update_multiple_objects_properties(object_list)

    def send_RezScript(self, agent, prim, item_id=UUID(), Enabled=True, GroupID=UUID(), BaseMask=Permissions.All, OwnerMask=Permissions.All, GroupMask=Permissions.None_, EveryoneMask=Permissions.None_, NextOwnerMask=Permissions.Transfer & Permissions.Move, GroupOwned=False, Type=AssetType.LSLText, InvType=AssetType.LSLText, Flags=0, SaleType=0, SalePrice=0, Name='New Script', Description='Created by PyOGP', CreationDate=0, CRC=0):
        """ sends a RezScript message to the sim, not providing a item_id will
        rez the default script otherwise the script with ItemID item_id will be rezzed
        to prim"""
        packet = Message('RezScript', Block('AgentData', AgentID=agent.agent_id, SessionID=agent.session_id, GroupID=agent.ActiveGroupID), Block('UpdateBlock', ObjectLocalID=prim.LocalID, Enabled=Enabled), Block('InventoryBlock', ItemID=item_id, FolderID=prim.FullID, CreatorID=agent.agent_id, OwnerID=agent.agent_id, GroupID=GroupID, BaseMask=BaseMask, OwnerMask=OwnerMask, GroupMask=GroupMask, EveryoneMask=EveryoneMask, NextOwnerMask=NextOwnerMask, GroupOwned=GroupOwned, TransactionID=UUID(), Type=Type, InvType=InvType, Flags=Flags, SaleType=SaleType, SalePrice=SalePrice, Name=Name, Description=Description, CreationDate=CreationDate, CRC=CRC))
        agent.region.enqueue_message(packet)


class Object(object):
    """ represents an Object

    Initialize the Object class instance
    >>> object = Object()

    Sample implementations: objects.py
    Tests: tests/test_objects.py
    """
    __module__ = __name__

    def __init__(self, LocalID=None, State=None, FullID=None, CRC=None, PCode=None, Material=None, ClickAction=None, Scale=None, ObjectData=None, ParentID=None, UpdateFlags=None, PathCurve=None, ProfileCurve=None, PathBegin=None, PathEnd=None, PathScaleX=None, PathScaleY=None, PathShearX=None, PathShearY=None, PathTwist=None, PathTwistBegin=None, PathRadiusOffset=None, PathTaperX=None, PathTaperY=None, PathRevolutions=None, PathSkew=None, ProfileBegin=None, ProfileEnd=None, ProfileHollow=None, TextureEntry=None, TextureAnim=None, NameValue=None, Data=None, Text=None, TextColor=None, MediaURL=None, PSBlock=None, ExtraParams=None, Sound=None, OwnerID=None, Gain=None, Flags=None, Radius=None, JointType=None, JointPivot=None, JointAxisOrAnchor=None, FootCollisionPlane=None, Position=None, Velocity=None, Acceleration=None, Rotation=None, AngularVelocity=None):
        """ set up the object attributes """
        self.LocalID = LocalID
        self.State = State
        self.FullID = FullID
        self.CRC = CRC
        self.PCode = PCode
        self.Material = Material
        self.ClickAction = ClickAction
        self.Scale = Scale
        self.ObjectData = ObjectData
        self.ParentID = ParentID
        self.UpdateFlags = UpdateFlags
        self.PathCurve = PathCurve
        self.ProfileCurve = ProfileCurve
        self.PathBegin = PathBegin
        self.PathEnd = PathEnd
        self.PathScaleX = PathScaleX
        self.PathScaleY = PathScaleY
        self.PathShearX = PathShearX
        self.PathShearY = PathShearY
        self.PathTwist = PathTwist
        self.PathTwistBegin = PathTwistBegin
        self.PathRadiusOffset = PathRadiusOffset
        self.PathTaperX = PathTaperX
        self.PathTaperY = PathTaperY
        self.PathRevolutions = PathRevolutions
        self.PathSkew = PathSkew
        self.ProfileBegin = ProfileBegin
        self.ProfileEnd = ProfileEnd
        self.ProfileHollow = ProfileHollow
        self.TextureEntry = TextureEntry
        self.TextureAnim = TextureAnim
        self.NameValue = NameValue
        self.Data = Data
        self.Text = Text
        self.TextColor = TextColor
        self.MediaURL = MediaURL
        self.PSBlock = PSBlock
        self.ExtraParams = ExtraParams
        self.Sound = Sound
        self.OwnerID = OwnerID
        self.Gain = Gain
        self.Flags = Flags
        self.Radius = Radius
        self.JointType = JointType
        self.JointPivot = JointPivot
        self.JointAxisOrAnchor = JointAxisOrAnchor
        self.FootCollisionPlane = FootCollisionPlane
        self.Position = Position
        self.Velocity = Velocity
        self.Acceleration = Acceleration
        self.Rotation = Rotation
        self.AngularVelocity = AngularVelocity
        self.CreatorID = None
        self.GroupID = None
        self.CreationDate = None
        self.BaseMask = None
        self.OwnerMask = None
        self.GroupMask = None
        self.EveryoneMask = None
        self.NextOwnerMask = None
        self.OwnershipCost = None
        self.SaleType = None
        self.SalePrice = None
        self.AggregatePerms = None
        self.AggregatePermTextures = None
        self.AggregatePermTexturesOwner = None
        self.Category = None
        self.InventorySerial = None
        self.ItemID = None
        self.FolderID = None
        self.FromTaskID = None
        self.LastOwnerID = None
        self.Name = None
        self.Description = None
        self.TouchName = None
        self.SitName = None
        self.TextureID = None
        return

    def update_object_permissions(self, agent, Field, Set, Mask, Override=False):
        """ update permissions for a list of objects

        This will update a specific bit to a specific value.
        """
        self.send_ObjectPermissions(agent, agent.agent_id, agent.session_id, Field, Set, Mask, Override)

    def send_ObjectPermissions(self, agent, AgentID, SessionID, Field, Set, Mask, Override):
        """ send an ObjectPermissions message to the host simulator"""
        packet = Message('ObjectPermissions', Block('AgentData', AgentID=AgentID, SessionID=SessionID), Block('HeaderData', Override=Override), Block('ObjectData', ObjectLocalID=self.LocalID, Field=Field, Set=Set, Mask=Mask))
        agent.region.enqueue_message(packet)

    def set_object_full_permissions(self, agent):
        """ 
        Set Next Owner Permissions Copy, Modify, Transfer 
        This is also called 'full permissions'.
        """
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Copy)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Modify)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Transfer)

    def set_object_copy_mod_permissions(self, agent):
        """ 
        Set Next Owner Permissions to Copy/Mod
        This is a common permission set for attachements.
        """
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Copy)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Modify)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 0, PermissionsMask.Transfer)

    def set_object_mod_transfer_permissions(self, agent):
        """
        Set Next Owner Permissions to Mod/Transfer
        This is a common permission set for clothing.
        """
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 0, PermissionsMask.Copy)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Modify)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Transfer)

    def set_object_transfer_only_permissions(self, agent):
        """
        Set Next Owner Permissions to Transfer Only
        This is the most restrictive set of permissions allowed.
        """
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 0, PermissionsMask.Copy)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 0, PermissionsMask.Modify)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Transfer)

    def set_object_copy_transfer_permissions(self, agent):
        """
        Set Next Owner Permissions to Copy/Transfer
        """
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Copy)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 0, PermissionsMask.Modify)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Transfer)

    def set_object_copy_only_permissions(self, agent):
        """
        Set Next Owner Permissions to Copy Only
        """
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 1, PermissionsMask.Copy)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 0, PermissionsMask.Modify)
        self.update_object_permissions(agent, PermissionsTarget.NextOwner, 0, PermissionsMask.Transfer)

    def set_object_name(self, agent, Name):
        """ update the name of an object 

        """
        self.send_ObjectName(agent, agent.agent_id, agent.session_id, {1: [self.LocalID, Name]})

    def send_ObjectName(self, agent, AgentID, SessionID, LocalID_Name_map):
        """ send on ObjectName message to the host simulator 

        expects LocalID_Name_map = {1:[LocalID, Name]}
        """
        packet = Message('ObjectName', Block('AgentData', AgentID=AgentID, SessionID=SessionID), *[ Block('ObjectData', LocalID=LocalID_Name_map[item][0], Name=LocalID_Name_map[item][1]) for item in LocalID_Name_map ])
        agent.region.enqueue_message(packet)

    def set_object_description(self, agent, Description):
        """ update the description of an objects 

        """
        self.send_ObjectDescription(agent, agent.agent_id, agent.session_id, {1: [self.LocalID, Description]})

    def send_ObjectDescription(self, agent, AgentID, SessionID, LocalID_Description_map):
        """ send on ObjectDescription message to the host simulator 

        expects LocalID_Description_map = {1:[LocalID, Description]}
        """
        packet = Message('ObjectDescription', Block('AgentData', AgentID=AgentID, SessionID=SessionID), *[ Block('ObjectData', LocalID=LocalID_Description_map[item][0], Description=LocalID_Description_map[item][1]) for item in LocalID_Description_map ])
        agent.region.enqueue_message(packet)

    def derez(self, agent, destination, destinationID, transactionID, GroupID, PacketCount=1, PacketNumber=0):
        """ derez an object, specifying the destination """
        self.send_DeRezObject(agent, agent.agent_id, agent.session_id, GroupID, destination, destinationID, transactionID, PacketCount, PacketNumber, self.LocalID)

    def send_DeRezObject(self, agent, AgentID, SessionID, GroupID, Destination, DestinationID, TransactionID, PacketCount, PacketNumber, ObjectLocalID):
        """ send a DerezObject message to the host simulator """
        packet = Message('DeRezObject', Block('AgentData', AgentID=AgentID, SessionID=SessionID), Block('AgentBlock', GroupID=GroupID, Destination=Destination, DestinationID=DestinationID, TransactionID=TransactionID, PacketCount=PacketCount, PacketNumber=PacketNumber), Block('ObjectData', ObjectLocalID=ObjectLocalID))
        agent.region.enqueue_message(packet)

    def take(self, agent):
        """ take object into inventory """
        parent_folder = self.FolderID
        if not (parent_folder and agent.settings.ENABLE_INVENTORY_MANAGEMENT):
            logger.warning('Inventory not available, please enable settings.ENABLE_INVENTORY_MANAGEMENT')
            return
        if not parent_folder:
            objects_folder = [ folder for folder in agent.inventory.folders if folder.Name == 'Objects' ]
            if objects_folder:
                parent_folder = objects_folder[0].FolderID
            else:
                logger.warning('Unable to locate top-level Objects folder to take item into inventory.')
                return
        self.derez(agent, 4, parent_folder, uuid.uuid4(), agent.ActiveGroupID)

    def select(self, agent):
        """ select an object

        """
        self.send_ObjectSelect(agent, agent.agent_id, agent.session_id, [self.LocalID])

    def send_ObjectSelect(self, agent, AgentID, SessionID, ObjectLocalIDs):
        """ send an ObjectSelect message to the agent's host simulator

        expects a list of ObjectLocalIDs """
        packet = Message('ObjectSelect', Block('AgentData', AgentID=AgentID, SessionID=SessionID), *[ Block('ObjectData', ObjectLocalID=ObjectLocalID) for ObjectLocalID in ObjectLocalIDs ])
        agent.region.enqueue_message(packet)

    def deselect(self, agent):
        """ deselect an object

        """
        self.send_ObjectDeselect(agent, agent.agent_id, agent.session_id, [self.LocalID])

    def send_ObjectDeselect(self, agent, AgentID, SessionID, ObjectLocalIDs):
        """ send an ObjectDeselect message to the agent's host simulator

        expects a list of ObjectLocalIDs """
        packet = Message('ObjectDeselect', Block('AgentData', AgentID=AgentID, SessionID=SessionID), *[ Block('ObjectData', ObjectLocalID=ObjectLocalID) for ObjectLocalID in ObjectLocalIDs ])
        agent.region.enqueue_message(packet)

    def _update_properties(self, properties):
        """ takes a dictionary of attribute:value and makes it so """
        for attribute in properties.keys():
            setattr(self, attribute, properties[attribute])