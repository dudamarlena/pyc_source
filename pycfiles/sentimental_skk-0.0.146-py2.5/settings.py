# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sskk/settings.py
# Compiled at: 2014-03-11 11:41:30
import os, sys, logging
_CONFDB = {'skk-j-mode': 10, 
   'skk-kakutei-key': 10, 
   'skk-toggle-kana': 113, 
   'skk-set-henkan-point-subr': 17, 
   'suggest.max': 30, 
   'cgi-api.enabled': True, 
   'cgi-api.timeout': 0.5}
_DEFAULT_CONF = '\n#\n#\n_CONFDB_OVERLAY = %s\n\ndef get():\n    return _CONFDB_OVERLAY\n\n'
homedir = os.path.expanduser('~')
rcdir = os.path.join(homedir, '.sskk')
if not os.path.exists(rcdir):
    os.makedirs(rcdir)
confpath = os.path.join(rcdir, 'conf.py')
if not os.path.exists(confpath):
    f = open(confpath, 'w')
    try:
        f.write(_DEFAULT_CONF % '{}')
    finally:
        f.close()

sys.path.insert(0, rcdir)
try:
    try:
        import conf
        for (key, value) in conf.get().items():
            _CONFDB[key] = value

    except Exception, e:
        logging.exception(e)

finally:
    sys.path.remove(rcdir)

def get(key):
    if key in _CONFDB:
        return _CONFDB[key]
    return


def set(key, value):
    _CONFDB[key] = value


def save():
    f = open(confpath, 'w')
    try:
        f.write(_DEFAULT_CONF % repr(_CONFDB))
    finally:
        f.close()