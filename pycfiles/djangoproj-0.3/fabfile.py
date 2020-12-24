# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\FilePkl\latihan_django\11agustus\djangoproj\djangoapp\fabfile.py
# Compiled at: 2014-08-20 23:32:02
from __future__ import with_statement
from fabric.api import *
from fabric.api import env
from fabric.contrib.console import confirm
from fabric.network import disconnect_all
import os, shutil
env.hosts = ['root@192.168.0.69']
env.password = 'rahasiakita'
env.keepalive = 3

def tes():
    env.password = 'urb4nbd9'


def hello(ew):
    run('echo hello ' + ew)


def connect_test():
    env.hosts = ['root@192.168.0.69']


def ok():
    lokasi = raw_input('lokasi: ')
    with cd(lokasi):
        lokasi = raw_input('lokasi: ')
        with cd(lokasi):
            perintah2 = raw_input('perintah2: ')
            run(perintah2)


def deploy():
    with settings(host_string='root@192.168.0.69', host_password='rahasiakita'):
        ls()


def session():
    local('ssh')


def cdir():
    run('cd Ipan')


def changedir(loc):
    cd(loc)


def cda(lokasi):
    cd(lokasi)


def ls():
    run('ls')


def directcmd():
    command = raw_input('perintah: ')
    run(command)


def connect():
    host = "['root@192.168.0.69']"
    pw = 'urb4nbd9'
    return (host, pw)


def host():
    hostnya = raw_input('hostnya apa: ')
    ip = raw_input('ipnya apa: ')
    iphost = hostnya + '@' + ip
    return iphost


def pw():
    passw = raw_input('passwordnya: ')
    return passw


def copy(sourcefile, destination):
    run('cp ' + sourcefile + ' ' + destination)


def mkdir(namadir):
    run('mkdir ' + namadir)


def rmdir(name):
    run('rmdir ' + name)


def deldir(namadir):
    run('rm -r ' + namadir)


def touchfile(namafile):
    run('touch ' + namafile)


def removefile(namafile):
    run('rm ' + namafile)