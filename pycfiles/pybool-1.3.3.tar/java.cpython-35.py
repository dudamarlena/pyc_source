# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v2/java.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 1209 bytes
from fabric.api import sudo, settings
from fabric.context_managers import hide
from bookshelf.api_v2.os_helpers import install_os_updates
from bookshelf.api_v2.pkg import apt_install

def install_oracle_java(distribution, java_version):
    """ installs oracle java """
    if 'ubuntu' in distribution:
        accept_oracle_license = 'echo oracle-java' + java_version + 'installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections'
        with settings(hide('running', 'stdout')):
            sudo(accept_oracle_license)
        with settings(hide('running', 'stdout'), prompts={'Press [ENTER] to continue or ctrl-c to cancel adding it': 'yes'}):
            sudo('yes | add-apt-repository ppa:webupd8team/java')
        with settings(hide('running', 'stdout')):
            install_os_updates(distribution)
            apt_install(packages=['oracle-java8-installer',
             'oracle-java8-set-default'])