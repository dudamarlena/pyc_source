# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gitbranchhealth/config.py
# Compiled at: 2014-08-29 20:03:05
import git.config, ConfigParser
from util import walkUp
import os.path

class BranchHealthConfig:

    def __init__(self, repo):
        self.mParser = git.config.SectionConstraint(repo.config_reader(), 'branchhealth')

    def shouldIgnoreBranches(self):
        try:
            ignoreBranches = not self.mParser.get_value(option='noignore')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            return True

        return ignoreBranches

    def shouldUseColor(self):
        try:
            color = not self.mParser.get_value(option='nocolor')
        except (ConfigParser.NoSectionError, ConfigParser.NoOptionError):
            return True

        return color