# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reviewday/launchpad.py
# Compiled at: 2011-11-19 15:02:41
from launchpadlib.launchpad import Launchpad

class LaunchPad(object):

    def __init__(self):
        self.lp = Launchpad.login_anonymously('reviewday', 'production', '~/.launchpadlib-reviewday', version='devel')
        self.spec_cache = {}

    def bug(self, id):
        return self.lp.bugs[id]

    def project(self, id):
        return self.lp.projects[id]

    def specifications(self, project):
        if project not in self.spec_cache:
            specs = self.project(project).valid_specifications
            self.spec_cache[project] = specs
        return self.spec_cache[project]

    def specification(self, project, spec_name):
        specs = self.specifications(project)
        for spec in specs:
            if spec.name == spec_name:
                return spec