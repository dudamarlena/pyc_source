# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/virtualenvwrapper/github.py
# Compiled at: 2011-01-16 17:17:06
import logging, os, subprocess, pkg_resources
log = logging.getLogger(__name__)

def run(*args):
    p = subprocess.Popen(args, stdout=subprocess.PIPE)
    p.wait()
    return p


def call(*args):
    subprocess.call(args, shell=False)


def get_url(project):
    p = run('git', 'config', '--global', 'github.user')
    try:
        user = tuple(p.stdout)[0].strip()
    except (TypeError, IndexError):
        user = os.environ.get('VIRTUALENVWRAPPER_GITHUB_USER', os.environ.get('USER'))

    if not user:
        log.error('Set USER or VIRTUALENVWRAPPER_GITHUB_USER')
        return None
    else:
        url = ('git@github.com:{user}/{project}.git').format(user=user, project=project)
        return url


def template(args):
    project = args[0]
    url = get_url(project)
    if url:
        call('git', 'init')
        call('git', 'remote', 'add', 'origin', url)
        call('git', 'config', 'branch.master.remote', 'origin')
        call('git', 'config', 'branch.master.merge', 'refs/heads/master')
        log.info('Repo setup to track %s' % url)