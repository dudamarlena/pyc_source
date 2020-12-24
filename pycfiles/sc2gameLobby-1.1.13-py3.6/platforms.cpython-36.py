# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sc2gameLobby\runConfigs\platforms.py
# Compiled at: 2018-10-28 02:39:02
# Size of source mod 2**32: 8511 bytes
"""Configs for how to run SC2 from a normal install on various platforms."""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from six import iteritems
import copy, os, platform, sys
from sc2gameLobby import versions
from pysc2.run_configs import lib
from pysc2.lib import sc_process

class LocalBase(lib.RunConfig):
    __doc__ = 'Base run config for the deepmind file hierarchy.'

    def __init__(self, base_dir, exec_name, cwd=None, env=None):
        base_dir = os.path.expanduser(base_dir)
        cwd = cwd and os.path.join(base_dir, cwd)
        super(LocalBase, self).__init__(replay_dir=(os.path.join(base_dir, 'Replays')),
          data_dir=base_dir,
          tmp_dir=None,
          cwd=cwd,
          env=env)
        self._exec_name = exec_name
        self.xyz = None

    @property
    def is64bit(self):
        """whether the this machine is 64-bit capable or not"""
        return platform.machine().endswith('64')

    @property
    def mapsDir(self):
        return os.path.join(self.data_dir, 'Maps')

    @property
    def mostRecentVersion(self):
        versMap = self.versionMap()
        orderedVersions = sorted((list(iteritems(versMap))), reverse=True)
        for baseVers, labelVs in orderedVersions:
            compatibleVers = versions.handle.search(baseVers)
            if not compatibleVers:
                continue
            compatibleVersions = [(v['version'], v) for v in compatibleVers]
            bestVersionLabel = max(compatibleVersions)[1]['label']
            return bestVersionLabel

        raise NotImplementedError("couldn't identify a valid version definition among the installed game versions: %s" % labelStrings)

    @property
    def validVersionExecutables(self):
        ret = []
        for x in os.listdir(self.versionsDir):
            if x.startswith('Base'):
                ret.append(int(x[4:]))

        return ret

    @property
    def versionsDir(self):
        return os.path.join(self.data_dir, 'Versions')

    def exec_path(self, baseVersion=None):
        """Get the exec_path for this platform. Possibly find the latest build."""
        if not os.path.isdir(self.data_dir):
            raise sc_process.SC2LaunchError('Install Starcraft II at %s or set the SC2PATH environment variable' % self.data_dir)
        if baseVersion == None:
            mostRecent = versions.handle.mostRecent
            if mostRecent:
                return mostRecent['base-version']
            raise sc_process.SC2LaunchError('When requesting a versioned executable path without specifying base-version, expected to find StarCraft II versions installed at %s.' % self.versionsDir)
        else:
            if isinstance(baseVersion, versions.Version):
                baseVersion = baseVersion.baseVersion
            else:
                if str(baseVersion).count('.') > 0:
                    baseVersion = versions.Version(baseVersion).baseVersion
        baseVersExec = os.path.join(self.versionsDir, 'Base%s' % baseVersion, self._exec_name)
        if os.path.isfile(baseVersExec):
            return baseVersExec
        raise sc_process.SC2LaunchError('Specified baseVersion %s does not exist at %s.%s    available: %s' % (
         baseVersion, baseVersExec, os.linesep,
         ' '.join(str(val) for val in sorted(self.versionMap().keys()))))

    def listVersions(self):
        ret = []
        map(ret.extend, self.versionMap().values())
        return sorted(ret)

    def versionMap(self, debug=False):
        ret = {}
        for vKey in self.validVersionExecutables:
            labels = [r['label'] for r in (versions.handle.search)(**{'version': vKey})]
            ret[vKey] = labels

        return ret

    def start(self, version=None, **kwargs):
        """Launch the game process."""
        if not version:
            version = self.mostRecentVersion
        pysc2Version = lib.Version(version.version, version.baseVersion, version.dataHash, version.fixedHash)
        return (sc_process.StarcraftProcess)(
 self, exec_path=self.exec_path(version.baseVersion), 
         version=pysc2Version, **kwargs)


class Windows(LocalBase):
    __doc__ = 'Run on Windows.'

    def __init__(self):
        super(Windows, self).__init__(os.environ.get('SC2PATH', 'C:/Program Files (x86)/StarCraft II').strip('"'), 'SC2_x64.exe', 'Support64')

    @classmethod
    def priority(cls):
        if platform.system() == 'Windows':
            return 1


class MacOS(LocalBase):
    __doc__ = 'Run on MacOS.'

    def __init__(self):
        super(MacOS, self).__init__(os.environ.get('SC2PATH', '/Applications/StarCraft II'), 'SC2.app/Contents/MacOS/SC2')

    @classmethod
    def priority(cls):
        if platform.system() == 'Darwin':
            return 1


class Linux(LocalBase):
    __doc__ = 'Config to run on Linux.'

    def __init__(self):
        base_dir = os.environ.get('SC2PATH', '~/StarCraftII')
        base_dir = os.path.expanduser(base_dir)
        env = copy.deepcopy(os.environ)
        env['LD_LIBRARY_PATH'] = ':'.join(filter(None, [
         os.environ.get('LD_LIBRARY_PATH'),
         os.path.join(base_dir, 'Libs/')]))
        super(Linux, self).__init__(base_dir, 'SC2_x64', env=env)

    @classmethod
    def priority(cls):
        if platform.system() == 'Linux':
            return 1