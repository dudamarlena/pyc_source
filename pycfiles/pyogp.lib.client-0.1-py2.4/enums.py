# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyogp/lib/client/enums.py
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

class ImprovedIMDialogue(object):
    """ mappings for the values sent in an ImprovedInstantMessage packet """
    __module__ = __name__
    FromAgent = 0
    MessageBox = 1
    GroupInvitation = 3
    InventoryOffered = 4
    InventoryAccepted = 5
    InventoryDeclined = 6
    GroupVote = 7
    TaskInventoryOffered = 9
    TaskInventoryAccepted = 10
    TaskInventoryDeclined = 11
    NewUserDefault = 12
    SessionInvite = 13
    SessionP2PInvite = 14
    SessionGroupStart = 15
    SessionConferenceStart = 16
    SessionSend = 17
    SessionLeave = 18
    MessageFromTask = 19
    BusyAutoResponse = 20
    ConsoleAndChatHistory = 21
    TeleportLure = 22
    TeleportAccepted = 23
    TeleportDeclined = 24
    GodTeleportLure = 25
    Unused = 26
    GotoURL = 28
    FromTaskAsAlert = 31
    GroupNotice = 32
    GroupNoticeInventoryAccepted = 33
    GroupNoticeInventoryDeclined = 34
    GroupInvitationAccept = 35
    GroupInvitationDecline = 36
    GroupNoticeRequested = 37
    FriendshipOffered = 38
    FriendshipAccepted = 39
    FriendshipDeclined = 40
    TypingStart = 41
    TypingStop = 42


class InventoryType(object):
    """ mappings for inventory asset type """
    __module__ = __name__
    Texture = 0
    Sound = 1
    Callingcard = 2
    Landmark = 3
    Object = 6
    Notecard = 7
    Category = 8
    Root_Category = 9
    LSL = 10
    Snapshot = 15
    Attachment = 17
    Wearable = 18
    Animation = 19
    Gesture = 20
    Count = 21
    NONE = -1


class PCodeEnum(object):
    """ classifying the PCode of objects """
    __module__ = __name__
    Primitive = 9
    Avatar = 47
    Grass = 95
    NewTree = 111
    ParticleSystem = 143
    Tree = 255


class CompressedUpdateFlags(object):
    """ map of ObjectData.Flags """
    __module__ = __name__
    ScratchPad = 1
    Tree = 2
    contains_Text = 4
    contains_Particles = 8
    contains_Sound = 16
    contains_Parent = 32
    TextureAnim = 64
    contains_AngularVelocity = 128
    contains_NameValues = 256
    MediaURL = 512


class ExtraParam(object):
    """ extended Object attributes buried in some packets """
    __module__ = __name__
    Flexible = 16
    Light = 32
    Sculpt = 48


class ParcelFlags(object):
    """ Parcel Flag constants """
    __module__ = __name__
    AllowFly = 1 << 0
    AllowOtherScripts = 1 << 1
    ForSale = 1 << 2
    ForSaleObjects = 1 << 7
    AllowLandmarks = 1 << 3
    AllowTerraform = 1 << 4
    AllowDamage = 1 << 5
    CreateObjects = 1 << 6
    UseAccessGroup = 1 << 8
    UseAccessList = 1 << 9
    UseBanList = 1 << 10
    UsePassList = 1 << 11
    ShowDirectory = 1 << 12
    AllowDeedToGroup = 1 << 13
    ContributeWithDeed = 1 << 14
    SoundLocal = 1 << 15
    SellParcelObjects = 1 << 16
    AllowPublish = 1 << 17
    MaturePublish = 1 << 18
    URLWebPage = 1 << 19
    URLRawHTML = 1 << 20
    ResrictPushObject = 1 << 21
    DenyAnonomous = 1 << 22
    AllowGroupScripts = 1 << 25
    CreateGroupObjects = 1 << 26
    AllowAllObjectEntry = 1 << 27
    AllowGroupObjectEntry = 1 << 28
    AllowVoiceChat = 1 << 29
    UseEstateVoiceChannel = 1 << 30
    DenyAgeUnverified = 1 << 31


class MoneyTransactionType(object):
    """ Money transaction type constants """
    __module__ = __name__
    Null = 0
    ObjectClaim = 1000
    LandClaim = 1001
    GroupCreate = 1002
    ObjectPublicClaim = 1003
    GroupJoin = 1004
    TeleportCharge = 1100
    UploadCharge = 1101
    LandAuction = 1102
    ClassifiedCharge = 1103
    ObjectTax = 2000
    LandTax = 2001
    LightTax = 2002
    ParcelDirFee = 2003
    GroupTax = 2004
    ClassifiedRenew = 2005
    GiveInventory = 3000
    ObjectSale = 5000
    Gift = 5001
    LandSale = 5002
    ReferBonus = 5003
    InventorySale = 5004
    RefundPurchase = 5005
    LandPassSale = 5006
    DwellBonus = 5007
    PayObject = 5008
    ObjectPays = 5009
    GroupLandDeed = 6001
    GroupObjectDeed = 6002
    GroupLiability = 6003
    GroupDividend = 6004
    MembershipDues = 6005
    ObjectRelease = 8000
    LandRelease = 8001
    ObjectDelete = 8002
    ObjectPublicDecay = 8003
    ObjectPublicDelete = 8004
    LindenAdjustment = 9000
    LindenGrant = 9001
    LindenPenalty = 9002
    EventFee = 9003
    EventPrize = 9004
    StipendBasic = 10000
    StipendDeveloper = 10001
    StipendAlways = 10002
    StipendDaily = 10003
    StipendRating = 10004
    StipendDelta = 10005


class TransactionFlags(object):
    __module__ = __name__
    Null = 0
    SourceGroup = 1
    DestGroup = 2
    OwnerGroup = 4
    SimultaneousContribution = 8
    SimultaneousContributionRemoval = 16


class AgentState(object):
    __module__ = __name__
    Null = 0
    Typing = 4
    Editing = 16


class AgentUpdateFlags(object):
    __module__ = __name__
    Null = 0
    HideTitle = 1


class AgentControlFlags(object):
    """ Used for the ControlFlags member of AgentUpdate packets """
    __module__ = __name__
    _ControlAtPosIndex = 0
    _ControlAtNegIndex = 1
    _ControlLeftPosIndex = 2
    _ControlLeftNegIndex = 3
    _ControlUpPosIndex = 4
    _ControlUpNegIndex = 5
    _ControlPitchPosIndex = 6
    _ControlPitchNegIndex = 7
    _ControlYawPosIndex = 8
    _ControlYawNegIndex = 9
    _ControlFastAtIndex = 10
    _ControlFastLeftIndex = 11
    _ControlFastUpIndex = 12
    _ControlFlyIndex = 13
    _ControlStopIndex = 14
    _ControlFinishAnimIndex = 15
    _ControlStandUpIndex = 16
    _ControlSitOnGroundIndex = 17
    _ControlMouselookIndex = 18
    _ControlNudgeAtPosIndex = 19
    _ControlNudgeAtNegIndex = 20
    _ControlNudgeLeftPosIndex = 21
    _ControlNudgeLeftNegIndex = 22
    _ControlNudgeUpPosIndex = 23
    _ControlNudgeUpNegIndex = 24
    _ControlTurnLeftIndex = 25
    _ControlTurnRightIndex = 26
    _ControlAwayIndex = 27
    _ControlLbuttonDownIndex = 28
    _ControlLbuttonUpIndex = 29
    _ControlMlLbuttonDownIndex = 30
    _ControlMlLbuttonUpIndex = 31
    _TotalControls = 32
    AtPos = 1 << _ControlAtPosIndex
    AtNeg = 1 << _ControlAtNegIndex
    LeftPos = 1 << _ControlLeftPosIndex
    LeftNeg = 1 << _ControlLeftNegIndex
    UpPos = 1 << _ControlUpPosIndex
    UpNeg = 1 << _ControlUpNegIndex
    PitchPos = 1 << _ControlPitchPosIndex
    PitchNeg = 1 << _ControlPitchNegIndex
    YawPos = 1 << _ControlYawPosIndex
    YawNeg = 1 << _ControlYawNegIndex
    FastAt = 1 << _ControlFastAtIndex
    FastLeft = 1 << _ControlFastLeftIndex
    FastUp = 1 << _ControlFastUpIndex
    Fly = 1 << _ControlFlyIndex
    Stop = 1 << _ControlStopIndex
    FinishAnim = 1 << _ControlFinishAnimIndex
    StandUp = 1 << _ControlStandUpIndex
    SitOnGround = 1 << _ControlSitOnGroundIndex
    Mouselook = 1 << _ControlMouselookIndex
    NudgeAtPos = 1 << _ControlNudgeAtPosIndex
    NudgeAtNeg = 1 << _ControlNudgeAtNegIndex
    NudgeLeftPos = 1 << _ControlNudgeLeftPosIndex
    NudgeLeftNeg = 1 << _ControlNudgeLeftNegIndex
    NudgeUpPos = 1 << _ControlNudgeUpPosIndex
    NudgeUpNeg = 1 << _ControlNudgeUpNegIndex
    TurnLeft = 1 << _ControlTurnLeftIndex
    TurnRight = 1 << _ControlTurnRightIndex
    Away = 1 << _ControlAwayIndex
    LbuttonDown = 1 << _ControlLbuttonDownIndex
    LbuttonUp = 1 << _ControlLbuttonUpIndex
    MlLbuttonDown = 1 << _ControlMlLbuttonDownIndex
    MlLbuttonUp = 1 << _ControlMlLbuttonUpIndex
    At = AtPos | AtNeg | NudgeAtPos | NudgeAtNeg
    Left = LeftPos | LeftNeg | NudgeLeftPos | NudgeLeftNeg
    Up = UpPos | UpNeg | NudgeUpPos | NudgeUpNeg
    Horizontal = At | Left
    NotUsedByLsl = Fly | Stop | FinishAnim | StandUp | SitOnGround | Mouselook | Away
    Movement = At | Left | Up
    Rotation = PitchPos | PitchNeg | YawPos | YawNeg
    Nudge = NudgeAtPos | NudgeAtNeg | NudgeLeftPos | NudgeLeftNeg


class TextureIndex(object):
    __module__ = __name__
    TEX_HEAD_BODYPAINT = 0
    TEX_UPPER_SHIRT = 1
    TEX_LOWER_PANTS = 2
    TEX_EYES_IRIS = 3
    TEX_HAIR = 4
    TEX_UPPER_BODYPAINT = 5
    TEX_LOWER_BODYPAINT = 6
    TEX_LOWER_SHOES = 7
    TEX_HEAD_BAKED = 8
    TEX_UPPER_BAKED = 9
    TEX_LOWER_BAKED = 10
    TEX_EYES_BAKED = 11
    TEX_LOWER_SOCKS = 12
    TEX_UPPER_JACKET = 13
    TEX_LOWER_JACKET = 14
    TEX_UPPER_GLOVES = 15
    TEX_UPPER_UNDERSHIRT = 16
    TEX_LOWER_UNDERPANTS = 17
    TEX_SKIRT = 18
    TEX_SKIRT_BAKED = 19
    TEX_HAIR_BAKED = 20
    TEX_COUNT = 21


class BakedIndex(object):
    __module__ = __name__
    BAKED_HEAD = 0
    BAKED_UPPER = 1
    BAKED_LOWER = 2
    BAKED_EYES = 3
    BAKED_SKIRT = 4
    BAKED_HAIR = 5
    BAKED_COUNT = 6

    def BakedToTextureIndex(self, bakedIndex):
        if bakedIndex is self.BAKED_HEAD:
            return TextureIndex.TEX_HEAD_BAKED
        elif bakedIndex is self.BAKED_UPPER:
            return TextureIndex.TEX_UPPER_BAKED
        elif bakedIndex is self.BAKED_LOWER:
            return TextureIndex.TEX_LOWER_BAKED
        elif bakedIndex is self.BAKED_EYES:
            return TextureIndex.TEX_EYES_BAKED
        elif bakedIndex is self.BAKED_SKIRT:
            return TextureIndex.TEX_SKIRT_BAKED
        elif bakedIndex is self.BAKED_HAIR:
            return TextureIndex.TEX_HAIR_BAKED
        else:
            return -1


class WearablesIndex(object):
    __module__ = __name__
    WT_SHAPE = 0
    WT_SKIN = 1
    WT_HAIR = 2
    WT_EYES = 3
    WT_SHIRT = 4
    WT_PANTS = 5
    WT_SHOES = 6
    WT_SOCKS = 7
    WT_JACKET = 8
    WT_GLOVES = 9
    WT_UNDERSHIRT = 10
    WT_UNDERPANTS = 11
    WT_SKIRT = 12
    WT_COUNT = 13


class WearableMap(object):
    __module__ = __name__

    def __init__(self):
        self.map = {}
        self.map[BakedIndex.BAKED_HEAD] = [
         WearablesIndex.WT_SHAPE, WearablesIndex.WT_SKIN, WearablesIndex.WT_HAIR]
        self.map[BakedIndex.BAKED_UPPER] = [WearablesIndex.WT_SHAPE, WearablesIndex.WT_SKIN, WearablesIndex.WT_SHIRT, WearablesIndex.WT_JACKET, WearablesIndex.WT_GLOVES, WearablesIndex.WT_UNDERSHIRT]
        self.map[BakedIndex.BAKED_LOWER] = [WearablesIndex.WT_SHAPE, WearablesIndex.WT_SKIN, WearablesIndex.WT_PANTS, WearablesIndex.WT_SHOES, WearablesIndex.WT_SOCKS, WearablesIndex.WT_JACKET, WearablesIndex.WT_UNDERPANTS]
        self.map[BakedIndex.BAKED_EYES] = [WearablesIndex.WT_EYES]
        self.map[BakedIndex.BAKED_SKIRT] = [WearablesIndex.WT_SKIRT]
        self.map[BakedIndex.BAKED_HAIR] = [WearablesIndex.WT_HAIR]


class AssetType(object):
    __module__ = __name__
    Texture = 0
    Sound = 1
    CallingCard = 2
    Landmark = 3
    Script = 4
    Clothing = 5
    Object = 6
    Notecard = 7
    Category = 8
    RootCategory = 9
    LSLText = 10
    LSLByteCode = 11
    TextureTGA = 12
    BodyPart = 13
    Trash = 14
    SnapshotCategory = 15
    LostAndFound = 16
    SoundWav = 17
    ImageTGA = 18
    ImageJPEG = 19
    Animation = 20
    Gesture = 21
    Simstate = 22
    Count = 23
    NONE = -1


class TransferChannelType(object):
    __module__ = __name__
    Unknown = 0
    Misc = 1
    Asset = 2
    NumTypes = 3


class TransferSourceType(object):
    __module__ = __name__
    Unknown = 0
    File = 1
    Asset = 2
    SimInvItem = 3
    SimEstate = 4
    NumTypes = 5


class TransferTargetType(object):
    __module__ = __name__
    Unknown = 0
    File = 1
    VFile = 2


class TransferStatus(object):
    __module__ = __name__
    OK = 0
    Done = 1
    Skip = 2
    Abort = 3
    Error = -1
    UnknownSource = -2
    InsufficientPermissions = -3


class Permissions(object):
    __module__ = __name__
    Transfer = 1 << 13
    Modify = 1 << 14
    Copy = 1 << 15
    Move = 1 << 19
    None_ = 0
    All = 2147483647
    Unrestricted = Transfer | Modify | Copy


class DeRezDestination(object):
    __module__ = __name__
    SaveIntoAgentInventory = 0
    AcquireToAgentInventory = 1
    SaveIntoTaskInventory = 2
    Attachment = 3
    TakeIntoAgentInventory = 4
    ForceToGodInventory = 5
    Trash = 6
    AttachmentToInventory = 7
    AttachmentExists = 8
    ReturnToOwner = 9
    ReturnToLastOwner = 10


class MapItem(object):
    __module__ = __name__
    Telehub = 1
    PGEvent = 2
    MatureEvent = 3
    AgentLocations = 6
    LandForSale = 7
    Classified = 8
    AdultEvent = 9
    LandForSaleAdult = 10