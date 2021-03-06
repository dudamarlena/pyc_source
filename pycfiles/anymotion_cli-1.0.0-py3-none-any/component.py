# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anymeta/availability/component.py
# Compiled at: 2011-01-19 13:57:12
__doc__ = "\nImplementations of AvailabilityComponents.\n\nThis module implements the following components:\n\n1. L{PowerComponent} - Monitors the power connector. It goes into\n   WARNING state when the computer is running on batter power, and to\n   ERROR when the power is critically low.\n\n2. L{InternetComponent} - Monitors the internet connection using\n   C{fizzjik.network}. Goes into ERROR state when the connection is\n   down. This severity is configurable ('severity' keyword in\n   constructor).\n\n3. L{RFIDReaderComponent} - Monitors (dis)connections of rfid readers\n   in the system. Can be configured to require a minimum, maximum or\n   specific number of readers, as well as requiring specific reader\n   serial numbers.\n\n4. L{AnymetaAPIComponent} - Monitor for a working Anymeta connection.\n\n"
import os
from twisted.internet import task
from twisted.python import log
import base

class PowerComponent(base.AvailabilityComponent):
    """
    Availability component which monitors the power of the computer.
    """
    name = 'power'
    caption = 'Power connection'
    powerAvailable = True
    powerLow = False

    def setParent(self, parent):
        base.AvailabilityComponent.setParent(self, parent)
        from fizzjik.input import power
        self.parent.addEvent(power.PowerAvailableEvent, self.onPowerAvailable)
        self.parent.addEvent(power.LowPowerEvent, self.onLowPower)
        svc = power.PowerMonitor()
        svc.setServiceParent(self.parent)

    def onPowerAvailable(self, event):
        changed = self.powerAvailable != event.data
        self.powerAvailable = event.data
        if changed:
            self.parent.availabilityChanged(self)

    def onLowPower(self, event):
        changed = self.powerLow != event.data
        on_battery = event.data
        self.powerLow = on_battery
        if changed:
            self.parent.availabilityChanged(self)

    def getState(self):
        if self.powerLow:
            return base.ERROR
        if not self.powerAvailable:
            return base.WARNING
        return base.OK

    def getHelp(self):
        if self.powerLow:
            return ('The computer is very low on power!', 'Try finding an elextricity outlet and connect the computer so it can recharge.')
        else:
            if not self.powerAvailable:
                return ('Running on battery power.', None)
            return ('Power is connected.', None)


class InternetComponent(base.AvailabilityComponent):
    """
    Availability component which monitors for a working connection to
    the internet.
    """
    name = 'internet'
    caption = 'Internet connection'
    severity = base.ERROR
    connection_present = None

    def __init__(self, **kwargs):
        base.AvailabilityComponent.__init__(self, **kwargs)
        if 'severity' in kwargs:
            self.severity = kwargs['severity']

    def setParent(self, parent):
        base.AvailabilityComponent.setParent(self, parent)
        from fizzjik.input import network
        self.parent.addEvent(network.NetworkConnectionPresentEvent, self.onConnectionAdded)
        self.parent.addEvent(network.NetworkConnectionAddedEvent, self.onConnectionAdded)
        self.parent.addEvent(network.NetworkConnectionRemovedEvent, self.onConnectionRemoved)
        svc = network.NetworkConnectionSensor()
        svc.destination = 'http://hwdeps.mediamatic.nl/ping.php?host=' + os.uname()[1]
        svc.immediate = True
        svc.setServiceParent(self.parent)

    def onConnectionRemoved(self, e):
        changed = self.connection_present
        self.connection_present = False
        if changed:
            self.parent.availabilityChanged(self)

    def onConnectionAdded(self, e):
        changed = not self.connection_present
        self.connection_present = True
        if changed:
            self.parent.availabilityChanged(self)

    def getState(self):
        if not self.connection_present:
            return self.severity
        return base.OK

    def getHelp(self):
        if not self.connection_present:
            return ('There is no internet connection.', 'Try to find an ethernet cable and plug it in the ethernet port of the computer. Alternatively, configure the computer to use the wireless network.')
        else:
            return ('Internet is available.', None)


class RFIDReaderComponent(base.AvailabilityComponent):
    """
    Component which watches for connected RFID readers.

    Options:
    - Minimum / maximum / specific number of readers
    - List of required serial numbers
    """
    name = 'rfid'
    caption = 'RFID readers'
    severity = base.ERROR
    min_readers = None
    max_readers = None
    num_readers = None
    serials = None
    connected_readers = None
    greedy = False

    def __init__(self, **kw):
        if 'min_readers' in kw:
            self.min_readers = kw['min_readers']
        if 'max_readers' in kw:
            self.max_readers = kw['max_readers']
        if 'num_readers' in kw:
            self.num_readers = kw['num_readers']
        if 'serials' in kw:
            self.serials = kw['serials']
        if 'greedy' in kw:
            self.greedy = kw['greedy']
        self.connected_readers = []

    def setParent(self, parent):
        base.AvailabilityComponent.setParent(self, parent)
        from fizzjik.input import sonmicro
        self.parent.addEvent(sonmicro.SonMicroMifareSensorAddedEvent, self.readerAdded)
        self.parent.addEvent(sonmicro.SonMicroMifareSensorRemovedEvent, self.readerRemoved)
        svc = sonmicro.SonMicroMifareSensorMonitor(greedy=self.greedy)
        svc.setServiceParent(self.parent)

    def readerAdded(self, e):
        serial = e.data.serial
        if serial in self.connected_readers:
            return
        self.connected_readers.append(serial)
        self.parent.availabilityChanged(self)

    def readerRemoved(self, e):
        serial = e.data
        if serial not in self.connected_readers:
            return
        self.connected_readers.remove(serial)
        self.parent.availabilityChanged(self)

    def getState(self):
        if not self.serials:
            if self.min_readers is not None and len(self.connected_readers) < self.min_readers:
                return self.severity
            if self.max_readers is not None and len(self.connected_readers) > self.max_readers:
                return self.severity
            if self.num_readers is not None and len(self.connected_readers) != self.num_readers:
                return self.severity
            return base.OK
        else:
            if set(self.connected_readers) != set(self.serials):
                return self.severity
            else:
                return base.OK
            return

    def getHelp(self):
        if not self.serials:
            if self.min_readers is not None and len(self.connected_readers) < self.min_readers:
                return ('There need to be at least %d reader(s) connected.' % self.min_readers, 'Connect at least %d more reader(s).' % (self.min_readers - len(self.connected_readers)))
            if self.max_readers is not None and len(self.connected_readers) > self.max_readers:
                return ('There need to be at maximum %d reader(s) connected.' % self.min_readers, 'Disconnect %d more reader(s).' % (self.max_readers - len(self.connected_readers)))
            if self.num_readers is not None and len(self.connected_readers) != self.num_readers:
                return ('There need to be precisely %d reader(s) connected.' % self.num_readers, 'Please connect the right number of readers.')
            return ('Readers are configured.', None)
        else:
            con = set(self.connected_readers)
            need = set(self.serials)
            if con != need:
                return ('You need to connect specifically the following reader(s): %s' % (', ').join(self.serials), None)
            return ('Readers are configured.', None)
            return


class AnymetaAPIComponent(base.AvailabilityComponent):
    """
    Checks whether the Anymeta API can be reached using a given
    C{AnyMetaAPI} instance and whether it does not return an erroneous
    result.
    """
    name = 'anymeta'
    caption = 'Anymeta connection'
    api = None
    call = 'anymeta.user.info'
    call_args = None
    lc = None
    state = None
    info = None
    severity = base.ERROR

    def __init__(self, **kw):
        base.AvailabilityComponent.__init__(self, **kw)
        if 'api' in kw:
            self.api = kw['api']
        if 'call' in kw:
            self.call = kw['call']
        if 'call_args' in kw:
            self.call_args = kw['call_args']
        else:
            self.call_args = {}
        self.state = self.severity

    def setAPI(self, api):
        if api == self.api:
            return
        else:
            self.state = self.severity
            self.api = api
            self.info = None
            if self.lc and self.lc.running:
                self.lc.stop()
            self._checkStart()
            return

    def setParent(self, parent):
        base.AvailabilityComponent.setParent(self, parent)
        self._checkStart()

    def _checkStart(self):
        if not self.api:
            return
        if self.lc and self.lc.running:
            self.lc.stop()
        self.lc = task.LoopingCall(self._checkAnymeta)
        self.lc.start(30)

    def _checkAnymeta(self):

        def connected(result):
            changed = self.state != base.OK
            self.state = base.OK
            self.info = result
            if changed:
                self.parent.availabilityChanged(self)

        def not_connected(failure):
            log.err(failure)
            self.result = None
            changed = self.state != self.severity
            self.state = self.severity
            if changed:
                self.parent.availabilityChanged(self)
            return

        self.api.doMethod(self.call, self.call_args).addCallback(connected).addErrback(not_connected)

    def getState(self):
        if not self.api:
            return base.NOTICE
        return self.state

    def getHelp(self):
        if not self.api:
            return ('No Anymeta connection has been configured.', 'Choose an AnyMeta site to connect to.')
        else:
            if self.state != base.OK:
                return ('Anymeta connection failed.', None)
            return ('Anymeta ok.', None)