# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/instrumentino/cfg.py
# Compiled at: 2015-11-23 10:12:58
from __future__ import division
from datetime import datetime
import time, os
from pkg_resources import resource_filename
import wx, threading
__author__ = 'yoelk'
numIntegerPartWidth = 6
numFractionPartWidth = 3
numStringFormat = '{:' + str(numIntegerPartWidth) + '.' + str(numFractionPartWidth) + 'f}'
methodWildcard = 'Method file (*.mtd)|*.mtd'
sequenceWildcard = 'Sequence file (*.seq)|*.seq'
EVT_LOG_UPDATE = wx.NewId()
EVT_UPDATE_CONTROLS = wx.NewId()
EVT_POP_MESSAGE = wx.NewId()
app = None
mainFrame = None
logTextCtrl = None
logGraph = None
commandsLogFile = None
signalsLogFile = None
systemUid = None
controllers = []
userStopped = False

def InitVariables(arguApp):
    """
    init system variables
    """
    global app
    global commandsLogFile
    global logGraph
    global logTextCtrl
    global mainFrame
    global signalsLogFile
    global systemUid
    global timeNow
    app = arguApp
    mainFrame = arguApp.mainFrame
    logTextCtrl = wx.xrc.XRCCTRL(arguApp.mainFrame, 'logTextCtrl')
    logTextCtrl.SetEditable(False)
    logGraph = arguApp.logGraph
    timeNow = datetime.now().strftime('%Y_%m_%d-%H_%M_%S')
    commandsLogFile = open(LogPath(timeNow + '.txt'), 'w')
    signalsLogFile = open(LogPath(timeNow + '.csv'), 'w')
    systemUid = arguApp.system.GetSystemUid()


def AddControllerIfNeeded(controllerClass):
    """
    add a controller to the needed controllers list, only if it doesn't exist already
    """
    global controllers
    for c in controllers:
        if isinstance(c, controllerClass):
            return

    controllers += [controllerClass()]


def Close():
    for c in controllers:
        c.Close()


def AllOnline():
    """
    check if all controllers are online
    """
    for c in controllers:
        if not c.online:
            return False

    return len(controllers) > 0


def IsCompOnline(sysComp):
    """
    check if the controller of a component is online
    """
    for c in controllers:
        if isinstance(c, sysComp.controllerClass):
            return c.online

    return False


def GetController(controllerClass):
    """
    return the active controller instance of this class
    """
    for c in controllers:
        if isinstance(c, controllerClass):
            return c

    return


def ResourcePath(relativePath=''):
    """
    Get the resource path
    """
    basePath = os.path.dirname(resource_filename('instrumentino.resources', 'main.xrc'))
    return os.path.join(basePath, relativePath)


def GetOrCreateDirectory(name):
    """
    Enter a directory and create it if needed
    """
    path = name + '/'
    try:
        os.mkdir(path)
    except:
        pass

    return path


def UserFilesPath(relativePath=''):
    """
    Get the user directory
    """
    return GetOrCreateDirectory('user') + relativePath


def LogPath(relativePath=''):
    """
    Get the log directory
    """
    return GetOrCreateDirectory('log') + relativePath


def Log(text):
    """
    Log an event
    """
    if logTextCtrl != None:
        logTextCtrl.WriteText(text + '\r')
    if commandsLogFile != None:
        commandsLogFile.write(text + '\r')
    return


def LogFromOtherThread(text, critical=False):
    """
    Log an event while running a method/sequence
    """
    wx.PostEvent(mainFrame, ResultEvent(EVT_LOG_UPDATE, (text, critical)))


def UpdateControlsFromOtherThread(runningOperation=False):
    """
    Update the control buttons while running a method/sequence
    """
    wx.PostEvent(mainFrame, ResultEvent(EVT_UPDATE_CONTROLS, runningOperation))


def Sleep(seconds, userStopEnabled=True):
    """
    Sleep, and wake up when user pressed the stop button
    """
    time.sleep(seconds % 1)
    end = time.time() + int(seconds)
    while time.time() <= end:
        if userStopped and userStopEnabled:
            return


def PopMessage(text=''):
    """
    Pop a message
    """
    e = threading.Event()
    wx.PostEvent(mainFrame, ResultEvent(EVT_POP_MESSAGE, (text, e, False)))


def WaitForUser(text=''):
    """
    Wait for the user to press a button
    """
    e = threading.Event()
    wx.PostEvent(mainFrame, ResultEvent(EVT_POP_MESSAGE, (text, e, True)))
    time.sleep(3)
    e.wait()


def HideVariableFromLog(varName):
    """
    Hide a variable trace from the signal log graph
    """
    logGraph.HideVariableFromLog(varName)


class ResultEvent(wx.PyEvent):
    """
    Simple event to carry arbitrary result data.
    """

    def __init__(self, eventType, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(eventType)
        self.data = data