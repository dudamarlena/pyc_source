# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/weborg/lib/client.py
# Compiled at: 2011-08-01 04:14:42
import subprocess, os, logging, re, memcache, settings
log = logging.getLogger('client')
log.setLevel(level=logging.DEBUG)
handler = logging.FileHandler(settings.LOG_FILE)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
log.addHandler(handler)
mc = memcache.Client(['localhost:11211'])

def execute(cmd):
    env = os.environ
    env['LANG'] = 'en_US.utf8'
    full_cmd = settings.EMACS + ' -q -batch -l ~/.emacs.d/70-org-mode.el -l ' + settings.ORG_EL + " -eval '%s'" % cmd.encode('utf-8')
    p = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, env=env)
    stdout, stderr = p.communicate()
    log.debug('RPC: %s' % full_cmd)
    log.debug('Result: %s' % stdout)
    return stdout


def entry_index():
    idx = mc.get('idx')
    if idx:
        return idx
    else:
        cmd = '(entry-index)'
        idx = execute(cmd)
        mc.set('idx', idx)
        return idx


def entry_create(eid, jsonstr):
    cmd = '(entry-create "%s" "%s")' % (eid, re.escape(jsonstr))
    return execute(cmd)


def entry_new(eid):
    cmd = '(entry-new "%s")' % eid
    return execute(cmd)


def entry_update(eid, jsonstr):
    cmd = '(entry-update "%s" "%s")' % (eid, re.escape(jsonstr))
    return execute(cmd)


def entry_delete(eid):
    cmd = '(entry-delete "%s")' % eid
    return execute(cmd)


def entry_show(eid):
    cache = mc.get(str(eid))
    if cache:
        return cache
    else:
        cmd = '(entry-show "%s")' % eid
        result = execute(cmd)
        mc.set(str(eid), result)
        return result


def entry_edit(eid):
    cmd = '(entry-edit "%s")' % eid
    return execute(cmd)