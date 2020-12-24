# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/gordo/.virtualenvs/coffer/lib/python2.7/site-packages/coffer/zeroconf_utils.py
# Compiled at: 2015-01-05 12:24:33
import os, socket, atexit, logging, zeroconf
log = logging.getLogger('avahi-utils')
DEFAULT_TYPE = '_coffer._tcp.local.'

def get_my_ip():
    return socket.gethostbyname(socket.gethostname())


def discover(service_type=DEFAULT_TYPE):
    z = zeroconf.Zeroconf()
    dns_outgoing = zeroconf.DNSOutgoing(zeroconf._FLAGS_QR_QUERY)
    dns_outgoing.add_question(zeroconf.DNSQuestion(service_type, zeroconf._TYPE_PTR, zeroconf._CLASS_IN))
    z.send(dns_outgoing)
    import time
    time.sleep(2)
    for serv_ptr in z.cache.entries_with_name(service_type):
        serv_info = z.get_service_info(service_type, serv_ptr.alias)
        yield serv_info


def announce(address, port, service_type=DEFAULT_TYPE):
    if address == '0.0.0.0':
        address = get_my_ip()
    info = zeroconf.ServiceInfo(service_type, 'Coffer-%d.%s' % (os.getpid(), service_type), socket.inet_aton(address), port, 0, 0, {})
    z = zeroconf.Zeroconf()
    z.register_service(info)

    def _close():
        log.info('Closing...')
        z.unregister_service(info)
        z.close()

    atexit.register(_close)
    return info