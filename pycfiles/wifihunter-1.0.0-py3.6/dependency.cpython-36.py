# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/plugins/dependency.py
# Compiled at: 2020-01-20 05:49:35
# Size of source mod 2**32: 2671 bytes


class Dependency(object):
    required_attr_names = [
     'dependency_name',
     'dependency_url', 'dependency_required']

    def __init_subclass__(cls):
        for attr_name in cls.required_attr_names:
            if attr_name not in cls.__dict__:
                raise NotImplementedError('Attribute "{}" has not been overridden in class "{}"'.format(attr_name, cls.__name__))

    @classmethod
    def exists(cls):
        from ..handlers.process import Process
        return Process.exists(cls.dependency_name)

    @classmethod
    def run_dependency_check(cls):
        from ..handlers.color import Color
        from .airmon import Airmon
        from .airodump import Airodump
        from .aircrack import Aircrack
        from .aireplay import Aireplay
        from .ifconfig import Ifconfig
        from .iwconfig import Iwconfig
        from .bully import Bully
        from .reaver import Reaver
        from .wash import Wash
        from .pyrit import Pyrit
        from .tshark import Tshark
        from .macchanger import Macchanger
        from .hashcat import Hashcat, HcxDumpTool, HcxPcapTool
        apps = [
         Aircrack,
         Iwconfig, Ifconfig,
         Reaver, Bully,
         Pyrit, Tshark,
         Hashcat, HcxDumpTool, HcxPcapTool,
         Macchanger]
        missing_required = any([app.fails_dependency_check() for app in apps])
        if missing_required:
            Color.pl('{!} {O}At least 1 Required app is missing. wifihunter needs Required apps to run{W}')
            import sys
            sys.exit(-1)

    @classmethod
    def fails_dependency_check(cls):
        from ..handlers.color import Color
        from ..handlers.process import Process
        if Process.exists(cls.dependency_name):
            return False
        else:
            if cls.dependency_required:
                Color.p('{!} {O}Error: Required app {R}%s{O} was not found' % cls.dependency_name)
                Color.pl('. {W}install @ {C}%s{W}' % cls.dependency_url)
                return True
            Color.p('{!} {O}Warning: Recommended app {R}%s{O} was not found' % cls.dependency_name)
            Color.pl('. {W}install @ {C}%s{W}' % cls.dependency_url)
            return False