# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/ipv6.py
# Compiled at: 2019-05-16 13:41:33
"""
IPv6 - Check whether IPv6 is disabled
=====================================

This combiner reports whether the user has disabled IPv6 via one of the
many means available to do so. At present, only whether IPv6 is disabled on
the running system is reported; it provides no information regarding whether it
would continue to be after a reboot.

Per https://access.redhat.com/solutions/8709 , IPv6 may be disabled by

RHEL 7:
 * ``ipv6.disable=1`` Kernel command line argument
 * ``disable_ipv6`` option in ``sysctl``

RHEL 6:
 * ``option ipv6 disable=1`` in `modprobe.d`
 * ``install ipv6 /bin/true`` (fake install) in `modprobe.d`
 * ``disable_ipv6`` option in ``sysctl``

While they aren't tested explicitly, there are some means by which you can
attempt to disable IPv6 that are ineffective, such as setting
``blacklist ipv6`` in `modprobe.d`; those methods will yield no result from
this combiner.

The only requirement of this combiner is ``Uname``, but accurate detection
relies on information from combiners marked optional. If, for example, it's run
against a RHEL6 system without information from ``ModProbe``, it will miss any
of those disabling options and possibly return a false negative. For that
reason, this combiner shouldn't be relied on to state definitively that IPv6 is
enabled or disabled.

Examples:
    >>> from insights.tests import context_wrap
    >>> from insights.parsers.uname import Uname
    >>> from insights.parsers.sysctl import Sysctl
    >>> from insights.combiners.ipv6 import IPv6
    >>> my_uname = '''
    ...  Linux localhost.localdomain 3.10.0-514.10.2.el7.x86_64 #1 SMP Mon Feb 20 02:37:52 EST 2017 x86_64 x86_64 x86_64 GNU/Linux
    ... '''.strip()
    >>> my_sysctl = '''
    ... net.ipv6.conf.all.autoconf = 1
    ... net.ipv6.conf.all.dad_transmits = 1
    ... net.ipv6.conf.all.disable_ipv6 = 0
    ... net.ipv6.conf.all.force_mld_version = 0
    ... net.ipv6.conf.all.force_tllao = 0
    ... net.ipv6.conf.all.forwarding = 0
    ... '''.strip()
    >>> shared = {Uname: Uname(context_wrap(my_uname)), Sysctl: Sysctl(context_wrap(my_sysctl))}
    >>> my_ipv6 = IPv6({},shared)
    >>> my_ipv6.disabled()
    False
    >>> my_ipv6.disabled_by()
    set([])
    >>> my_sysctl = '''
    ... net.ipv6.conf.all.autoconf = 1
    ... net.ipv6.conf.all.dad_transmits = 1
    ... net.ipv6.conf.all.disable_ipv6 = 1
    ... net.ipv6.conf.all.force_mld_version = 0
    ... net.ipv6.conf.all.force_tllao = 0
    ... net.ipv6.conf.all.forwarding = 0
    ... '''.strip()
    >>> shared[Sysctl] = Sysctl(context_wrap(my_sysctl))
    >>> my_ipv6 = IPv6({},shared)
    >>> my_ipv6.disabled()
    True
    >>> my_ipv6.disabled_by()
    set(['sysctl'])

"""
from ..core.plugins import combiner
from ..parsers.modprobe import ModProbe
from ..parsers.lsmod import LsMod
from ..parsers.cmdline import CmdLine
from ..parsers.sysctl import Sysctl
from ..parsers.uname import Uname
RHEL_UNSUPPORTED_VERSION = 9999

@combiner(Uname, optional=[ModProbe, LsMod, CmdLine, Sysctl])
class IPv6(object):
    """A combiner which detects disabled IPv6 networking."""

    def __init__(self, uname, mod_probe, lsmod, cmdline, sysctl):
        self.disablers = set()
        if uname.rhel_release[0] == '7':
            self.rhelver = 7
        elif uname.rhel_release[0] == '6':
            self.rhelver = 6
        elif uname.rhel_release[0] == '5':
            self.rhelver = 5
        else:
            self.rhelver = RHEL_UNSUPPORTED_VERSION
        self.modprobe = mod_probe or []
        if isinstance(self.modprobe, ModProbe):
            self.modprobe = [
             self.modprobe]
        self.lsmod = getattr(lsmod, 'data', None)
        self.cmdline = getattr(cmdline, 'data', {})
        self.sysctl = getattr(sysctl, 'data', {})
        self._check_ipv6()
        return

    def _check_ipv6(self):
        if self.cmdline.get('ipv6.disable') == ['1']:
            self.disablers.add('cmdline')
        if self.sysctl.get('net.ipv6.conf.all.disable_ipv6') == '1':
            self.disablers.add('sysctl')
        if self.rhelver < 7 and len(self.modprobe) > 0:
            for it in self.modprobe:
                if it.get('options', {}).get('ipv6') == ['disable=1']:
                    self.disablers.add('modprobe_disable')
                if self.lsmod is not None and 'ipv6' not in self.lsmod:
                    if it.get('install', {}).get('ipv6') == ['/bin/true']:
                        self.disablers.add('fake_install')

        return

    def disabled(self):
        """Determine whether IPv6 has been disabled on this system.

        Returns:
            bool: True if a configuration that disables IPv6 was found.
        """
        return self.disablers != set([])

    def disabled_by(self):
        """Get the means by which IPv6 was disabled on this system.

        Returns:
            set: Zero or more of ``cmdline``, ``modprobe_disable``,
            ``fake_install``, or ``sysctl``, depending on which methods to
            disable IPv6 have been found.
        """
        return self.disablers