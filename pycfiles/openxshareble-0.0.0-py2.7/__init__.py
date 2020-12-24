# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/openxshareble/__init__.py
# Compiled at: 2016-06-13 23:52:40
"""
openxshareble - pure python driver to communicate with Dexcom G4+Share
over ble.  Allows openaps to use ble to talk to Dexcom G4+Share.

Examples:
```
# add vendor to openaps
openaps vendor add openxshareble
# create device called share to use the new vendor
openaps device add share openxshareble
# use it, eg:
openaps use share iter_glucose 2
```

"""
import logging
log = logging.getLogger(__name__)
import os, app
from openaps.uses.use import Use
from openaps.uses.registry import Registry
from openaps.vendors import dexcom

def configure_use_app(app, parser):
    pass


def configure_add_app(app, parser):
    pass


def configure_app(app, parser):
    pass


def configure_parser(parser):
    pass


def main(args, app):
    """
  """
    pass


def set_config(args, device):
    return ''


def display_device(device):
    return '/%s' % device.get('serial')


use = Registry()
get_uses = use.get_uses

class BLEUsage(Use, app.App):
    """ Generic subclass for a single openaps use to use Dexcom's ble
  """
    __init__ = Use.__init__

    def before_main(self, args, app):
        """
    Get info such as serial from the device configuration.
    """
        logAddress = self.device.get('logAddress', '/dev/log')
        logLevel = getattr(logging, self.device.get('logLevel', 'INFO'))
        for handler in log.handlers[:]:
            log.removeHandler(handler)

        log.addHandler(logging.handlers.SysLogHandler(address=logAddress))
        log.setLevel(logLevel)
        serial = self.device.get('serial', None)
        mac = self.device.get('mac', None)
        self.prolog(mac=mac)
        self.setup_dexcom(serial=serial)
        return

    def after_main(self, args, app):
        self.epilog()

    def __call__(self, args, app):
        """
    Using BLE requires dropping into glib's threading mechanics.
    """
        output = None
        self.setup_ble()

        def run():
            """
      Run the main logic of the app, capturing the output.
      """
            self.before_main(args, app)
            output = self.main(args, app)
            self.after_main(args, app)
            return output

        res = self.ble.run_mainloop_with(run, quit_with_loop=False)
        return res


@use()
class configure(Use):
    DEXCOMRX = os.environ.get('DEXCOMRX', '')
    __doc__ = ('\n  Configure DEXCOMRX serial number.\n\n\n  Update the configuration so that your serial number is used to communicate\n  with your Dexcom G4 with Share.\n  Default: {DEXCOMRX}\n  ').format(DEXCOMRX=DEXCOMRX)
    __init__ = Use.__init__

    def configure_app(self, app, parser):
        parser.add_argument('--serial', metavar='DEXCOMRX', default=os.environ.get('DEXCOMRX', ''), help='DexcomRX Serial Number')
        parser.add_argument('--mac', metavar='DEXCOMRX_MAC', default=os.environ.get('DEXCOMRX_MAC', ''), help='DexcomRX BLE MAC address')

    def get_params(self, args):
        conf = dict()
        if args.serial.startswith('SM') and len(args.serial) > 8:
            conf.update(serial=args.serial)
        else:
            conf.update(serial=None)
        if len(args.mac.split(':')) == 6:
            conf.update(mac=args.mac)
        else:
            conf.update(mac=None)
        return conf

    def main(self, args, app):
        results = dict(serial=self.device.get('serial', None), mac=self.device.get('mac', None))
        params = self.get_params(args)
        dirty = False
        for field in ['serial', 'mac']:
            value = params.get(field)
            if getattr(self.device, 'extra', None):
                print ('{field}={value}').format(field=field, value=results[field])
                log.info(('{field}={value}').format(field=field, value=results[field]))
                if value:
                    if value != results.get(field, None):
                        dirty = True
                        print 'saving %s' % value
                        results[field] = value
                        self.device.extra.add_option(field, value)

        if dirty:
            self.device.store(app.config)
            app.config.save()
        return results


@use()
class list_dexcom(BLEUsage):
    """
  Scan the environment looking for Dexcom devices.
  
  Returns a list of scanned devices.
  """
    disconnect_on_after = False

    def before_main(self, args, app):
        pass

    def main(self, args, app):
        if not self.device.get('serial', None):
            self.disconnect_on_after = False
        receivers = self.enumerate_dexcoms()
        results = []
        for device in receivers:
            results.append(dict(name=str(device.name), mac=str(device.id), advertised=map(str, device.advertised)))

        return results


class DexcomTask(BLEUsage):
    """
  Generic utility to help swap original dexcom uses with new ones using
  the logic from this module to set up the usage.
  """
    disconnect_on_after = True

    @classmethod
    def Emulate(Klass, usage):
        """
    Given an original Use, an implementation, returns a transformed
    Use class so that our logic controls how data gets transported.
    """

        class EmulatedUsage(usage, Klass):
            __doc__ = usage.__doc__
            __name__ = usage.__name__
            before_main = Klass.before_main
            after_main = Klass.after_main
            __call__ = Klass.__call__

        EmulatedUsage.__name__ = usage.__name__
        return EmulatedUsage


def transform(existing, Emulator, Original):
    """
  helper method to extract substitutes from original list of uses.
  """
    results = dict()
    for name, usage in existing.use.__USES__.items():
        if issubclass(usage, Original):
            adapted = Emulator.Emulate(usage)
            adapted.__name__ = name
            if name not in results:
                results[name] = adapted

    return results


adapted = transform(dexcom, DexcomTask, dexcom.scan)
use.__USES__.update(**adapted)