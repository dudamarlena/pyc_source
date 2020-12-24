# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/python/insolater/insolater/version_tools.py
# Compiled at: 2013-12-07 00:45:05
from __future__ import absolute_import
from __future__ import print_function
import os, shutil

def init(repo):
    if not os.path.isdir(repo):
        os.mkdir(repo)
        os.mkdir(repo + '/removed')
        os.mkdir(repo + '/versions')
        with open(repo + '/current_version', 'w') as (f):
            f.write('original')
        shutil.copytree('.', repo + '/original', ignore=shutil.ignore_patterns(repo))


def current_version(repo):
    with open(repo + '/current_version', 'r') as (f):
        return f.readline().strip()


def save_version(repo, version=''):
    if version == '':
        version = current_version(repo)
    version_path = repo + '/versions/' + version
    if os.path.isdir(version_path):
        os.rmdir(version_path)
    shutil.copytree('.', version_path, ignore=shutil.ignore_patterns(repo))
    with open(repo + '/current_version', 'w') as (f):
        f.write(version)


def open_version(repo, version):
    cv = current_version(repo)
    if cv == 'original':
        save_version(repo, 'head')
    else:
        save_version(repo, cv)
    for f in os.listdir('.'):
        if f == repo:
            continue
        if os.path.isdir(f):
            os.rmdir(f)
        else:
            os.remove(f)

    vp = repo + '/versions/' + version + '/'
    for f in os.listdir(vp):
        if os.path.isdir(vp + f):
            shutil.copytree(vp + f, f)
        else:
            shutil.copy2(vp + f, f)

    with open(repo + '/current_version', 'w') as (f):
        f.write(version)