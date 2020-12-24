# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/foundation/factories/ldap_connection_factory.py
# Compiled at: 2012-10-12 07:02:39
import logging
from coils.foundation.defaultsmanager import ServerDefaultsManager
try:
    import ldap, ldap.sasl
except:

    class LDAPConnectionFactory(object):

        @staticmethod
        def Connect(source):
            raise Exception('LDAP support not available')


else:

    class LDAPConnectionFactory(object):
        _dits = None

        @staticmethod
        def Connect(source):
            log = logging.getLogger('OIE')
            sd = ServerDefaultsManager()
            config = sd.default_as_dict('OIELDAPSources')
            if source in config:
                config = config.get(source)
                try:
                    dsa = ldap.initialize(config.get('url'))
                    if config.get('starttls', 'YES').upper() == 'YES':
                        dsa.start_tls_s()
                    if config.get('bindmech', 'SIMPLE').upper() == 'SIMPLE':
                        dsa.simple_bind_s(config.get('identity'), config.get('secret'))
                    else:
                        raise NotImplementedException('Non-simple LDAP bind not implemented')
                        tokens = ldap.sasl.digest_md5(config.get('identity'), config.get('secret'))
                        dsa.sasl_interactive_bind_s('', tokens)
                except Exception, e:
                    log.exception(e)
                    log.error(('Unable to provide connection to source name {0}').format(source))
                    return
                else:
                    return dsa
            else:
                log.error(('No LDAP source defined with name {0}').format(source))
                return
            return