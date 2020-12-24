# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-armv6l/egg/barobo/__init__.py
# Compiled at: 2014-09-16 19:33:24
__doc__ = "\nThe Barobo Python Module\n\nThis python module can be used to control Barobo robots. The easiest way to use\nthis package is in conjunction with BaroboLink. After connecting to the robots\nyou want to control in BaroboLink, the following python program will move\njoints 1 and 3 on the first connected Linkbot in BaroboLink::\n\n    from barobo import Linkbot\n    linkbot = Linkbot()\n    linkbot.connect()\n    linkbot.moveTo(180, 0, -180)\n\nYou may also use this package to control Linkbots without BaroboLink. In that\ncase, a typical control program will look something like this::\n    from barobo import Linkbot, Dongle\n\n    dongle = Dongle()\n    dongle.connect() # Connect to the dongle\n    linkbot = dongle.getLinkbot() # or linkbot = dongle.getLinkbot('2B2C') where \n                                  # '2B2C' should be replaced with the serial ID \n                                  # of your Linkbot. Note that the serial ID \n                                  # used here can be that of a nearby Linkbot \n                                  # that you wish to connect to wirelessly. If \n                                  # no serial ID is provided, the new linkbot \n                                  # will refer to the Linkbot currently \n                                  # connected via USB.\n                                  # Also, note that this function can be called\n                                  # multiple times to retrieve handles to \n                                  # multiple wireless Linkbots, which can all\n                                  # be controlled in the same Python script.\n    linkbot.moveTo(180, 0, -180)  # Move joint 1 180 degrees in the positive \n                                  # direction, joint 3 180 degrees in the \n                                  # negative direction\n\nFor more documentation, please refer to the documentation under the\nL{Linkbot<barobo.linkbot.Linkbot>} class.\n"
import struct, sys
try:
    import Queue
except:
    import queue as Queue

import threading, barobo._comms as _comms
from barobo.linkbot import Linkbot
from barobo.mobot import Mobot
ROBOTFORM_MOBOT = 1
ROBOTFORM_I = 2
ROBOTFORM_L = 3
ROBOTFORM_T = 4
ROBOT_NEUTRAL = 0
ROBOT_FORWARD = 1
ROBOT_BACKWARD = 2
ROBOT_HOLD = 3
ROBOT_POSITIVE = 4
ROBOT_NEGATIVE = 5
PINMODE_INPUT = 0
PINMODE_OUTPUT = 1
PINMODE_INPUTPULLUP = 2
AREF_DEFAULT = 0
AREF_INTERNAL = 1
AREF_INTERNAL1V1 = 2
AREF_INTERNAL2V56 = 3
AREF_EXTERNAL = 4
import os
if os.name == 'nt':
    if sys.version_info[0] == 3:
        import winreg
    else:
        import _winreg as winreg
if sys.platform.startswith('linux'):

    def __FROM(x):
        return ' find ' + x + ' -maxdepth 0 -print '


    def __SELECT():
        return " | xargs -I}{ find '}{' "


    def __AND():
        return __SELECT() + ' -maxdepth 1 '


    def __SUBSYSTEM(x):
        return ' -type l -name subsystem -lname \\*/' + x + " -printf '%h\\n' "


    def __SUBSYSTEMF(x):
        return ' -type l -name subsystem -lname \\*/' + x + " -printf '%%h\\n' "


    def __SYSATTR(x, y):
        return ' -type f -name ' + x + " -execdir grep -q '" + y + "' '{}' \\; -printf '%h\\n' "


    def __SYSATTRF(x, y):
        return ' -type f -name ' + x + " -execdir grep -q '" + y + "' '{}' \\; -printf '%%h\\n' "


    def __FIRST():
        return ' -quit '


    def __SELECTUP():
        return ' | xargs -I}{ sh -c \'x="}{"; while [ "/" != "$x" ]; do dirname "$x"; x=$(dirname "$x"); done\' ' + __AND()


    def findDongle():
        dongleIDs = [
         ('Barobo, Inc.', 'Mobot USB-Serial Adapter'),
         ('Barobo, Inc.', 'Linkbot USB-Serial Adapter'),
         ('Barobo, Inc.', 'Barobo USB-Serial Adapter')]
        import os, subprocess
        try:
            sysfs = os.environ['SYSFS_PATH']
        except:
            sysfs = '/sys'

        for manufacturer, productid in dongleIDs:
            cmd = __FROM(sysfs + '/devices') + __SELECT() + __SYSATTR('manufacturer', manufacturer) + __AND() + __SYSATTR('product', productid) + __SELECT() + __SUBSYSTEM('tty') + " | xargs -I{} grep DEVNAME '{}'/uevent" + ' | cut -d= -f2'
            with open('/dev/null') as (nullFile):
                p = subprocess.check_output([
                 '/bin/sh', '-c', cmd], stderr=nullFile)
            if len(p) > 1:
                return (str('/dev/') + p.decode('utf-8')).rstrip()


def _getSerialPorts():
    import serial
    if os.name == 'nt':
        available = []
        handle = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\\DEVICEMAP\\SERIALCOMM')
        for i in range(256):
            try:
                name, port, _ = winreg.EnumValue(handle, i)
                if name[:14] == '\\Device\\USBSER':
                    available.append(port)
            except:
                break

        return available
    else:
        from serial.tools import list_ports
        return [port[0] for port in list_ports.comports()]


def __checkLinkbotTTY(comport):
    import serial
    s = serial.Serial(comport, baudrate=230400)
    s.timeout = 2
    numtries = 0
    maxtries = 3
    while numtries < maxtries:
        try:
            s.write(bytearray([48, 3, 0]))
            r = s.recv(3)
            if r == [16, 3, 17]:
                break
        except:
            if numtries < maxtries:
                numtries += 1
            else:
                return True


def _unpack(fmt, buffer):
    if sys.version_info[0] == 2 and sys.version_info[1] == 6:
        return struct.unpack(fmt, bytes(buffer))
    else:
        if sys.version_info[0] == 3:
            return struct.unpack(fmt, buffer)
        return struct.unpack(fmt, str(buffer))


class BaroboException(Exception):

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)


class Dongle:
    """
    The BaroboCtx (BaroboContext) is the entity which manages all of the 
    Linkbots in a computational environment. If loosely represents a ZigBee 
    dongle which can communicate and with and control all Linkbots within its 
    communication range. 
    """
    RESP_OK = 16
    RESP_END = 17
    RESP_ERR = 255
    RESP_ALREADY_PAIRED = 254
    EVENT_BUTTON = 32
    EVENT_REPORTADDRESS = 33
    TWI_REGACCESS = 34
    EVENT_DEBUG_MSG = 35
    EVENT_JOINT_MOVED = 36
    EVENT_ACCEL_CHANGED = 37
    CMD_STATUS = 48
    CMD_DEMO = 49
    CMD_SETMOTORDIR = 50
    CMD_GETMOTORDIR = 51
    CMD_SETMOTORSPEED = 52
    CMD_GETMOTORSPEED = 53
    CMD_SETMOTORANGLES = 54
    CMD_SETMOTORANGLESABS = 55
    CMD_SETMOTORANGLESDIRECT = 56
    CMD_SETMOTORANGLESPID = 57
    CMD_GETMOTORANGLES = 58
    CMD_GETMOTORANGLESABS = 59
    CMD_GETMOTORANGLESTIMESTAMP = 60
    CMD_GETMOTORANGLESTIMESTAMPABS = 61
    CMD_SETMOTORANGLE = 62
    CMD_SETMOTORANGLEABS = 63
    CMD_SETMOTORANGLEDIRECT = 64
    CMD_SETMOTORANGLEPID = 65
    CMD_GETMOTORANGLE = 66
    CMD_GETMOTORANGLEABS = 67
    CMD_GETMOTORANGLETIMESTAMP = 68
    CMD_GETMOTORSTATE = 69
    CMD_GETMOTORMAXSPEED = 70
    CMD_GETENCODERVOLTAGE = 71
    CMD_GETBUTTONVOLTAGE = 72
    CMD_GETMOTORSAFETYLIMIT = 73
    CMD_SETMOTORSAFETYLIMIT = 74
    CMD_GETMOTORSAFETYTIMEOUT = 75
    CMD_SETMOTORSAFETYTIMEOUT = 76
    CMD_STOP = 77
    CMD_GETVERSION = 78
    CMD_BLINKLED = 79
    CMD_ENABLEBUTTONHANDLER = 80
    CMD_RESETABSCOUNTER = 81
    CMD_GETHWREV = 82
    CMD_SETHWREV = 83
    CMD_TIMEDACTION = 84
    CMD_GETBIGSTATE = 85
    CMD_SETFOURIERCOEFS = 86
    CMD_STARTFOURIER = 87
    CMD_LOADMELODY = 88
    CMD_PLAYMELODY = 89
    CMD_GETADDRESS = 90
    CMD_QUERYADDRESSES = 91
    CMD_GETQUERIEDADDRESSES = 92
    CMD_CLEARQUERIEDADDRESSES = 93
    CMD_REQUESTADDRESS = 94
    CMD_REPORTADDRESS = 95
    CMD_REBOOT = 96
    CMD_GETSERIALID = 97
    CMD_SETSERIALID = 98
    CMD_SETRFCHANNEL = 99
    CMD_FINDMOBOT = 100
    CMD_PAIRPARENT = 101
    CMD_UNPAIRPARENT = 102
    CMD_RGBLED = 103
    CMD_SETMOTORPOWER = 104
    CMD_GETBATTERYVOLTAGE = 105
    CMD_BUZZERFREQ = 106
    CMD_GETACCEL = 107
    CMD_GETFORMFACTOR = 108
    CMD_GETRGB = 109
    CMD_GETVERSIONS = 110
    CMD_PLACEHOLDER201304121823 = 111
    CMD_PLACEHOLDER201304152311 = 112
    CMD_PLACEHOLDER201304161605 = 113
    CMD_PLACEHOLDER201304181705 = 114
    CMD_PLACEHOLDER201304181425 = 115
    CMD_SET_GRP_MASTER = 116
    CMD_SET_GRP_SLAVE = 117
    CMD_SET_GRP = 118
    CMD_SAVE_POSE = 119
    CMD_MOVE_TO_POSE = 120
    CMD_IS_MOVING = 121
    CMD_GET_MOTOR_ERRORS = 122
    CMD_MOVE_MOTORS = 123
    CMD_TWI_SEND = 124
    CMD_TWI_RECV = 125
    CMD_TWI_SENDRECV = 126
    CMD_SET_ACCEL = 127
    CMD_SMOOTHMOVE = 128
    CMD_SETMOTORSTATES = 129
    CMD_SETGLOBALACCEL = 130
    CMD_PING = 137
    CMD_GET_HW_REV = 138
    CMD_SET_HW_REV = 139
    CMD_SET_JOINT_EVENT_THRESHOLD = 140
    CMD_SET_ENABLE_JOINT_EVENT = 141
    CMD_SET_ACCEL_EVENT_THRESHOLD = 142
    CMD_SET_ENABLE_ACCEL_EVENT = 143
    MOTOR_FORWARD = 1
    MOTOR_BACKWARD = 2
    TWIMSG_HEADER = 34
    TWIMSG_REGACCESS = 1
    TWIMSG_SETPINMODE = 2
    TWIMSG_DIGITALWRITEPIN = 3
    TWIMSG_DIGITALREADPIN = 4
    TWIMSG_ANALOGWRITEPIN = 5
    TWIMSG_ANALOGREADPIN = 6
    TWIMSG_ANALOGREF = 7

    def __init__(self):
        self.writeQueue = Queue.Queue()
        self.readQueue = Queue.Queue()
        self.ctxReadQueue = Queue.Queue()
        self.link = None
        self.phys = None
        self.children = {}
        self.scannedIDs = {}
        self.scannedIDs_cond = threading.Condition()
        self.giant_lock = threading.Lock()
        return

    def __init_comms(self):
        self.commsInThread = threading.Thread(target=self._commsInEngine)
        self.commsInThread.daemon = True
        self.commsInThread.start()
        self.commsOutThread = threading.Thread(target=self._commsOutEngine)
        self.commsOutThread.daemon = True
        self.commsOutThread.start()

    def addLinkbot(self, linkbot):
        self.children[linkbot.getSerialID()] = linkbot

    def autoConnect(self):
        try:
            self.connectBaroboBrowser()
        except:
            if os.name == 'nt':
                myports = _getSerialPorts()
            else:
                myports = [
                 findDongle()]
            connected = False
            for port in myports:
                try:
                    self.connectDongleSFP(port)
                    connected = True
                except:
                    pass

            if not connected:
                raise BaroboException('Could not find attached dongle.')

    def connect(self):
        """
        Automatically connect to an attached Barobo Dongle. Throw an 
        exception if no dongle is found.
        """
        self.autoConnect()

    def connectBaroboBrowser(self):
        """
        Connect the dongle to BaroboBrowser
        """
        self.phys = _comms.PhysicalLayer_Socket('localhost', 5769)
        self.link = _comms.LinkLayer_TTY(self.phys, self.handlePacket)
        self.link.start()
        self._Dongle__init_comms()
        try:
            self._Dongle__init_comms()
            self._Dongle__checkStatus()
            self._Dongle__getDongleID()
        except Exception as e:
            self.phys.close()
            self.link.stop()
            raise e

    def connectBaroboLink(self):
        """
        Connect the BaroboContext to BaroboLink.
        """
        self.phys = _comms.PhysicalLayer_Socket('localhost', 5768)
        self.link = _comms.LinkLayer_Socket(self.phys, self.handlePacket)
        self.link.start()
        self._Dongle__init_comms()
        self._Dongle__getDongleID()

    def connectBluetooth(self, macaddr):
        """
        Connect the BaroboContext to a Bluetooth LinkPod.
        """
        self.phys = _comms.PhysicalLayer_Bluetooth(macaddr)
        self.link = _comms.LinkLayer_TTY(self.phys, self.handlePacket)
        self.link.start()
        try:
            self._Dongle__init_comms()
            self._Dongle__checkStatus()
            self._Dongle__getDongleID()
        except:
            raise BaroboException('Could not connect to Bluetooth at {0}'.format(macaddr))

    def connectMobotBluetooth(self, macaddr):
        """
        Connect the BaroboContext to a Bluetooth Mobot or legacy Bluetooth 
        Linkbot.
        """
        self.phys = _comms.PhysicalLayer_Bluetooth(macaddr)
        self.link = _comms.LinkLayer_Socket(self.phys, self.handlePacket)
        self.link.start()
        try:
            self._Dongle__init_comms()
        except:
            raise BaroboException('Could not connect to Bluetooth at {0}'.format(macaddr))

    def connectDongleTTY(self, ttyfilename):
        """
        Connect the BaroboCtx to a Linkbot that is connected with a USB cable.
        """
        self.phys = _comms.PhysicalLayer_TTY(ttyfilename)
        self.link = _comms.LinkLayer_TTY(self.phys, self.handlePacket)
        self.link.start()
        try:
            self._Dongle__init_comms()
            self._Dongle__checkStatus()
            self._Dongle__getDongleID()
        except:
            self.phys.close()
            self.link.stop()
            self.connectDongleSFP(ttyfilename)

    def connectDongleSFP(self, ttyfilename):
        """
        Connect the BaroboCtx to a Linkbot using libsfp that is connected with a 
        USB cable.
        """
        self.phys = _comms.PhysicalLayer_TTY(ttyfilename)
        self.link = _comms.LinkLayer_SFP(self.phys, self.handlePacket)
        self.link.start()
        try:
            self._Dongle__init_comms()
            self._Dongle__checkStatus()
            self._Dongle__getDongleID()
        except:
            raise BaroboException('Could not connect to dongle at {0}'.format(ttyfilename))

    def disconnect(self):
        self.link.stop()
        self.phys.disconnect()
        self.children = {}

    def handlePacket(self, packet):
        self.readQueue.put(packet)

    def scanForRobots(self):
        buf = [
         self.CMD_QUERYADDRESSES, 3, 0]
        self.writePacket(_comms.Packet(buf, 0))

    def getScannedRobots(self):
        return self.scannedIDs

    def getLinkbot(self, serialID=None, linkbotClass=None):
        if serialID is None:
            self.giant_lock.acquire()
            serialID = list(self.scannedIDs.keys())[0]
            self.giant_lock.release()
        serialID = serialID.upper()
        if serialID not in self.scannedIDs:
            self.findRobot(serialID)
            self.waitForRobot(serialID)
        if linkbotClass is None:
            linkbotClass = Linkbot
        if serialID in self.children:
            return self.children[serialID]
        else:
            l = linkbotClass()
            l.zigbeeAddr = self.scannedIDs[serialID]
            l.serialID = serialID
            l.baroboCtx = self
            self.children[serialID] = l
            l.form = l.getFormFactor()
            if l.zigbeeAddr != self.zigbeeAddr:
                l._pairParent()
            return l

    def findRobot(self, serialID):
        if serialID in self.scannedIDs:
            return
        buf = bytearray([self.CMD_FINDMOBOT, 7])
        buf += bytearray(serialID.encode('ascii'))
        buf += bytearray([0])
        self.writePacket(_comms.Packet(buf, 0))

    def waitForRobot(self, serialID, timeout=2.0):
        self.scannedIDs_cond.acquire()
        numtries = 0
        while serialID not in self.scannedIDs:
            self.scannedIDs_cond.wait(2)
            numtries += 1
            if numtries >= 3:
                self.scannedIDs_cond.release()
                raise BaroboException('Robot {0} not found.'.format(serialID))
                continue

        self.scannedIDs_cond.release()
        return serialID in self.scannedIDs

    def writePacket(self, packet):
        self.writeQueue.put(packet)

    def _commsInEngine(self):
        while True:
            packet = self.readQueue.get(block=True, timeout=None)
            if packet.data[0] == self.EVENT_REPORTADDRESS:
                botid = _unpack('!4s', packet.data[4:8])[0]
                zigbeeAddr = _unpack('!H', packet[2:4])[0]
                if botid not in self.scannedIDs:
                    self.scannedIDs_cond.acquire()
                    self.scannedIDs[botid.decode('ascii')] = zigbeeAddr
                    self.scannedIDs_cond.notify()
                    self.scannedIDs_cond.release()
                continue
            else:
                if packet.data[0] == self.EVENT_DEBUG_MSG:
                    print(packet.data[2:])
                    continue
                zigbeeAddr = packet.addr
                if 0 == zigbeeAddr:
                    self.ctxReadQueue.put(packet)
                    continue
            for _, linkbot in self.children.items():
                if zigbeeAddr == linkbot.zigbeeAddr:
                    linkbot.readQueue.put(packet, block=True)
                    break

        return

    def _commsOutEngine(self):
        while True:
            packet = self.writeQueue.get()
            self.link.write(packet.data, packet.addr)

    def __checkStatus(self):
        numtries = 0
        maxtries = 3
        while True:
            buf = [
             self.CMD_STATUS, 3, 0]
            self.writePacket(_comms.Packet(buf, 0))
            try:
                response = self.ctxReadQueue.get(block=True, timeout=2.0)
                break
            except:
                if numtries < maxtries:
                    numtries += 1
                    continue
                else:
                    raise

    def __getDongleID(self):
        numtries = 0
        maxtries = 3
        while True:
            buf = [
             self.CMD_GETSERIALID, 3, 0]
            self.writePacket(_comms.Packet(buf, 0))
            try:
                response = self.ctxReadQueue.get(block=True, timeout=2.0)
                break
            except:
                if numtries < maxtries:
                    numtries += 1
                    continue
                else:
                    raise

        serialID = _unpack('!4s', response[2:6])[0].decode('UTF-8')
        buf = [self.CMD_GETADDRESS, 3, 0]
        self.writePacket(_comms.Packet(buf, 0))
        response = self.ctxReadQueue.get(block=True, timeout=2.0)
        zigbeeAddr = _unpack('!H', response[2:4])[0]
        self.zigbeeAddr = zigbeeAddr
        self.scannedIDs[serialID] = zigbeeAddr


BaroboCtx = Dongle