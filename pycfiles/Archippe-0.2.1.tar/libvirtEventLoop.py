# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/archipel/libvirtEventLoop.py
# Compiled at: 2013-03-20 13:50:16
import sys, getopt, os, libvirt, select, errno, time, threading
use_pure_python_event_loop = True
do_debug = False

def debug(msg):
    global do_debug
    if do_debug:
        print msg


class virEventLoopPure():

    class virEventLoopPureHandle:

        def __init__(self, handle, fd, events, cb, opaque):
            self.handle = handle
            self.fd = fd
            self.events = events
            self.cb = cb
            self.opaque = opaque

        def get_id(self):
            return self.handle

        def get_fd(self):
            return self.fd

        def get_events(self):
            return self.events

        def set_events(self, events):
            self.events = events

        def dispatch(self, events):
            self.cb(self.handle, self.fd, events, self.opaque)

    class virEventLoopPureTimer:

        def __init__(self, timer, interval, cb, opaque):
            self.timer = timer
            self.interval = interval
            self.cb = cb
            self.opaque = opaque
            self.lastfired = 0

        def get_id(self):
            return self.timer

        def get_interval(self):
            return self.interval

        def set_interval(self, interval):
            self.interval = interval

        def get_last_fired(self):
            return self.lastfired

        def set_last_fired(self, now):
            self.lastfired = now

        def dispatch(self):
            self.cb(self.timer, self.opaque)

    def __init__(self):
        self.poll = select.poll()
        self.pipetrick = os.pipe()
        self.pendingWakeup = False
        self.runningPoll = False
        self.nextHandleID = 1
        self.nextTimerID = 1
        self.handles = []
        self.timers = []
        self.quit = False
        debug('Self pipe watch %d write %d' % (self.pipetrick[0], self.pipetrick[1]))
        self.poll.register(self.pipetrick[0], select.POLLIN)

    def next_timeout(self):
        next = 0
        for t in self.timers:
            last = t.get_last_fired()
            interval = t.get_interval()
            if interval < 0:
                continue
            if next == 0 or last + interval < next:
                next = last + interval

        return next

    def get_handle_by_fd(self, fd):
        for h in self.handles:
            if h.get_fd() == fd:
                return h

        return

    def get_handle_by_id(self, handleID):
        for h in self.handles:
            if h.get_id() == handleID:
                return h

        return

    def run_once(self):
        sleep = -1
        self.runningPoll = True
        try:
            try:
                next = self.next_timeout()
                debug('Next timeout due at %d' % next)
                if next > 0:
                    now = int(time.time() * 1000)
                    if now >= next:
                        sleep = 0
                    else:
                        sleep = (next - now) / 1000.0
                debug('Poll with a sleep of %d' % sleep)
                events = self.poll.poll(sleep)
                for (fd, revents) in events:
                    if fd == self.pipetrick[0]:
                        self.pendingWakeup = False
                        data = os.read(fd, 1)
                        continue
                    h = self.get_handle_by_fd(fd)
                    if h:
                        debug('Dispatch fd %d handle %d events %d' % (fd, h.get_id(), revents))
                        h.dispatch(self.events_from_poll(revents))

                now = int(time.time() * 1000)
                for t in self.timers:
                    interval = t.get_interval()
                    if interval < 0:
                        continue
                    want = t.get_last_fired() + interval
                    if now >= want - 20:
                        debug('Dispatch timer %d now %s want %s' % (t.get_id(), str(now), str(want)))
                        t.set_last_fired(now)
                        t.dispatch()

            except (os.error, select.error), e:
                if e.args[0] != errno.EINTR:
                    raise

        finally:
            self.runningPoll = False

    def run_loop(self):
        self.quit = False
        while not self.quit:
            self.run_once()

    def interrupt(self):
        if self.runningPoll and not self.pendingWakeup:
            self.pendingWakeup = True
            os.write(self.pipetrick[1], 'c')

    def add_handle(self, fd, events, cb, opaque):
        handleID = self.nextHandleID + 1
        self.nextHandleID = self.nextHandleID + 1
        h = self.virEventLoopPureHandle(handleID, fd, events, cb, opaque)
        self.handles.append(h)
        self.poll.register(fd, self.events_to_poll(events))
        self.interrupt()
        debug('Add handle %d fd %d events %d' % (handleID, fd, events))
        return handleID

    def add_timer(self, interval, cb, opaque):
        timerID = self.nextTimerID + 1
        self.nextTimerID = self.nextTimerID + 1
        h = self.virEventLoopPureTimer(timerID, interval, cb, opaque)
        self.timers.append(h)
        self.interrupt()
        debug('Add timer %d interval %d' % (timerID, interval))
        return timerID

    def update_handle(self, handleID, events):
        h = self.get_handle_by_id(handleID)
        if h:
            h.set_events(events)
            self.poll.unregister(h.get_fd())
            self.poll.register(h.get_fd(), self.events_to_poll(events))
            self.interrupt()
            debug('Update handle %d fd %d events %d' % (handleID, h.get_fd(), events))

    def update_timer(self, timerID, interval):
        for h in self.timers:
            if h.get_id() == timerID:
                h.set_interval(interval)
                self.interrupt()
                debug('Update timer %d interval %d' % (timerID, interval))
                break

    def remove_handle(self, handleID):
        handles = []
        for h in self.handles:
            if h.get_id() == handleID:
                self.poll.unregister(h.get_fd())
                debug('Remove handle %d fd %d' % (handleID, h.get_fd()))
            else:
                handles.append(h)

        self.handles = handles
        self.interrupt()

    def remove_timer(self, timerID):
        timers = []
        for h in self.timers:
            if h.get_id() != timerID:
                timers.append(h)
                debug('Remove timer %d' % timerID)

        self.timers = timers
        self.interrupt()

    def events_to_poll(self, events):
        ret = 0
        if events & libvirt.VIR_EVENT_HANDLE_READABLE:
            ret |= select.POLLIN
        if events & libvirt.VIR_EVENT_HANDLE_WRITABLE:
            ret |= select.POLLOUT
        if events & libvirt.VIR_EVENT_HANDLE_ERROR:
            ret |= select.POLLERR
        if events & libvirt.VIR_EVENT_HANDLE_HANGUP:
            ret |= select.POLLHUP
        return ret

    def events_from_poll(self, events):
        ret = 0
        if events & select.POLLIN:
            ret |= libvirt.VIR_EVENT_HANDLE_READABLE
        if events & select.POLLOUT:
            ret |= libvirt.VIR_EVENT_HANDLE_WRITABLE
        if events & select.POLLNVAL:
            ret |= libvirt.VIR_EVENT_HANDLE_ERROR
        if events & select.POLLERR:
            ret |= libvirt.VIR_EVENT_HANDLE_ERROR
        if events & select.POLLHUP:
            ret |= libvirt.VIR_EVENT_HANDLE_HANGUP
        return ret


eventLoop = virEventLoopPure()
eventLoopThread = None

def virEventAddHandleImpl(fd, events, cb, opaque):
    global eventLoop
    return eventLoop.add_handle(fd, events, cb, opaque)


def virEventUpdateHandleImpl(handleID, events):
    return eventLoop.update_handle(handleID, events)


def virEventRemoveHandleImpl(handleID):
    return eventLoop.remove_handle(handleID)


def virEventAddTimerImpl(interval, cb, opaque):
    return eventLoop.add_timer(interval, cb, opaque)


def virEventUpdateTimerImpl(timerID, interval):
    return eventLoop.update_timer(timerID, interval)


def virEventRemoveTimerImpl(timerID):
    return eventLoop.remove_timer(timerID)


def virEventLoopPureRegister():
    libvirt.virEventRegisterImpl(virEventAddHandleImpl, virEventUpdateHandleImpl, virEventRemoveHandleImpl, virEventAddTimerImpl, virEventUpdateTimerImpl, virEventRemoveTimerImpl)


def virEventLoopPureRun():
    eventLoop.run_loop()


def virEventLoopNativeRun():
    while True:
        libvirt.virEventRunDefaultImpl()


def virEventLoopPureStart():
    global eventLoopThread
    virEventLoopPureRegister()
    eventLoopThread = threading.Thread(target=virEventLoopPureRun, name='libvirtEventLoop')
    eventLoopThread.setDaemon(True)
    eventLoopThread.start()


def virEventLoopNativeStart():
    global eventLoopThread
    libvirt.virEventRegisterDefaultImpl()
    eventLoopThread = threading.Thread(target=virEventLoopNativeRun, name='libvirtEventLoop')
    eventLoopThread.setDaemon(True)
    eventLoopThread.start()


def eventToString(event):
    eventStrings = ('Defined', 'Undefined', 'Started', 'Suspended', 'Resumed', 'Stopped',
                    'Shutdown')
    return eventStrings[event]


def detailToString(event, detail):
    eventStrings = (
     ('Added', 'Updated'),
     'Removed',
     ('Booted', 'Migrated', 'Restored', 'Snapshot', 'Wakeup'),
     ('Paused', 'Migrated', 'IOError', 'Watchdog', 'Restored', 'Snapshot'),
     ('Unpaused', 'Migrated', 'Snapshot'),
     ('Shutdown', 'Destroyed', 'Crashed', 'Migrated', 'Saved', 'Failed', 'Snapshot'),
     'Finished')
    return eventStrings[event][detail]


def myDomainEventCallback1(conn, dom, event, detail, opaque):
    print 'myDomainEventCallback1 EVENT: Domain %s(%s) %s %s' % (dom.name(), dom.ID(),
     eventToString(event),
     detailToString(event, detail))


def myDomainEventCallback2(conn, dom, event, detail, opaque):
    print 'myDomainEventCallback2 EVENT: Domain %s(%s) %s %s' % (dom.name(), dom.ID(),
     eventToString(event),
     detailToString(event, detail))


def myDomainEventRebootCallback(conn, dom, opaque):
    print 'myDomainEventRebootCallback: Domain %s(%s)' % (dom.name(), dom.ID())


def myDomainEventRTCChangeCallback(conn, dom, utcoffset, opaque):
    print 'myDomainEventRTCChangeCallback: Domain %s(%s) %d' % (dom.name(), dom.ID(), utcoffset)


def myDomainEventWatchdogCallback(conn, dom, action, opaque):
    print 'myDomainEventWatchdogCallback: Domain %s(%s) %d' % (dom.name(), dom.ID(), action)


def myDomainEventIOErrorCallback(conn, dom, srcpath, devalias, action, opaque):
    print 'myDomainEventIOErrorCallback: Domain %s(%s) %s %s %d' % (dom.name(), dom.ID(), srcpath, devalias, action)


def myDomainEventGraphicsCallback(conn, dom, phase, localAddr, remoteAddr, authScheme, subject, opaque):
    print 'myDomainEventGraphicsCallback: Domain %s(%s) %d %s' % (dom.name(), dom.ID(), phase, authScheme)


def myDomainEventDiskChangeCallback(conn, dom, oldSrcPath, newSrcPath, devAlias, reason, opaque):
    print 'myDomainEventDiskChangeCallback: Domain %s(%s) disk change oldSrcPath: %s newSrcPath: %s devAlias: %s reason: %s' % (
     dom.name(), dom.ID(), oldSrcPath, newSrcPath, devAlias, reason)


def myDomainEventTrayChangeCallback(conn, dom, devAlias, reason, opaque):
    print 'myDomainEventTrayChangeCallback: Domain %s(%s) tray change devAlias: %s reason: %s' % (
     dom.name(), dom.ID(), devAlias, reason)


def myDomainEventPMWakeupCallback(conn, dom, reason, opaque):
    print 'myDomainEventPMWakeupCallback: Domain %s(%s) system pmwakeup' % (
     dom.name(), dom.ID())


def myDomainEventPMSuspendCallback(conn, dom, reason, opaque):
    print 'myDomainEventPMSuspendCallback: Domain %s(%s) system pmsuspend' % (
     dom.name(), dom.ID())


def myDomainEventBalloonChangeCallback(conn, dom, utcoffset, actual):
    print 'myDomainEventBalloonChangeCallback: Domain %s(%s) %d' % (dom.name(), dom.ID(), actual)


def usage(out=sys.stderr):
    print >> out, 'usage: ' + os.path.basename(sys.argv[0]) + ' [-hdl] [uri]'
    print >> out, '   uri will default to qemu:///system'
    print >> out, '   --help, -h   Print this help message'
    print >> out, '   --debug, -d  Print debug output'
    print >> out, '   --loop, -l   Toggle event-loop-implementation'


def main():
    global do_debug
    global use_pure_python_event_loop
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hdl', ['help', 'debug', 'loop'])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)

    for (o, a) in opts:
        if o in ('-h', '--help'):
            usage(sys.stdout)
            sys.exit()
        if o in ('-d', '--debug'):
            do_debug = True
        if o in ('-l', '--loop'):
            use_pure_python_event_loop ^= True

    if len(args) >= 1:
        uri = args[0]
    else:
        uri = 'qemu:///system'
    print 'Using uri:' + uri
    if use_pure_python_event_loop:
        virEventLoopPureStart()
    else:
        virEventLoopNativeStart()
    vc = libvirt.openReadOnly(uri)
    old_exitfunc = getattr(sys, 'exitfunc', None)

    def exit():
        print 'Closing ' + str(vc)
        vc.close()
        if old_exitfunc:
            old_exitfunc()

    sys.exitfunc = exit
    vc.domainEventRegister(myDomainEventCallback1, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_LIFECYCLE, myDomainEventCallback2, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_REBOOT, myDomainEventRebootCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_RTC_CHANGE, myDomainEventRTCChangeCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_IO_ERROR, myDomainEventIOErrorCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_WATCHDOG, myDomainEventWatchdogCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_GRAPHICS, myDomainEventGraphicsCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_DISK_CHANGE, myDomainEventDiskChangeCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_TRAY_CHANGE, myDomainEventTrayChangeCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_PMWAKEUP, myDomainEventPMWakeupCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_PMSUSPEND, myDomainEventPMSuspendCallback, None)
    vc.domainEventRegisterAny(None, libvirt.VIR_DOMAIN_EVENT_ID_BALLOON_CHANGE, myDomainEventBalloonChangeCallback, None)
    vc.setKeepAlive(5, 3)
    while vc.isAlive() == 1:
        time.sleep(1)

    return


if __name__ == '__main__':
    main()