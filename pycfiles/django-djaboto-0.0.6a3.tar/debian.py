# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/growlf/django/django-djaboto/djaboto/debian.py
# Compiled at: 2013-02-26 15:20:47
from subprocess import check_call
import os

def install_system():
    """
    Install OS specific modules as needed
    """
    print '...performing system updates'
    check_call(['sudo', 'apt-get', 'update', '-y'])
    check_call(['sudo', 'apt-get', 'dist-upgrade', '-y'])
    check_call(['sudo', 'apt-get', 'install', '-y',
     'build-essential',
     'python-setuptools',
     'python-dev',
     'python-virtualenv',
     'git-core',
     'mercurial',
     'gcc',
     'unison',
     'python-pip',
     'node-less',
     'libtidy-dev',
     'apache2',
     'libapache2-mod-wsgi'])
    try:
        check_call(['sudo', 'apt-get', 'install', '-y', 'libjpeg62-dev', 'libjpeg62', 'libjpeg8'])
        if not os.path.lexists('/usr/lib/libz.so'):
            os.symlink('/usr/lib/x86_64-linux-gnu/libz.so', '/usr/lib/libz.so')
        if not os.path.lexists('/usr/lib/libjpeg.so'):
            os.symlink('/usr/lib/x86_64-linux-gnu/libjpeg.so', '/usr/lib/libjpeg.so')
        check_call(['sudo', 'apt-get', 'install', '-y', 'python-imaging'])
    except:
        pass

    print '...adding MySQL components'
    check_call(['sudo', 'apt-get', 'install', '-y', 'mysql-server', 'mysql-client', 'python-mysqldb', 'libmysqlclient-dev'])