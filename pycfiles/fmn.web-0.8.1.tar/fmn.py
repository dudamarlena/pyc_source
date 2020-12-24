# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/threebean/devel/fmn.web/fedmsg.d/fmn.py
# Compiled at: 2015-03-20 15:38:07
import socket
hostname = socket.gethostname().split('.')[0]
config = {'fmn.consumer.enabled': True, 
   'fmn.sqlalchemy.uri': 'sqlite:////var/tmp/fmn-dev-db.sqlite', 
   'datanommer.sqlalchemy.url': 'postgresql+psycopg2://datanommer:bunbunbun@localhost:5432/datanommer', 
   'fmn.web.default_login': 'fedora', 
   'fmn.rules.utils.use_pkgdb2': False, 
   'fmn.rules.utils.pkgdb2_api_url': 'http://209.132.184.188/api/', 
   'fmn.rules.cache': {'backend': 'dogpile.cache.dbm', 
                       'expiration_time': 300, 
                       'arguments': {'filename': '/var/tmp/fmn-cache.dbm'}}, 
   'fmn.backends': [
                  'email', 'irc'], 
   'fmn.email.mailserver': '127.0.0.1:25', 
   'fmn.email.from_address': 'notifications@fedoraproject.org', 
   'fmn.irc.network': 'irc.freenode.net', 
   'fmn.irc.nickname': 'pingoubot', 
   'fmn.irc.port': 6667, 
   'fmn.irc.timeout': 120, 
   'fmn.gcm.post_url': 'wat', 
   'fmn.gcm.api_key': 'wat', 
   'fmn.base_url': 'http://localhost:5000/', 
   'fmn.acceptance_url': 'http://localhost:5000/confirm/accept/{secret}', 
   'fmn.rejection_url': 'http://localhost:5000/confirm/reject/{secret}', 
   'fmn.support_email': 'notifications@fedoraproject.org', 
   'endpoints': {'fmn.%s' % hostname: [
                                     'tcp://127.0.0.1:3041',
                                     'tcp://127.0.0.1:3042']}, 
   'logging': dict(loggers=dict(fmn={'level': 'DEBUG', 
               'propagate': False, 
               'handlers': [
                          'console']}))}