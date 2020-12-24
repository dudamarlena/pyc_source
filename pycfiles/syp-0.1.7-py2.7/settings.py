# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syp/settings.py
# Compiled at: 2017-01-22 04:50:02
"""
Create this file with syp --init
and tweak the settings in ~/.syp/settings.py.

One can overwrite the REQUIREMENTS_FILES dictionnary:

REQUIREMENTS_FILES['apt'] = {
    "file": "my-apt-requirements.txt",
    "pacman": "aptitude",
    "install": "install -y",
    "uninstall": "remove",
}
"""
REQUIREMENTS_ROOT_DIR = '~/dotfiles/'
REQUIREMENTS_FILES = {'apt': {'file': 'apt.txt', 
           'pacman': 'apt-get', 
           'install': 'install -y --force-yes', 
           'uninstall': 'remove'}, 
   'pip': {'file': 'pip.txt'}, 
   'pip3': {'file': 'pip3.txt'}, 
   'npm': {'file': 'npm.txt', 
           'install': 'install -g', 
           'uninstall': 'remove'}, 
   'gem': {'file': 'ruby.txt'}, 
   'guix': {'file': 'guix.txt', 
            'pacman': 'guix', 
            'install': 'guix package -i', 
            'uninstall': 'guix package -r'}, 
   'docker': {'file': 'docker.txt', 
              'install': 'pull', 
              'uninstall': 'rm', 
              'sudo': ''}}
CONF = '~/.syp/'
SYSTEM_PACMAN = 'apt-get'