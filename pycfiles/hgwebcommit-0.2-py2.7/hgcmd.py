# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/hgcmd.py
# Compiled at: 2011-10-28 19:16:45
DEFAULT_CONFIG = {'SECRET_KEY': '(secret key)', 
   'HGWEBCOMMIT_ENCODING': 'utf-8', 
   'HGWEBCOMMIT_ALLOW_COMMIT': True, 
   'HGWEBCOMMIT_ACTIONS': ()}

def webcommit(ui, repo, **opts):
    """start hgwebcommit webserver"""
    from hgwebcommit import app
    app.config.update(DEFAULT_CONFIG)
    app.config['HGWEBCOMMIT_REPOSITORY'] = repo.root
    app.run(host=opts['address'], port=opts['port'])


cmdtable = {'^webcommit|wc': (
                   webcommit,
                   [
                    ('p', 'port', 5000, 'port number'),
                    ('a', 'address', '127.0.0.1', 'bind address')],
                   '[options]')}