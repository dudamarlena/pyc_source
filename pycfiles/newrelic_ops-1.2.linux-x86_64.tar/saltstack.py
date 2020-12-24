# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/abukamel/Dropbox/code_base/newrelic_ops/venv/lib/python2.7/site-packages/newrelic_ops/saltstack.py
# Compiled at: 2015-03-28 11:34:55
import subprocess, urllib, logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def install(sys_update=True, daemon_start=False, nix_shell='/bin/bash'):
    info = {'sys_update': '-U' if sys_update else '', 
       'daemon_start': '-X' if not daemon_start else '', 
       'nix_shell': nix_shell, 
       'bootstrap_url': 'https://bootstrap.saltstack.com'}
    try:
        import salt.config
        logger.info('saltstack is already installed!')
    except:
        subprocess.call([info.get('nix_shell'),
         urllib.urlretrieve(info.get('bootstrap_url'))[0],
         info.get('sys_update'), info.get('daemon_start')])


if __name__ == '__main__':
    install()