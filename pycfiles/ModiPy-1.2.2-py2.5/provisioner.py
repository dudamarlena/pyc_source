# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/modipy/provisioner.py
# Compiled at: 2009-08-25 18:19:45
"""
Provisioners contact remote devices and apply changes to them.

Should be implemented as a Protocol/Factory style thing to fit
with the async mechanism. A Provisioner is an interface applied
to a Factory that creates a, for example, ssh session with a
remote site.
"""
from zope.interface import Interface, implements
from twisted.internet import defer, reactor
from twisted.python import log as tlog
from twisted.internet.error import ProcessDone, ProcessTerminated, AlreadyCancelled, AlreadyCalled
from interfaces import IProvisioner
from base import XMLConfigurable
from change import ChangeConditionFailure
from change import UserBailout
from util import run_after_delay
import traceback, logging, debug
log = logging.getLogger('modipy')
from twisted.internet.base import DelayedCall
DelayedCall.debug = True

class NoTargetsError(Exception):
    """
    Raised when a change is detected that has no targets
    and isn't in NOOP mode.
    """
    pass


class Provisioner(XMLConfigurable):
    """
    A Provisioner performs the actual execution of Changesets. It could, for example,
    connect to a remote system via SSH and then execute the Changeset Actions.
    """
    implements(IProvisioner)

    def __init__(self, name, namespace={}, authoritarian=False, autobackout=False, sessionlog=None, **kwargs):
        """
        @param sessionlog: a FileDescriptor for writing all session data to a logfile
        """
        self.name = name
        self.connectedDevice = None
        self.namespace = namespace
        self.authoritarian = authoritarian
        self.autobackout = autobackout
        self.sessionlog = sessionlog
        self.change_ok = {}
        self.change_failed = {}
        self.backout_ok = {}
        self.backout_failed = {}
        self.delayed_retry = {}
        return

    def parse_config_node(self, node):
        pass

    def perform_change(self, ignored, change, namespace={}, backout=False):
        """
        A wrapper around the perform_delayed_change function, in
        order to enable a callLater functionality.
        """
        d = defer.Deferred()
        if change.state() == 'retry':
            change.state('retry_pending')
            log.info("Change '%s' scheduled to retry in '%d' seconds", change.name, change.retry_delay)
            reactor.callLater(change.retry_delay, self.perform_delayed_change, ignored, d, change, namespace, backout)
        else:
            log.debug('CHANGE WILL EXECUTE IMMEDIATELY')
            reactor.callLater(0, self.perform_delayed_change, ignored, d, change, namespace, backout)
        return d

    def perform_delayed_change(self, ignored, d, change, namespace, backout):
        """
        Calls back the deferred 'd' that is passed in, and immediately
        executes the change. This function is called after some sort of
        delay, usually via reactor.callLater()
        """
        newd = self.do_perform_change(ignored, change, namespace, backout)
        newd.chainDeferred(d)

    def do_perform_change(self, ignored, change, namespace={}, backout=False):
        """
        Perform a change on one or more (potentially) remote entities.

        @param namespace: The global namespace passed in to the provisioner.
               This gets merged with the provisioner, device and change namespaces.
        """
        log.debug('perform change with namespace: %s', namespace)
        devices = change.devices
        if len(devices) == 0 and change.noop is False:
            d = defer.fail(NoTargetsError("No targets specified for change '%s', and it's not in NOOP mode." % change.name))
            d.addErrback(self.change_failure, change, namespace)
            return d
        if change.serial_mode:
            log.debug('change %s will be performed on devices: %s', change.name, devices)
            d = defer.succeed(None)
            for device in devices:
                d.addCallback(self.setup_device_change, device, change, namespace, backout=backout)

            d.addCallbacks(self.change_complete_success, self.change_failure, callbackArgs=(change, namespace), errbackArgs=(change, namespace))
            return d
        else:
            dlist = []
            for device in devices:
                d = self.setup_device_change(device, change, namespace, backout=backout)
                dlist.append(d)

            dl = defer.DeferredList(dlist, fireOnOneErrback=True)
            dl.addCallback(self.change_complete_success, change, namespace)
            dl.addErrback(self.change_failure, change, namespace)
            return dl
        return

    def setup_device_namespace(self, device, change, namespace={}):
        """
        Set up a per device namespace for the change
        """
        namespace['provisioner.name'] = self.name
        namespace['provisioner.type'] = self.__class__.__name__
        namespace['change.name'] = change.name
        namespace['change.type'] = change.__class__.__name__
        namespace['device.name'] = device.name
        namespace['device.fqdn'] = device.fqdn
        namespace['device.ipaddress'] = device.get_ipaddress()
        log.debug('updating with my namespace')
        namespace.update(self.namespace)
        log.debug('updating with change namespace')
        namespace.update(change.namespace)
        log.debug('updating with device namespace')
        namespace.update(device.namespace)
        return namespace

    def setup_device_change(self, ignored, device, change, namespace, backout):
        """
        Do the change for the device
        """
        log.debug("performing change '%s' on device '%s'", change.name, device)
        namespace = self.setup_device_namespace(device, change, namespace)
        log.debug('Checking for an iterator...')
        if getattr(change, 'iterator', None) is not None:
            d = defer.succeed(None)
            for ns in change.iterator:
                newnamespace = ns.copy()
                newnamespace.update(namespace)

                def callsoon(ignored, iterns):
                    """
                    Be careful to pass in the thing that changes in each loop,
                    or you'll end up with a later value than you want when the
                    delay is up.
                    """
                    return run_after_delay(change.iterator.delay, self.backout_or_apply, device, change, iterns, backout)

                d.addCallback(callsoon, newnamespace)

            return d
        else:
            return self.backout_or_apply(device, change, namespace, backout)
        return

    def iterator_delay(self, ignored, device, change, namespace, backout, delay=0):
        """
        Use this to delay iteration if required.
        Mostly because NetApp simulators barf if we talk to them too quickly.
        """
        pass

    def backout_or_apply(self, device, change, namespace, backout=False):
        """
        Set up the backout or apply of a change,
        depending on the backout setting.
        """
        log.debug('namespace: %s', namespace)
        if backout:
            log.debug('backout selected.')
            d = self.backout_change(None, device, change, namespace)
        else:
            d = self.apply_change(None, device, change, namespace)
        return d

    def apply_change(self, ignored, device, change, namespace={}):
        """
        Apply the change to a device
        """
        log.debug('Applying change %s with namespace: %s', change.name, namespace)
        d = self.connect(device, namespace)
        d.addCallback(self.do_pre_apply_check, device, change, namespace)
        d.addCallbacks(self.pre_apply_success, self.pre_apply_failed, callbackArgs=(device, change, namespace), errbackArgs=(device, change, namespace))
        return d

    def change_apply_success(self, result, device, change, namespace):
        """
        Change was applied successfully.
        """
        log.debug("change applied to device '%s' successfully." % device)
        log.debug('result: %s', result)
        self.change_ok[device] = change
        return change.post_apply_check(result, self, device, namespace)

    def change_apply_failed(self, failure, device, change, namespace):
        log.info("Change '%s' failed to apply: %s", change.name, failure.value)
        e = failure.check(UserBailout)
        if e:
            return defer.fail(failure)
        e = failure.check(ChangeConditionFailure)
        if e:
            self.change_failed[device] = failure
            change.state('total_failure')
            d = self.backout_change(None, device, change, namespace)
            if change.on_fail_continue:
                log.info('Attempting to continue, despite failure...')
                change.state('partial_failure')
            elif change.backout_all:
                for device in self.change_ok.keys():
                    d.addCallback(self.backout_change, device, change, namespace)

            return d
        else:
            log.error('Fatal change error. Cannot backout: %s', failure)
            return failure
        return

    def change_failure(self, failure, change, namespace):
        log.debug("Change failure for '%s': %s", change.name, failure.value)
        if log.level == logging.DEBUG:
            tlog.err(failure)
        if change.state() in ('pending', 'retry', 'retry_pending'):
            if change.can_retry():
                change.state('retry')
            else:
                change.state('total_failure')
        elif change.state() in ('backout_failed', 'total_failure'):
            pass
        else:
            log.error('change_failure unhandled change state: %s', change.state())
            raise ValueError('Unhandled change state: %s' % change.state())
        if failure.type in [UserBailout, NoTargetsError]:
            return failure

    def change_complete_success(self, result, change, namespace):
        if change.state() in ('pending', 'retry'):
            change.state('success')
            log.info("Change '%s' was a success!", change.name)
        elif change.state() == 'backout_ok':
            log.debug('Backout successful.')
        else:
            log.info('change_complete_success in weird state: %s', change.state)

    def do_pre_apply_check(self, result, device, change, namespace):
        log.info("Doing pre-apply check for change '%s' on device '%s'", change.name, device)
        return change.pre_apply_check(self, device, namespace)

    def pre_apply_success(self, result, device, change, namespace):
        log.info("Pre-apply check passed for change '%s' on device '%s'", change.name, device)
        d = self.do_apply(result, device, change, namespace)
        d.addCallback(self.change_apply_success, device, change, namespace)
        d.addErrback(self.change_apply_failed, device, change, namespace)
        return d

    def pre_apply_failed(self, failure, device, change, namespace):
        log.info("Pre-apply check failed for change '%s' on device '%s'", change.name, device)
        raise failure

    def do_apply(self, result, device, change, namespace):
        """
        Apply the actual change
        """
        log.info("Applying change '%s' to device '%s'", change.name, device)
        return change.apply(self, device, namespace)

    def backout_change(self, ignored, device, change, namespace):
        """
        Back out a change that was applied to a device.
        """
        if not change.has_backout():
            return defer.fail(NotImplementedError('No backout steps defined for change.'))
        if not self.autobackout:
            log.info("About to back out change '%s'.", change.name)
            change.do_pause()
        log.info("Backing out change '%s' from device '%s'", change.name, device)
        d = change.pre_backout_check(self, device, namespace)
        d.addCallback(change.backout, self, device, namespace)
        d.addCallback(change.post_backout_check, self, device, namespace)
        d.addCallback(self.backout_success, device, change, namespace)
        d.addErrback(self.backout_failure, device, change, namespace)
        return d

    def backout_success(self, ignored, device, change, namespace):
        log.info("Successfully backed out change: '%s' from device '%s'", change.name, device)
        change.state('backout_ok')
        self.backout_ok[device] = change

    def backout_failure(self, failure, device, change, namespace):
        log.info("Backout of change '%s' failed for device '%s'!", change.name, device)
        change.state('backout_failed')
        self.backout_failed[device] = change
        return failure

    def connect(self, device, namespace):
        """
        The default Provisioner doesn't connect, as it assumes a connection
        will be made for each change step, perhaps for each substep within
        a change.
        If you only want to connect once for the entire change session,
        override this method in your subclass.
        """
        return defer.succeed(None)

    def disconnect(self, ignored, device):
        """
        The default Provisioner doesn't connect, so disconnect
        has no effect.
        """
        log.debug('disconnecting from %s' % device)
        return defer.succeed(None)

    def check_authoritarian(self):
        """
        If we're in authoritarian mode, wait for confirmation
        that we should execute the command.
        """
        if self.authoritarian:
            log.debug('Authoritarian mode. Waiting for ok to proceed...')
            isok = raw_input('Issue command (y/n)[n]?> ')
            if isok.startswith('y'):
                log.debug("Ok! Let's continue!")
            else:
                log.info(' Bailing out at your command.')
                raise UserBailout('Bailing out at your command')
                return