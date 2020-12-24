# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modules/updater.py
# Compiled at: 2018-07-01 06:51:02
# Size of source mod 2**32: 1688 bytes
import subprocess

def updateTor():
    """
        Currently updates Tor by calling terminal commands using subprocess
        Not a great method and will be replaced in the future.

    """
    print('Checking for latest stable release')
    isGit = subprocess.Popen([
     'git', 'branch'],
      stdout=(subprocess.PIPE),
      stderr=(subprocess.STDOUT))
    output = isGit.stdout.read()
    branch = output[2:8].decode('utf-8')
    print(branch)
    if branch == 'master':
        update = subprocess.Popen([
         'git', 'pull', 'origin', 'master'],
          stdout=(subprocess.PIPE),
          stderr=(subprocess.STDOUT))
        update_out = update.stdout.read()
        if update_out[90:109].decode('utf-8') == 'Already up-to-date.':
            print('TorBot is already up-to-date.')
        else:
            print('TorBot has succesfully updated to latest stable version.')
    else:
        subprocess.Popen([
         'git', 'init'],
          stdout=(subprocess.PIPE),
          stderr=(subprocess.STDOUT))
        subprocess.Popen([
         'git', 'remote', 'add', 'origin',
         'https://github.com/DedSecInside/TorBoT.git'],
          stdout=(subprocess.PIPE),
          stderr=(subprocess.STDOUT))
        update = subprocess.Popen([
         'git', 'pull', 'origin', 'dev'],
          stdout=(subprocess.PIPE),
          stderr=(subprocess.STDOUT))
        update_out = update.stdout.read()
        if update_out[90:109].decode('utf-8') == 'Already up-to-date.':
            print('TorBot is already up-to-date.')
        else:
            print('TorBot has succesfully updated to latest stable version.')