# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-QtVhoA/setuptools/setuptools/command/saveopts.py
# Compiled at: 2019-02-06 16:42:30
from setuptools.command.setopt import edit_config, option_base

class saveopts(option_base):
    """Save command-line options to a file"""
    description = 'save supplied options to setup.cfg or other config file'

    def run(self):
        dist = self.distribution
        settings = {}
        for cmd in dist.command_options:
            if cmd == 'saveopts':
                continue
            for opt, (src, val) in dist.get_option_dict(cmd).items():
                if src == 'command line':
                    settings.setdefault(cmd, {})[opt] = val

        edit_config(self.filename, settings, self.dry_run)