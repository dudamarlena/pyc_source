# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/rdkafka/helpers.py
# Compiled at: 2017-12-20 01:12:43
# Size of source mod 2**32: 1188 bytes


def rdk_ssl_config(cluster):
    """Generate rdkafka config keys from cluster's ssl_config"""
    if cluster._ssl_config is None:
        return {}
    else:
        ciphers = _get_ciphers_from_sockets(cluster.brokers)
        assert ciphers
        conf = cluster._ssl_config
        rdk_conf = {'security.protocol':'ssl', 
         'ssl.cipher.suites':ciphers, 
         'ssl.ca.location':conf.cafile, 
         'ssl.certificate.location':conf.certfile, 
         'ssl.key.location':conf.keyfile, 
         'ssl.key.password':conf.password}
        return {k:v for k, v in rdk_conf.items() if v is not None if v is not None}


def _get_ciphers_from_sockets(brokers):
    """Obtain ciphers currently used by pykafka BrokerConnections"""
    ciphers = set()
    for b in brokers.values():
        ciph = b._connection._socket.cipher()
        if ciph is not None:
            ciphers.add(ciph[0])

    return ','.join(ciphers)