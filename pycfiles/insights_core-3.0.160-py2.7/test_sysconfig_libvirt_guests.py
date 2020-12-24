# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_libvirt_guests.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import LibvirtGuestsSysconfig
from insights.tests import context_wrap
SYSCONFIG_LIBVIRT_GUESTS = ("\n# URIs to check for running guests\n# example: URIS='default xen:/// vbox+tcp://host/system lxc:///'\n#URIS=default\n\n# action taken on host boot\n# - start   all guests which were running on shutdown are started on boot\n#           regardless on their autostart settings\n# - ignore  libvirt-guests init script won't start any guest on boot, however,\n#           guests marked as autostart will still be automatically started by\n#           libvirtd\nON_BOOT=ignore\n\n# Number of seconds to wait between each guest start. Set to 0 to allow\n# parallel startup.\n#START_DELAY=0\n\n# action taken on host shutdown\n# - suspend   all running guests are suspended using virsh managedsave\n# - shutdown  all running guests are asked to shutdown. Please be careful with\n#             this settings since there is no way to distinguish between a\n#             guest which is stuck or ignores shutdown requests and a guest\n#             which just needs a long time to shutdown. When setting\n#             ON_SHUTDOWN=shutdown, you must also set SHUTDOWN_TIMEOUT to a\n#             value suitable for your guests.\n#ON_SHUTDOWN=suspend\n\n# If set to non-zero, shutdown will suspend guests concurrently. Number of\n# guests on shutdown at any time will not exceed number set in this variable.\n#PARALLEL_SHUTDOWN=0\n\n# Number of seconds we're willing to wait for a guest to shut down. If parallel\n# shutdown is enabled, this timeout applies as a timeout for shutting down all\n# guests on a single URI defined in the variable URIS. If this is 0, then there\n# is no time out (use with caution, as guests might not respond to a shutdown\n# request). The default value is 300 seconds (5 minutes).\n#SHUTDOWN_TIMEOUT=300\n\n# If non-zero, try to bypass the file system cache when saving and\n# restoring guests, even though this may give slower operation for\n# some file systems.\n#BYPASS_CACHE=0\n\n# If non-zero, try to sync guest time on domain resume. Be aware, that\n# this requires guest agent with support for time synchronization\n# running in the guest. For instance, qemu-ga doesn't support guest time\n# synchronization on Windows guests, but Linux ones. By default, this\n# functionality is turned off.\n#SYNC_TIME=1\n").strip()

def test_sysconfig_libvirt_guests():
    libvirt_guests_sysconfig = LibvirtGuestsSysconfig(context_wrap(SYSCONFIG_LIBVIRT_GUESTS))
    assert 'ON_BOOT' in libvirt_guests_sysconfig
    assert libvirt_guests_sysconfig.get('ON_BOOT') == 'ignore'
    assert libvirt_guests_sysconfig.get('SYNC_TIME') is None
    return