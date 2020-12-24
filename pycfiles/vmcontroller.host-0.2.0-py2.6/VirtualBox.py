# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/vmcontroller/host/controller/hypervisors/VirtualBox.py
# Compiled at: 2011-03-06 20:21:16
try:
    import logging, os, platform, sys, uuid, pdb
    from twisted.internet import protocol, reactor, defer, threads
    from vmcontroller.common import support, exceptions
except ImportError, e:
    print 'Import error in %s : %s' % (__name__, e)
    import sys
    sys.exit()

WAITING_GRACE_MS = 800
logger = logging.getLogger(__name__)

def version():

    def impl():
        return ctx['vb'].version

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def createVM(vboxFile):
    vb = ctx['vb']

    def impl():
        mach = vb.openMachine(vboxFile)
        vb.registerMachine(mach)
        logger.debug("Created VM '%s' with UUID %s" % (mach.name, mach.id))
        return (True, mach.name)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def removeVM(vm):

    def impl():
        mgr = ctx['mgr']
        vb = ctx['vb']
        mach = machById(vm)
        id = mach.id
        name = mach.name
        logger.debug("Removing VM '%s' with UUID %s " % (mach.name, id))
        mediums = mach.unregister(ctx['global'].constants.CleanupMode_DetachAllReturnHardDisksOnly)
        for medium in mediums:
            logger.debug('Unregistering Hard Disk: %s' % medium.name)
            medium.close()

        return (
         True, name)

    d = threads.deferToThread(impl)
    return d


def start(vm, guiMode):
    if platform.system() != 'Windows':

        def impl():
            mgr = ctx['mgr']
            vb = ctx['vb']
            perf = ctx['perf']
            mach = machById(vm)
            session = mgr.getSessionObject(vb)
            logger.info('Starting VM for machine %s' % mach.name)
            if guiMode:
                progress = mach.launchVMProcess(session, 'gui', '')
            else:
                progress = mach.launchVMProcess(session, 'vrdp', '')
            while not progress.completed:
                logger.debug('Loading VM %s - %s %%' % (mach.name, str(progress.percent)))
                progress.waitForCompletion(WAITING_GRACE_MS)

            if progress.completed and int(progress.resultCode) == 0:
                logger.info('Startup of machine %s completed: %s' % (mach.name, str(progress.completed)))
                if perf:
                    try:
                        perf.setup(['*'], [mach], 10, 15)
                    except Exception, e:
                        logger.error('Error occured %s' % e)

                session.unlockMachine()
            else:
                reportError(progress)
                return False
            return True

        d = threads.deferToThread(impl)
    else:
        m = machById(vm)
        mName = str(m.name)
        processProtocol = VBoxHeadlessProcessProtocol()
        pseudoCWD = os.path.dirname(sys.modules[__name__].__file__)
        vboxBinariesPath = None
        cmdWithPath = os.path.join(pseudoCWD, 'scripts', 'vboxstart.bat')
        cmdWithArgs = ('vboxstart.bat', vboxBinariesPath, mName)
        cmdPath = os.path.join(pseudoCWD, 'scripts')
        newProc = lambda : reactor.spawnProcess(processProtocol, cmdWithPath, args=cmdWithArgs, env=None, path=cmdPath)
        reactor.callWhenRunning(newProc)
        d = True
    logger.debug('Controller method %s invoked' % support.discoverCaller())
    return d


def shutdown(vm):

    def impl():
        return cmdExistingVm(vm, 'shutdown', None)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def reset(vm):

    def impl():
        return cmdExistingVm(vm, 'reset', None)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def powerOff(vm):

    def impl():
        return cmdExistingVm(vm, 'powerdown', None)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def pause(vm):

    def impl():
        return cmdExistingVm(vm, 'pause', None)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def resume(vm):

    def impl():
        return cmdExistingVm(vm, 'resume', None)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def states():

    def impl():
        return ctx['const']._Values['MachineState']

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def getState(vm):

    def impl():
        m = machById(vm)
        mstate = m.state
        stateName = getNameForMachineStateCode(mstate)
        return stateName

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def saveState(vm):

    def impl():
        return cmdExistingVm(vm, 'saveState', None)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def discardState(vm):

    def impl():
        return cmdExistingVm(vm, 'discardState', None)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def listVMs():

    def impl():
        vb = ctx['vb']
        ms = getMachines()
        msNames = [ str(m.name) for m in ms ]
        return msNames

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def listVMsWithState():

    def impl():
        vb = ctx['vb']
        ms = getMachines()
        msNamesAndStates = [ (str(m.name), getNameForMachineStateCode(m.state)) for m in ms
                           ]
        return dict(msNamesAndStates)

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def listRunningVMs():

    def impl():
        vb = ctx['vb']
        ms = getMachines()
        isRunning = lambda m: m.state == ctx['const'].MachineState_Running
        res = filter(isRunning, ms)
        res = [ str(m.name) for m in res ]
        return res

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def listSnapshots(vm):

    def impl():
        sl = []
        if machById(vm).snapshotCount > 0:
            root = machById(vm).findSnapshot('')

            def recurseTree(snapList, node):
                snapList.append(node.name)
                for child in node.getChildren():
                    recurseTree(snapList, child)

            recurseTree(sl, root)
        return sl

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def takeSnapshot(vm, name, desc):

    def impl():
        logger.debug("Taking snapshot of VM: '%s' and description: %s" % (name, desc))
        return cmdExistingVm(vm, 'takeSnapshot', (name, desc))

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def restoreSnapshot(vm, name):

    def impl():
        mach = machById(vm)
        if name == '':
            return False
        snapshot = mach.findSnapshot(name)
        logger.debug("Restoring snapshot named '%s' and id: %s" % (name, snapshot.id))
        return cmdExistingVm(vm, 'restoreSnapshot', (snapshot,))

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def deleteSnapshot(vm, name):

    def impl():
        mach = machById(vm)
        if name == '':
            return False
        snapshot = mach.findSnapshot(name)
        logger.debug("Deleting snapshot named '%s' and id: %s" % (name, snapshot.id))
        return cmdExistingVm(vm, 'deleteSnapshot', (snapshot.id,))

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def getNamesToIdsMapping():
    macToName = getMACToNameMapping()
    nameToMac = support.reverseDict(macToName)
    return nameToMac


def getIdsToNamesMapping():
    macToName = getMACToNameMapping()
    return macToName


def getStats(vm, key):

    def impl():
        if not ctx['perf']:
            return
        return ctx['perf'].query([key], [machById(vm)])

    logger.debug('Controller method %s invoked' % support.discoverCaller())
    d = threads.deferToThread(impl)
    return d


def reportError(progress):
    ei = progress.errorInfo
    if ei:
        logger.error('Error in %s: %s' % (ei.component, ei.text))


def getMachines():
    if ctx['vb'] is not None:
        return ctx['global'].getArray(ctx['vb'], 'machines')
    else:
        return


def machById(id):
    try:
        mach = ctx['vb'].getMachine(id)
    except:
        mach = ctx['vb'].findMachine(id)

    return mach


def detachVmDevice(mach, args):
    atts = ctx['global'].getArray(mach, 'mediumAttachments')
    hid = args[0]
    for a in atts:
        if a.medium:
            if hid == 'ALL' or a.medium.id == hid:
                mach.detachDevice(a.controller, a.port, a.device)


def detachMedium(mid, medium):
    cmdClosedVm(machById(mid), detachVmDevice, [medium])


def cmdClosedVm(mach, cmd, args=[], save=True):
    session = ctx['global'].openMachineSession(mach, True)
    mach = session.machine
    try:
        cmd(mach, args)
    except Exception, e:
        save = False
        logger.error('Error: %s' % e)

    if save:
        try:
            mach.saveSettings()
        except Exception, e:
            logger.error('Error: %s' % e)

    ctx['global'].closeMachineSession(session)


def cmdExistingVm(vm, cmd, args):
    session = None
    mach = machById(vm)
    try:
        vb = ctx['vb']
        session = ctx['mgr'].getSessionObject(vb)
        mach.lockMachine(session, ctx['global'].constants.LockType_Shared)
    except Exception, e:
        logger.error(ctx, "Session to '%s' not open: %s" % (mach.name, str(e)))
        return

    if session.state != ctx['const'].SessionState_Locked:
        logger.info("Session to '%s' in wrong state: %s" % (mach.name, session.state))
        session.unlockMachine()
        return
    else:
        console = session.console
        ops = {'pause': lambda : console.pause(), 'resume': lambda : console.resume(), 
           'start': lambda : console.powerUp(), 
           'shutdown': lambda : console.powerButton(), 
           'powerdown': lambda : console.powerDown(), 
           'reset': lambda : console.reset(), 
           'saveState': lambda : console.saveState(), 
           'discardState': lambda : console.discardSavedState(True), 
           'takeSnapshot': lambda : console.takeSnapshot(args[0], args[1]), 
           'restoreSnapshot': lambda : console.restoreSnapshot(args[0]), 
           'deleteSnapshot': lambda : console.deleteSnapshot(args[0])}
        try:
            progress = ops[cmd]()
            if progress:
                while not progress.completed:
                    logger.debug('Command (%s) progress - %s %%' % (cmd, str(progress.percent)))
                    progress.waitForCompletion(WAITING_GRACE_MS)

                if progress.completed and int(progress.resultCode) == 0:
                    logger.info("Execution of command '%s' on VM %s completed" % (cmd, mach.name))
                else:
                    session.unlockMachine()
                    reportError(progress)
                    return False
        except Exception, e:
            logger.error("Problem while running cmd '%s': %s" % (cmd, str(e)))

        session.unlockMachine()
        return True


def getMACToNameMapping():
    vb = ctx['vb']

    def numsToColonNotation(nums):
        nums = str(nums)
        g = (nums[i:i + 2] for i in xrange(0, len(nums), 2))
        return (':').join(g)

    ms = getMachines()
    entriesGen = ((numsToColonNotation(m.getNetworkAdapter(1).MACAddress), str(m.name)) for m in getMachines())
    mapping = dict(entriesGen)
    return mapping


def getNameForMachineStateCode(c):
    d = ctx['const']._Values['MachineState']
    revD = [ k for (k, v) in d.iteritems() if v == c ]
    return revD[0]


class _VBoxHeadlessProcessProtocol(protocol.ProcessProtocol):
    logger = logging.getLogger(support.discoverCaller())

    def connectionMade(self):
        self.transport.closeStdin()
        self.logger.debug('VBoxHeadless process started!')

    def outReceived(self, data):
        self.logger.debug('VBoxHeadless stdout: %s' % data)

    def errReceived(self, data):
        self.logger.debug('VBoxHeadless stderr: %s' % data)

    def inConnectionLost(self):
        pass

    def outConnectionLost(self):
        self.logger.info('VBoxHeadless closed its stdout')

    def errConnectionLost(self):
        self.logger.info('VBoxHeadless closed its stderr')

    def processExited(self, reason):
        pass

    def processEnded(self, reason):
        self.logger.warn('Process ended (code: %s) ' % reason.value.exitCode)


from vboxapi import VirtualBoxManager
g_virtualBoxManager = VirtualBoxManager(None, None)
ctx = {'global': g_virtualBoxManager, 'mgr': g_virtualBoxManager.mgr, 
   'vb': g_virtualBoxManager.vbox, 
   'const': g_virtualBoxManager.constants}
ctx['perf'] = ctx['global'].getPerfCollector(ctx['vb'])