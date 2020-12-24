# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/macchanger.py
# Compiled at: 2020-01-15 14:21:38
# Size of source mod 2**32: 2944 bytes
from .dependency import Dependency
from ..plugins.ifconfig import Ifconfig
from ..handlers.color import Color

class Macchanger(Dependency):
    dependency_required = False
    dependency_name = 'macchanger'
    dependency_url = 'apt-get install macchanger'
    is_changed = False

    @classmethod
    def down_macch_up(cls, iface, options):
        """Put interface down, run macchanger with options, put interface up"""
        from ..handlers.process import Process
        Color.clear_entire_line()
        Color.p('\r{+} {C}macchanger{W}: taking interface {C}%s{W} down...' % iface)
        Ifconfig.down(iface)
        Color.clear_entire_line()
        Color.p('\r{+} {C}macchanger{W}: changing mac address of interface {C}%s{W}...' % iface)
        command = [
         'macchanger']
        command.extend(options)
        command.append(iface)
        macch = Process(command)
        macch.wait()
        if macch.poll() != 0:
            Color.pl('\n{!} {R}macchanger{O}: error running {R}%s{O}' % ' '.join(command))
            Color.pl('{!} {R}output: {O}%s, %s{W}' % (
             macch.stdout(), macch.stderr()))
            return False
        else:
            Color.clear_entire_line()
            Color.p('\r{+} {C}macchanger{W}: bringing interface {C}%s{W} up...' % iface)
            Ifconfig.up(iface)
            return True

    @classmethod
    def get_interface(cls):
        from ..config import Configuration
        return Configuration.interface

    @classmethod
    def reset(cls):
        iface = cls.get_interface()
        Color.pl('\r{+} {C}macchanger{W}: resetting mac address on %s...' % iface)
        if cls.down_macch_up(iface, ['-p']):
            new_mac = Ifconfig.get_mac(iface)
            Color.clear_entire_line()
            Color.pl('\r{+} {C}macchanger{W}: reset mac address back to {C}%s{W} on {C}%s{W}' % (new_mac, iface))

    @classmethod
    def random(cls):
        from ..handlers.process import Process
        if not Process.exists('macchanger'):
            Color.pl('{!} {R}macchanger: {O}not installed')
            return
        iface = cls.get_interface()
        Color.pl('\n{+} {C}macchanger{W}: changing mac address on {C}%s{W}' % iface)
        if cls.down_macch_up(iface, ['-e']):
            cls.is_changed = True
            new_mac = Ifconfig.get_mac(iface)
            Color.clear_entire_line()
            Color.pl('\r{+} {C}macchanger{W}: changed mac address to {C}%s{W} on {C}%s{W}' % (new_mac, iface))

    @classmethod
    def reset_if_changed(cls):
        if cls.is_changed:
            cls.reset()