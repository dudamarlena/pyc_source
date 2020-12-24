# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/virsh_start_stop/virsh_start_stop.py
# Compiled at: 2019-02-27 06:17:38
# Size of source mod 2**32: 3283 bytes
import libvirt, time, argparse

def _libvirt_silence_error(*args):
    pass


def _get_libvirt_machine(machine):
    libvirt.registerErrorHandler(f=_libvirt_silence_error, ctx=None)
    conn = libvirt.open('qemu:///system')
    libvirt_machine = conn.lookupByName(machine)
    return libvirt_machine


def start_machine(machine):
    libvirt_machine = _get_libvirt_machine(machine)
    if not libvirt_machine.state()[0] == libvirt.VIR_DOMAIN_RUNNING:
        libvirt_machine.create()
        print('{}: started'.format(machine))
    else:
        print("{}: libvirt reported state VIR_DOMAIN_RUNNING, assuming it's true".format(machine))


def stop_machine(machine, timeout):
    libvirt_machine = _get_libvirt_machine(machine)
    elapsed_seconds = 0
    while not libvirt_machine.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
        try:
            libvirt_machine.shutdownFlags(libvirt.VIR_DOMAIN_SHUTDOWN_GUEST_AGENT | libvirt.VIR_DOMAIN_SHUTDOWN_ACPI_POWER_BTN)
        except libvirt.libvirtError as err:
            if libvirt_machine.state()[0] == libvirt.VIR_DOMAIN_SHUTOFF:
                pass
            else:
                raise

        time.sleep(1)
        elapsed_seconds += 1
        if elapsed_seconds == timeout:
            libvirt_machine.destroyFlags(libvirt.VIR_DOMAIN_DESTROY_GRACEFUL)
            print('{}: had to yank the virtual powercord'.format(machine))

    print('{}: shutdown took {} seconds'.format(machine, elapsed_seconds))


def cli_interface():
    parser = argparse.ArgumentParser(description='start / stop libvirt VMs in a blocking fashion')
    parser.add_argument('--machine', metavar='myVM', type=str, required=True, help='machine name')
    parser.add_argument('--state', metavar='[started | stopped]', type=str, required=True, help='desired machine state')
    parser.add_argument('--timeout', metavar='80', type=int, required=False, default=0, help='timeout sec for graceful shutdown request, yank virtual powercord afterwards. ignored when 0 (the default).')
    args = parser.parse_args()
    if args.state == 'stopped':
        stop_machine(args.machine, args.timeout)
    if args.state == 'started':
        start_machine(args.machine)


if __name__ == '__main__':
    cli_interface()