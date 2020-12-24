# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/stdplus/_sshConfig.py
# Compiled at: 2018-12-18 14:38:54
# Size of source mod 2**32: 4022 bytes
import os, re, fnmatch, threading
from pprint import pprint
from stdplus._readfile import readfile
from stdplus._run_cmd import run
knownHostsLock = threading.Lock()

class SshConfigBlock(list):

    def __init__(self, line, lineNumber):
        list.__init__(self)
        self.line = line
        self.lineNumber = lineNumber

    def __str__(self):
        return '{}{}{}'.format(self.line, '\n' if len(self) > 0 else '', '\n'.join((x.__repr__() for x in self)))

    def __repr__(self):
        return '{}:<{}>{}{}'.format(self.lineNumber, self.line, '\n' if len(self) > 0 else '', '\n'.join((x.__repr__() for x in self)))


class SshConfig(SshConfigBlock):

    def __init__(self):
        SshConfigBlock.__init__(self, '', 0)
        self.hosts = {}

    def __str__(self):
        return '\n'.join((x.__repr__() for x in self))

    def __repr__(self):
        return '\n'.join((x.__repr__() for x in self))


class WithSettings(SshConfigBlock):

    def __init__(self, line, lineNumber):
        SshConfigBlock.__init__(self, line, lineNumber)
        self.settings = {}

    def addSetting(self, setting):
        if setting.name not in self.settings:
            self.settings[setting.name] = []
        self.settings[setting.name].append(setting)


class Host(WithSettings):

    def __init__(self, line, lineNumber):
        WithSettings.__init__(self, line, lineNumber)
        m = re.search('^.*Host[ \t]+([^#]*)(#.*)*', line)
        self.name = m.group(1)


class Comment(SshConfigBlock):
    pass


class Match(WithSettings):
    pass


class Setting(SshConfigBlock):

    def __init__(self, line, lineNumber):
        SshConfigBlock.__init__(self, line, lineNumber)
        m = re.search('^[ \t]*([A-Za-z_]*)[ \t]+([^#]*)(#.*)*', line)
        self.name = m.group(1)
        self.value = m.group(2)
        self.comment = m.group(3)


def parseSshConfig(contents):
    lines = contents.split('\n')
    lineNumber = 0
    rootBlock = SshConfig()
    currentBlock = rootBlock
    for line in lines:
        lineNumber += 1
        if 0 == len(line.strip()) or line.startswith('#'):
            currentBlock.append(Comment(line, lineNumber))
        elif line.strip().startswith('Host '):
            currentBlock = Host(line, lineNumber)
            rootBlock.append(currentBlock)
            rootBlock.hosts[currentBlock.name] = currentBlock
        elif line.strip().startswith('Match '):
            currentBlock = Match(line, lineNumber)
            rootBlock.append(currentBlock)
        else:
            setting = Setting(line, lineNumber)
            currentBlock.append(setting)
        if isinstance(currentBlock, Host) or isinstance(currentBlock, Match):
            currentBlock.addSetting(setting)

    return rootBlock


def readSshConfig(path=os.path.expanduser('~/.ssh/config')):
    config = readfile(path)
    return parseSshConfig(config)


def getSshHost(sshConfig, host):
    for pattern, settings in sshConfig.hosts.iteritems():
        if fnmatch.fnmatch(host, pattern):
            return settings


def resetKnownHost(ip):
    removeKnownHosts([ip])
    keyscanHost(ip)


def resetKnownHosts(ips):
    removeKnownHosts(ips)
    for ip in ips:
        keyscanHost(ip)


def keyscanHost(ip):
    global knownHostsLock
    sshConfig = readSshConfig()
    sshHost = getSshHost(sshConfig, ip)
    proxyCommand = ''
    if sshHost:
        if 'ProxyCommand' in sshHost.settings:
            if sshHost.settings['ProxyCommand']:
                if sshHost.settings['ProxyCommand'][0].value:
                    proxyCommand = sshHost.settings['ProxyCommand'][0].value.replace('-W %h:%p', '')
    with knownHostsLock:
        run('touch ~/.ssh/known_hosts && {} ssh-keyscan -H {} >> ~/.ssh/known_hosts 2> /dev/null'.format(proxyCommand, ip))


def removeKnownHosts(ips):
    if not ips:
        return
    args = []
    for ip in ips:
        args.append('-R {}'.format(ip))

    with knownHostsLock:
        if not os.path.exists(os.path.expanduser('~/.ssh/known_hosts')):
            return
        run('ssh-keygen {}'.format(' '.join(args)))