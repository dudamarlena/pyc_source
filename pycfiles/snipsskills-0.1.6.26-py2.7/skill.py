# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/commands/install/skill.py
# Compiled at: 2017-10-25 12:42:01
import os
from ..base import Base
from ...utils.pip_installer import PipInstaller
from snipsskillscore import pretty_printer as pp

class SkillInstallerException(Exception):
    pass


class SkillInstallerWarning(Exception):
    pass


class SkillInstaller(Base):

    def run(self):
        url_or_pip = self.options['<skill_url>']
        force_download = self.options['--force-download']
        debug = self.options['--debug']
        try:
            SkillInstaller.install(url_or_pip, force_download=force_download, debug=debug)
        except SkillInstallerWarning as e:
            if debug:
                raise e
            pp.pwarning(str(e))
        except Exception as e:
            if debug:
                raise e
            pp.perror(str(e))

    @staticmethod
    def install(url_or_pip, force_download=False, debug=False):
        message = pp.ConsoleMessage(('Installing skill: $GREEN{}$RESET').format(url_or_pip))
        message.start()
        try:
            PipInstaller.install(url_or_pip, force_download=force_download)
            message.done()
        except Exception as e:
            message.error()
            if debug:
                raise e
            raise SkillInstallerWarning(('Error installing skill {}: make sure you have the required access rights, and that the module is available').format(url_or_pip))