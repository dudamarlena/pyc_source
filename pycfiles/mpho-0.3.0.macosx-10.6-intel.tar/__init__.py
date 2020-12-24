# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/hvn/python2/lib/python2.7/site-packages/pho/__init__.py
# Compiled at: 2015-04-04 06:08:35
import datetime, os, subprocess
__version__ = '0.3.0'
__doc__ = 'Utility help managing tasks'
TEMPLATE = '#!/bin/sh\n# Script helper for {taskname}\n# created at {datetime}\necho $0\n'

def datadir():
    path = os.path.expanduser('~/.utask')
    if not os.path.isdir(os.path.abspath(path)):
        os.mkdir(path)
    return path


def task_path(taskname, done=False):
    fname = '.' + taskname if done else taskname
    return os.path.join(datadir(), fname)


def create(taskname):
    """create a bash script, chmod it"""
    tpath = task_path(taskname)
    if os.path.exists(tpath):
        print ('Task {0} exists').format(taskname)
        return
    with open(task_path(taskname), 'a+') as (f):
        f.write(TEMPLATE.format(datetime=datetime.datetime.now(), taskname=taskname))
    print ('Task {0} is created.').format(taskname)
    os.chmod(tpath, 488)


def delete(taskname):
    tpath = task_path(taskname)
    donepath = task_path(taskname, done=True)
    try:
        os.remove(tpath)
    except OSError:
        try:
            os.remove(donepath)
        except OSError:
            print ('Task {0} does not exist').format(taskname)
            return

    print ('Deleted task {0}.').format(taskname)


def run(taskname):
    """Run helper script"""
    print subprocess.check_output(task_path(taskname))


def edit(taskname):
    """edit ``taskname`` by $EDITOR"""
    editor = os.environ.get('EDITOR', 'nano')
    subprocess.call([editor, task_path(taskname)])


def comment(taskname, comment):
    """Append a comment to task"""
    with open(task_path(taskname), 'a+') as (f):
        f.write('# ' + comment)


def _is_done(taskname):
    donepath = task_path(taskname, done=True)
    return os.path.exists(donepath)


def status(taskname):
    if _is_done(taskname):
        return 'Done'
    return 'Undone'


def done(taskname):
    if _is_done(taskname):
        print ('Task {0} was done.').format(taskname)
    else:
        os.rename(task_path(taskname), task_path(taskname, done=True))
        print ('Marked {0} as done.').format(taskname)


def undone(taskname):
    if _is_done(taskname):
        os.rename(task_path(taskname, done=True), task_path(taskname))
        print ('Undone {0}.').format(taskname)
    else:
        print ('Task {0} is not done.').format(taskname)


def show(taskname):
    with open(task_path(taskname)) as (f):
        print f.read()


def list(show_done=False):
    filter_ = bool if show_done else (lambda f: not f.startswith('.'))
    fns = filter(filter_, [ f for f in os.listdir(datadir()) ])
    normalized_tasknames = map(lambda x: x.lstrip('.'), fns)
    for taskname in normalized_tasknames:
        print ('{0:<30}:{1}').format(taskname, status(taskname))