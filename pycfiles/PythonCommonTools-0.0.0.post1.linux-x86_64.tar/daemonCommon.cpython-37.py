# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.7/dist-packages/pythoncommontools/daemonCommon/daemonCommon.py
# Compiled at: 2019-05-03 20:34:21
# Size of source mod 2**32: 3244 bytes
from argparse import ArgumentParser
from enum import unique, Enum
from os import kill, P_NOWAIT, spawnlp, getpid, remove
from os.path import sep, extsep, isfile
from signal import SIGTERM
from psutil import Process, pid_exists
from tempfile import gettempdir
pidExtension = extsep + 'pid'
pidDirectory = gettempdir() + sep

@unique
class Action(Enum):
    START = 'start'
    STOP = 'stop'
    STATUS = 'status'


@unique
class Status(Enum):
    RUNNING = 'running'
    SLEEPING = 'sleeping'
    ZOMBIE = 'zombie'


def startSingleInstance(scriptName):
    pid = writePidFile(scriptName)
    return pid


def stopSingleInstance(scriptName):
    pid = readPidFile(scriptName)
    stop(pid)
    pidFileName = getPidFileName(scriptName)
    if isfile(pidFileName):
        remove(pidFileName)


def statusSingleInstance(scriptName):
    pid = readPidFile(scriptName)
    pidStatus = status(pid)
    return pidStatus


def readPidFile(scriptName):
    pid = 0
    pidFileName = getPidFileName(scriptName)
    if isfile(pidFileName):
        with open(pidFileName, 'r') as (pidFile):
            pid = pidFile.read()
        pidFile.closed
        pid = int(pid)
    return pid


def writePidFile(scriptName):
    pidFileName = getPidFileName(scriptName)
    pid = getpid()
    with open(pidFileName, 'w') as (pidFile):
        pidFile.write(str(pid))
    pidFile.closed
    return pid


def getPidFileName(scriptName):
    pidFileName = pidDirectory + scriptName + pidExtension
    return pidFileName


def daemonize(customStart, customStop, customStatus):
    parser = ArgumentParser()
    parser.add_argument('action', help='start|stop|status', type=str)
    args = parser.parse_args()
    if args.action == Action.START.value:
        customStop()
        customStart()
    else:
        if args.action == Action.STOP.value:
            customStop()
        else:
            if args.action == Action.STATUS.value:
                customStatus()
            else:
                raise Exception('Unknown command')


def start(commandName, *commandArguments):
    pid = spawnlp(P_NOWAIT, commandName, commandName, *commandArguments)
    return pid


def stop(pid):
    if pid:
        if pid_exists(pid):
            kill(pid, SIGTERM)


def status(pid):
    status = None
    if pid:
        if pid_exists(pid):
            process = Process(pid)
            status = process.status()
    return status