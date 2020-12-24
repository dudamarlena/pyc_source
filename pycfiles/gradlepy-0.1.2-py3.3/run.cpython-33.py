# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gradlepy/run.py
# Compiled at: 2016-09-21 05:04:36
# Size of source mod 2**32: 3039 bytes
import os, subprocess
from shutil import which

class Gradle(object):

    def __init__(self):
        self.useWrapper = True
        self.fallbackToInstalled = True
        self.targets = []
        self.properties = {}
        self.extraArgs = []
        self.settingsFile = None
        self.mavenLocalRepo = None
        self.offline = False
        self.daemon = None
        self.debug = False
        self.stacktrace = False
        self.info = False
        self.quiet = False
        self.noNative = False
        self.opts = None
        self.env = {}
        return

    def run_in_dir(self, cwd, *extraTargets, **extraProperties):
        self.run(cwd, None, *extraTargets, **extraProperties)
        return

    def run_on_file(self, buildFile, *extraTargets, **extraProperties):
        self.run(None, buildFile, *extraTargets, **extraProperties)
        return

    def run(self, cwd, buildFile, *extraTargets, **extraProperties):
        args = []
        if self.useWrapper:
            searchPath = cwd or os.getcwd()
            path = which('gradlew', path=searchPath) or which('gradlew')
            if not path:
                if self.fallbackToInstalled:
                    path = which('gradle')
        else:
            path = which('gradle')
        if path:
            args.append(path)
        else:
            raise RuntimeError('Cannot run Gradle, executable not found on the path')
        if self.noNative:
            args.append('-Dorg.gradle.native=false')
        if buildFile:
            args.append('--data-file "{}"'.format(buildFile))
        if self.settingsFile:
            args.append('--settings-file "{}"'.format(self.settingsFile))
        if self.mavenLocalRepo:
            args.append('-Dmaven.repo.local={}'.format(self.mavenLocalRepo))
        if self.offline:
            args.append('--offline')
        if self.daemon == True:
            args.append('--daemon')
        else:
            if self.daemon == False:
                args.append('--no-daemon')
            if self.debug:
                args.append('--debug')
            if self.stacktrace:
                args.append('--stacktrace')
            if self.info:
                args.append('--info')
            if self.quiet:
                args.append('--quiet')
            allProperties = {}
            allProperties.update(self.properties)
            allProperties.update(extraProperties)
            for name, value in allProperties.items():
                args.append('-D{}={}'.format(name, value))

            allTargets = []
            allTargets.extend(self.targets)
            allTargets.extend(extraTargets)
            args.extend(allTargets)
            if self.extraArgs:
                args.extend(self.extraArgs)
            env = os.environ.copy()
            if self.opts:
                env['GRADLE_OPTS'] = self.opts
            env.update(self.env)
            cmd = ' '.join(args)
            if self.opts:
                print('GRADLE_OPTS="{}" {}'.format(self.opts, cmd))
            else:
                print(cmd)
        try:
            process = subprocess.Popen(cmd, cwd=cwd, env=env, shell=True)
            process.communicate()
            if process.returncode != 0:
                raise RuntimeError('Gradle run failed')
        except KeyboardInterrupt:
            raise RuntimeError('Gradle run interrupted')