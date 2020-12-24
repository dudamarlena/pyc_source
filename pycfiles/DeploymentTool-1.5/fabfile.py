# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\FilePkl\hasil_development\Deploymentnew\Deployment\Deploymentapp\fabfile.py
# Compiled at: 2014-11-11 23:02:28
from __future__ import with_statement
from fabric.api import *
from fabric.contrib.console import confirm
from fabric.network import disconnect_all
from fabric.context_managers import settings
from itertools import count
import os, shutil, time

def newfile(param1, param2, user, idtask):
    try:
        with cd(env.base_remote):
            location = param1.encode('string_escape')
            with cd(location):
                run('touch ' + param2)
                cmd = user + ' run touch newfile named as ' + param2 + ' in ' + env.base_remote + '/' + location
                write_log(cmd)
    except:
        cmd = user + ' Failed run touch newfile ' + param2 + ' in ' + env.base_remote + '/' + location
        write_log(cmd)
        return run().failed


def copy(param1, param2, user, idtask):
    try:
        run('cp ' + env.base_local + '/' + param2 + ' ' + env.base_remote + '/' + param1)
        cmd = user + ' run copy ' + param2 + ' from ' + env.base_local + ' to ' + env.base_remote + '/' + param1
        write_log(cmd)
    except:
        cmd = user + ' Failed run copy ' + param2 + ' from ' + source + ' to ' + env.base_remote + '/' + param1
        write_log(cmd)
        return run().failed


def deldir(param1, param2, user, idtask):
    try:
        with cd(env.base_remote):
            location = param1.encode('string_escape')
            with cd(location):
                run('rm -r ' + param2)
                cmd = user + ' run delete directory ' + param2 + ' in ' + env.base_remote + '/' + location
                write_log(cmd)
    except:
        cmd = user + ' Failed run delete directory ' + param2 + ' in ' + env.base_remote + '/' + location
        write_log(cmd)
        return run().failed


def delfile(param1, param2, user, idtask):
    try:
        with cd(env.base_remote):
            location = param1.encode('string_escape')
            with cd(location):
                run('rm ' + param2)
                cmd = user + ' run remove file ' + param2 + ' in ' + env.base_remote + '/' + location
                write_log(cmd)
    except:
        cmd = user + ' Failed run remove file ' + param2 + ' in ' + env.base_remote + '/' + location
        write_log(cmd)
        return run().failed


def mkdir(param1, param2, user, idtask):
    try:
        with cd(env.base_remote):
            location = param1.encode('string_escape')
            with cd(location):
                run('mkdir ' + param2)
                cmd = user + ' run make directory ' + param2 + ' in ' + env.base_remote + '/' + location
                write_log(cmd)
    except:
        cmd = user + ' Failed run make directory ' + param2 + ' in ' + env.base_remote + '/' + location
        write_log(cmd)
        return run().failed


def uploadfile(param1, param2, user, idtask):
    try:
        put(env.base_local + '/' + param2, env.base_remote + '/' + param1)
        cmd = user + ' upload file ' + param2 + ' from ' + env.base_local + ' to ' + env.base_remote + '/' + param1
        write_log(cmd)
    except:
        cmd = user + ' Failed run upload file ' + param2 + ' from ' + env.base_local + ' to ' + env.base_remote + '/' + param1
        write_log(cmd)
        return run().failed


def write_log(command):
    times = time.strftime('%c')
    setting = '(setting host: ' + hostnya + ' base domain: ' + env.base_domain + ')'
    log_write = command + ' ' + times + ' ' + setting + '\n'
    file = open('log/log.dj', 'a')
    file.write(log_write)
    file.close()


def write_errorlog():
    times = time.strftime('%c')
    log_write = 'an error has occurred, do rollback on ' + times + '\n'
    file = open('log/log.dj', 'a')
    file.write(log_write)
    file.close()


def createbackup(param1, param2, idtask, base_remote):
    if env.base_remote == '':
        env.base_remote = base_remote
    with cd(env.base_remote):
        run('mkdir -p temp')
        temp = 'temp'
        with cd(temp):
            tempfoldercommand = temp + '_' + idtask
            run('mkdir -p ' + tempfoldercommand)
        run('[ -e ' + param1 + '/' + param2 + ' ] && cp --parent -avr ' + param1 + '/' + param2 + ' temp/' + tempfoldercommand + '|| true')


def createtempexecbackup(param1, param2, idtask, base_remote):
    if env.base_remote == '':
        env.base_remote = base_remote
    with cd(env.base_remote):
        run('mkdir -p temp')
        temp = 'temp'
        with cd(temp):
            tempfoldercommand = temp + '_' + idtask
            run('mkdir -p ' + tempfoldercommand)
            with cd(tempfoldercommand):
                run('mkdir -p ' + temp)
        run('[ -e ' + param1 + '/' + param2 + ' ] && cp --parent -avr ' + param1 + '/' + param2 + ' temp/' + tempfoldercommand + '/' + temp + '|| true')


def dorevert(param1, param2, idtask, base_remote):
    if env.base_remote == '':
        env.base_remote = base_remote
        tempfoldercommand = 'temp_' + idtask
        with cd(env.base_remote):
            run('[ -e temp/' + tempfoldercommand + '/' + param1 + '/' + param2 + ' ] && cp -avr temp/' + tempfoldercommand + '/' + param1 + '/' + param2 + ' ' + param1 + '||rm -rf ' + param1 + '/' + param2)
    else:
        tempfoldercommand = 'temp_' + idtask
        with cd(env.base_remote):
            run('[ -e temp/' + tempfoldercommand + '/' + param1 + '/' + param2 + ' ] && cp -avr temp/' + tempfoldercommand + '/' + param1 + '/' + param2 + ' ' + param1 + '||rm -rf ' + env.base_remote + '/' + param1 + '/' + param2)


def dorollbackexecutefail(param1, param2, idtask, base_remote):
    if env.base_remote == '':
        env.base_remote = base_remote
        tempfoldercommand = 'temp_' + idtask
        with cd(env.base_remote):
            run('[ -e temp/' + tempfoldercommand + '/temp/' + param1 + '/' + param2 + ' ] && cp -avr temp/' + tempfoldercommand + '/temp/' + param1 + '/' + param2 + ' ' + param1 + '||rm -rf ' + param1 + '/' + param2)
    else:
        tempfoldercommand = 'temp_' + idtask
        with cd(env.base_remote):
            run('[ -e temp/' + tempfoldercommand + '/temp/' + param1 + '/' + param2 + ' ] && cp -avr temp/' + tempfoldercommand + '/temp/' + param1 + '/' + param2 + ' ' + param1 + '||rm -rf ' + env.base_remote + '/' + param1 + '/' + param2)


def preset(hostname, username, password, basepath, localbasepath):
    global hostnya
    hostnya = username + '@' + hostname
    env.hosts = [hostnya]
    env.password = password
    env.base_domain = basepath
    env.base_local = localbasepath.encode('string_escape')
    env.base_remote = env.base_domain


def default():
    env.base_local = 'blog/project'
    env.base_remote = env.base_domain


def list():
    preset()
    run('ls ' + env.base_domain)


def docommand(command, user):
    run(command)
    cmd = user + " do custom command: '" + command + "'"
    write_log(cmd)