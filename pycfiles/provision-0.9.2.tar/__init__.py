# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jay/proj/genforma/provision_core/provision/defaults/__init__.py
# Compiled at: 2011-07-27 02:46:43


def init(config):
    config.DEFAULT_PROVIDER = None
    config.DEFAULT_USERID = None
    config.DEFAULT_SECRET_KEY = None
    config.add_bundle('bootstrap-python', ['bootstrap-python.sh'])
    config.add_bundle('dev', ['emacs.sh', 'screen.sh'], [
     '/root/.emacs.d/init.el', '/root/.screenrc'])
    config.add_bundle('hudson', ['jre.sh', 'postfix.sh', 'hudson.sh'])
    config.add_bundle('libcloud', ['libcloud-env.sh'])
    config.add_bundle('mta', ['postfix.sh'])
    config.add_bundle('nginx', ['nginx.sh'])
    config.add_bundle('pyenv', ['python-env.sh'])
    config.add_bundle('proxy', ['apache-proxy.sh'])
    config.add_bundle('snmpd', ['snmpd.sh'])
    config.add_bundle('tz', ['tz.sh'])
    config.add_bundle('zenoss', ['zenoss.sh'])
    return