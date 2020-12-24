# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/orpheus/Desarrollo/netflix/freedesktop_setup/__init__.py
# Compiled at: 2017-03-11 15:14:40
# Size of source mod 2**32: 811 bytes
from setuptools.command.install import install as BaseInstall
from setuptools.dist import Distribution as BaseDistribution
from .freedesktop import install_desktop
from .icons import update_icons

class install(BaseInstall):
    sub_commands = BaseInstall.sub_commands + [
     ('install_desktop', None),
     ('update_icons', None)]


class Distribution(BaseDistribution):
    default_cmdclass = {'install':install, 
     'install_desktop':install_desktop, 
     'update_icons':update_icons}
    desktop_entries = None
    icon_themes_dir = None

    def __init__(self, attrs):
        cmdclass = self.default_cmdclass.copy()
        cmdclass.update(attrs.get('cmdclass', ()))
        attrs['cmdclass'] = cmdclass
        super(Distribution, self).__init__(attrs)